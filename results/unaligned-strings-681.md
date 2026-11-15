# Inline strings without cell alignment - built (Iteration 681; item 6, step 1 of results/drafts/search-reopen-plan-677.md)

A CV8 inline string now ends where its characters do: the count byte and the characters, no padding. CV8's byte code
has no alignment to keep after a string; the cell and cpt16 families keep kernel.4's ALIGNED (their threaded code is
cells or tokens), so kernel.4, cross.4 and the frozen stages (s2-s5) are untouched. Made in every place that knew it:

- forth/cv8.4 and forth/cv8t.4: (S")8, (.")8, (ABORT")8 and STRING,8 - the run-time words and the run-time compiler
  without ALIGNED / ALIGN, swapped into the kernel's words in every CV8 image (the X8 mechanism);
- tools/sod16.py: op_bytes gives a string its own bytes under V8 (the translator's CV8 and tag-2 streams);
- forth/cross-cv8.4: S-STR and E-STR the same (the self-built images);
- engine/jit.c: the decoder resumes right after (S"), (.") and (ABORT")'s string;
- forth/spn-cv8.4 and forth/spn-cv8-decode.4: PAST-STRING (the s8 stages' decoders - found by run-tests, s8 failing).

## Every design and s6, before and after (lab/evolve/design-sizes.py; bytes, the search's build from each genome)

| design | engine 8 | image 8 | app 8 | total 8 | engine 4 | image 4 | app 4 | total 4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| s6 | +0 | -64 | -147 | -211 | +0 | -24 | -28 | -52 |
| smallest | +0 | -72 | -155 | -227 | +0 | -32 | -32 | -64 |
| least-memory | +0 | -72 | -173 | -245 | +0 | -32 | -31 | -63 |
| portable-small | +0 | -48 | -166 | -214 | +0 | -40 | -40 | -80 |
| portable-knee | +0 | -96 | -161 | -257 | +0 | -28 | -36 | -64 |
| portable-arm | +0 | -104 | -162 | -266 | +0 | -56 | -37 | -93 |
| portable-fastest | +0 | -64 | -180 | -244 | +0 | -24 | -27 | -51 |
| best-all-round | -16 | -64 | -137 | -217 | -16 | -20 | -46 | -82 |
| small-jit | +0 | -56 | -150 | -206 | +0 | -32 | -37 | -69 |
| fastest-x86-64 | +0 | -40 | -112 | -152 | +0 | -24 | -37 | -61 |
| fastest-x86-32 | +32 | -72 | -131 | -171 | +0 | -24 | -40 | -64 |

Every total smaller at both widths: -152 to -266 bytes at 8-byte cells, -51 to -93 at 4. The application code moves
as string-price.py priced it (s6 -147 both ways; the designs -112 to -180 against -103 to -203 priced) and the kernel
image's own strings -40 to -104 bytes. Two JIT engines move with engine/jit.c's two lines (best-all-round -16,
fastest-x86-32 +32 at 8-byte cells: the code's alignment, not the change). All 22 builds alive (corpus, kernel
workload, far). Speed: a string's execution loses ALIGNED (a primitive in CV8, so one dispatch fewer each), and the
padding it skipped was never executed - no workload can run more operations; the JIT's change is in its decoding.
Self-hosting (tools/selfhost-check.sh, forth/cross-cv8.4 with S-STR and E-STR unpadded): 8 of 11 PASS - s6 (A = B at
8,926 bytes; 668's 9,077), smallest at both widths, least-memory, portable-small, portable-knee, portable-arm,
portable-fastest, small-jit. **Open: the three jitexec designs FAIL** (best-all-round at both widths, fastest-x86-64,
fastest-x86-32): A is written, but A on its own engine (built with A's JIT layout lines) segfaults rebuilding itself.
Narrowed on fastest-x86-64's A: `: X7 3 0 DO ."  y" LOOP ; X7` prints once and dies; `."` in a BEGIN loop likewise;
`S" ab" TYPE` in the same loop, strings outside loops and loops without strings run. The translator-built designs
(the search's) and 676's shipped self-built images run all of these. So: jitexec's native (.") - TYPE through
EXECUTE's helper and its inline cache (engine/jit.c, the JITEXEC block) - against the self-built image's layout lines
(cross-cv8.4's J-OFF, jit_wends). To find before self-hosting phase 6; the search does not use self-built images.

### The fault narrowed (Iteration 682) - fastest-x86-64's image A on its engine (build/selfhost/check-fastest-x86-64)

- Deterministic: `: X7 3 0 DO ."  y" LOOP ; X7` dies 20 of 20 runs with address randomisation and 10 of 10 without;
  0 of 20 on designs/fastest-x86-64 (676's self-built image) and on the translator's build of the same genome.
- Not the bytes: X7 compiles to the same bytes on A and on the translator's image but for the call encodings
  (`10 14 0 0 128 | 5 3 5 0 11 | call (.") | 2 32 121 | 12 250 255 | 1`), and the calls decode to A's own offsets -
  (S") 6179, (.") 6191, TYPE 908, (ABORT") 6208 - which are A.img.jit.h's JIT_W_ lines; JIT_W_COLD has the same
  twelve entries in both; TYPE's word end (908, 910) is right.
- The site: JITLOG (a forth-libc build with -DJITLOG=1) - X7 translated native (offset 0x2c0), then `X 38c ... TYPE`:
  the native (.")'s EXECUTE of TYPE refused native code (f = 1), so TYPE runs in the interpreter through jitre's
  sentinel. gdb (-Oz -g, .text identical to the crashing build): the CPU at jit_mem + 0xFFFFF - the JIT buffer's last
  byte - with jit_call's return address on the stack; the EXECUTE site's inline cache (jit_ic[0]) still empty. An -O0
  build of the same source runs X7. `['] TYPE EXECUTE` in a loop died once and ran once on A.
- Next: the sentinel path's return in A (engine/vm-lab.c's jit_interp and L_x_jit, engine/jit.c's jit_exec and
  jit_leave) - what the interpreted TYPE's EXIT lands on - against the translator's engine under the same JITLOG
  build; why TYPE is refused native in A (its kslot, jit_body).

designs/ is unchanged: its images, engines and the cross compiler's copy (designs/forth/) stay the roles as shipped
at 676, consistent with each other (run-tests' make selfhost); the new roles come from the reopened search.

### Resolved (Iteration 683) - not a fault of the lab: the check ran designs/'s shipped files

tools/selfhost-check.sh runs a design from designs/ - its shipped engine, its engine's source rebuilt with A's layout,
its genes.4 - against today's cross compiler and kernel sources. Two of 681's changes reach those shipped files:

- engine/jit.c's string skip: designs/'s jitexec engines (best-all-round, fastest-x86-64, fastest-x86-32) are 676's
  source, rounding the string's end to a cell; A's strings are unpadded, so the decoder jumped past (LOOP) and EXIT -
  X1's translation ended after the EXECUTE helper's return (the translator's build: its (LOOP) stencil and ret, 52
  bytes more; the buffers otherwise the same but four address bytes), the native code ran on into the zeroed buffer
  and slid to its last byte (jit_mem + 0xFFFFF). small-jit has no jitexec, the portable designs no JIT.
- the tag-2 map: the translator ranks the one-byte codes by use, and with the string words no longer calling ALIGNED,
  fastest-x86-64's opcode 119 fell from rank 69 to 88 (src/vm-tag2-one.h, 20 codes moved one place); its genes.4 kept
  676's map (export-genes.py reads it from designs/NAME/src), so A was coded by the old map and decoded by the new -
  a return stack overflow at boot, once the engine was the lab's.

With each design exported from the lab (lab/evolve/export-designs.py) and its genes from that export (DESIGNS=
export-genes.py), all three self-host: best-all-round A = B 8,034 bytes (4-byte cells 7,486), fastest-x86-32 8,506,
fastest-x86-64 9,518 (4-byte 8,566). The step is tools/selfhost-lab.sh NAME ... (designs/ untouched). designs/ stays
the shipped roles: its images, engines and genes consistent with each other (make selfhost); the lab's state is checked
with selfhost-lab.sh; phase 6 ships new roles from it. `sh tools/selfhost-lab.sh` on all ten: PASS at 8-byte cells
(smallest 8,603, least-memory 9,278, portable-small 8,839, portable-knee 8,681, portable-arm 8,810, portable-fastest
9,386, small-jit 8,406 - the lab's map 8 bytes off designs/'s 8,398 - best-all-round 8,034, fastest-x86-32 8,506,
fastest-x86-64 9,518); at 4-byte cells best-all-round and fastest-x86-64 (smallest through designs/); s6 PASS.
