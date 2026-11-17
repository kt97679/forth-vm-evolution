# The after-seed-95 batch - to apply first at seed 95's processing (Iteration 701)

process-run.sh checks and applies it. Seed 94's stall (Iteration 700) left three things the laptop's run does not
record - each patch adds a record and changes no gene, objective, selection or in-run measurement, so the series'
method stands (no NEXT_METHOD) and seed 96 is judged against seeds 92-95 as before.

    git apply results/pending/why32-after-seed95.patch
    git apply results/pending/remeasure32-after-seed95.patch
    git apply results/pending/ticker-after-seed95.patch

**why32-after-seed95.patch** (lab/evolve/evolve.py, lab/evolve/review-checks.py) - a 32-bit failure's message keeps its
first 150 and last 400 characters (all of it up to 600), not its first 200: seed 94's 3b5bdaebbc kept only the start of
its clang command, the cause cut off - built here at 4-byte cells it is right on kernel, apps and fib (700). fail32 labels
a "timed out after" or a CPU-limit message with the command that tells the machine from a hang (design.py ID --width 4);
rule 5 still counts it as another cause, since a hang would be a fault. Tested: the parse of both files, and the
batch's run-tests.

**remeasure32-after-seed95.patch** (lab/evolve/evolve.py, lab/evolve/next-run.sh) - `evolve.py --remeasure N` measured
only the 64-bit front: it was never given two widths, so its front and evaluate() were one width's, and seed 94's fastest
at 32 bits - 2806f89619, one wrong kernel reading - was never measured again (700). Now a database selected at two widths
(most alive designs with a 32-bit speed) sets them before the setup: the 64-bit pass as before (the same front, one
width, remeasure.json the same shape), then the two-width front's 32-bit fastest tenth, at least 10, measured again at 32
bits alone, N rounds, into build/evolve/remeasure32.json - its own file, which next-run.sh packs beside remeasure.json and
lab/evolve/outliers.py reads (--remeasure32; process-seed.sh passes it). report() picks its widths from the records, so
report.md is unchanged. The laptop's cost: about 45 designs' 32-bit build and N rounds - about 8 minutes at seed 94's
pace; phase_record times the step for the next chain's reserve as before. Tested in a scratch clone on 12 of seed 94's
records (2806f89619 and its parent among them), --remeasure 2: the 64-bit pass the same 8 designs, the 32-bit pass 9;
2806f89619's 32-bit kernel re-measured 0.475 against its parent's 0.455 (the VM's ratios, higher than the laptop's at
both); outliers.py's remeasure32 line read the file.

**ticker-after-seed95.patch** (lab/evolve/chainctl.py) - each `next-run: progress` line ends with what the machine was
doing - the load, the memory free and the swap used, the cores' mean clock, the hottest thermal zone, AC or battery, each
where Linux has it - and "the tick N s late" when a 300 s tick ran a tenth or more over: seed 94's ticks ran 25-70 s late
through its 93-minute stall and nothing said why (memory pressure, the clock, heat or the power - 700). No tool parses
the line past the database's count. Tested: machine() on the VM (load and memory - it has no cpufreq, thermal or
power-supply files) and the ticker itself at TICK_EVERY=2.
