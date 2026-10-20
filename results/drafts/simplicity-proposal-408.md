# The simplicity review - a proposal for the owner (Iteration 408, HANDOFF item 4b)

Seed 60 answered the anchoring question (Iteration 406: no evidence of anchoring), so what every front chooses is the
search's choice, not a carried habit - and freezing it fixes no trap. The fronts of seeds 53-60 together, 1,431
designs (results/drafts/gene-usage-53-60.md), two of them not carried: seed 58 from scratch and free of the tag-2
requirement, seed 60 from the hand-made designs alone.

**Freeze - on in every front design** (or all but one or two of the 1,431): bytehdr, doesfar, thinhdr, varcall (1,431),
bss (1,430), lean (1,429). Each becomes part of every design, its gene and its off path gone - the genome six
dimensions smaller, and (in a second step, measured on its own) the engine's and the converter's off branches deleted.

**Remove - on in no front design**: msc (the multi-state engine) and scale (call scaling), 0 of 1,431; neither had a
fault behind it, as tail had (results/fail32-400.md). Not yet tail: every tail design was the slowest at 32 bits for a
fault from seed 57 to the after-seed-62 batch - judge it after seed 63.

**Watch - nearly never**: jitos (12 of 1,431), nogcse (4) - out if seeds 63-64 keep them there.

**When**: after seed 62 (seeds 60-62 run one evolver), as a batch of its own or with the after-seed-62 one - a frozen
gene was chosen everywhere and a removed one nowhere, so neither moves a front; each change checked by gene-equiv.py and
the batch's tests, then rehearsed (results/rehearsal-405.md's way).

## Approved and built (Iteration 409)

The owner: yes. results/applied-after-seed62/frozen-after-seed62.patch, the after-seed-62 batch's tenth: evolve.py's FROZEN - the six
on, msc and scale at 0 - applied by require() to every design the search makes (now always, not only under a
requirement), and mutation no longer picks them; hand-made designs keep their own. Rehearsed: a short free run here with patches 1-10 (pop 16, one round, both widths, noevolved, no tag-2 requirement), to generation 13: 222 designs, 7 hand-made; status {'ok': 222}; 32-bit failures none; designs the search made off a frozen value: 0 (results/drafts/frozen-check-409.py) - and no reach-limit death, where seed 60 had 247. batch-check, the ten: PASS - 10 patches on a fresh clone of 50942b8: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.
