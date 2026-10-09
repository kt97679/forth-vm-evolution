# Dead code out of every engine, and two flag genes (Iteration 113)

The owner: new genes for the night run. The two engine trims of the deep
dive were priced first: 16-bit dispatch tables would save ~768 bytes, but
the table is built from the engine's list and three per-design generated
headers, and the tail-call and multi-state generators rewrite it by its
text - too wide a change to prove across every engine form in one afternoon;
the cold escaped operations overlap crossjumping, which already merges the
handlers' identical dispatch tails. A wider compiler-flag pool for the binary
(the deep dive's 15) was cheap, safe and gave evolution choices - priced
exactly on the VM, bytes of the stripped engine:

| flag | fastest (-O2, the JIT) | middle (-Os) | smallest (-Os) |
|---|---|---|---|
| -ffunction-sections -fdata-sections -Wl,--gc-sections | -2,976 | -2,112 | -1,920 |
| -fno-inline-small-functions | -1,312 | 0 | 0 |
| -falign-functions=1 -falign-loops=1 | -1,152 | 0 | 0 |
| -fno-stack-clash-protection | -64 | -32 | -32 |
| -fno-jump-tables | 0 | -32 | -32 |
| -fno-inline-functions-called-once | 0 | +64 | +32 |

**--gc-sections is dead code going, so it is every engine's, not a gene**:
the runtime is one object file, and code nothing calls came along -
vsnprintf (1,155-1,940 bytes), execvp, snprintf, syscall, getrusage, munmap,
memmove, memset. (vsnprintf was dead, not the shell's: the deep dive's OS
layer is ~1.3 KB smaller than it said.) On the front of all runs (138
designs, against session 29's engines): every one smaller, by 1,888 to
3,392 bytes, median 2,112.

**Two genes** for what is a trade: `alignfn` (-falign-functions=1
-falign-loops=1) and `noinls` (-fno-inline-small-functions) - ~1.1 and
~1.3 KB on -O2 engines, maybe some speed; nothing on -Os ones; +32 bytes on a
tail-call engine. Evolution weighs them.

Through the gate: 23 front designs under --gc-sections (plain, tail calls,
the JIT with jitx), a cached-top and a tail-call design with both genes on,
four designs with all three (their sieves right too); tests pass; hand-made
stages identical. Every design's size changed again: the stopping rule
counts afresh.
