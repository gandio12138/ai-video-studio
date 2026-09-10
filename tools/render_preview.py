"""Conservative FFmpeg preview renderer; no network, no source overwrite.
Only implements the declared v2 subset, rejecting unsupported editing fields.
"""
from __future__ import annotations
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any
from harness_core import (StudioError, require, run, probe, output_path, safe_path,
                          sha256_file, validate_timeline, file_ref)


def assert_binaries(soft_subtitles: bool = False) -> tuple[str, str]:
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    require(bool(ffmpeg and ffprobe), '渲染需要本机已有 ffmpeg 和 ffprobe；本工具不会安装')
    encoders = run([ffmpeg, '-hide_banner', '-encoders']).stdout
    for encoder in (['libx264', 'aac', 'pcm_s16le'] + (['mov_text'] if soft_subtitles else [])):
        require(any(len(line.split())>=2 and line.split()[1]==encoder for line in encoders.splitlines()), f'FFmpeg 缺少编码器 {encoder}')
    filters = run([ffmpeg, '-hide_banner', '-filters']).stdout
    for name in ('scale','pad','crop','fps','format','setsar','tpad','trim','setpts','atrim','asetpts','aresample','aformat','volume','afade','adelay','amix','alimiter','anullsrc'):
        require(any(len(line.split())>=2 and line.split()[1]==name for line in filters.splitlines()), f'FFmpeg 缺少滤镜 {name}')
    return ffmpeg, ffprobe


def render(timeline: dict, root: Path, output: str, execute: bool = False) -> dict:
    root=root.resolve()
    # A dry-run also validates real files and measurements; it does not synthesize media.
    validation=validate_timeline(timeline,root,check_files=True)
    out=output_path(root,output,'.mp4')
    require(Path(output).parts[:2]==('11_exports','previews'),'此后端只写11_exports/previews；最终发布需单独验收/导出')
    report_path=out.with_suffix('.render.json')
    require(not report_path.exists(),'该版本渲染报告已存在，请使用新版本名')
    sub=timeline['subtitles'];soft=bool(sub and sub['mode']=='soft')
    ffmpeg,_=assert_binaries(soft)
    sidecar=out.with_suffix('.srt') if sub and sub['mode']=='sidecar' else None
    if sidecar: require(not sidecar.exists(),'同名外挂字幕已存在，拒绝覆盖')
    fps=Fraction(timeline['fps_num'],timeline['fps_den']);fps_arg=f'{fps.numerator}/{fps.denominator}'
    total=validation['duration_s'];w,h=timeline['width'],timeline['height']
    summary={'status':'planned','execute':execute,'output':output,'duration_s':total,'frames':timeline['duration_frames'],
             'video_events':len(timeline['video']),'audio_events':len(timeline['audio']),
             'subtitle_mode':sub['mode'] if sub else None,'warnings':validation['warnings'],
             'stages':['normalize video segments','hard-cut concat','position and mix audio','mux preview','decode and probe output'],
             'limitations':['no cloud generation','no NLE native project','no burned-in subtitles','no loudness certification','no creative QC']}
    if not execute:
        return summary
    out.parent.mkdir(parents=True,exist_ok=True)
    commands=[]
    start=datetime.now(timezone.utc).isoformat()
    def invoke(cmd: list[str], cwd: Path | None=None) -> None:
        commands.append(cmd)
        run(cmd,timeout=900,cwd=cwd)
    prefix=[ffmpeg,'-nostdin','-hide_banner','-loglevel','error','-n']
    published=[]
    try:
        with tempfile.TemporaryDirectory(prefix='.render_',dir=out.parent) as tmp_name:
            tmp=Path(tmp_name)
            segments=[]
            for i,c in enumerate(timeline['video']):
                # Rehash immediately before use as well as at initial validation.
                source=file_ref(root,c,True)
                dest=tmp/f'seg_{i:03d}.mp4';segments.append(dest.name)
                cmd=prefix+['-protocol_whitelist','file,pipe']
                if c['kind']=='image':
                    cmd+=['-loop','1','-framerate',fps_arg,'-i',str(source)]
                else:
                    cmd+=['-ss',f'{c["source_in_ms"]/1000:.9f}','-i',str(source)]
                if c['fit']=='contain':
                    size=f'scale={w}:{h}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2'
                else:
                    size=f'scale={w}:{h}:force_original_aspect_ratio=increase:force_divisible_by=2,crop={w}:{h}'
                # tpad only covers the explicitly allowed <= one-frame quantization difference.
                vf=f'setpts=PTS-STARTPTS,scale=iw*sar:ih,setsar=1,fps={fps_arg},{size},setsar=1,format=yuv420p,tpad=stop_mode=clone:stop_duration={1/float(fps):.9f}'
                cmd+=['-map','0:v:0','-an','-vf',vf,'-frames:v',str(c['duration_frames']),'-c:v','libx264','-preset','veryfast','-crf','24','-threads','2','-filter_threads','1',str(dest)]
                invoke(cmd)
                info=probe(dest,count_frames=True)
                streams=[s for s in info['streams'] if s.get('codec_type')=='video']
                require(streams and int(streams[0].get('nb_read_frames',0))==c['duration_frames'],f'{c["clip_id"]}: 实际解码帧数不足，源片段需重新检查')
            listing=tmp/'segments.ffconcat'
            listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{n}'\n" for n in segments),encoding='utf-8')
            joined=tmp/'joined.mp4'
            invoke(prefix+['-protocol_whitelist','file,pipe','-f','concat','-safe','1','-i',str(listing),'-map','0:v:0','-c:v','copy','-an',str(joined)])
            # Mix a full-length silent base with selected audio events. Silence is explicit, not TTS.
            mix=tmp/'mix.wav';cmd=prefix.copy()
            for c in timeline['audio']:
                source=file_ref(root,c,True)
                cmd+=['-protocol_whitelist','file,pipe','-i',str(source)]
            graph=[f'anullsrc=channel_layout=stereo:sample_rate=48000,atrim=duration={total:.9f}[base]']
            labels=['[base]']
            for i,c in enumerate(timeline['audio']):
                dur=c['duration_frames']/float(fps);src=c['source_in_ms']/1000
                chain=f'[{i}:a:0]atrim=start={src:.9f}:duration={dur:.9f},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,volume={c["gain_db"]:.6f}dB'
                if c['fade_in_frames']:
                    chain+=f',afade=t=in:st=0:d={c["fade_in_frames"]/float(fps):.9f}'
                if c['fade_out_frames']:
                    fd=c['fade_out_frames']/float(fps)
                    chain+=f',afade=t=out:st={dur-fd:.9f}:d={fd:.9f}'
                delay=round(Fraction(c['start_frame']*48000,1)/fps)
                chain+=f',adelay={delay}S:all=1[a{i}]'
                graph.append(chain);labels.append(f'[a{i}]')
            graph.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0:dropout_transition=0,alimiter=limit=0.89:level=0:latency=1,atrim=duration={total:.9f},asetpts=PTS-STARTPTS[mix]')
            cmd+=['-filter_complex',';'.join(graph),'-filter_complex_threads','1','-map','[mix]','-c:a','pcm_s16le','-ar','48000','-ac','2','-t',f'{total:.9f}',str(mix)]
            invoke(cmd)
            final=tmp/'final.mp4';cmd=prefix+['-protocol_whitelist','file,pipe','-i',str(joined),'-protocol_whitelist','file,pipe','-i',str(mix)]
            subpath=None
            if sub:
                subpath=file_ref(root,sub,True,{'.srt'})
            if soft:cmd+=['-protocol_whitelist','file,pipe','-i',str(subpath)]
            cmd+=['-map','0:v:0','-map','1:a:0']
            if soft:cmd+=['-map','2:0','-c:s','mov_text','-metadata:s:s:0',f'language={sub["language"]}']
            cmd+=['-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-t',f'{total:.9f}','-movflags','+faststart',str(final)]
            invoke(cmd)
            # Decode the complete preview rather than trusting container existence.
            invoke([ffmpeg,'-nostdin','-v','error','-protocol_whitelist','file,pipe','-i',str(final),'-map','0:v:0','-map','0:a:0','-f','null','-'])
            measured=probe(final,count_frames=True)
            vs=[s for s in measured['streams'] if s.get('codec_type')=='video']
            require(vs and int(vs[0].get('nb_read_frames',0))==timeline['duration_frames'],'合成后的帧数与时间线不符')
            require(vs[0]['width']==w and vs[0]['height']==h,'合成分辨率不符')
            observed=float(measured['format']['duration'])
            require(abs(observed-total)<=max(2/float(fps),0.1),'合成后的总时长超出允许编码误差')
            # Refuse stale inputs if an editor changed a file during rendering.
            for c in timeline['video']+timeline['audio']+([sub] if sub else []):file_ref(root,c,True)
            # Hard-link publication is atomic and fails rather than overwriting an existing name.
            os.link(final,out);published.append(out)
            if sidecar:
                temp_sub=tmp/'captions.srt';shutil.copyfile(subpath,temp_sub)
                os.link(temp_sub,sidecar);published.append(sidecar)
            summary.update({'status':'render_success','started_at':start,'finished_at':datetime.now(timezone.utc).isoformat(),
                            'sha256':sha256_file(out),'timeline_timing_sha256':validation['timing_sha256'],
                            'measured':measured,'decode_check':'passed','human_visual_audio_review':'not_checked',
                            'loudness_true_peak_check':'not_checked','publication_approved':False,'commands':commands})
            # This output is private project information; commands contain no secrets by design.
            with report_path.open('x',encoding='utf-8') as f:json.dump(summary,f,ensure_ascii=False,indent=2)
            return {k:v for k,v in summary.items() if k not in ('commands','measured')}
    except Exception as e:
        # Remove only outputs published in this call, never source media or older versions.
        for p in published:
            p.unlink(missing_ok=True)
        if not report_path.exists():
            with report_path.open('x',encoding='utf-8') as f:
                json.dump({'status':'failed','started_at':start,'error':str(e),'commands':commands,'publication_approved':False},f,ensure_ascii=False,indent=2)
        if isinstance(e,StudioError):raise
        raise StudioError(f'本地渲染失败: {e}') from e
