# A converter death seed 54 found: "call target 1390 not 8-aligned" (Iteration 333)

One design of seed 54's 41,406 died converting its image: a2c8d50d0a, "image did not convert
(AssertionError: call target 1390 not 8-aligned)" - tools/layout.py asserting on its own placement:
a call's target off the 8-byte boundary some encoding needs. Discarded by the evolution, as the
JIT fault's designs were (results/drafts/jit-loop-crash.md); not yet looked into. Next: reproduce
(evolve.build of the genome), bisect its genes against s6 as for the JIT fault, find the assertion's
assumption. When fixed, the genome goes to lab/evolve/regressions.json.

The genome (the database's record):

```
{"abortif": 0, "align1": 0, "alignfn": 0, "alignhot": 0, "bfind": 0, "bss": 0, "bytehdr": 0, "compiler": 0, "d256": 0, "doesfar": 0, "dskew": 0, "enc": "cpt16", "escape": 0, "factor": 0, "fbuf": 0, "fold": 0, "folds": ["+", "=", "!", "@", "LSHIFT", "RSHIFT", "C@", "C!", "AND", "OR", "XOR", "LIT", "<", "U<", "OVER", "DROP", "DUP", "SWAP", "ROT", ">R", "R>", "R@", "NEGATE"], "fsys": 0, "gotodup": 0, "guard": 0, "hotcalls": 0, "hotinl": 0, "ipaclone": 0, "jit": 0, "jitinl": 0, "jitk": 0, "jitloop": 0, "jitos": 0, "jittail": 0, "jitx": 0, "kfast": 0, "kinput": 0, "klookup": 0, "knumber": 0, "kstack": 0, "lean": 0, "lto": 0, "msc": 0, "nocet": 0, "nocrossjump": 1, "nogcse": 0, "noinls": 0, "noreorder": 0, "opbody": 0, "opcall": [], "opinline": 0, "ops10": [], "opt": "O2", "peel": 0, "regpin": 0, "rtempty": 0, "rtfuse": 0, "rtimm": 0, "rtiplus": 0, "rtloop": 0, "rtloopall": 0, "scale": 3, "sharedcall": 1, "skippad": 1, "spec": ["loc", "var", "tiny", "small", "imm"], "supers": [], "swapi": 0, "sysc": 0, "t2hot": 0, "t2wide": 0, "tag2": 0, "tail": 0, "tailpn": 0, "tfind": 0, "thinhdr": 0, "threads": 0, "tos": 1, "tracer": 0, "varcall": 1, "varslot": 1}
```
