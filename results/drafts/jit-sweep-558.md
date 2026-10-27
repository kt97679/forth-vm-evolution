# The JIT's stencils swept across the compiler genes (Iteration 558)

Seed 76's corpus deaths came from one pair of compiler genes; the tests check the stencils under the default flags and,
from the after-seed-77 batch, under that pair. The owner (558): sweep the rest. The base: d11c9a6300 with every compiler
gene at its default - its JIT genes, and so the stencils it builds (the stack cache's among them), kept - compiled as a
design's engine is, through the after-seed-77 batch's stencil-check.py (a design's own flags; a value hole that repeats
reported). The compiler genes that change the flags: align1, alignhot (1-3), gotodup (1, 2), ipaclone, nocet,
nocrossjump, nogcse, noinls, noreorder, opt (O3, Os), peel, tracer - 16 values: every one alone, every pair of two genes
(115), and 200 random triples (seed 558): 332 flag sets. Script: results/drafts/jit-sweep-558.py.

**Not safe to copy: none** - no stencil, under any of the 332, refers outside itself or branches past its copied part;
every set compiled and read its stencils.

**A value hole twice in a copied part** - the fault seed 76 found, harmless once jit.c patches every copy:
- st_callx under 48 of the 332 - every set with tracer=1: -ftracer alone duplicates its block. A path the workloads never
  took, in every tracer design with jitexec (557 said every build: the design it was compared with had tracer too).
- st_execute under 7 - every set with tracer=1 and nocrossjump=1, and only those: seed 76's pair.

Nothing else repeats. So the after-seed-77 batch's fix covers what the compiler genes can do to the stencils, and the
JIT needs no guard beyond it. Not swept: the -D side (the JIT genes, regpin, the stack cache's depth) - the base's own,
one set.
