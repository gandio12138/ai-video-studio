#!/usr/bin/env python3
"""Opt-in integration smoke test. Creates synthetic colors/tones, not AI media.
Uses installed FFmpeg, never calls a cloud service. Outputs only to an empty test root.
Run: python3 tools/smoke_test.py --root /path/to/new/test-folder
"""
from __future__ import annotations
import argparse
import copy
import json
import math
import shutil
import struct
import wave
from pathlib import Path
from harness_core import require,run,sha256_file,timing_fingerprint,validate_alignment,srt_text,probe,StudioError
from render_preview import render


def write_json(p: Path,o: dict) -> None:
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',required=True);args=parser.parse_args()
    root=Path(args.root).resolve();require(not root.exists() or not any(root.iterdir()),'测试目录必须不存在或为空，避免覆盖用户文件')
    root.mkdir(parents=True,exist_ok=True)
    for name in ('06_assets/generated','08_audio/takes','08_audio/alignment','10_edit/timelines','11_exports/previews'):(root/name).mkdir(parents=True,exist_ok=True)
    ff=shutil.which('ffmpeg');require(bool(ff),'需要已安装 FFmpeg')
    image=root/'06_assets/generated/静帧 测试.png';video=root/'06_assets/generated/视频 测试.mp4'
    run([ff,'-v','error','-n','-f','lavfi','-i','color=c=0x36566b:s=180x320:r=30','-frames:v','1','-threads','1',str(image)])
    run([ff,'-v','error','-n','-f','lavfi','-i','testsrc2=s=180x320:r=30','-t','3','-c:v','libx264','-threads','1','-pix_fmt','yuv420p',str(video)])
    for name,freq,amp,sec in [('tone.wav',440,.15,2),('music.wav',220,.03,4)]:
        p=root/'08_audio/takes'/name
        with wave.open(str(p),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000)
            w.writeframes(b''.join(struct.pack('<h',round(amp*32767*math.sin(2*math.pi*freq*n/48000))) for n in range(sec*48000)))
    def ref(p: Path):return {'path':p.relative_to(root).as_posix(),'sha256':sha256_file(p)}
    tl={'schema_version':'2.0','episode_id':'TEST','status':'draft','fps_num':30,'fps_den':1,'width':180,'height':320,'duration_frames':120,
        'video':[
            dict(clip_id='V1',shot_id='TEST_SH001',asset_id='IMG1',kind='image',**ref(image),start_frame=0,duration_frames=60,source_in_ms=0,fit='contain',motion='none',playback_rate=1,source_audio='drop'),
            dict(clip_id='V2',shot_id='TEST_SH002',asset_id='VID1',kind='video',**ref(video),start_frame=60,duration_frames=60,source_in_ms=500,fit='cover',motion='none',playback_rate=1,source_audio='drop')],
        'audio':[
            dict(clip_id='A1',asset_id='AUD1',line_id='TEST_DL001',kind='dialogue',**ref(root/'08_audio/takes/tone.wav'),start_frame=15,duration_frames=45,source_in_ms=250,gain_db=-3,fade_in_frames=3,fade_out_frames=3),
            dict(clip_id='A2',asset_id='MUS1',kind='music',**ref(root/'08_audio/takes/music.wav'),start_frame=0,duration_frames=120,source_in_ms=0,gain_db=-6,fade_in_frames=6,fade_out_frames=6)],
        'subtitles':None,'notes':'Synthetic engineering test; dialogue is a tone, not a human or AI voice.'}
    a={'schema_version':'2.0','episode_id':'TEST','status':'verified','timing_source':'manual_verified','timeline_timing_sha256':timing_fingerprint(tl),'review_reference':'Synthetic known-placement fixture; not actual speech alignment','cues':[{'cue_id':'Q1','line_id':'TEST_DL001','speaker_id':'C001','audio_asset_id':'AUD1','start_ms':500,'end_ms':1900,'text':'技术测试：只有测试音，没有人物配音。'}]}
    validate_alignment(a,tl,root)
    sub=root/'08_audio/alignment/test.srt';sub.write_text(srt_text(a),encoding='utf-8')
    tl['subtitles']=dict(**ref(sub),mode='sidecar',language='zho')
    write_json(root/'10_edit/timelines/timeline_sidecar.json',tl);write_json(root/'08_audio/alignment/alignment.json',a)
    draft=render(tl,root,'11_exports/previews/dry_run.mp4',False)
    require(draft['status']=='planned' and not (root/'11_exports/previews/dry_run.mp4').exists(),'dry-run不应生成文件')
    side=render(tl,root,'11_exports/previews/test_sidecar.mp4',True)
    require((root/'11_exports/previews/test_sidecar.srt').exists(),'外挂字幕没有发布')
    soft=copy.deepcopy(tl);soft['subtitles']['mode']='soft'
    write_json(root/'10_edit/timelines/timeline_soft.json',soft)
    sr=render(soft,root,'11_exports/previews/test_soft.mp4',True)
    info=probe(root/'11_exports/previews/test_soft.mp4')
    require(any(s.get('codec_type')=='subtitle' for s in info['streams']),'软字幕流不存在')
    no_audio=copy.deepcopy(tl);no_audio['audio']=[];no_audio['subtitles']=None
    nr=render(no_audio,root,'11_exports/previews/test_silent.mp4',True)
    require(bool(nr['warnings']),'无音频未显示明确警告')
    refused=False
    try:render(tl,root,'11_exports/previews/test_sidecar.mp4',True)
    except StudioError:refused=True
    require(refused,'未拒绝覆盖已有文件')
    # Inspect actual cut content and delayed tone placement, not only stream metadata.
    out=root/'11_exports/previews/test_sidecar.mp4'
    def frame_at(seconds: float) -> bytes:
        import subprocess
        p=subprocess.run([ff,'-v','error','-ss',str(seconds),'-i',str(out),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
        return p.stdout
    require(frame_at(.25)!=frame_at(2.25),'硬切前后画面未变化')
    import subprocess,array
    raw=subprocess.run([ff,'-v','error','-i',str(out),'-map','0:a:0','-ac','1','-ar','48000','-f','s16le','-'],capture_output=True,check=True).stdout
    samples=array.array('h');samples.frombytes(raw)
    import sys
    if sys.byteorder!='little':samples.byteswap()
    def rms(lo,hi):
        xs=samples[round(lo*48000):round(hi*48000)];return math.sqrt(sum(x*x for x in xs)/len(xs))
    require(rms(.7,1.2)>rms(.25,.4)*2,'定位测试音未在计划入点之后显著出现')
    summary={'status':'passed','synthetic_only':True,'cloud_calls':0,'duration_s':4,'frames':120,'resolution':[180,320],
      'checks':['dry-run produces no media','image hold + video source trim + hard cut','audio source trim + positioning + fades + multitrack mix','sidecar SRT copied','soft subtitles stream muxed','explicit silent-audio behavior','full decode + dimensions + 120-frame check','refuse overwrite','actual before/after cut frames differ','delayed audio event amplitude timing'],
      'human_or_ai_voice_tested':False,'macos_tested':False,'paid_provider_tested':False}
    write_json(root/'smoke_summary.json',summary);print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
