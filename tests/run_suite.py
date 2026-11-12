"""Regression suite for Karim's Laptop (MANUAL).

    python3 tests/run_suite.py            # regression (Sunday-Tuesday) + feature checks
    python3 tests/run_suite.py --quick    # feature checks only

Runs every test against public/index.html (build it first: python3 src/build.py).
Writes tests/results/latest.txt and compares the regression part with
tests/results/baseline_rc29.txt. Set CHROMIUM=/path/to/chrome to use a specific browser.
"""
import os, subprocess, sys, difflib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PAGE = 'file://' + os.path.join(ROOT, 'public', 'index.html')
SUITE = 'sweep mon v12 v13 v14 v15 esc9cyc yt tuepath newtasks ai3 audio3 replay tarek lo v11_manual manual_v1'.split()
CHECKS = 'rc23 rc23b rc24 rc28 meet'.split()
def run(t):
    r = subprocess.run([sys.executable, os.path.join(HERE, t + '.py'), PAGE], capture_output=True, text=True, timeout=900, cwd=HERE)
    return r.stdout + r.stderr
out, bad = [], 0
if '--quick' not in sys.argv:
    for t in SUITE: print('suite', t, flush=True); out += ['--- ' + t] + run(t).rstrip('\n').split('\n')
    base = open(os.path.join(HERE, 'results', 'baseline_rc29.txt'), encoding='utf-8').read().rstrip('\n').split('\n')
    diff = [l for l in difflib.unified_diff(base, out, lineterm='', n=0) if not l.startswith(('---', '+++', '@@'))]
    print('REGRESSION:', 'identical to the rc29 baseline' if not diff else 'DIFFERENCES (check whether they are intended):'); [print('  ' + l[:200]) for l in diff]
    bad += bool(diff)
checks = []
for t in CHECKS:
    print('check', t, flush=True); res = run(t); checks += ['--- ' + t] + res.rstrip('\n').split('\n')
    fails = [l for l in res.split('\n') if l.startswith('FAIL') or 'Traceback' in l or 'Error' in l]
    print('  ', 'all pass' if not fails else '\n   '.join(fails)); bad += bool(fails)
open(os.path.join(HERE, 'results', 'latest.txt'), 'w', encoding='utf-8').write('\n'.join(out + checks) + '\n')
print('RESULT:', 'OK' if not bad else 'NEEDS ATTENTION'); sys.exit(1 if bad else 0)
