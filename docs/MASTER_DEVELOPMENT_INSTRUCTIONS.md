# Master Development Instructions (as given by the client) — summary of binding rules

## 1. Simulation development & feature preservation
- Continuous development, never rebuilt from scratch. BUILD FORWARD. NEVER REGRESS.
- Never delete, remove, overwrite, simplify or disable any existing feature, mechanic, content, visual, calculation, interaction or logic unless explicitly instructed.
- Every request is an addition or targeted modification of the latest working version; unrelated components keep their behaviour; smallest necessary change.
- Conflicts with existing functionality: explain and ask for approval first. If uncertain, STOP and ask.
- Protected: rounds/progression, rules, scoring/calculations, roles/profiles, scenarios/consequences, interactions/navigation, visual design/UX, data relationships and stored progress, approved content, fixed bugs.
- Change impact analysis before every change; mandatory regression check after every change; never claim untested results.
- Maintain feature inventory & change log (existing, new, modified, protected, known issues).
- Version control & recovery: recoverable version before significant changes; never overwrite the only working version; never revert wholesale.
- Report after each request: Implemented · Preserved · Tested · Risks or Issues · Version Status.

## 2. Dual-version development & synchronization
- Two permanent versions: MANUAL (karim_laptop_simulation.html) and LIVE (karim_laptop_simulation_LIVE.html).
- Identical shared content/features/rules/scoring/design; only approved difference: how Tuesday interruptions trigger (on placement vs on the live timeline), plus each version's own controls and separate saved-progress storage.
- Every change applies to BOTH versions by default; never leave one outdated.
- One shared source; version-specific behaviour controlled separately.
- Dual verification after every change; shared features verified only when checked in both.
- One unified inventory with SHARED / MANUAL ONLY / LIVE ONLY.
- Synchronized version numbers; checkpoints of both before significant changes; no new baseline until both builds are approved.
- Report: what changed · MANUAL implemented/tested/issues · LIVE implemented/tested/issues · version-specific mechanics intact · anything unverified.
