# Which genes interact - read from seed 46's own mutations (Iteration 250)

The outside reviews asked for a gene-interaction study before more changes to
the search. Seed 46's database has 14,367 children made by one gene changed;
6,547 of them flip a 0/1 gene of a measured parent and change nothing else the
parent expresses (a flip that switches other genes on or off - tos enabling the
JIT - is gating, not interaction, and is left out). For each such gene A and
each other gene B, the effect of turning A on - the change in log speed and
log size, child against parent - is compared between parents with B on and off
(Welch's t). The tool: `lab/evolve/gene-interactions.py`.

## What it finds

- **The JIT is a regime, not a gene among others.** Over all parents, every
  strong interaction is "B = the JIT": turning rtloop on makes a design 33%
  faster without the JIT (log -0.40) and 62% faster with it (-0.98) - the JIT
  translates the loop forms rtloop makes; -fno-gcse costs 18% without the JIT
  and nothing with it; peel, align1, bss and ipaclone change a JIT engine's
  size less or not at all. Under the JIT most interpreter genes are nearly
  neutral.
- **rtloop and the JIT:** the one synergy that would justify linking two genes
  for crossover - but evolution has fixed it already: rtloop is on in all 45 JIT
  designs on the front and in 10,202 of the 10,420 JIT designs that lived.
- **Within the interpreter (parents without the JIT)** interactions are weak:
  the strongest, t 6-8, are all with ipaclone (the dispatch cloned per handler,
  which changes the code layout the other compiler genes act on) - ipaclone
  with klookup, guard, align1, nocet, varslot, d256: effects of 5-10% in speed
  that change with it. Size interactions have high t but tiny effects (sizes are
  exact, so a 0.1% difference is "significant").

## What it means for the search

- The crossover links (E.LINKS) are right as they are: the JIT's genes inherit
  together and need to (jit x jitx, jit x jitloop: t 42-44); no other pair
  interacts strongly enough to link, and the strong one, rtloop, is fixed.
- Possible saving, not built: on a JIT design, a mutation of an interpreter-only
  gene (peel, align1, noinls, ipaclone, nogcse...) rarely changes its measures;
  the surrogate screen already skips some of these children. Weighting the
  mutation choice by regime would spend those evaluations elsewhere - worth a
  look if the JIT end stalls.
