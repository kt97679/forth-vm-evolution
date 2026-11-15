# The gene rtconst - a constant compiled as its value at run time (Iteration 691; step 3, mechanism 1)

forth/cv8-fuse-const.4: a call to a word whose code is one literal and EXIT - CONSTANT8 lays LIT, (LIT8, LIT16, LIT32
or LIT64) and a plain EXIT; `: X 5 ;` lays the same - becomes that literal, through LITERAL (rtimm's n + still fuses
after it). relf's rule: always the literal, whatever its width; relf's test: constant-time, the callee's first byte and
the byte after its operand (59's rtlit searched, and lost the compiling workloads). No converter table: the codes are
the overlays' constants, which the converter writes to the design's own. evolve.py's gene rtconst (it needs the
run-time fusers) and its -const dumps, loaded after rtvar's overlay; under the tag with the JIT a colon definition
begins with the JIT's header, which the test does not step over - there CONSTANTs only.

## Checked (lab/evolve/rtconst-check.py): PASS on portable-knee and fastest-x86-64

Alive with rtconst 0 and 1; the same and right values for constants of every literal width (64, 70000, -5,
5000000000), `: F 7 ;`, BL and `N 3 + M +`; T1 (`N`) compiles to LIT8 64 and EXIT where it was a call and EXIT.

## What it buys

| design | the apps workload (medians of 15) | each program alone (the knee) |
|---|---|---|
| portable-knee | 37.2 -> 36.2 ms, **0.975** | sim16 0.968, gc16 0.943, scan 0.923, evo 0.981, shellmix 1.017 (7 constants: noise) |
| fastest-x86-64 (the JIT) | 23.6 -> 18.2 ms, **0.770** | - |

On the JIT design a run-time CONSTANT has no JIT header, so native code called it through the interpreter at every
use; as its literal it stays native - the larger gain. Bytes: a LIT8 constant (2 bytes) is no longer than its call;
wider ones are longer, and rare.
