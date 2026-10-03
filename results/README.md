# Published measurement runs

`RESULTS.md` in the repository root is generated and untracked - it
differs on every machine and would conflict on every pull. Files here
are deliberate snapshots, each naming the machine it came from, so two
runs can be compared without either being mistaken for the canonical
one.

    tools/collect-results.sh run
    tools/collect-results.sh report --save results/<machine>.md

Ratios travel between machines; absolute milliseconds do not. Each file
carries the host block the sweep recorded, so it says for itself what it
ran on.

## The Ryzen 8840HS, in CPU time and in cycles

`amd-ryzen-8840hs.md` is the September snapshot: CPU time, five layout
builds, three builds from a clean tree. `amd-ryzen-7-pro-8840hs-x86_64-run1.md`
and `-run2.md` are the two sweeps of one build at 27cc702, measured in
CPU CYCLES by `tools/bench-laptop.sh` (powersave governor, load 0.63);
`spn-amd-ryzen-7-pro-8840hs-x86_64.md` is the same run's SPN
measurements: start-up, end to end, memory, in CPU time, cycles and
instructions.

The two snapshots agree: for s1-s6 the ratios differ by a median of
1.2%, none by more than about one and a half combined standard errors -
a run in cycles reproduces a run in CPU time.

The same files at bfec34e are the run before the compare-and-branch
fusion (load 1.7), so the pair measures it: fib for s8-spncv8 went from
0.194 to 0.111 of the cell engine, level with s7 (FINDINGS-SPN.md).
Everything the change could not touch agreed between the two runs to a
median of 0.3%. That earlier SPN report's sections on CPU time versus
cycles were rewritten from its raw minima by `tools/clockfit.py`, whose
first explanation had blamed the clock; this one's were written by it.

`evolve-amd-ryzen-7-pro-8840hs-seed1.md`: the first evolution run on the Ryzen
(lab/evolve) - the front, measured again, against the hand-made stages.
