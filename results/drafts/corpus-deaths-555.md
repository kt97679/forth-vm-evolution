# Two corpus deaths in seed 76, reproduced (Iteration 555)

Seed 76's records hold two designs that died on the corpus (status "died: corpus", no error text): e80800407e
(generation 67, a crossover - tag2, t2hot and t2wide borrowed from b696007be3) and d11c9a6300 (generation 85, a mutation
- factor=3, nocrossjump=1, via the attic). Both cv8 JIT designs; neither near the front.

Rebuilt here (the processing sandbox: x86-64, gcc 13.3) and run on the corpus three times each, neither dies - each
prints an output different from s6's, the same every time: d11c9a6300 7827eeea, e80800407e f36f87e4, s6 5a4c122a (the
hash run_metric keeps, OUT_LAST). Ten other designs from the same records, front designs among them, match s6. A wrong
computation - deterministic here, a death on the laptop: an open correctness issue in a JIT combination (GOALS.md's stop
needs none open). The run's checks kept both off the front: seed 76's gate 289 of 289 alive, ans-check 0 of 69 differ.

To reproduce, as the build user in a built tree: read the genome below, then in Python with lab/evolve on the path -
`import evolve as E; E.setup(); eng, img = E.build(E.canon(genome), DIR); pw = E.private_work(DIR);
E.run_metric(eng, img, pw, 'corpus'); E.OUT_LAST[0]` against the same for `E.run_metric(*E.REF, 'corpus')`. The next
step: the genes these two share against their nearest designs that compute it right - one gene at a time.

Their records:

    {"id": "d11c9a6300", "gen": 85, "status": "died: corpus", "how": "mutation: factor=3, nocrossjump=1; via the attic", "genome": {"tos": 1, "scale": 0, "bytehdr": 1, "spec": ["var", "tiny", "small", "imm"], "sharedcall": 0, "doesfar": 1, "varcall": 1, "varslot": 1, "d256": 0, "guard": 0, "folds": ["+", "=", "!", "@", "LSHIFT", "RSHIFT", "C@", "C!", "AND", "OR", "XOR", "LIT", "<", "U<", "OVER", "DROP", "DUP", "SWAP", "ROT", ">R", "R>", "R@", "NEGATE"], "skippad": 0, "fold": 1, "supers": [["DUP", ">R"], ["C!", "R>"], [">R", "C!"], ["ROT", "DUP"], ["R@", "ROT"], ["DUP", "C@"], [">R", "OVER"], ["OVER", "C@"], ["C@", "="], ["C@", "DUP"], ["SWAP", "R>"], ["LSHIFT", "OVER"], ["OVER", "R>"], ["ROT", "ROT"], ["C@", "SWAP"], ["C@", "OR"], ["SWAP", "DUP"], ["R>", "SWAP"], ["OVER", "R@"], ["C@", ">R"], ["DUP", "@"], ["+", "R>"], ["R>", "="], ["C@", "OVER"]], "rtfuse": 0, "ops10": ["(DO)", "(LOOP)", "(+LOOP)", "(?DO)", "(LEAVE)", "I", "J", "UNLOOP"], "escape": 1, "tail": 0, "msc": 0, "opt": "O2", "nogcse": 0, "nocrossjump": 1, "nocet": 1, "align1": 0, "noreorder": 0, "peel": 0, "ipaclone": 1, "tracer": 1, "enc": "cv8", "lean": 1, "tag2": 1, "jit": 1, "jitx": 1, "jitloop": 1, "jitinl": 1, "thinhdr": 1, "bss": 1, "kstack": 0, "tailpn": 0, "alignhot": 0, "threads": 0, "fsys": 2, "regpin": 3, "dskew": 0, "hotcalls": 0, "rtimm": 2, "rtloop": 1, "rtloopall": 1, "kfast": 1, "tfind": 0, "kinput": 1, "klookup": 1, "rtiplus": 0, "swapi": 0, "t2hot": 0, "hotinl": 20, "opbody": 0, "t2wide": 0, "rtempty": 1, "alignfn": 0, "noinls": 1, "fbuf": 0, "abortif": 1, "opcall": [], "sysc": 0, "jitos": 1, "jittail": 1, "jitk": 2, "lto": 0, "gotodup": 0, "compiler": 0, "jitmul": 1, "jitdoes": 1, "jitexec": 1, "jitcfa": 1, "jitrp": 1, "jitfuse": 0, "opinline": 0, "knumber": 0, "jitret": 0, "jitvar": 0, "jitimg": 1, "bfind": 0, "factor": 3}}
    {"id": "e80800407e", "gen": 67, "status": "died: corpus", "how": "crossover; borrowed tag2+t2hot+t2wide from b696007be3; mutation: tracer=1, nocrossjump=1; via the attic; screened, audited", "genome": {"tos": 1, "scale": 0, "bytehdr": 1, "spec": ["loc"], "sharedcall": 0, "doesfar": 1, "varcall": 1, "varslot": 0, "d256": 0, "guard": 0, "folds": ["+", "=", "!", "@", "LSHIFT", "RSHIFT", "C@", "C!", "AND", "OR", "XOR", "LIT", "<", "U<", "OVER", "DROP", "DUP", "SWAP", "ROT", ">R", "R>", "R@", "NEGATE"], "skippad": 0, "fold": 1, "supers": [], "rtfuse": 0, "ops10": ["(DO)", "(LOOP)", "(+LOOP)", "OVER?BRANCH8", "(?DO)", "(LEAVE)", "I", "J", "2!"], "escape": 0, "tail": 0, "msc": 0, "opt": "O3", "nogcse": 0, "nocrossjump": 1, "nocet": 1, "align1": 1, "noreorder": 0, "peel": 0, "ipaclone": 0, "tracer": 1, "enc": "cv8", "threads": 1, "fsys": 2, "regpin": 1, "dskew": 1, "hotcalls": 0, "rtimm": 0, "lean": 1, "rtloop": 1, "rtloopall": 1, "bss": 1, "kfast": 1, "tfind": 0, "kinput": 0, "klookup": 0, "thinhdr": 1, "rtiplus": 0, "swapi": 0, "tag2": 1, "t2hot": 1, "jit": 1, "hotinl": 0, "opbody": 1, "t2wide": 0, "rtempty": 0, "jitx": 1, "alignfn": 0, "noinls": 1, "fbuf": 1, "kstack": 0, "abortif": 0, "opcall": [], "jitloop": 1, "sysc": 0, "jitinl": 1, "jitos": 0, "jittail": 1, "jitk": 0, "lto": 1, "gotodup": 1, "compiler": 0, "jitmul": 1, "jitdoes": 0, "jitexec": 1, "jitcfa": 0, "jitrp": 1, "jitfuse": 1, "opinline": 0, "tailpn": 0, "knumber": 0, "alignhot": 0, "jitret": 0, "jitvar": 0, "jitimg": 1, "bfind": 0, "factor": 1}}

## The bisect (Iteration 556)

One gene at a time here, on the corpus (results/drafts/corpus-deaths-bisect-556.py):

| design | the corpus |
|---|---|
| acf592137d - d11c9a6300's parent (JIT; tracer 1, nocrossjump 0) | right |
| the parent with factor=3 | right |
| the parent with nocrossjump=1 | wrong - 7827eeea, d11c9a6300's own |
| d11c9a6300 (both) | wrong |
| e80800407e (tracer 1, nocrossjump 1) | wrong |
| e80800407e with nocrossjump=0 | right |
| e80800407e with tracer=0 | right |
| e80800407e with both 0 | right |

The fault needs -ftracer and -fno-crossjumping together (tracer=1, nocrossjump=1) on a JIT design - and more besides:
268 JIT designs of seed 76 carry the pair and ran right; these two died. A layout-dependent fault, most likely in a JIT
stencil - machine code copied out of the compiled engine - that tail duplication without cross-jumping leaves wrong;
compilers lay it out differently (a death on the laptop, a wrong output here). Not guarded: the pair is mostly right, and
the run's output checks reject the rest. Open, for the JIT: acf592137d with and without nocrossjump=1 - one engine
source, one flag apart - is the smallest pair to compare stencil by stencil.

## The root cause and the fix (Iteration 557)

The two designs' flags differ by -fno-crossjumping alone. Compiled with each, spn-stencils.c's st_execute - EXECUTE
inline (jitexec) - holds EXECUTE's helper hole once with cross-jumping, twice without: -ftracer duplicated the block and
nothing merged the copy back. jit_scan notes one offset for each value hole and jit_put patches that one, so the other
copy kept its marker value (0x2ea1ed5ea1ed5e22) - a jump to nowhere on that path: a death on the laptop, here a fault
trapped into a wrong output. st_callx holds the same hole twice under -ftracer alone, on a path the workloads never take (the sweep, 558: in every build with tracer - 557 said every build; the design it was compared with had tracer too).
stencil-check.py passed both: it checks what leaves a stencil, not a hole that repeats - and under a design's own flags it
read no stencil at all (-ffunction-sections). The fix - the after-seed-77 batch (results/pending/ORDER.md): jit_fill
patches every copy; the checker reads a design's flags and reports repeated holes; jitholes-check.py in run-tests.
