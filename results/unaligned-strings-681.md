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

designs/ is unchanged: its images, engines and the cross compiler's copy (designs/forth/) stay the roles as shipped
at 676, consistent with each other (run-tests' make selfhost); the new roles come from the reopened search.
