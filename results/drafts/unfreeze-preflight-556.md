# Every freeze lifted - the pre-flight (Iteration 556)

The owner (556): seed 77 from scratch, 12 hours, on every gene that still has code. Before a 12-hour run each lifted
freeze's code was checked here - deterministic, no timing (results/drafts/unfreeze-preflight-556.py): four bases from seed
76's true front - the fastest (7f6362b7e5, JIT), the smallest (344b8fe8fe), a JIT design and a non-JIT design from its
middle (b738e61a04, f65f78b4ce) - each with one gene at a time set to every other value of its domain, built and run on
all nine workloads (the seven selection workloads, sieve and parse), each output against s6's; at 64 bits and at 32
(the 32-bit builds have no JIT). Then eight random designs from the unfrozen space (seed 556). A cell reads the same at
both widths unless it says otherwise.

| gene = value | the fastest | the smallest | a JIT design, mid | a non-JIT design, mid |
|---|---|---|---|---|
| alignhot=1 | right | right | right | right |
| alignhot=2 | right | right | right | right |
| alignhot=3 | right | right | right | right |
| msc=1 | right | right | right | right |
| scale=1 | canon keeps 0 | canon keeps 0 | canon keeps 0 | canon keeps 0 |
| scale=2 | canon keeps 0 | canon keeps 0 | canon keeps 0 | canon keeps 0 |
| scale=3 | canon keeps 0 | canon keeps 0 | canon keeps 0 | canon keeps 0 |
| sharedcall=1 | right | right | right | right |
| bytehdr=0 | right | right | right | right |
| doesfar=0 | right | kernel WRONG, corpus WRONG | right | kernel WRONG, corpus WRONG |
| thinhdr=0 | right | right | right | right |
| varcall=0 | right | kernel WRONG, corpus WRONG | right | kernel WRONG, corpus WRONG |
| bss=0 | right | right | right | right |
| lean=0 | right | right | right | right |

The random designs, both widths alike: six of eight right on all nine; two cpt16 designs wrong on apps -
cpt16's known reach (seed 76: 28 such at 64 bits).

    random 0 (cv8; JIT False; unfrozen values: doesfar=0 varcall=0): right on all 9
    random 1 (cell; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): right on all 9
    random 2 (cpt16; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): apps WRONG
    random 3 (sod16; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): right on all 9
    random 4 (sod16; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): right on all 9
    random 5 (cpt16; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): apps WRONG
    random 6 (cell; JIT False; unfrozen values: sharedcall=1 thinhdr=0 bss=0): right on all 9
    random 7 (cv8; JIT False; unfrozen values: doesfar=0 varcall=0 bss=0 lean=0): right on all 9

**The reading - no new failure.** alignhot, msc, sharedcall, bytehdr, thinhdr, bss and lean work at every value on every
base, both widths. scale is inert on cv8: canon keeps it 0, so lifting it changes nothing there. doesfar and varcall at 0
hit the reach limit on the threaded engines (wrong kernel and corpus); the evolver's reach_lethal predicts all of these -
the JIT bases' too, which run right, so it is conservative there - and a child with either gets 'died: reach limit at
scale 0 - not run', no build: a cheap rejection. The run's per-workload output check rejects the wrong designs that do
get built. Working is not winning: whether the lifted values reach the front is seed 77's to say (results/predictions.md,
556).
