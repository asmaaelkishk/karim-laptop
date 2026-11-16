"""Build Karim's Laptop (MANUAL simulation) from the shared source.

    python3 src/build.py            -> writes public/index.html and prints its fingerprint
    python3 src/build.py --check    -> also fails if the fingerprint differs from EXPECTED

The page is the shared source + the manual-only Tuesday engine + the closing tags.
LIVE is frozen at v1.2-rc21 (see archive/) and is not built here.
"""
import hashlib, os, sys
EXPECTED = '648c0c33a4d9b94d'   # v1.2-rc30 — update after every approved change
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
read = lambda n: open(os.path.join(SRC, n), encoding='utf-8').read()
page = read('shared_before.html') + read('manual_only.js') + read('shared_after.html')
out = os.path.join(ROOT, 'public'); os.makedirs(out, exist_ok=True)
with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8') as f: f.write(page)
fp = hashlib.sha256(page.encode('utf-8')).hexdigest()[:16]
print('MANUAL fingerprint', fp, '->', os.path.join('public', 'index.html'))
if '--check' in sys.argv and fp != EXPECTED:
    print('MISMATCH: expected', EXPECTED); sys.exit(1)
