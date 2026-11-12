# Karim's Laptop — project reference (status at v1.2-rc29, 11 Nov 2026)

## Binding development rules (unchanged)
- Build forward, never regress. Never remove or change an approved feature without explicit permission; smallest targeted change; impact check first; if unsure, ask.
- Two versions from one shared source: MANUAL (interruptions fire on placement) and LIVE (live line). Decision 11 Nov 2026: LIVE is FROZEN at v1.2-rc21 and not used — from now on changes go into the MANUAL simulation only. The online (Vercel) file is the manual simulation.
- Checkpoint before significant changes; test both versions after every change (full Sunday–Tuesday regression suite + LIVE checks); never claim untested results.
- Keep the Master Feature Inventory and change log up to date (SHARED / MANUAL ONLY / LIVE ONLY).
- Report: what changed · MANUAL implemented/tested/issues · LIVE implemented/tested/issues · version-specific mechanics · unverified.
- Addendum: you direct the learning experience; Claude designs the full round (tasks, branches, consequences, report), waits for approval of the design, then builds and tests. Preservation takes priority over autonomy.

## Status
- Version 1.1 (changes 1–35): approved and locked 29 Oct 2026.
- Version 1.2 (changes 36–119, Wednesday · Round 4 · Perform, plus change 86 on Monday's negotiation): release candidate rc29, pending approval.
- LIVE: frozen at v1.2-rc21 (not used). The Wednesday trial file is not used either — every rule built in it is part of the normal simulation.
- Files (attach these when development continues):
  - karim_laptop_v1.2-rc29_package.zip — everything: shared source + build script (src/), all tests and results, the inventory, this reference, LIVE frozen at rc21, Version 1.1 for recovery
  - karim_laptop_simulation_v1.2-rc29.html — the simulation (Sunday → Wednesday), the file to publish on Vercel
- How to resume: unzip the package, rebuild with `python3 src/build.py <out>/`, and confirm the manual fingerprint is 469e306a7fc68cfc before changing anything.

## Changes to approved days made in 1.2 (all requested by you)
- G9: leftovers that don't fit Karim's energy wait in To plan (day stays playable).
- Negotiation: role play scored by observers; threads read as real emails. Monday (change 86): the first task negotiated is scored 0–1 per part (D, E, A, L, BATNA), 3 of 5 = agreed, one more try; every later Monday negotiation has no score card (options + new day + BATNA → "Agree the new deadline"). Tuesday and Wednesday: score out of 15, 10+ agreed, one more try.
- Reduced mode (all days) = do not disturb: handling a notification now always costs; only calls from important people (Hala, Nour, Mom) are free.
- Eisenhower (all days): moves to Negotiate only once every Q3 task has a delegate.
- Batch picker (all days): offers the current task, tasks still to come, and office tasks still in To plan.
- Tag & mode screen lists only tasks that need it and no longer jumps to the calendar.
- Undo for participants (↶ Undo / Ctrl+Z): undoes a move together with its interruption.

## Wednesday — design decisions to keep
- Start: brief → "Build Karim's habits" → Habits tool → "Now open Karim's laptop" → calendar; emails start arriving.
- Habits tool: scorecard (+/−/=) → choose ONE productivity habit (strategic focus block 60 min · email batching 2 × 20 min · end-of-day shutdown 10 min) + the evening walk (values) → each through stacking (formula shown; checker: clear time from a daily anchor, clear place), want after need (formula), two-minute version + preparation, tracker (formula). No implementation intention, no never-miss-twice.
- Habit cards: participants place them; each card says what it is stacked on; treats land automatically right after their habit and cannot be dragged; the tracker pops up right after each habit card (desk calendar / paper clips / app; walk: app / Apple Watch / home board).
- Walk wants: LEGO Technic (best), konafa, Facebook in bed — all accepted. Office wants: Turkish coffee, 5-minute scroll, match highlights. Shutdown want: playlist on the way home.
- Focus block holds a task: only tasks sorted into Q2 (plus yesterday's Q2 work); first 60 minutes inside, the rest stays in To plan.
- Email windows: window 1 starts with the morning inbox emails; Karim's short emails (delegations, negotiation replies, confirmations) go into the windows automatically (20 min each, can be moved or given their own slot); email interruptions can be batched only into windows still to come; emails held in deep work go to the next window.
- Interruptions (Tuesday's rules): deep focus = nothing gets through except desk visits and thoughts; social/app notifications wait for the ONE lunch buffet; after lunch they wait as "Held notifications" until the task ends; reduced mode = Handle now (costs) / Delete / Batch (lunch buffet for social, email window for email). Workday interruptions only during work tasks; none after work. Each interruption arrives once.
- Wednesday interruptions: IT password email (phishing test; 2-hour limit), Hala at the desk (10 min, 5 if Q2 done before; call-back must not cut into the approval cycle), the internet-bill thought (deep work only), Marketing's chaser (if Wednesday was agreed), Facebook tag (Mostafa, LEGO throwback), Noon LEGO flash sale, Nour (ceremony photos → celebration dinner at 6 PM once her WhatsApp chat is opened), routine emails (HR, Facilities, Omar's update, newsletter).
- Morning: green box "Today, because of an earlier decision" (ceremony approved Sunday) separate from "Left from yesterday"; ceremony without permission = decision (call Hala / go anyway → half-day deduction + apology / skip); car carries commutes of 30 min; Monday's AI choices carry.
- Tasks: Quarterly Meeting slides (1 hour), patterns review, FAQ sheet for the board (delegable to Mariam), ESC/10–11, approval GW-0412 + WE-0187 (Mariam 8:40), approval EX-0533 (Mariam 12:00, due 5 PM), duplicate codes (Nadia only — Omar has the backlog), Nadia's question (delegate to Mariam), HR training needs (negotiate to Sunday), Finance refund vouchers (negotiate to Thursday), printed forms (routine backup — delete or delegate to Nadia); negotiated tasks arrive as "Agreed for today" threads; launch message only as the 5-minute confirmation to Marketing.
- Office work may run after 5 PM (commute moves) unless Karim must be home for something fixed (celebration dinner, CCXP).
- Report: Karim's habits (fired, tracked, what it changed) and Tuesday vs Wednesday.

## Changes in rc23 (87–94, your play-through)
- 87 Sunday minutes come back on Monday as a normal LEFT OVER task (Hala's email/card unchanged).
- 88 Sound: if a browser refuses to start a sound, the screen stays open with ▶ Play (no auto-close).
- 89 Ahmed's CV: voice note + CV only; Open → his WhatsApp chat, click the voice note there; Done → back to the session.
- 90 Coaching: on the calendar at 12:30, no energy, no sorting, not draggable; a task dropped on it pushes it later.
- 91 Statistics log not done → next morning Hala's email "Where is the statistics log?" (nothing else changes).
- 92 Tuesday/Wednesday negotiations: no score card (like Monday's later ones); VIP still needs a split.
- 93 No more than 2 negotiated tasks moved to Wednesday (picker shows "full", third refused).
- 94 Tuesday offers note + Print & brief are Q2: no deadline, not negotiable.
- Test setup: tests expect Chromium at /opt/pw-browsers/chromium-1194/chrome-linux/chrome (link it to the installed Chromium if missing).

## Changes in rc29 (95–107, your second play-through)
- 95 sleep 7 h in all equations · 96 slides 1 h 15 (20+20+10+25) · 97 VIP 2 h, Tarek 3 h, notes fixed (VIP hint: part today, Mariam and the CRM lists) · 98 IT email 5 min · 99 thought "= 35 min"
- 100 done emails for delegated work = green GOOD NEWS · 101 report counts tasks planned with a problem as handled and names them
- 102 one held/batch block per approval cycle · 103 batch choice remembered · 104 Mom: dialogue + clinic plan card (10 / 15 / 30 / 15, pharmacy) · 105 split keeps the first part today · 106 Tuesday batch list offers the lunch buffet · 107 Wednesday FB tag from Sherif Nabil

- 108 energy: Sunday 21, Monday 21, Tuesday 23, Wednesday 21

- 109 Meet Karim: explore Karim's profile, team, CRM and chats before Sunday (free exploring, checklist as a guide; "I'm ready — start Sunday"; facilitator can skip)

- 110 Meet Karim list folds into a small tab (opens again on click); Plan it in Calendar locked while exploring

- 111 coaching card explains it moves later when pushed · 112 Undo removes Youssef's interruption; refocus never carried · 113 VIP rest Thursday or later (supplier quotes, two working days) · 114 planned-late tasks are not leftovers · 115 patterns review no deadline · 116 delegation confirmations silent · 117 (replaced by 119) · 118 sound: embedded first, retry, Play; "Show as text" for every recording

- 119 Monday AI hint: one note in the Eisenhower tool, pinned below all tasks in "To sort"

## Energy redesign — agreed, not built yet
Bedtime midnight (12:10 grace); wake 7:00 every day (Monday 6:55 desk alarm kept); energy never closes the day (Option B); bar adapts to the day's work; every task 1 point; negotiation costs only through its reply email; plain deletion free; sleep 7 h in all equations (Sunday: overcommitted by 2 h 40 instead of 3 h 40). To decide: "energy borrowed" display, top-up up to the next meal.

## Open items
- Approve 1.2 (rc21) when ready.
- Wednesday is the final round — the simulation ends after Wednesday (no Thursday).
- Next: your final changes, then export to Vercel.
- Earlier audit items G10–G12 still open.
- Known test timing flakes (Monday replay line, a report minute count) — not simulation changes.
