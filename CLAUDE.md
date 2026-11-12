# Karim's Laptop — rules for Claude Code

This repo is the ASAP course simulation "Karim's Laptop" (LOGIC Training & HR Development).
The page participants use is `public/index.html`, built from `src/`. Vercel serves `public/`.

## Before changing anything
1. `python3 src/build.py --check` must print fingerprint **469e306a7fc68cfc** (v1.2-rc29).
   If it doesn't, stop and tell the owner.
2. Never edit `public/index.html` by hand — edit `src/` and rebuild.

## Binding rules (from the owner)
- Build forward, never regress. Never remove or change an approved feature unless the owner says so explicitly.
- Smallest targeted change. Check the impact first; if a change touches an approved feature or you are unsure, stop and ask.
- MANUAL simulation only. LIVE is frozen at v1.2-rc21 (`archive/`) and is not used.
- Wednesday is the final round — there is no Thursday.
- After every change: `python3 src/build.py`, then `python3 tests/run_suite.py`.
  The regression must stay identical to `tests/results/baseline_rc29.txt` except for differences you can explain as the requested change.
  Never claim a result you didn't test.
- Keep `docs/` up to date: add the change to the Master Feature Inventory and the project reference
  (number it after 119, scope MANUAL), and update `EXPECTED` in `src/build.py` and the fingerprint in this file.
- Report each change as: what changed · implemented · tested · issues · anything unverified.

## Where things are
- `src/shared_before.html` — the whole app (HTML, CSS, data and logic). Later versions add override blocks
  at the end, marked `/* ===== v1.2 (rcNN): ... ===== */` — add new changes the same way.
- `src/manual_only.js` — Tuesday's/Wednesday's interruption engine (interruptions fire on placement).
- `src/shared_after.html` — closing tags.
- Saved progress lives in the browser (localStorage key `asap-karim-sim-v1`).
- Automated browsers skip the "Meet Karim" start screen unless a test sets `window.MEET_TEST = true`.
