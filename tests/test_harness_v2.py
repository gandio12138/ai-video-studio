import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from harness_core import (StudioError,safe_path,output_path,read_json,sha256_file,
    validate_timeline,validate_alignment,validate_job,request_fingerprint,
    timing_fingerprint,srt_text,parse_srt,stream_duration)


def timeline():
    return {'schema_version':'2.0','episode_id':'EP01','status':'draft','fps_num':30,'fps_den':1,'width':180,'height':320,'duration_frames':90,
      'video':[{'clip_id':'V1','shot_id':'EP01_SH001','asset_id':'IMG1','kind':'image','path':'06_assets/generated/test.png','sha256':'a'*64,'start_frame':0,'duration_frames':90,'source_in_ms':0,'fit':'contain','motion':'none','playback_rate':1,'source_audio':'drop'}],
      'audio':[{'clip_id':'A1','asset_id':'AUD1','line_id':'EP01_DL001','kind':'dialogue','path':'08_audio/takes/test.wav','sha256':'b'*64,'start_frame':15,'duration_frames':30,'source_in_ms':0,'gain_db':-6,'fade_in_frames':0,'fade_out_frames':0}],
      'subtitles':None,'notes':'test fixture, no real speech'}


def alignment(tl):
    return {'schema_version':'2.0','episode_id':'EP01','status':'verified','timing_source':'manual_verified','timeline_timing_sha256':timing_fingerprint(tl),'review_reference':'unit fixture only; not a real listening review','cues':[{'cue_id':'Q1','line_id':'EP01_DL001','speaker_id':'C001','audio_asset_id':'AUD1','start_ms':500,'end_ms':1400,'text':'测试字幕'}]}


class HarnessChecks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.tl=timeline()
    def bad_tl(self):
        with self.assertRaises(StudioError):validate_timeline(self.tl,self.root)
    def test_valid_timeline(self):self.assertEqual(validate_timeline(self.tl,self.root)['duration_s'],3)
    def test_reject_boolean_frame(self):self.tl['duration_frames']=True;self.bad_tl()
    def test_reject_nan_gain(self):self.tl['audio'][0]['gain_db']=float('nan');self.bad_tl()
    def test_reject_zero_duration(self):self.tl['video'][0]['duration_frames']=0;self.bad_tl()
    def test_reject_gap(self):self.tl['video'][0]['start_frame']=1;self.bad_tl()
    def test_reject_wrong_total(self):self.tl['duration_frames']=91;self.bad_tl()
    def test_reject_unknown_transition(self):self.tl['video'][0]['transition']='fade';self.bad_tl()
    def test_reject_motion(self):self.tl['video'][0]['motion']='zoom';self.bad_tl()
    def test_reject_speed(self):self.tl['video'][0]['playback_rate']=1.1;self.bad_tl()
    def test_reject_original_audio_implicit(self):self.tl['video'][0]['source_audio']='keep';self.bad_tl()
    def test_reject_odd_dimensions(self):self.tl['width']=181;self.bad_tl()
    def test_reject_audio_overrun(self):self.tl['audio'][0]['duration_frames']=90;self.bad_tl()
    def test_reject_duplicate_id(self):self.tl['audio'][0]['clip_id']='V1';self.bad_tl()
    def test_reject_fade_overrun(self):self.tl['audio'][0]['fade_out_frames']=31;self.bad_tl()
    def test_reject_missing_real_files(self):
        with self.assertRaises(StudioError):validate_timeline(self.tl,self.root,True)
    def test_refuse_path_traversal(self):
        for s in ('../outside.mp4','/etc/passwd','https://x/a.mp4','./../a','a\nb','a\\b'):
            with self.subTest(s=s),self.assertRaises(StudioError):safe_path(self.root,s)
    def test_refuse_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root/'link').symlink_to(outside,target_is_directory=True)
            with self.assertRaises(StudioError):safe_path(self.root,'link/a.mp4')
    def test_accept_spaces_and_chinese(self):self.assertEqual(safe_path(self.root,'08_audio/中文 空格.wav').name,'中文 空格.wav')
    def test_no_source_output(self):
        with self.assertRaises(StudioError):output_path(self.root,'00_source/a.srt','.srt')
    def test_no_output_overwrite(self):
        (self.root/'11_exports').mkdir();(self.root/'11_exports/a.mp4').write_bytes(b'x')
        with self.assertRaises(StudioError):output_path(self.root,'11_exports/a.mp4','.mp4')
    def test_json_no_nan(self):
        p=self.root/'t.json';p.write_text('{"value":NaN}')
        with self.assertRaises(StudioError):read_json(p)
    def test_json_no_duplicate_keys(self):
        p=self.root/'t.json';p.write_text('{"x":1,"x":2}')
        with self.assertRaises(StudioError):read_json(p)
    def test_alignment_valid(self):self.assertEqual(validate_alignment(alignment(self.tl),self.tl,self.root)['cue_count'],1)
    def test_estimated_cannot_export(self):
        a=alignment(self.tl);a['timing_source']='estimated'
        with self.assertRaises(StudioError):validate_alignment(a,self.tl,self.root)
    def test_alignment_stale_after_audio_change(self):
        a=alignment(self.tl);self.tl['audio'][0]['sha256']='c'*64
        with self.assertRaises(StudioError):validate_alignment(a,self.tl,self.root)
    def test_alignment_no_circular_subtitle_hash(self):
        h=timing_fingerprint(self.tl);self.tl['subtitles']={'path':'a.srt','sha256':'d'*64,'mode':'sidecar','language':'zho'}
        self.assertEqual(h,timing_fingerprint(self.tl))
    def test_alignment_reject_unknown_audio(self):
        a=alignment(self.tl);a['cues'][0]['audio_asset_id']='AUD999'
        with self.assertRaises(StudioError):validate_alignment(a,self.tl,self.root)
    def test_alignment_reject_outside_audio(self):
        a=alignment(self.tl);a['cues'][0]['end_ms']=1700
        with self.assertRaises(StudioError):validate_alignment(a,self.tl,self.root)
    def test_srt_roundtrip(self):self.assertEqual(parse_srt(srt_text(alignment(self.tl)))[0]['start_ms'],500)
    def test_srt_overlap_rejected(self):
        s='1\n00:00:00,000 --> 00:00:01,000\nx\n\n2\n00:00:00,900 --> 00:00:02,000\ny\n'
        with self.assertRaises(StudioError):parse_srt(s)
    def test_stream_duration_not_container(self):
        info={'format':{'duration':'10'},'streams':[{'codec_type':'video','duration':'3'},{'codec_type':'audio','duration':'10'}]}
        self.assertEqual(stream_duration(info,'video'),3)
    def test_request_hash_stable_across_attempt(self):
        j=read_json(ROOT/'templates/job.json');h=request_fingerprint(j);j['attempt']=1;j['status']='failed'
        self.assertEqual(h,request_fingerprint(j))
    def test_request_hash_changes_with_text(self):
        j=read_json(ROOT/'templates/job.json');h=request_fingerprint(j);j['parameters']['text']='改一句'
        self.assertNotEqual(h,request_fingerprint(j))
    def test_job_planned_valid(self):self.assertTrue(validate_job(read_json(ROOT/'templates/job.json'),self.root)['valid'])
    def test_job_false_success_rejected(self):
        j=read_json(ROOT/'templates/job.json');j.update(status='succeeded',provider='manual_import',model='manual');j['request_fingerprint']=request_fingerprint(j)
        with self.assertRaises(StudioError):validate_job(j,self.root)
    def test_job_retries_limit(self):
        j=read_json(ROOT/'templates/job.json');j['attempt']=3
        with self.assertRaises(StudioError):validate_job(j,self.root)
    def test_job_budget_limit(self):
        j=read_json(ROOT/'templates/job.json');j['budget']['actual_cost']=1
        with self.assertRaises(StudioError):validate_job(j,self.root)
    def test_cloud_ready_without_approval(self):
        j=read_json(ROOT/'templates/job.json');j.update(status='ready',provider='vendor',model='m');j['budget'].update(estimated_cost=0,estimate_source='test');j['request_fingerprint']=request_fingerprint(j)
        with self.assertRaises(StudioError):validate_job(j,self.root)
    def test_missing_top_object(self):
        with self.assertRaises(StudioError):validate_timeline([],self.root)
    def test_no_audio_is_explicit_warning(self):
        self.tl['audio']=[];self.assertTrue(validate_timeline(self.tl,self.root)['warnings'])

if __name__=='__main__':unittest.main()
