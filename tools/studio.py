#!/usr/bin/env python3
"""CLI entry: offline checks, fingerprints, verified SRT export, local preview.
Examples are documented in tools/README.md. External generation is not implemented.
"""
from __future__ import annotations
import argparse
import json
import platform
import shutil
import sys
from pathlib import Path
from harness_core import (StudioError, require, safe_path, output_path, read_json,
    run, probe, sha256_file, validate_timeline, validate_alignment, validate_job,
    timing_fingerprint, request_fingerprint, srt_text)


def doctor(root: Path) -> dict:
    names=sorted(p.parent.name for p in (root/'.agents/skills').glob('*/SKILL.md'))
    binaries={k:shutil.which(k) for k in ('ffmpeg','ffprobe')}
    versions={}
    for k,p in binaries.items():
        if p:
            try:versions[k]=run([p,'-version']).stdout.splitlines()[0]
            except StudioError as e:versions[k]=str(e)
    ready=False;reason=''
    try:
        from render_preview import assert_binaries
        assert_binaries();ready=True
    except StudioError as e:reason=str(e)
    return {'python':platform.python_version(),'python_minimum':'3.9','platform':platform.platform(),'skill_count':len(names),'skills':names,
            'required_project_files':{n:(root/n).is_file() for n in ('AGENTS.md','STATE.md','PROJECT.md','CAPABILITIES.md','config/runtime.json','config/providers.json')},
            'binaries':binaries,'versions':versions,'local_preview_dependencies_ready':ready,'local_preview_blocker':reason,
            'cloud_adapters_implemented':False,'network_calls_made':False,'installed_anything':False,
            'note':'这不是你的生产权限批准，也没有验证 Codex 已加载 skill。'}


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    subs=parser.add_subparsers(dest='cmd',required=True)
    d=subs.add_parser('doctor',help='只读环境检查');d.add_argument('--root',default='.')
    p=subs.add_parser('probe',help='测实际媒体流和时长');p.add_argument('path');p.add_argument('--root',default='.')
    p=subs.add_parser('hash',help='文件/时间线/任务指纹');p.add_argument('path');p.add_argument('--kind',choices=['file','timing','request'],default='file');p.add_argument('--root',default='.')
    v=subs.add_parser('validate',help='格式/引用检查，不联网');v.add_argument('kind',choices=['timeline','job','alignment']);v.add_argument('path');v.add_argument('--timeline');v.add_argument('--check-files',action='store_true');v.add_argument('--root',default='.')
    s=subs.add_parser('srt',help='只导出已核验对齐；拒绝估时');s.add_argument('path');s.add_argument('--timeline',required=True);s.add_argument('--output',required=True);s.add_argument('--root',default='.')
    r=subs.add_parser('render',help='默认只计划；--execute 才渲染本地小样');r.add_argument('path');r.add_argument('--output',required=True);r.add_argument('--execute',action='store_true');r.add_argument('--root',default='.')
    args=parser.parse_args(argv);root=Path(args.root).resolve()
    try:
        require(root.is_dir(),'项目根目录不存在')
        if args.cmd=='doctor':result=doctor(root)
        elif args.cmd=='probe':
            p=safe_path(root,args.path,True);result={'path':args.path,'sha256':sha256_file(p),'media':probe(p)}
        elif args.cmd=='hash':
            p=safe_path(root,args.path,True)
            digest=sha256_file(p) if args.kind=='file' else (timing_fingerprint(read_json(p)) if args.kind=='timing' else request_fingerprint(read_json(p)))
            result={'kind':args.kind,'sha256':digest}
        else:
            obj=read_json(safe_path(root,args.path,True))
            if args.cmd=='validate':
                if args.kind=='timeline':result=validate_timeline(obj,root,args.check_files)
                elif args.kind=='job':result=validate_job(obj,root,args.check_files)
                else:
                    require(bool(args.timeline),'检查alignment必须提供 --timeline')
                    tl=read_json(safe_path(root,args.timeline,True))
                    if args.check_files:validate_timeline(tl,root,True)
                    result=validate_alignment(obj,tl,root)
            elif args.cmd=='srt':
                tl=read_json(safe_path(root,args.timeline,True));validate_timeline(tl,root,True)
                result=validate_alignment(obj,tl,root)
                out=output_path(root,args.output,'.srt');out.parent.mkdir(parents=True,exist_ok=True)
                with out.open('x',encoding='utf-8') as f:f.write(srt_text(obj))
                result.update({'output':args.output,'sha256':sha256_file(out)})
            else:
                from render_preview import render
                result=render(obj,root,args.output,args.execute)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (StudioError,OSError,KeyError,TypeError,ValueError) as e:
        print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False),file=sys.stderr);return 2

if __name__=='__main__':
    raise SystemExit(main())
