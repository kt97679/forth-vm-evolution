# The prompt for a new chat (Iteration 162)

Paste the text below into the new chat, with the newest bundle attached
(`forth-vm-evolution-claude-iterN-*.bundle`) and any packs not yet processed
(`forth-vm-evolution-*.tar.gz`).

---

We are continuing my project forth-vm-evolution: an evolutionary search over
the design of a small Forth virtual machine (engine + image), descended from
my RelF. Attached is the newest git bundle of the repository, and the packs of
any laptop runs not yet processed.

**Set up first.**
0. As root, give the VM the laptop's 32-bit half: `apt-get update -qq && apt-get install -y -qq gcc-multilib` -
   the build then makes 8-byte and 4-byte cells, as the laptop's does (Iteration 129).
1. Clone the bundle as the user `claude` - the repository must be owned by it,
   and every git, build and tool command runs as `runuser -u claude -- ...`.
   If /home/claude belongs to root, make the directory and hand it over first:
   `cd /home/claude && mkdir -p forth-vm-evolution && chown claude:claude forth-vm-evolution && runuser -u claude -- git clone /mnt/user-data/uploads/<bundle> forth-vm-evolution`
2. Build and check, in the clone:
   `runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh && runuser -u claude -- bash tools/run-tests.sh && runuser -u claude -- python3 lab/evolve/evolve.py --validate`
   - expect "PASS - no regressions" and the seven hand-made stages IDENTICAL.
3. Read GOALS.md first: its section "Resuming in a new chat" opens with a
   HANDOFF - the state, the pending run, the open threads in order, where to
   look. Then lab/evolve/NEXT-RUN, lab/evolve/GENES.md (the genes and the
   ranked lists of ideas), the newest PROGRESS.md entries, lab/evolve/RUNNING.md,
   and prompts/INDEX.md - the methods library: use it when its triggers fire.

**How we work - my standing preferences.**
- The aim is the smallest, simplest system that does the job. Three equal
  objectives: speed (the geometric mean against hand-made s6 over the selected
  workloads), binary + image bytes, and memory (pages touched; within 8 KB is
  a tie). Simplicity and readable Forth matter: prefer improving the Forth
  over adding C fast paths.
- Every mechanism is priced before it is built, and built behind a gene so
  evolution weighs it; with the gene off, recorded designs must stay identical
  (check their ids and images). Measurement changes go in alone.
- Measure honestly: prove a check can fail before trusting it (prompts/15),
  audit the tools (prompts/03). The VM has one CPU: its timings are noise, its
  byte counts and dispatch counts exact; speed is measured on my laptop.
- Runs happen on my laptop, `sh lab/evolve/next-run.sh`, which reads
  lab/evolve/NEXT-RUN; I send back the packs. Processing a run: the stopping
  rule against the earlier runs of the same comparison session (small = the
  fastest better by under 5%, the smallest by under 2%, memory under 8 KB; two
  small in a row and the gene set has converged); results/evolve-...-seedN.md
  with the front's genomes; the session appended to
  results/compare-fronts-amd-ryzen-7-pro-8840hs.md; GOALS.md, PROGRESS.md and
  NEXT-RUN updated. Run lengths and run choices are mine: propose, don't
  impose.
- Every change is a commit `Iteration N: ...` (the bundle script requires that
  subject; git identity Kirill Timofeev <kt97679@gmail.com>) and a bundle:
  `runuser -u claude -- sh tools/make-bundle.sh /mnt/user-data/outputs`, the
  file presented to me. The next iteration is 133.

**Where it stands.** Seed 35 was the second small run in a row: the gene set
converged. New since: the genes fbuf (memory), kstack, abortif and opcall; the
stack guard fixed; a held-out check, lab/evolve/ans-check.py. Seed 36, 4
hours from scratch, answered the anchoring question: no. Iteration 124: the
held-out check is now the Forth 2012 test suite (tests/ans); it found five
faults every stage shares - DELETE-FILE's segfault fixed; tests/core/tester.fr
restored. Iteration 125: RelF's fixes taken (the project forked from RelF at
e8440ed) - +LOOP, a standard PARSE and the strings on it, the file words,
CONVERT, long names and IF outside a definition refused - with their tests in
run-tests.sh; every image changed (+120-160 bytes). Seed 37, 9 hours with the
new genes: not small - memory 184 -> 156 KB, 90 of 107 on the front of all
runs. Iteration 127: the measurement changed - Haley's +LOOP cases in the
gate, bubble and ackermann selected, parse held out. Bubble and
ackermann are my RelF/bench programs (Iteration 128). Seed 38's first start
failed at the tests - two new sections expected SPN stages at 4 bytes, a half
the VM did not build; fixed in Iteration 129. Iteration 130: the gene jitloop ((+LOOP) and (?DO)
native on the JIT), built and dormant until seed 39 has run. Seed 38 processed (Iteration 151:
small). Pending: seed 39, 7 hours, the same genes; then the after-seed-39 batch - process its
packs when I send them, then apply the batch (GOALS.md has the procedure). The open threads after it are in the HANDOFF.

Please set up, confirm the checks pass, and tell me what you will do next.
