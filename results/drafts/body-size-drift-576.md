# Seed 85's new death: "body size drift" - the scale-0 call reach, found late (Iteration 576)

**What**: 55 of seed 85's 35,760 designs (the random baseline) died "image did not convert (AssertionError: body size
drift at WORD)" - tools/layout.py's check that each body is the size the layout gave it. New: no results file before
seed 85 names it (seeds 77-84 none). Every one has bytehdr=0, lean=0 and scale=0 (the living 0.57, 0.40, 0.48); of the
1,326 designs with all three, 1,002 were refused at the reach limit, 266 lived, 55 died so, 3 failed apps
(results/drafts/body-size-drift-576.py on the seed pack's db.jsonl). 8 of 8 rebuilt at master die the same, the same word.

**Why**: with varcall a call is 2 bytes when its target is under 2^14 units, else 3 (tools/sod16.py's V8 call). The layout
sizes every code body once, before placement (layout.py: `tok[...] = to_tokens(...)` with V8_CALLTOK not yet set - every
call costs 2 bytes); the emit encodes the real targets. At scale 0 a unit is a byte, so a call past 16 KB of image grows
by a byte and the body no longer fits: 81cbd024e6's KEY, laid out 15 bytes (16 aligned), emitted 17 (24) - a call to
offset 16,728. evolve.py's reach_lethal() refuses scale 0 unless varcall and doesfar are both on - these have both, so
they run; bytehdr=0 and lean=0 make the image larger than 16 KB. At scale 1 and up the reach is 32 KB or more, past
every image the series made.

**Judged**: the scale-0 reach limit (Iteration 10), met by a road the series never took - it dies loudly, before any
measure; no wrong output, no correctness issue open. No change before seed 86: a fix sizes calls after placement and
iterates (a new mechanism for a corner no front design uses - against the aim), and the confirmation run's method stays
seed 84's. If consolidation keeps scale 0, retire varcall+doesfar's exemption or the corner with it.
