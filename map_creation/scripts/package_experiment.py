#!/usr/bin/env python3
"""Build an explicit public kit ZIP, excluding all working projects."""
import argparse
import hashlib
from pathlib import Path
import zipfile
from check_package import ROOT, audit


def build(root,output):
    files,issues=audit(root)
    if issues:
        raise ValueError('\n'.join(issues))
    if output.exists() or output.with_suffix(output.suffix+'.sha256').exists():
        raise ValueError('Output or checksum already exists; use a new release filename.')
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=output.with_name(output.name+'.writing')
    try:
        with zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for file in files:
                info=zipfile.ZipInfo('map_creation/'+file.relative_to(root).as_posix(),date_time=(2026,9,16,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED
                info.external_attr=0o100644<<16
                archive.writestr(info,file.read_bytes())
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.sha256').write_text(f'{digest}  {output.name}\n',encoding='utf-8')
    return len(files)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    try:
        count=build(ROOT,args.output.resolve())
    except (OSError,ValueError) as e:
        p.exit(1,f'Packaging failed: {e}\n')
    print(f'Packaged {count} maintained files; wrote ZIP and SHA-256 checksum. No working project was included.')


if __name__=='__main__':
    main()
