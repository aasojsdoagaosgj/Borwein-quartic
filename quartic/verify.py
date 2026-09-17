"""Verify saved calculations, or replay them with --replay; not a proof checker."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

BASE=Path(__file__).resolve().parent
JOBS=[('certify_infinite.py','infinite_certificate.json'),
      ('certify_endpoint_constants.py','endpoint_certificate.json'),
      ('certify_limit.py','limit_certificate.json'),
      ('diagnostic.py','diagnostic.json'),
      ('saddle_diagnostic.py','saddle_diagnostic.json')]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def run(replay=False):
    if not __debug__:raise RuntimeError('Run without optimization; assertions are part of the certificates.')
    records=[]
    for script,report in JOBS:
        if replay:
            env=os.environ.copy();env['PYTHONOPTIMIZE']='0'
            child=subprocess.run([sys.executable,'-B',str(BASE/script)],cwd=BASE.parent,
                capture_output=True,text=True,encoding='utf-8',env=env)
            if child.returncode:raise RuntimeError(script+' failed:\n'+child.stdout+child.stderr)
        path=BASE/'results'/report
        data=json.loads(path.read_text(encoding='utf-8'))
        assert data['status'] in ('passed','diagnostic_completed')
        assert data['source_sha256']==sha(BASE/script),(script,'stale report')
        for dep,digest in data.get('dependency_sha256',{}).items():
            assert digest==sha(BASE/dep),(script,dep,'stale dependency')
        records.append({'script':script,'report':report,'status':data['status'],'report_sha256':sha(path)})
        print(script+': '+data['status'],flush=True)
    files=sorted(list(BASE.glob('*.md'))+list(BASE.glob('*.py')))
    result={'status':'all_saved_computations_verified','replayed':replay,
        'checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'theorem_scope':'All n sufficiently large; threshold N0 not numerically evaluated.',
        'jobs':records,'input_sha256':{p.name:sha(p) for p in files},
        'limitation':'Source hashes and computations only; written analytic arguments are not mechanically checked.'}
    (BASE/'results'/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Saved quartic/results/verification.json')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
