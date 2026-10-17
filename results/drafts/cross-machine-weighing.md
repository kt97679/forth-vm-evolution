# Weighing results across machines - a proposal (Iteration 376, for the owner)

The owner's question: what if a design does very well on the Tegra and badly on the laptop?

**What the checks show so far** (results/xcheck-seed56.md, seed 55's front on four machines): at the
same width, machines agree on the order - Spearman 0.944 laptop against the Tegra (12 designs), 0.917
against dream at 64 bits (24), 0.977 for the same designs at 64 bits on dream. What differs is the size
of an advantage: the fastest designs are ~1.45x slower on the Tegra than on the laptop, slow ones ~1.2x
- fast designs win everywhere, by less on smaller cores. The width reorders more (0.833 at 32 bits on
dream): the width's doing, not the machine's (Iteration 353).

**A blind spot: the scenario cannot be seen yet.** xcheck.py samples the laptop's front, so a design
the laptop rejects is never measured elsewhere - however good it would be there.

**Proposed policy**, under GOALS.md's aim and the generic-first order (RELF.md):
1. **Selection stays on the laptop**, at both widths since seed 57 - the other machines cannot measure
   thousands of designs a run. They are what held-out workloads are for the workloads: the test of
   whether the selection generalizes.
2. **A disagreement is diagnosed before it is weighed**: measured again (seed 55's fsys 3 looked bad
   at 32 bits on the VM - its 32-bit system calls 140x slower, not the design); the width separated
   from the architecture (the laptop at 32 bits against the Tegra); then knockouts on both machines -
   which gene makes the difference. That gene is the finding, worth recording either way.
3. **The best generic design is chosen for all classes of machine**: the final candidates measured on
   each - x86-64 (laptop, dream), x86 at 32 bits, ARMv7 (the Tegra) - ranked by the geometric mean of
   their speeds across the classes (each class once, so two x86-64 machines do not count twice), with
   a veto: none more than a set margin behind the best of its class. Example: A at 0.12 on the laptop
   and 0.52 on the Tegra, B at 0.14 and 0.40 - A's mean 0.250, B's 0.237: B, though slower here.
4. **A mechanism that helps one architecture and hurts another** becomes a per-architecture build
   choice only if its gain is large and the mechanism simple (GOALS.md); otherwise the design good
   everywhere is kept, and the finding written down.
5. **The blind spot tested**: after a run, a sample of designs the laptop rejected - from the whole
   population, not its front - measured on the Tegra and dream. Any that rank far higher there than on
   the laptop are the owner's scenario, real; none, and the laptop's selection stands for the others.

**Decided (the owner, Iteration 377): the three classes, equal** - recorded in GOALS.md. Open: the veto's
margin (25% proposed). **The blind spot's test is built** (Iteration 377): xcheck.py --sample ... --rejected K,
set in lab/evolve/REMOTES for the Tegra (4 of 16) and dream at 32 bits (6 of 30, and its paired 64-bit
check) - from seed 58's chain, its checks of seed 57's front and of designs seed 57 rejected.
