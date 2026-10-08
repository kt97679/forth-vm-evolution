# The engine's file without page padding (Iteration 110)

**Why.** An engine's file grew in 4 KB steps, by luck: a 430-byte saving
(Iteration 102) showed as -4,296 bytes in one engine and -72 in another;
t2wide's 288 bytes of code (Iteration 95) as +4,352; jitx's ~400 (Iteration
108) as +4,288. Not the page-aligned memory area, as first thought - that
is .bss, which takes no room in the file - but the default linker script:
under -n it still starts the data sections on a page boundary, so
.data.rel.ro sat at 0x4000 after .rodata ended at 0x3E80 - and when the code
ends just past a boundary, the gap is nearly 4 KB. The owner had the fix
deferred; seed 30's knockouts (jitx paying 4.3 KB for ~400 bytes of code)
made it the first thing to do.

**The fix.** Link with -N instead of -n (lab/evolve/evolve.py rt()): the data
sections end to end, the file its sections and ~800 bytes of headers. The
single segment was readable, writable and executable under -n already. A
16-byte page size under -n was tried too: some engines then crashed.

**Before and after, the front of all runs** (75 designs, session 27, built
both ways on the VM - sizes are exact): 16 unchanged, 59 smaller, none
larger; median -160 bytes, the most -2,528:

| design | engine file under -n | under -N | change |
|---|---|---|---|
| dba0e3ac28 | 26,232 | 23,704 | -2528 |
| 84b3c20d34 | 26,232 | 23,704 | -2528 |
| d447843170 | 26,232 | 23,864 | -2368 |
| 2653c5e636 | 26,232 | 23,864 | -2368 |
| 1fae942d98 | 26,232 | 23,864 | -2368 |

Images are unchanged (link flags touch only the engine). Through the gate
under -N: 15 designs of the front, every engine form among them (plain,
cached top, tail calls, the JIT with jitx); tests pass; the hand-made stages
identical. From here on a gene's bytes are its bytes: jitx ~400, t2wide 128
on the smallest design - and the engine trims become measurable.

Speeds are untouched (the same code; only the data's addresses moved), but
every design's size changed: comparisons stay fair (each session rebuilds
every run's designs), and the stopping rule counts afresh.
