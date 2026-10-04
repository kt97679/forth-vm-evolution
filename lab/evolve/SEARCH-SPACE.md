# The search space - prompts/02 on the gene pool

Iteration 4. Before any further gene: is the gene pool a search of the
design space, or a recital of designs that already exist? The seven steps
of prompts/02-escape-recall, each with its evidence.

## 1. The recall

| gene | a named existing system? | from |
|---|---|---|
| cell threading, 16-bit tokens, CV8 bytecode | yes | classic Forths; relf's SOD16, CPT16, CV8 |
| superinstructions; run-time fusion | yes | gforth (Ertl, Gregg) |
| tail-call threading | yes | Wasm3, CPython 3.14 |
| multi-state stack caching | yes | Ertl's stack caching |
| escape band, format-10 opcodes | yes | relf |
| folds, specialisations, short branches | yes | relf's CV8; the JVM's goto/goto_w |
| guard pages; the GCC flags | yes | operating systems; gforth's build |

Every row says yes: the pool was recalled, not searched. Steps 2-7 are
therefore mandatory.

## 2-3. The axes, and what the pool leaves out

Counted by code, not estimated: each axis's possible values written out,
the included ones checked to be among them.

| axis | possible | included | missing |
|---|---|---|---|
| instruction unit | 5 | 3 | nibble; variable bit length (Huffman-like) |
| call encoding | 6 | 3 | position-relative offset; one-byte calls through a table of hot words; no call: body inlined at the call site |
| dispatch | 8 | 3 | switch; direct threading; indirect threading; subroutine threading; call threading |
| top of stack in registers | 6 | 3 | two, always; dynamic 0-3; static, chosen by the converter |
| stack bound checks | 4 | 2 | one check per word entry; none |
| opcodes beyond primitives | 11 | 8 | triples and longer runs; two escape levels; compare-and-branch |
| which pairs | 4 | 3 | chosen by the converter from the image itself |
| headers | 4 | 2 | apart from the code; hash threads varied |
| C compiler | 12 | 6 | profile-guided (PGO); -march=native; LTO; global register variables; no PIE; no stack protector |
| primitive set | 3 | 1 | hot colon words made primitives; rare primitives moved to Forth |
| native code | 3 | 1 | SPN stencils; an optimising compiler |
| **all 11 axes** | **66** | **35** | **31 missing** |

Every missing value decided (14 candidate, 8 excluded, 4 stranger, 4 deferred, 1 planned; checked against the register of rejected and deferred approaches in GOALS.md):

| missing value | decided | why |
|---|---|---|
| nibble unit | excluded | 16 codes cannot hold 68 primitives without an escape on most of them - a variable-length code by another name, covered next |
| variable bit length (Huffman-like) | stranger | see step 4 |
| position-relative calls | excluded | the image loads at a fixed base: relative and image-offset calls cost the same bytes and the same add |
| one-byte calls through a table of hot words | stranger | see step 4 |
| bodies inlined at the call site | stranger | see step 4 |
| switch dispatch | excluded | measured slower than the token table in the dispatch lab |
| direct threading | deferred | the register in GOALS.md: the dispatch lab gave -5% fib, -12% sieve but +9% loop; relf found dispatch already at the indirect-jump rate |
| indirect threading | planned | GOALS.md, remaining genes |
| subroutine threading | deferred | native code - the user deferred it at Iteration 4 |
| call threading | excluded | real calls and returns for dispatch lost in the dispatch lab (the register in GOALS.md); tail calls are the same shape without them |
| two items always in registers | excluded | lost in the dispatch lab (the register in GOALS.md) - multi-state caching is its dynamic form |
| dynamic 0-3 items | candidate | a third more handlers for a state the profile may rarely need - unmeasured |
| static caching, states chosen by the converter | candidate | large: the converter would need every instruction's stack state |
| one stack check per word entry | candidate | hard: a word's depth is not known statically across EXECUTE and loops |
| no stack checks at all | excluded | an underflow would corrupt memory instead of being reported - not a design to ask the gate about |
| triples and longer runs | candidate | the next step from pairs; gen-super.py composes two bodies, three is the same path |
| two escape levels | candidate | the escape is the largest single gain in every knockout - more slots may be worth more |
| compare-and-branch opcodes | candidate | SPN has them as stencils; in bytecode a pair whose second half takes an operand |
| pairs chosen from the image itself | stranger | see step 4 |
| headers apart from code | candidate | separated heads, known in Forths - denser code |
| number of hash threads | candidate | kernel-level; FIND's speed is most of parse and corpus |
| profile-guided optimisation | candidate | strong: the engine is one large function whose layout GCC can only guess |
| -march=native | candidate | cheap; designs tuned to the machine they are measured on |
| LTO | excluded | one translation unit - nothing across units to optimise |
| global register variables | candidate | gforth pins ip, sp and the top of stack this way |
| no PIE | candidate | cheap: absolute addresses in the dispatch tables |
| no stack protector | candidate | cheap, likely no effect: the handlers keep no arrays on the stack |
| hot colon words made primitives | candidate | format-10 and tiny words cover part of it; the general form is open |
| rare primitives moved to Forth | excluded | until the size measure counts the engine, it could only grow the image |
| SPN stencils | deferred | native code - deferred at Iteration 4 |
| an optimising native compiler | deferred | relf's - measured at Iteration 3, deferred at Iteration 4 |

## 4. Deliberate strangers

Chosen because no well-known system uses them; kept, because for each I
cannot say it is worse rather than unfashionable:

- **One-byte calls through a table of hot words.** A band of opcodes, each
  a call to one of the design's hottest colon words, the targets in a
  per-design table. VMs spend scarce opcodes on operations and use one
  generic call; here the escape frees slots, and a few words take most
  of the calls.
- **Bodies inlined at the call site by the converter.** Bytecode VMs leave
  inlining to a JIT: it grows code and loses a word's identity for
  redefinition and debugging. Our images are fixed after conversion,
  and the size objective prices the growth.
- **Pairs chosen by their count in the image, not by a run-time profile.**
  Superinstructions are pursued for speed; for the small end of the front
  what saves bytes is how often a pair is written, not how often it runs.
- **Variable-bit-length opcodes.** Decoding bits slows dispatch - for speed
  probably genuinely worse; but the smallest end of the front has nothing
  else this strong to try.

## 5. A uniform sample, before trusting the optimum

`evolve.py --sample N --seed S` draws N designs uniformly - the family
uniformly, then every gene over its domain - and builds, checks and
times them as the run does, into its own file. On the VM, 32 designs,
seed 1, 2 rounds:

- **alive 30 of 32**; speed against s6: fastest 0.935, quartiles 1.306 and
  1.759, median 1.592, slowest 2.202; **faster than s6: 1 of 30**; size
  10,177 to 25,144 bytes.
- **The run's best (0.662 on this VM) is faster than all 30.** The front is
  a peak the search found, not a plateau that random designs reach: the
  gain is structure, and the evolver earned it.
- **Both deaths are the reach limit SCAN.md describes** - two-byte-only
  forms at scale 0 - verified by reverting genes one at a time, not
  inferred: the corpus death lives with doesfar 0 -> 1 alone and with no
  other single reversion of its 16; the timed-out one lives only with both
  far forms back. New: past its reach, a near DOES> can fail *silently* -
  wrong output, not an error.

**On the Ryzen, 128 designs, 3 rounds** (Iteration 5,
`results/sample-amd-ryzen-7-pro-8840hs.md`): alive 108 of 128; fastest
0.860, median 1.242, 10 faster than s6; the run's best, 0.595, beats all
108 - the same answer at four times the size and on the real machine.
19 of its 20 deaths are the reach limit; **the 20th was a generator
fault**, not a design's limit: cached top of stack with format-10 words
and no specialisations could not compile (`tools/gen-tos.py` had dropped
two preprocessor lines), and behind it multi-state caching without
specialisations could not either (`tools/gen-msc.py`). Both fixed;
neither run had reached that region. This is what step 5 is for: a
search that starts from hand-made designs never visits where they are
not.

## 6. What stayed fixed

| fixed | if it were varied |
|---|---|
| the kernel's source and its 68 primitives | designs could move work between Forth and C (step 3's primitive-set rows) |
| the workloads: kernel, fib, parse, corpus; loop held out | the front is tuned to them; other programs could rank designs differently |
| the gate: corpus output and the kernel image byte for byte | nothing correct is lost to it; designs that are faster by being wrong are |
| GCC 13 and one C function with computed goto | clang, or another engine structure, changes which handler code wins |
| the metric: CPU time over s6's, geometric mean | cycles (EVOLVE_METRIC) or wall time could reorder close designs |
| size: the self-hosting image, not the engine | pairs and cached-stack variants cost engine bytes the front never sees |
| x86-64 Linux | another architecture's branch predictor and registers change the ranking |

## 7. What could not work

- Two-byte-only calls or DOES> at scale 0 or 1: the dictionary outgrows
  2^14 units (SCAN.md; the sample's two deaths).
- Byte headers with scaled calls: the converter refuses - byte headers
  need scale 0.
- Skip-padding with scale 2 or 3: the alignment would be undone.
- Run-time fusion: alive and correct, rejected by selection - 560-576
  bytes of overlay for no measured gain.
- Tail calls with multi-state caching: excluded by construction - two
  ways of keeping the stack that cannot share handlers.
