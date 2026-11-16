# Karim's Laptop — ASAP time-management simulation

A single-page, offline HTML simulation of a Customer Service Team Lead's laptop
(Karim, Nile Home Appliances), used in the ASAP course by LOGIC Training & HR Development.
Participants plan Karim's Sunday–Wednesday while emails, WhatsApp messages, calls and
interruptions arrive. Version **1.2-rc30** · fingerprint **648c0c33a4d9b94d**.

## What's in this folder

| Path | What it is |
|---|---|
| `public/index.html` | **The simulation** — the only file Vercel serves. Built from `src/`. |
| `src/` | Shared source + manual interruption engine + `build.py` |
| `tests/` | Regression suite (Sunday–Tuesday) and feature checks, with the rc29 baseline |
| `docs/` | Master Feature Inventory (v1.2-rc30), project reference, development instructions |
| `archive/` | LIVE version, frozen at v1.2-rc21 — kept for the record, not deployed |
| `CLAUDE.md` | Rules Claude Code follows when it works in this repo |
| `vercel.json` | Tells Vercel to serve `public/` |

## Push it with Claude Code — step by step

1. Unzip `karim-laptop.zip` and open the `karim-laptop` folder in Claude Code
   (terminal: `cd karim-laptop` then `claude`; or open the folder in the Claude desktop app's Code tab).
2. Paste this prompt:

   > Read CLAUDE.md. Run `python3 src/build.py --check` and confirm the fingerprint.
   > Then initialise a git repository, commit everything with the message
   > "Karim's Laptop v1.2-rc30", create a **private** GitHub repository called `karim-laptop`
   > and push the main branch to it.

   Claude Code uses `git` and the GitHub CLI (`gh`). If `gh` isn't signed in, it will ask you to run
   `gh auth login` once.
3. Publish on Vercel (one time):
   - vercel.com → **Add New… → Project** → import the `karim-laptop` repository.
   - Framework preset: **Other**. Leave the build command empty. Vercel reads `vercel.json` and serves `public/`.
   - Click **Deploy**. Your link looks like `https://karim-laptop.vercel.app`.

   Or ask Claude Code: *"Deploy this repo to Vercel with the Vercel CLI (`npx vercel --prod`)."*
4. From then on, every push to `main` updates the Vercel site automatically.

Keep the GitHub repository **private**: the docs contain the facilitator PIN.

## Making a change later

```bash
# edit src/ … then:
python3 src/build.py          # rebuilds public/index.html and prints the fingerprint
python3 tests/run_suite.py    # regression + feature checks (about 15 minutes)
git commit -am "Change 121: …" && git push
```

Tests need Python 3.10+ and Playwright once:

```bash
pip install playwright
python3 -m playwright install chromium
```

`run_suite.py` compares the regression output with `tests/results/baseline_rc29.txt`. Any difference
is listed — keep it only if it is the change you asked for, then refresh the baseline from
`tests/results/latest.txt`. `python3 tests/run_suite.py --quick` runs only the feature checks.

## Good to know

- **Saved progress** stays in each participant's browser. To start clean: Facilitator panel → reset the whole simulation.
- **Meet Karim**: a new game opens on "Meet Karim" (explore his profile, team, CRM and chats) before Sunday.
  The facilitator panel has "Skip Meet Karim".
- **Sound**: Claude's own preview window can block sound. Test the recordings on the Vercel link or the downloaded
  file. Every recording also has "📝 Show as text".
- **Car seller text**: the "Show as text" version of the car seller's call was written to match the scene — check it
  against the recording once.
- **Known test flake**: under heavy load the `lo` test can stop early in Monday's morning sequence;
  it passes when run on its own (`python3 tests/lo.py`).
