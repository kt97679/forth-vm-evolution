# Progress log

Append-only: one entry per session, newest last. A wrong entry is
corrected by a later one that says so, not edited (prompts/12-progress-log).
History before this log: the git log, `FINDINGS-*.md`, `lab/*/README.md`.

## 2026-10-03 - Claude, commits 868c4c3 .. this one

**Done.** The evolution lab's gene pool grew: superinstructions (pairs from
each design's own profile), run-time fusion, relf's format-10 opcodes
(eleven words and two short branches), the escape, tail-call threading,
multi-state stack caching with composed pair effects. The evolver was made
trustworthy: four genome-to-image mapping bugs, a survival check that
never checked the kernel was written, runaway designs contained, a
mutational scan, a deterministic resume, and the design built is now the
design recorded. Measurement is the process's CPU time, paired with s6.
Also: every image reproducible (the SPN savers), READ/WRITE as SPN
stencils (parse 0.974), line-at-a-time ACCEPT (5-14% faster on stdin,
seeds bootstrapped), and `prompts/` from relf with this log and
`GOALS.md`.

**Measured.** A full rehearsal on the VM (1,306 designs; `REHEARSAL.md`)
and the first run on the Ryzen (`results/evolve-amd-ryzen-7-pro-8840hs-
seed1.md`): measured again, 0.609 of s6's CPU time at 13,480 bytes, and
0.649 at 9,801. Both searches found the same kind of design.

**Failed, reverted or rejected** - each in `GOALS.md`'s register: run-time
fusion; the first ACCEPT (3-11% slower); multi-state caching with 25
operations (lost); a retry added on a wrong diagnosis; the claim that
multi-state caching buys less on Zen 4.

**Learned.** Every bug that cost a run lived in how the lab built or
recorded designs, not in the designs: the lesson of the four mapping
bugs, the unchecked kernel, the forked resume and the raw genome. And a
selected front re-measures 3-6% worse: quote `--remeasure`.

**Open.** `GOALS.md`, "Next". Pick up first: the knockout study.

## Iteration 1 - 2026-10-03 - Claude

**Correction to the entry above.** It ended with a handoff named
`forth-vm-evolution.bundle`, as every handoff before it was. That is
prompts/07-git-handoff's placeholder, not a name: 07 asks for
`project-claude-iterN-YYYYMMDD-HHMMSS.bundle` unless the project has its
own convention, and this one had none written down. The user caught it.

**Done.** The convention is now in `GOALS.md` ("Conventions"), where 07
says to look before a handoff; `tools/make-bundle.sh` follows relf's
script - N from HEAD's `Iteration N:` subject, UTC time, HEAD and master,
the clone check, the path printed. Handoffs are numbered from this one.
`lab/evolve/RUNNING.md` names the bundle by the convention.

**Open.** Unchanged - `GOALS.md`, "Next". Pick up first: the knockout study.

## Iteration 2 - 2026-10-04 - Claude

**Search first (prompts/12):** "knockout", "ablation", "contribution" in
GOALS.md, PROGRESS.md and lab/evolve - only the plan; no prior attempt.

**Done.** `evolve.py --knockout [ID,...] [--rounds N] [--db FILE]`: for
each design, every gene that differs from hand-made s6 set back to s6's
value, one at a time, and measured again. Shaped by prompts/03 and 11:
every figure labelled measured; a calibration against known answers (s6
against itself: speed 1.000, size exactly 10,065; the design itself
measured again in the session); the ways it can mislead stated in the
report (knockouts are in context and do not add up; "also changed" lists
what moved with a gene - the escape takes its slots, undoing multi-state
caching wakes the tail calls a genome carries dormant); for pasting back,
machine and commit in the report, progress on stderr.

**Tried here (VM, one design, 1-2 rounds) - not results.** It runs end to
end: s6 against itself 0.992 and 1.024, size exact. At one round the
noise is large - the pairs' knockout came out +22% in one run, +4% in the
next - so the default stays 6 rounds.

**Open.** Run on the Ryzen. Pick up first: its report.

## Iteration 3 - 2026-10-04 - Claude

**Knockouts on the Ryzen** (`results/evolve-knockout-amd-ryzen-7-pro-
8840hs.md`; calibration: s6 against itself 1.003, size exact). What
carries the front's 30-40%: the escape with the pairs it makes room for
(+28-37% when undone), superinstructions (+17-35%), guard pages instead of
a bound check per push (+9-19%), relf's format-10 opcodes (+6-14%), no
endbr64 (+6-13% - the dispatch lab on the VM had found that did not carry
over; on the Ryzen it does). Multi-state caching: only 2-9%.

**Asked: can relf's native compiler (relf master, NATIVE.md) join the
genome?** prompts/02 skipped: the user named the candidate. Measured, not
read about - relf master at 8b03275, `make relf64 native-kernel`, here on
the VM:

- **Our corpus: identical to our cell engine's output, byte for byte.**
- **Our kernel workload: segmentation fault** (exit 139), kernel.img never
  written. extend.4 loads, INCLUDED and run-time DOES> work; cross.4
  cross-compiles kernel.4 to its end (last message "Redefining: COLD")
  and the crash comes after - where cross.4's RESOLVEs walk the forward
  chains through ' >BODY @. Reproducer: in this project's build/work,
  `printf 'S" extend.4" INCLUDED\nS" cross.4" INCLUDED\n' |
  .../native-kernel`; expected kernel.img written and equal to the
  reference; actual SIGSEGV. A report for relf.
- **Speed against s6, paired, CPU time (VM - scale only):** fib 0.127,
  parse 0.309, corpus 0.363, loop 0.102; output identical to s6's on all
  four. The best evolved bytecode designs are at about 0.61 on the Ryzen.

**So:** not addable as it stands - it would die at the gate (kernel
workload), and its N2 rules are fixed in its code generator, not
switches. Two ways it could join: (A) a `native` family - relf's native
compiler with its rules made switchable (relf-side), the crash fixed, a
species of its own, its genes the rules and the inline threshold - which
fits relf's own "speed first, size watched" question; (B) our SPN, the
native back end of THIS project (s7, s8), into the genome, with relf's
rules ported to it as genes - recombining with the CV8 genes beneath it.
The user to choose.

**Open.** GOALS.md, "Next". Pick up first: the user's choice between A and B.

## Iteration 4 - 2026-10-04 - Claude

**The user deferred native code** (both ways from Iteration 3) - into the
register in GOALS.md with what Iteration 3 measured.

**The stdin figures, reproducible.** `tools/compare-commits.py OLD NEW`
builds two commits in worktrees and times them against each other on
stdin, with a calibration (the old build against itself). Both findings
reproduced at their published settings: ACCEPT (12 rounds, calibration
0.995) s0-cell 0.900/0.878, s4 0.906/0.880, s6 0.933/0.939, s8
0.939/0.917 for parse/corpus, against 0.861-0.961 published; the stencils
(25 rounds, calibration 1.001) parse 0.969, corpus 0.972 against 0.974,
0.976. Same direction and size; single figures move by up to 4% on the
VM. Each finding names its command now. At 5 rounds, the trial's
calibration was 0.975 - the change's 0.971 within its noise: the
calibration doing its job.

**prompts/02 on the gene pool** (`lab/evolve/SEARCH-SPACE.md`). Step 1:
every gene is recalled from a named system. Steps 2-3: 11 axes, 66 values,
35 in the pool, 31 out - each decided: 14 candidates, 8 excluded, 4
strangers, 4 deferred, 1 planned. Three decisions I first got wrong
(two cached registers a candidate, direct threading "planned", call
threading's reason) the register in GOALS.md corrected - it had them.
Step 5: `evolve.py --sample N` added; 32 uniform designs on the VM: 30
alive, median 1.59 times s6's time, 1 faster than s6; the run's best,
0.662, beats all of them. Both deaths the reach limit of two-byte-only
forms at scale 0, verified by reverting genes one at a time; new - a near
DOES> past its reach can fail silently, with wrong output.

**Open.** GOALS.md, "Next". Pick up first: the owner's runs on the Ryzen
(seed 2, then the sample); then the first candidates from SEARCH-SPACE.md.

**An incident, and its cause fixed.** Checking the edited evolver with
`evolve.py --help`, I started a full run: the evolver did not know
`--help`, and an unrecognised option fell through to evolving. In 4
minutes it appended 86 records (generations 1-6 of a new run) to the VM
rehearsal's database. Removed by the one place where the generation
drops (after the rehearsal's last generation-40 record; exactly one such
place, checked before cutting); the database is again the rehearsal's
1,306 records; the whole file kept as `db.jsonl.with-stray-run`. Now
`-h`/`--help` prints the usage and any unknown option is refused before
anything runs - `--sampel` would have done the same as `--help`.

## Iteration 5 - 2026-10-04 - Claude

**The owner's runs on the Ryzen**: seed 2 and a uniform sample of 128.

**Seed 2 found seed 1's front** (`results/evolve-amd-ryzen-7-pro-8840hs-
seed2.md`), re-measured: 9cd791dd84 0.619 at 13,472 bytes against seed
1's 0.609 at 13,480; 0ebf0445e0 0.667 at 9,761 against 0.649 at 9,801 -
within noise, and the same genes. Re-measuring moved the run's figures by
-2% to +10%. Its 161 deaths, each genome checked: 160 the reach limit,
1 the converter's alignment refusal.

**The sample** (`results/sample-amd-ryzen-7-pro-8840hs.md`): 108 of 128
alive, median 1.242, 10 faster than s6; the run's best beats all of
them. Regenerating its draws here first gave 2 of 125 matching ids: my
harness drew before `setup()`, which sets the fold pool - the evolver's
own path calls it first, and with it 125 of 125 matched. Of 20 deaths,
19 the reach limit; **one a generator fault**: a design with cached top of
stack, format-10 words and no specialisations whose engine did not
compile.

**Two generator faults, fixed.** (1) `tools/gen-tos.py` replaces a handler
it has a cached body for (HOT) whole, keeping only trailing '#' lines;
where a comment followed them, the "#endif" closing SPEC and the "#if ENC
== 3 && OPS10" were lost, so the format-10 handlers were compiled only
with SPEC. Now it keeps trailing comments and blank lines too, checks that
every preprocessor line outside the replaced bodies survives in order (it
fired at once on its first, too-strict version: the HOT bodies' own ENC
conditionals go with them, rightly), and the file refuses any ENC but 3.
(2) Fixing (1) uncovered `tools/gen-msc.py` comparing the state tables
with every handler's address unconditionally: multi-state caching without
specialisations could not compile - and, with (1) alone, nor without
format-10 words, which until then compiled only because of (1)'s fault.
Now each variant and comparison is emitted under its handler's own
condition, computed from the source's #if nesting. All eight combinations
of multi-state caching, specialisations and format-10 words live.

**What the fixes change.** Seed 2's five front designs: machine code
identical under the old and the new generators - the runs stand. Hand-made
s5 and s6: different code, same size and behaviour (the format-10 handlers
no longer compiled as dead code inside SPEC); s6 new against old, paired
on the VM: 0.997. Tests: 616 cases on every 64-bit system; --validate all
seven IDENTICAL.

**Open.** GOALS.md, "Next". Pick up first: the s6 check on the Ryzen;
then the first candidates from SEARCH-SPACE.md.

## Iteration 6 - 2026-10-04 - Claude

**The s6 check on the Ryzen, first try: inconclusive.** New s6 against
old: fib 1.011, parse 0.996, corpus 1.047 - but the calibration (old
against itself, fib only) was 1.030, and the run was not pinned. Two
flaws of `tools/compare-commits.py`, fixed: (1) it pinned only with
BENCH_CPU - it now picks the quietest core with its sibling, as the
evolver does; (2) one calibration, on the first workload, judged every
row - corpus, the shortest (8 ms), was judged by fib's noise. Each round
now runs old, new and old again in rotating order, so every row carries
its own old against itself; a change counts as beyond noise only if
larger than both that and 2% - one pair is a single draw of the noise,
not its width, and 2% is the project's stated run-to-run noise. A first
version with a 1% floor flagged fib +0.5% on the VM: the floor came from
the data, not taste - on the VM corpus read 0.996, 1.010 and 1.011 in
three sessions.

**Open.** The same check again on the Ryzen with the new tool (GOALS.md,
"Next" 1).

## Iteration 7 - 2026-10-04 - Claude

**The s6 check on the Ryzen, second try** (pinned to cpu 2, 20 rounds,
each row calibrated): fib 0.977 (calibration 0.995), parse 0.997 (1.012),
corpus 0.994 (1.000). corpus's 1.047 of the first try was the unpinned
noise; fib's 0.977 is at the 2% floor and the first try had it at 1.011,
the other way. No correction factor: later runs compare with seeds 1 and
2 to within the ~2% noise. Noted, unexplained: fib's absolute time was
21.5 ms in the first try and 34.4 ms in the second, parse and corpus the
same both times - paired ratios do not see such a shift, and they have
reproduced across sessions.

**PGO, measured before building** (prompts/10). Upper bound first - s6
trained on the four measured workloads: 0.903 on them, 0.877 on held-out
loop. A first look said no profile had been written: my glob missed the
nested directory GCC 13 writes it in; the profile was there and used. A
control - -fprofile-use with no profile - gave 0.974: most of the gain is
the profile's. Then honestly, trained on `lab/evolve/pgo-train.fth` (new:
none of the measured text; checksum 52163 on the cell engine and s6):
0.980 on the four, the same as the flags alone, fib 1.012. PGO is not a
gene. Ablating the flags with four layout-only builds as the control:
loop's gains are layout (moving code alone gives it 10%); fib's 6-7% from
-fpeel-loops, -fipa-cp-clone and -ftracer is beyond the layout band.
Added as genes `peel`, `ipaclone`, `tracer`; on the VM they help s6 2-4%
and seed 2's fastest design not at all (+ tracer 2.9% slower) - selection
on the Ryzen decides.

**Ids kept.** Three new compiler genes would have changed every design's
id (express() includes every compiler gene). Genes added after recorded
runs (`LATE`) are now left out of the identity when off and default to
off in old genomes: 1,308 of 1,308 ids in seed 2's database and 1,306 of
1,306 in the VM rehearsal's recompute identically. The sampler's file is
named after a fingerprint of the gene pool - a new gene changes its draws.

**Open.** GOALS.md, "Next": triples, two escape levels, one-byte calls
through a table of hot words.

## Iteration 8 - 2026-10-04 - Claude

**Triples, priced before building** (prompts/10) with a new tool,
`lab/evolve/price.py`: it profiles a design's own dispatched stream and
prices fusions. On seed 2's front: the best 8-16 triples would remove
0-4.9% of dispatches, none on fib - not built. The same profile showed
what pairs never touch: fib, all calls, returns, a test and a branch; and
tests followed by a conditional branch at 6.6-9.1% of dispatches on every
workload. Three hot opcodes had no names at first - the specialisation
band is laid out positionally from 0x60; `0=` there is the largest single
test (about 4% on kernel, parse, corpus).

**Built: `0= IF` as one branch** - `?NBRANCH`/`?NBRANCH8`, format-10
opcodes; the converter's testbranch pass; handlers in all three engine
forms. Two false starts: (1) the size did not move - s6 has two free
slots, the short form got none, every fused branch stayed long and as
large as before; (2) timed as two designs, the fused one was 5% slower,
fib 12% - a workload that never runs `0= IF`: the engines differed, and
that was layout. Measured again on ONE engine binary, the image converted
with and without the fusion (`SOD16_NO_TESTBR=1`): kernel 0.969, parse
0.972, corpus 0.966, fib 1.003, loop 0.997 - what the price said. Lives
under multi-state caching, tail calls, no caching, without tiny words,
and in seed 2's fastest design. Hand-made engines byte-identical;
--validate all seven IDENTICAL.

**Open.** GOALS.md "Next": `< IF` in run-time code (fib), via the image's
compiler; the other tests; then a Ryzen run.

## Iteration 9 - 2026-10-04 - Claude

**Tests fused at run time.** IF8 compiles ?BRANCH with OP,, not COMPILE,,
so the overlay's pair fusion never saw it; the overlay now has `?BRANCH,`
and its own IF8 and UNTIL8, fusing the test before them from SUPER-TABLE
entries the converter writes first. `rtfuse` builds the overlay for such
a design even without pairs; express() keeps rtfuse then - every recorded
id unchanged (1,308 of 1,308).

**< and then = and U<**, table-driven in the converter (`TESTBR`); the
handlers generated from one template for the plain, cached and
multi-state engines. Measured on one engine per design, image with and
without: all four in kernel code 0.960 (kernel 0.948, parse 0.945, corpus
0.945, held-out loop 0.949); with the run-time overlay 0.935 (fib 0.903)
for about 620 bytes. Hand-made engines byte-identical; --validate seven
IDENTICAL; tests PASS. A founder fusing tests at run time added.

**Open.** A third run on the Ryzen (GOALS.md "Next" 1).

## Iteration 10 - 2026-10-04 - Claude

**The third run froze the owner's laptop**: many `engine` processes; only
killing them all from a console brought it back. A broken design reaching
the FORK primitive in a loop: every child forks again. sh()'s own
docstring recorded the hazard ("once took the machine down"), but the
only limits were CPU time and a process-group kill on timeout - both too
late for a fork bomb.

**Fixed: every engine is jailed.** No workload forks (corpus, benches,
extend.4, cross.4, pgo-train.fth - checked), so: RLIMIT_NPROC 0 - no new
processes - plus 1 GB address space, 64 MB files, 64 open files, no core
dumps. In the evolver's own runs via preexec (any command not a known
build tool counts as an engine: a new tool fails loudly rather than
escaping); in timed runs by cputime itself, in its child after the one
fork it needs (CPUTIME_JAIL). RLIMIT_NPROC does not bind root: the
evolver refuses root (EVOLVE_ALLOW_ROOT=1 to override, where a bomb
cannot hurt). compare-commits.py jails its engines too.

**Proved by `lab/evolve/test-jail.py`**, safe even if the jail fails: one
jailed FORK must be refused (-1) - else it stops; one unjailed must
succeed (two processes) - so the refusal is real; only then a fork bomb,
jailed, directly and under cputime: at most one engine, stopped by its
CPU limit, nothing left. Its first version passed vacuously - the bomb
used AGAIN, which the kernel lacks, and "ran" an error message; a bomb
that exits now fails the test. Under the jail: --validate seven
IDENTICAL, tests PASS, front-style designs evaluate.

**The cause, found.** Seed 3's first generation replayed here as an
unprivileged user, fully jailed: 62 designs, 5 deaths - all the known
reach limit, none unexplained, so no sign of a fault in the new fused
branches. With a shim that logs and refuses fork() (`lab/evolve/
forklog.c`), the five dead and s6 run through their gate workloads:
8cfd49f24c tried to fork 8,181 times, every other 0 - a design at scale 0
with near calls executing what lies past its reach, looping through
FORK. Seeds 1 and 2 had such designs too (20 timeouts each) and were
lucky; sh()'s docstring records one earlier time it was not.

**A second layer: not run.** Two-byte-only forms at scale 0 died 345
times of 345 (seed 2, the VM rehearsal; at scale 1, 13 of 18 lived). They
are now recorded dead without running ("died: reach limit at scale 0 -
not run"): no hand-made stage and none of 2,296 living designs is
flagged; 8cfd49f24c is declined in no time. Ids unchanged; selection the
same - dead either way.

## Iteration 11 - 2026-10-04 - Claude

**Seed 3 on the Ryzen** (resumed after the freeze, engines jailed):
1,310 designs, 1,174 alive; re-measured 0.595 at 13,464 bytes and 0.622
at 9,785 - past seeds 1 and 2 by 2-4% and 4-7%
(`results/evolve-amd-ryzen-7-pro-8840hs-seed3.md`). Every front design
has all eight fused-test opcodes; pairs fell to 13 for them; the run-time
overlay was not chosen. Deaths audited: 129 declined unrun; 7 in
generation 1 before the freeze - 6 the scale-0 reach limit (one the fork
bomb itself), 1 the alignment refusal; none after the resume.

**Priced: more slots.** On the fastest design the next 16 pairs would
remove 6.4-12.9% of dispatches on three workloads. Ranking its kept
primitives by use: the rarest are rare partly because they are folded -
escaping them would break their folds - but ten in no fold or pair come to
0.36% of its dispatches together.

**A second escape level, built and measured.** The nine rarest kept
primitives in no fold or pair are the compacted band's tail (27-35):
escaped too, nothing else moves - `escape=2`, 41 behind ESC, nine slots
more; every engine form lives, level-1 designs keep identical machine
code. It does not pay: the fastest design's own best pairs in the new
slots cut dispatches by 0.2-2.4% (counted), not the 6.4-12.9% price.py
said - its pair and triple columns count overlapping pairs; the tool now
says so. Timed, both front designs lost 5-6% on the VM, in fib and loop,
which use neither - layout. Kept as a gene; recorded as not paying.

**Open.** GOALS.md "Next": `=` with an immediate before a branch.

## Iteration 12 - 2026-10-04 - Claude

**The rest of the tests before a branch**: -, <> (one pair), >, 0<, and
EQI n then ?BRANCH - fused in place as a head and a tail, so nothing about
positions or targets changes. Eight format-10 opcodes; each pair compiled
only where a design has it, so seed 3's front keeps identical machine
code (checked). Every engine form lives with all 29 format-10 opcodes.
Measured on one engine, image with and without: 48 sites, 48 bytes; 1.1-
2.3% fewer dispatches on kernel, parse, corpus (counted); time 1.001 -
about 1% expected, inside the noise. A first count was nonsense (+1117%):
the profiler appends, and my script reused one file name.

**Open.** GOALS.md "Next": one-byte calls, priced first; then a fourth run.

## Iteration 13 - 2026-10-04 - Claude

**One-byte calls, priced** (`lab/evolve/callsites.py`): the converter
writes every call site (CALLMAP, tools/layout.py) and lays an image out
again with chosen targets as one-byte calls (`--hotcalls-file`, image
only). On seed 3's front, 412-661 sites to 122-155 targets; the top 32,
the table charged to the image at 2 bytes an entry: 136 bytes net on
8dd8a7a146 (1.0%: bodies padded to 8 swallow single bytes), 221-320 on
the three 9.6 KB designs (2.3-3.3%). No dispatch removed. Taking the
pairs' slots loses - the fewest-site pairs are among the hottest (four
carry 3-8% of the dispatches); the top of the far-call prefixes costs no
slot. Not built yet: GOALS.md "Next" 1.

**Found on the way: four format-10 words were never there.** The exact-
body check (tools/sod16.py, ops10_at, tiny_at) compared bodies already
rewritten by the pairs, short branches (Phase 3d) and fused tests
(Iterations 8-12). The converter printed "no exact body match"; nothing
read it. 1,032 of seed 3's 1,145 living CV8 designs lost a word - every
front design `(LOOP)`, `(+LOOP)`, `(?DO)`, `?DUP`; 610 `(DO)` to their pairs
(`lab/evolve/scan-bodycheck.py --old`). Fixed: every rewrite off while
checking; 0 of 1,145; build() now kills a design the check fails;
`SOD16_OLD_BODYCHECK=1` keeps the fault, to measure it. Hand-made stages
byte-identical. The front, one engine each (`lab/evolve/image-ab.py`):
99-112 bytes smaller, through the gate, the selection workloads'
dispatches unchanged. Correction to Phases 3c-3d: those words were
measured alone, where the check held; with short branches they were
never in any design.

**Two measurement faults.** (1) The profiler counts an escaped primitive
twice, and with the 256-entry dispatch every call twice: price.py's seed
3 table overstated 60753a0eb0's dispatches by 8% and doubled its calls
(14.8% of kernel, really 8.0%) - corrected forward in
`results/price-seed3-front.md`, both tools fixed. (2) The held-out loop
moves with the image's size mod 8: before `(LOOP)` in code compiled at run
time the compiler pads with NOOPs, run on every pass - 60753a0eb0, 99
bytes smaller, made 1,200,000 more NOOP dispatches on loop (+14%).

**Slips of my own, caught by the tool's checks**: the call-map hook,
inserted between `if V8:` and its `else:`, re-emitted every body as
tokens (the layout's drift assertion stopped it); a one-byte call at
0xE0 was taken for a three-byte one by its first byte (the decode check
stopped it). Times on this VM scattered by 9%: only sizes and counts are
used.

**Open.** GOALS.md "Next": one-byte calls as a size gene, then the fourth
run; the loop words at run time, priced first.

## Iteration 14 - 2026-10-04 - Claude

**One-byte calls, built** as the gene `hotcalls` (0, 8, 16, 32): the
converter gives 0xE0-0xFF to the targets with the most call sites in the
design's own code (`--hotcalls N`, tools/layout.py), the table ends the
image's header, the engine reaches `L_hcall` by the 256-entry table or one
compare in do_call (engine/vm-lab.c, gen-tos.py, gen-msc.py; gen-tail.py
needed nothing). In LATE: every id unchanged. Every engine form passes the
gate with it; without it, nine designs over every form compile to machine
code and images identical to Iteration 13's (a worktree at 3382588,
objdump). Achieved beside predicted, 32 targets: 143/212/319/303 bytes on
seed 3's front against 136/221/320/304 priced; s6 255. On one engine:
dispatches unchanged (parse -0.2%), time inside this VM's noise - measured
by the same tool on two identical images: 0.976-1.005 on the selection
mean. A size gene, for the fourth run.

**Open.** GOALS.md "Next": the fourth run on the Ryzen; then the far-call
reach check (unmeasured, unchecked: 2 MB at scale 0 with the gene).

## Iteration 15 - 2026-10-04 - Claude

**The next run in one command** (`lab/evolve/next-run.sh`, asked for by the
owner): pull the newest bundle from ~/Downloads into the existing clone
(fast-forward only, refusing changed tracked files), then run the pulled
copy of itself; archive the previous run's outputs outside the
repository (moved, never deleted - seed 3's database is the record of that
run, and the evolver would reuse its stale records: the body-check fix
changed 1,032 designs' images under unchanged ids); rebuild; tests,
`--validate`, the jail test; the run and `--remeasure 6` in the background;
the pack to send back. A state file makes a second call with the same seed
and commit resume rather than start over; a lock and a check for a running
evolve.py keep two runs from measuring each other. Tested here on a
simulated laptop: a clone at Iteration 14 with a fake previous run, the
script from "Downloads", a small run, then the same command again.

## Iteration 16 - 2026-10-04 - Claude

**next-run.sh would have deleted the earlier seeds' databases.** Its
fresh start kept four named files (db.jsonl, report.md, remeasure.json,
sample-*.jsonl) and then removed build/ - where the owner's laptop also
keeps db-seed1.jsonl, db-seed2.jsonl, db-rehearsal.jsonl, their reports
and re-measures, knockout.md, five bench-laptop archives and
build/results/. Found from the owner's `find .`, before any run. It now
keeps by kind: every untracked file at the top (but RESULTS.md, the
sweep's working copy), every file in build/evolve/, build/bench-laptop/
and build/results/ - moved, with a MANIFEST.txt - and removes only the
rest. The test that passed at Iteration 15 had one database in build/;
the new one replays the laptop's tree, upgrading from Iteration 15's
script.

**Tidying.** RUNNING.md's knockout and sample commands wrote reports at the
top (the knockout's already went to build/evolve/ too); now under
build/evolve/. .gitignore covers the old names and lscpu's output.

## Iteration 17 - 2026-10-04 - Claude

**next-run.sh as a tool of the repository** (asked for by the owner; it had
been committed since Iteration 15, but handed over as a separate download
too, and it took its clone from a fixed path): it now works on the clone
it is in - a copy outside one keeps the owner's path, or REPO= - and is run
from the clone, `sh lab/evolve/next-run.sh 4`; only bundles are downloaded.
Running it from inside the clone means the pull rewrites the script while
it runs: git replaces the file rather than writing into it, so the shell
reads on from the old one and then executes the pulled copy - tested,
from the top of a clone and from elsewhere, with the clone away from the
fixed path.

## Iteration 18 - 2026-10-04 - Claude

**next-run.sh stopped on the laptop's own measurements**: three tracked
files under results/ were changed - tools/bench-laptop.sh writes its stage
tables and SPN figures straight into results/<cpu>-runN.md and
results/spn-<cpu>.md, so every benchmark run there leaves them changed (the
committed ones are from 2026-09-30 02:33 UTC). They are measurements, not
edits: the script now keeps such changes as a git stash, says which, and
puts the patch in the pack (results-measured-here.patch); a change to any
other tracked file still stops it. Open: the benchmark suite writing
tracked files at all - a commit here and a run there then always differ.

## Iteration 19 - 2026-10-04 - Claude

**The prompt library, from this session's failures** (asked for by the
owner). No new prompt - USAGE.md: keep the count low, and every lesson
had a home. Extended: 03 - step 8, a switch is not a feature (the body
check: 1,032 of 1,145 designs silently without opcodes), the converse of
step 5 (an identity asserted found the profiler's double counts), the
A/A case in step 2 (identical images gave this VM's noise floor), and
triggers for credited options and wrong-way moves (loop +14%, all
alignment NOOPs); 07 - tools write where nothing is tracked (Iteration
18's stop), and a script that pulls its own repository runs the copy it
pulled; 08 - what is already there (Iteration 16's near loss of seeds 1
and 2) and where it is (Iteration 17's fixed path), and its trigger; 10 -
exact prices where the build can produce them, and what a change
displaces. INDEX, USAGE and README rows follow; UPSTREAM no longer says
"unchanged" and lists what to carry back to relf.

Which prompts fired, and which should have: 01, 03, 09, 10 and 12 fired
when they should. 08 did not fire for next-run.sh - its trigger was
calling a suite green, not handing over a script - and that is the
miss that nearly cost the earlier databases; its trigger now names it.
11 applied to the pack the script sends back and was not consulted; it
asks for nothing the pack lacks.

## Iteration 20 - 2026-10-04 - Claude

**Seed 4 recorded** (`results/evolve-amd-ryzen-7-pro-8840hs-seed4.md`), run by
next-run.sh on the laptop: 1,310 designs, 1,188 alive, 37 minutes; the
archive step kept seeds 1-3, the rehearsal and the bench archives
(MANIFEST on the laptop). Re-measured: 0.589 at 13,352 bytes; the small end
0.669 at 9,523 to 0.727 at 9,335. One-byte calls on six of the seven front
designs; the second escape level on the fastest, holding 17 pairs.

**The calibration was poor**: s6 against itself 1.038, fib 1.117 (seed 3,
looked up: 0.986, kernel 0.926 - not noticed then). The re-measure took
up to 24% off the selected figures. So seed 4's small end - 7.5% slower
than seed 3's best small design - is open: both fronts in one session
(GOALS.md "Next" 1). Deaths audited: 121 declined, 1 timeout - the scale-1
near-DOES> reach limit, verified by rebuilding it here (lives with
doesfar=1 alone). The laptop's later benchmark sweep (02:48Z, sent back by
next-run.sh's stash) agrees with the recorded one within error bars: not
re-recorded.

## Iteration 20 - 2026-10-04 - Claude

**Seed 4 recorded** - the entry above, committed as Iteration 20 (part).
**Every run's front in one session**: lab/evolve/compare-fronts.py and
`next-run.sh compare`, which archives and removes nothing. Its replica test
- the laptop's clone at Iteration 18, seed 4's database here, seed 3's in
the archive - failed at once: the Iteration 18 copy checks its argument
before it pulls, so it refused `compare` and never fetched the copy that
knows it - the hazard prompts/07 item 8 names, one turn after writing it.
Arguments are now checked after the pull; this once, the owner pulls by
hand. Then the same replica: no archive made, seed 4's database
byte-identical, the table and the pack made.

## Iteration 21 - 2026-10-04 - Claude

**All runs' fronts measured in one session** (`next-run.sh compare` on the
laptop, 34 designs, 10 rounds, s6 against itself 0.991):
`results/compare-fronts-amd-ryzen-7-pro-8840hs.md`. The front of all runs
together is seed 4's, all seven: at equal size (13,352) 1.5% faster than
seed 3's best, at the small end 1.1% faster and 123 bytes smaller. The 7.5%
Iteration 20 left open was the sessions' calibrations. Between sessions one
design moves by up to 7% with the means unmoved (1.000, 0.999): designs are
ranked within one session only. fib was again the noisiest in the
calibration (0.946): GOALS.md "Next" 1.

A slip of mine, caught before it was written: matching the databases by
the tail of their path labelled seed 3's archived `.../build/evolve/db.jsonl`
as this clone's (seed 4); compare-fronts.py now labels a run by its archive
or "this clone".

## Iteration 22 - 2026-10-04 - Claude

**Seed 4 again**, unplanned: next-run.sh with no argument meant seed 4, and
after Iteration 21's pull (a new commit) it began a fresh one - archiving
the first seed 4 run, as designed. The measured code was identical, so it
is a replicate: same seed, other noise
(`results/evolve-amd-ryzen-7-pro-8840hs-seed4b.md`). The runs share their 35
starting designs and 2 more of 1,310; they reach the same kind of front
(one-byte calls on every design, the same smallest size, 9,335). Its
calibration was good (s6 1.004, fib 1.020) and its re-measure gap small
(0-7%): fib's noise comes and goes between sessions. One timeout, the
scale-1 reach limit again (here it gave wrong output instead).

**What to run is now the bundle's to say**: `lab/evolve/NEXT-RUN` - "seed N",
"compare" or "none" - read by next-run.sh when given no argument, after the
pull. The owner runs the same command every time; a default seed in the
script made "pull and run" mean a run nobody had decided on. My last
message said the plain command "works from here on" - true, and read as
"run it". This bundle's NEXT-RUN: compare.

## Iteration 23 - 2026-10-04 - Claude

**The second one-session comparison overturned the first.** Calibration
0.996 (the first 0.991), yet seed 3's 8dd8a7a146 fastest of all, where
Iteration 21 had put seed 4's whole front ahead: that conclusion is
withdrawn (results/compare-fronts-amd-ryzen-7-pro-8840hs.md, GOALS.md).
The same 34 designs moved between sessions 2-8% on kernel, parse and
corpus and 0.71-1.28 on fib - each design its own way, while s6's fib
calibration held (0.946, 0.981). A good s6 calibration does not make two
sessions agree on a design. I said in Iteration 21 that a design moves "up
to 7%" between sessions - from one pair of sessions; fib alone moves 28%.

Address randomisation tested on the VM: spread 2-6% with it on or off, the
best-of-15 ratios unmoved - not the cause there. The sessions were pinned
to cpu 8 and cpu 2; `lab/evolve/cpu-noise.py` times the designs that moved
most on two cores and both threads of each, in one session, and
`next-run.sh experiment TOOL` runs any tracked lab/evolve tool on the
laptop the way `compare` runs compare-fronts.py (now one of them).
NEXT-RUN: experiment cpu-noise.py --rounds 20.

## Iteration 24 - 2026-10-04 - Claude

**Not the CPU** (`results/cpu-noise-amd-ryzen-7-pro-8840hs.md`): on four
CPUs of one session, kernel's ratios agree within 2.4%, fib's differ 7-20%
- between the two threads of one core as much as between cores - each
design with its own best CPU. Both spread wide run to run (median 11% and
8.5% above the best), but only kernel's best run is reproducible: the
suspect is the estimator. The evolver ranks by the best of N; if fib's runs
depend on where each lands in memory (randomised every run), the best of N
is the luckiest draw. `lab/evolve/run-spread.py` keeps every run, on two
cores, randomisation on and off, and compares the best and the median by
whether two halves of one session agree. evolve.py's jail sees past
`setarch ARCH -R` as it sees past taskset - else cputime, which must fork
once, would have been jailed as an engine (found reading, not running).
Correction: cpu 8's sibling is 9, not 0. NEXT-RUN: experiment
run-spread.py --runs 40.

## Iteration 25 - 2026-10-05 - Claude

**The estimator, settled** (`results/run-spread-amd-ryzen-7-pro-8840hs.md`):
with every run kept, two halves of one session disagree by up to 52% on fib
by the best run and by at most 3.6% by the median; across CPUs the median
agrees within 2.1%. The cause: about one fib run in 40 lands 34-38% fast
(8dd8a7a146: 14.9 ms against a median of 23.9), with address randomisation
on, never with it off, never for s6 - and the best of N reports it when
drawn. Iterations 21-24's disagreements were this.

**Changed**: `measure()` takes the median of the rounds, and so do
compare-fronts.py and image-ab.py; new records' unit says so. Every speed
recorded before - seeds 1-4, the replicate - is a best of N. compare-fronts
--cpus A,B times every design on both CPUs in one session and reports
whether the rankings agree. NEXT-RUN: experiment compare-fronts.py
--rounds 10 --cpus 2,8. Open: what the lucky runs share - a 35% faster fib.

## Iteration 26 - 2026-10-05 - Claude

**The fronts by the median, on two CPUs in one session**: the CPUs agree per
design within 1.7% (10-90%), rank agreement 0.98 - the estimator works.
Seven of the eight designs on the front of all runs are seed 4's (five
from the replicate); at the fast end the replicate's e99da68667 is 3%
faster than seed 3's best and 151 bytes smaller, 4% faster than the first
seed 4 run's best; at the small end speeds tie, seed 4 smaller by 163-311
bytes. Iteration 23's "seed 3 fastest of all" was 8dd8a7a146's lucky fib
run. results/compare-fronts-amd-ryzen-7-pro-8840hs.md.

**Next, the lucky run itself**: lab/evolve/lucky.py - randomisation off,
the environment padded through a page of stack offsets (the environment's
size moves the initial stack and nothing else), every offset twice, and
randomisation on for the rate of lucky runs. NEXT-RUN: experiment lucky.py.

## Iteration 27 - 2026-10-05 - Claude

**The lucky run is not a place** (`results/lucky-amd-ryzen-7-pro-8840hs.md`):
256 stack offsets, randomisation off, swept twice - no offset fast in both
sweeps for any design; and fast runs come with randomisation off at the
same rate as on (0.4-2.3% of runs for some designs, s6 almost never). My
Iteration 25 claim, "never with randomisation off", was 0 of 40 runs - what
a 1-2% rate gives half the time; corrected in evolve.py, RUNNING.md, the
run-spread results (forward) and lucky.py. Left: something transient in a
run, particular to some designs - not cheap to test, not for an engine to
choose. Lead closed; the median stands. NEXT-RUN: seed 5, the first run
selected by the median.

## Iteration 28 - 2026-10-05 - Claude

**Seed 5, the first run selected by the median**
(`results/evolve-amd-ryzen-7-pro-8840hs-seed5.md`): re-measure within 4% of
selection; every front design has 32 one-byte calls and the second escape
level; provisionally (across sessions) 5% faster than anything before at
13,073 bytes and a new fastest at 14,017. Deaths audited here, each rebuilt:
three scale-1 reach limits; one converter assertion (scale 3, folding off)
that Iteration 12's converter fails the same - old, rare, fails safe.

**The owner asked for fewer laptop runs: counted here what counting can
settle.** `lab/evolve/loopwords.py` (`results/price-runtime-loops.md`): the
loop opcodes in code compiled at run time would save 0.1% of kernel's
dispatches and 0.8-1% of corpus's, none of fib's or parse's - priced, not
built (the held-out loop's 68-70% is not a reason: it is held out). The
workloads run code up to 68 KB against a far reach of 2-4 MB - measured, no
check built. Both off GOALS.md's list into its register. NEXT-RUN: none.

## Iteration 29 - 2026-10-05 - Claude

The owner: postpone the article, finish the other items first.

**Indirect threading, priced - not built.** An `itc` variant in the dispatch
lab (answers identical on every program): on the VM it lands in token and
direct threading's band, which this one CPU cannot separate (one variant's
repeats differ 10-40%). Its code is a cell a reference - beside s0-cell's
25 KB, which has never been near a front. Dominated. run.py now keeps the
median, as the evolver does.

**The register machine, priced** (`lab/evolve/stackops.py`,
`results/price-register-machine.md`): on seed 5's front designs 38-50% of
dispatches only move values or push a lone literal - an upper bound (calls
and returns keep their moves), and the largest prize left; the largest work
too. GOALS.md plans it in stages.

**SPN on ARM**: gcc-arm-linux-gnueabihf and qemu-user install in this
sandbox - the port can be built and checked here; the Tegra only times it.

**SPN on ARM, begun.** gcc-arm-linux-gnueabihf, libc6-dev-armhf-cross and
qemu-user install here. `tools/arm-qemu-check.sh`: the cell engine
cross-compiled for ARMv7 (ARM mode, static) runs the 32-bit kernel under
qemu - PASS. spn.c compiles for ARM without a warning (it has the 32-bit
cell path); spn-stencils.c does not assemble - its holes are `movabs`, and
its state struct and marker constants are 64-bit. The port's parts are in
GOALS.md "Next" 3.

## Iteration 30 - 2026-10-05 - Claude

**SPN's proof of concept runs on 32-bit ARM** (qemu): fib and sumto,
translated by spn.4 into ARM machine code, give the interpreter's answers.
What it took:
- `engine/spn-abi.h`, shared by stencils, markers and engine: a cell is a
  pointer's size; the state (sp, tos) is a two-word struct on x86-64 and
  one 64-bit value on ARM - r0:r1 in and out, where a struct would come
  back through memory.
- The stencils' holes on ARM: explicit movw/movt pairs of 32-bit markers,
  one value each (the compiler kept every pair adjacent); every uint64_t
  that meant "a cell, unsigned" now ucell, every 8 and 16 a cell size.
- spn.4's ARCH section chooses by cell size: `b`/`bl` decoded and re-encoded
  by their 24-bit word offset, holes found as a movw then movt to one
  register, bodies ending at the last branch to NEXT or JUMP (or `bx lr`),
  the dropped tail 4 bytes, the scan every 4th byte; literals that do not
  fit 32 bits built from 16-bit pieces so a 32-bit system can read the file.
- spn.c flushes the instruction cache before entering native code, on ARM
  only - qemu would never show it missing.
Checked: x86-64's spn engine and s8's engine are machine-code identical
to before (both built from both sources); the tests PASS, the stages
IDENTICAL; `tools/arm-qemu-check.sh` PASSes - and FAILs when the ARM tail
length is broken on purpose ("Illegal instruction").

Two slips of mine on the way: `IF ... THEN` at the top level to choose two
constants - this kernel compiles IF even when interpreting, and the
dictionary broke (arithmetic chooses now); and a comparison of s8's machine
code that printed IDENTICAL for two binaries that had never been built -
`sh` refused the substitution and two empty disassemblies agreed. Redone
in bash, both binaries checked to exist. FINDINGS-SPN.md corrected: the
port needs no `-mslow-flash-data`, which exists for M-profile cores only.

## Iteration 31 - 2026-10-05 - Claude

**s8 - the current SPN - runs on 32-bit ARM** (qemu): s8-full, s8-spncv8
(recipes replayed at boot) and s8-lazy, made from the 32-bit s6 image,
each pass the ANS corpus - the good one to its end with no error, the
deliberately wrong one caught; 259 words native.

- **gcc-multilib on this VM, for the first time**: the 4-byte-cell ladder
  builds here (26 s) and the tests run with no SKIP. It conflicts with
  gcc-arm-linux-gnueabihf on Ubuntu; with the cross-compiler kept, the
  one file the 4-byte build missed is /usr/include/asm (linked by hand).
- spn-cv8.c: the shared ABI header; uintptr_t for the code base Forth
  reads; the fault report's registers per architecture; service 7 - ARM
  only - makes new code visible to instruction fetch, which spn-cv8.4
  asks for after each word's code is whole (lazy translation included).
- spn-cv8.4: the ARCH section as spn.4's; its hole scan and patcher for
  movw/movt pairs (kinds 3-7); TABLE zeroed a cell at a time (it zeroed
  bytes/8 cells - half the table on ARM); the stencil hash 32-bit FNV on
  ARM; CV8's LIT32 sign-extended by SL@.
- **The crash, found by its own report**: the fault handler gave a native
  offset; a throwaway instrumented copy mapped offsets to words
  (SEARCH-WORDLIST8); the word's native code, dumped and disassembled,
  showed CELLS translated as `3 LSHIFT` - E-TINY expanded CELL+, CELLS
  and ALIGNED with 8-byte constants. Isolated tests (>R and R@, the
  interpreter call-back) passed first, which pointed away from the
  stencils.
- spn-cv8-save.4 wrote the magic's cell width as 8: a 32-bit image the
  engine refused.
- Checked: the build script's x86-64 s8 binary is machine-code identical
  to Iteration 29's sources (both built, 4,885 lines, .rodata and .data
  too); tests PASS with no SKIP, stages IDENTICAL; the ARM check FAILs
  with the 64-bit CELLS expansion put back.

Three slips of mine: the s8 build could not find the new header (the
generated engine compiles in build/ - my own compile command had added
the path; the build's run showed it); a printf in the check script
written through three layers of quoting passed Forth `S\"` instead of
`S"`; and a bash-only `${PIPESTATUS}` in sh aborted the command that was to
restore the deliberately broken spn-cv8.4 - caught by checking the file
before anything else, restored, compared byte for byte with the saved
copy.

## Iteration 32 - 2026-10-05 - Claude

**The register machine's first stage, priced exactly**
(`lab/evolve/regprice.py`, `results/price-register-stage1.md`): from the
converter's operation map (CALLMAP) and the profiler's per-address counts
- both already there, never joined - every executed block is walked: runs
of data-stack moves absorbed into the operation after them, or collapsed
at a block's end; lone literals made immediates. On seed 5's front 19-24%
of the image's dispatches (s6: 26%); return-stack moves, left alone, 13-16%
more - which reconciles with Iteration 29's bound.

**And where it is**: 5-8 of 42-53 patterns give 80% - `DUP ?BRANCH` and
`SWAP addi` lead on every workload. Both end in an operation with an
operand, which the pairs never fuse - so the next step is a gene of
operand-carrying fused opcodes, at the fused tests' cost, rather than a
register machine.

The first count was wrong twice before it was right: fib showed 70,297
dispatches - FIB is compiled at run time, outside the image's map, so each
row now says what share of everything executed it covers; and the
evolved designs' kinds (SP pairs, fused test-and-branches, EQIH) ended
blocks, as did ?BRANCH and the immediates themselves - 4-9% became 19-24%
once they were read. Also: the per-address profile's comment names a
patterns.py that this repository never had; and `find .` from the
repository root timed out on the build tree - git ls-files instead.

## Iteration 33 - 2026-10-05 - Claude

**The first opcodes from the stage-1 price**: `DUP ?BRANCH` and `OVER
?BRANCH`, tests that keep their value - converter (TESTBR), engine (under
X_DUPBR / X_OVERBR), the cached-top and multi-state generators, and the
gene. Designs without them unchanged: stages IDENTICAL; 8dc0f97f2c's
image the same from the old converter and the new (the swap of sod16.py
in a try/finally, checked restored).

image-ab.py on 8dc0f97f2c with the four opcodes in its slots (its last four
pairs displaced, on both sides): 1.8-3.2% fewer dispatches, 8 bytes,
selection 0.980 - all the two can reach. The price had said 6% for "DUP |
?BRANCH": it had folded every test-and-branch into that name. Kept apart,
most of it is `DUP 0= ?BRANCH` (3.4-4.3%); regprice.py keeps the kinds
apart now. image-ab.py's --set takes a JSON list.

## Iteration 34 - 2026-10-05 - Claude

**DUP 0= ?BRANCH kept, and SWAP n +** - the two largest patterns left in
the first-stage price - as opcodes and a gene, through the same five
places as Iteration 33's; DUP 0= ?BRANCH as a four-cell branch kind
(keepbranch, after testbranch has fused the 0= ?BRANCH). Designs without
them unchanged: stages IDENTICAL; 8dc0f97f2c as recorded and with
Iteration 33's four, identical images from the old converter and the new.

image-ab.py on 8dc0f97f2c: all seven new opcodes about 10% fewer
dispatches on kernel, parse and corpus (the price said 10-12%), 40 bytes,
selection 0.951 on the VM; this iteration's two alone 7-8%. Net of the
seven pairs whose slots they take - dispatches counted on profiling
engines, the design as recorded against it with the seven - 6-7% fewer.
Next for them: a seed run, so evolution weighs them design by design.

A slip: the A/B commands nested a JSON list inside two layers of sh -c
and failed on its parentheses; written to a script file with a quoted
heredoc instead. And Iteration 33's commit first said "(part)", which
make-bundle refuses - reworded before any bundle was made.

## Iteration 35 - 2026-10-05 - Claude

**next-run.sh chains "A then B"**: B starts when A has finished and packed,
as if typed by hand - split in the foreground, carried to the detached run
in NEXT_RUN_THEN, started at the end with the lock released and the mode
decided anew. NEXT-RUN: `seed 6 then experiment compare-fronts.py --rounds
10 --cpus 2,8` - one sitting, two packs.

Tested end to end on the VM before handing it over: two cheap comparisons
chained (one round, a two-design database standing in for an archive),
through the real path - the pull from a bundle of this commit, the split,
the detach, each part's build, tests, stages, jail, tool and pack. The
first said DONE, `then:` started the second, which detached on its own -
no lock conflict - and made its own pack; nothing left running. Its
one-round calibration on this VM was 0.910, and the tool said so: this
session cannot rank.

A slip: NEXT-RUN was first edited by a replace that did not check it had
matched - the file's command line comes before its comments, not after -
and still said none; caught by reading the line back, then edited with an
assertion and rewritten in reading order.

## Iteration 36 - 2026-10-05 - Claude

**Seed 6, and every front in one session** - both packs back from one
sitting (Iteration 35's chain). The comparison: 64 front designs from
eight databases, calibration 0.996, cpu 2 and cpu 8 agreeing (median
1.001, ranks 0.99), six and a half minutes - not the 40 I had guessed.

**The front of all runs is seed 6's**, every design of it: 0.547 at 14,081
bytes (the fastest yet) to 0.685 at 9,327 (the smallest yet); 4-7% faster
than the fastest earlier design no larger at most sizes. **And the new
opcodes are why**: three designs of generation 0 had any; at the end
58-80% of the living, and every design on the front; on three of those,
declined against kept on one engine, they remove 9-10% of the dispatches
on kernel, parse and corpus (counted). fib and loop do not move - their
hot code is compiled at run time - and fib is now the weakest workload:
the next item.

Seed 5's provisional claims (Iteration 28, across sessions) settled: its
"new fastest" measures 0.585, dominated by seed 4b's 0.582 at 13,201; its
13,073-byte design 0.610, not 0.593.

NEXT-RUN: none.

## Iteration 37 - 2026-10-05 - Claude

**n + and SWAP n + in code compiled at run time - the gene `rtimm`.**
fib's FIB, dumped from a seed-6 front design's own image: `-1 +` and
`SWAP -2 +` were LIT32 n, + and SWAP, LIT32 n, + - the run-time compiler
had no ADDI and no SWAP+I. forth/cv8-fuse-imm.4 gives it both (LITERAL8
leaves LAST-OP on a small literal; a + straight after takes its place).
FIB: 32 bytes to 23, 13 dispatches a recursive call to 10. On the four
front designs with run-time fusion, image against image: fib 15% fewer
dispatches, 17-27% faster, selection 5-8% faster.

**Why a gene**: built first into cv8-fuse.4, it made every run-time-fusion
design 480 bytes bigger - cd943ed219, the fastest, 14,081 to 14,561, no
longer its recorded size (measured with the old overlay set up in its own
process: the evolver dumps the overlay once, at setup). As rtimm, in LATE,
the recorded designs build byte for byte and keep their ids (all 1,309 of
seed 6's); dormant without run-time fusion and spec imm.

Slips on the way, each caught by a check before anything was measured:
NIP and 0<> are not in this kernel - the overlay stopped loading at the
first, silently, until build/k64-b-fuse.txt was read (and the design
lived, its run-time fusion simply gone: 14,505 bytes and `< ?BRANCH`
unfused were the tell); `['] +` compiled the cell system's address, which
the converter does not relocate - every colon definition crashed, so the
converter now writes the + and SWAP opcodes into the overlay's table;
and a Forth test with DO ... LOOP outside a definition crashed the engine
(the same lesson as Iteration 30's IF).

## Iteration 38 - 2026-10-05 - Claude

The owner: postpone the laptop run, go on.

**The compiler's X8 copies, dropped - the gene `dropx8`.** rtimm's size
(Iteration 37) came partly from a converter habit: each X8 word's body is
copied into X, and the X8 word stays - "harmlessly", said the comment.
Priced first: 25-27 copies, 7.7-8.1% of seed 6's front images, and only
two of them called (CREATE8, NAME>8, from copied bodies). `--drop-x8`
sends every call to a swapped X8 to its X (the same code), resolves a
(POSTPONE) of one to its X, and leaves the X8 words out of `order`, so
threads, links and offsets are laid out without them.

On all ten of seed 6's front designs, image against image on one engine:
769-1,120 bytes smaller (6-10%), 0.2-3.6% fewer dispatches on kernel,
parse and corpus (shorter threads), fib unchanged - free. Both checked
designs alive, and the compiler words compiled at run time give the
recorded designs' answers. As a gene in LATE so recorded designs build as
recorded (all of seed 6's ids unchanged); evolution should take it
everywhere. seed 6's smallest would be 8,558 bytes, its fastest 12,961.

## Iteration 39 - 2026-10-05 - Claude

**The gene `lean`** - Iteration 38's dropx8, renamed (no recorded design
used it) and extended: an image is a dump of what the build loaded, and
three kinds of words came along that the running system never uses - the
compiler's X8 copies (38), **the dump tool itself** (tools/dict-dump-addr.4
is loaded last, to write the dump: 12 words, 490-688 bytes of seed 6's
front), and dead shadowed words (cv8.4's FOLD-OP under cv8-fuse.4's).
Each leaves only where nothing refers to it - checked in the converter.
Priced first with SYMMAP and CALLMAP: "never called" is not "unused" -
`;`, LOOP, EVALUATE are run by name - so the rest stays.

All ten of seed 6's front designs, image against image: 12-16% smaller
(1,267-1,896 bytes), kernel, parse and corpus 1-5% fewer dispatches, no
slower; alive, run-time compiled control structures, VARIABLE, CONSTANT,
CREATE DOES> as recorded. rtimm is a third cheaper with it (278 and 336
bytes, from 408 and 472). Smallest would be 8,060 bytes (seed 6: 9,327).

**NEXT-RUN: seed 7 then compare** - the owner asked to be told when a run
is wanted: rtimm and lean are for evolution to weigh.

## Iteration 40 - 2026-10-05 - Claude

**Seed 7 and session 5** - both packs from one sitting. The comparison:
nine databases, 76 front designs, calibration 1.008, the two CPUs agreeing
(median 1.000, ranks 0.99). **Seven of the eight designs on the front of
all runs are seed 7's: 0.673 at 8,073 bytes - the smallest yet (seed 6:
9,327) - to 0.550 at 11,777**; seed 6's cd943ed219, 0.541 at 14,081, is
still the fastest.

`lean` spread from nothing - no design of generation 0 - to 77% of the
living and every front design: free, as measured. `rtimm` was weighed and
mostly left: expressed on one front design (8,957 bytes); three more carry
it dormant. Beyond lean's bytes, seed 7 is 2.5-7% faster than seed 6's
front with lean applied, through the middle.

NEXT-RUN: none.

## Iteration 41 - 2026-10-05 - Claude

The owner: speed up loops, and put the loop test in the selection.

**The gene `rtloop`** (`forth/cv8-fuse-loop.4`, `results/rtloop.md`): the
compiler the image carries emits the design's loop opcodes, each where it
has one - DO LOOP +LOOP ?DO LEAVE with 16-bit operands, no alignment
NOOPs (which ran on every pass), and I J UNLOOP through a table the
converter writes. loop 57-80% fewer dispatches, 2-4x faster; about 6% of
the image. **loop selected, sieve held out** (`bench/sieve.fth`, the BYTE
sieve) so the generalisation check stays.

Four slips, each caught before anything was measured:
- my first patch script stopped at its first edit (a block Iteration 39
  had changed), and the build and tests after it ran on unchanged code -
  "PASS" that meant nothing; git status showed one new file and no edits;
- an all-or-nothing gene (all five loop opcodes) would have applied to
  39 of seed 7's 1,207 living designs and none of its front - evolution,
  with loop held out, had dropped what it did not need; each word on its
  own instead;
- lean's aliasing first made a deferring X8 call itself; narrowed to the
  last X8 of each name, it changed seed 7's 4cc12fc1e7 by 8 bytes - WHILE8
  had reached the fusing IF through the alias - so the rule became: every
  reference to any X8 goes to X, except a deferral to an earlier one of
  the same name; seed 7's front byte for byte again;
- that exception covered calls but not (POSTPONE): POSTPONE of an
  immediate word compiles (POSTPONE) and an xt, so ?DO8's deferral still
  recursed - a return-stack overflow on the first ?DO, found by testing
  each loop word alone on a design whose ?DO and LEAVE take the old path.

A miniature seed run (6 designs, one generation) ran the evolver end to
end on the new lists: six workloads timed, the report saying so.
NEXT-RUN: seed 8, then compare.

## Iteration 42 - 2026-10-05 - Claude

**Seed 8 and session 6** - the first run with loop selected. The comparison:
ten databases, 98 front designs, five workloads, calibration 1.003, the two
CPUs agreeing (ranks 0.99). **14 of the 17 designs on the front of all runs
are seed 8's: 0.449 at 13,073 bytes (fastest yet), 0.454 at 9,278, down to
8,034 (smallest yet)**; 15-27% faster than the fastest earlier design no
larger from 8.5 KB up. rtloop on every front design from 8,525 bytes and
55% of the living (none in generation 0); the loop opcodes taken back (I
in 83%); loop five times faster than s6. **The held-out sieve improved
with it** - 0.51-0.66 against seed 7's 0.78-0.85.

A slip in the tool, not the data: compare-fronts.py's column header was a
fixed list of the old five workloads while its rows came from the new
lists, so the last data column - sieve - sat under "loop", and a parser
reading by name found no front at all. Read by position; the header is
built from the lists now.

NEXT-RUN: none.

## Iteration 43 - 2026-10-05 - Claude

**rtloop's bytes, priced word by word, and `rtloopall`.** Seed 8's front
jumped 0.661 to 0.550 between 8,171 and 8,525 bytes - rtloop's overlay,
about 470 bytes: the words it defers to kept alive (~150-190), three
padded tables (~127), the machinery that serves any subset of the loop
opcodes (~170). Seven of the ten rtloop designs on the front have all
eight, so `forth/cv8-fuse-loopall.4` - no fallbacks, one chain, one
12-byte table - for them, as the LATE gene rtloopall: 380-488 bytes less
on five of them, dispatches within half a percent on every workload,
alive, the loop tests answering as before. Recorded designs untouched:
stages IDENTICAL, seed 8's front byte for byte, its ids kept.

## Iteration 44 - 2026-10-05 - Claude

**An audit of a small image, and the gene `bss`.** seed 8's 85cac726b5 with
rtloopall, 8,234 bytes: a third names and links, 353 bytes of image
header, and the largest "words" buffers - INCLUDE-BUFFER 548, POCKET 285,
TIB 284 - VARIABLEs with an ALLOT, written before they are ever read.
`--bss` moves them past the image's end: each becomes a word pushing
START plus an offset (a LITOFF patched after layout), v8pfa and
remap_pfa_off send references there, DP starts after them; the engine's
memory there is a zeroed static array. NAMEBUF stays (FIND reads it per
candidate; as a call it would cost).

On four of seed 8's front designs, image against image: 1,056-1,064 bytes
(11-13%), kernel, fib, parse, corpus and sieve dispatches unchanged; loop
moves only on the two without rtloop - the (LOOP) padding artefact, DP
starting elsewhere. Recorded designs untouched (seed 8's front byte for
byte, every id kept); alive, and S", loops and the prompt answer as before.
seed 8's smallest would be 6,970 bytes.

NEXT-RUN: seed 9, then compare - rtloopall and bss for evolution to take.

## Iteration 45 - 2026-10-05 - Claude

**Seed 9 and session 7.** The comparison: eleven databases, 109 front
designs, calibration 1.000, the CPUs' ranks agreeing 1.00. **Seed 9 has
the small end - 0.794 at 7,019 bytes, the smallest yet, to 0.515 at 7,725
- with bss on every front design** (none in generation 0, 79% of the
living); seed 8 keeps 8,614 bytes and up, the fastest 0.442. Seed 9's own
fastest were 0.493-0.502: it did not find seed 8's fast end.

**What does not compound**: seed 8's seven front designs built with bss and
rtloopall - all alive on the VM - are 1,426-1,504 bytes smaller at their
measured speeds: 0.508 at 7,178 ... 0.442 at 11,569, dominating every
seed-9 front design from 7,178 bytes up. Each run starts from the same
founders; the next step proposed is to seed runs with the earlier fronts.

NEXT-RUN: none.

## Iteration 46 - 2026-10-05 - Claude

**The fronts carried into every run** (the owner's go). `evolve.py --carry
DB,DB,...`: each database's own front - chosen by its own records, which
were measured in other sessions and some over four workloads - joins the
first generation beside the founders, and every one is timed again like
any design of the run; sorted, so a resumed run makes the same first
generation, and no random draw is spent. next-run.sh passes every
archived database to a seed run. compare-fronts.py leaves a carried design
to the run that found it, so it is neither counted twice nor as new.

A miniature run on the VM carrying seeds 8 and 9: 33 designs carried in,
all alive, each recorded as "carried from archived-seedN/db.jsonl: <id>",
the run going on from there.

NEXT-RUN: seed 10, then compare.

## Iteration 47 - 2026-10-05 - Claude

**Seed 10 and session 8 - progress compounds.** The first run carrying the
earlier fronts: 109 designs in, seven minutes more. The comparison (twelve
databases, 131 designs, calibration 1.004, ranks 1.00): **15 of the 16
designs on the front of all runs are seed 10's own - 6,977 bytes the
smallest yet, 0.486 at 7,236, 0.438 at 12,145** - and every one descends
from carried designs. 5-26% faster than the fastest earlier design no
larger at every size, 25-26% at 7.1-7.2 KB; past Iteration 45's
projection (0.508 at 7,178). Seed 8's 0.436 at 13,073 still the fastest.
bss on all fifteen, rtloopall on eleven.

NEXT-RUN: none.

## Iteration 48 - 2026-10-05 - Claude

The owner: the article on the backburner; the Tegra session after all the
improvements we have so far; and to capture that the Forth sources may
hold simplifications and optimisations. GOALS.md's list now says so, in
that order: improvements on the VM - (a) the Forth sources, (b) the
image's remaining fixed costs, (c) the register machine's tail - with
carry-over seed runs between batches; then the Tegra session, its two
prerequisites named; the article last. The items built from the old list
moved under "Built from this list".

## Iteration 49 - 2026-10-05 - Claude

The owner: pushing to GitHub is theirs, continuously - off the list. On to
the Forth sources.

**Where the dispatches go**, word by word (profile per address, symbol
map), on seed 10's 96f2d8bfd7: a quarter of kernel, parse and corpus was
FILL, almost all of it NAME>BUF zero-filling NAMEBUF's 32 bytes a byte at
a time before every dictionary lookup; the dictionary walk a third of
parse more. **The gene `kfast`** (`forth/cv8b-kfast.4`, byte headers):
NAME>BUF8 = 32 MIN NAMEBUF PLACE - the byte compare never reads the
padding. 24-29% fewer dispatches on kernel, parse and corpus; alive;
recorded designs untouched.

The cell-header version did not make it: the converter refused `?DO`
("UNTRANSLATED code bodies"); rewritten with BEGIN WHILE REPEAT it hung the
converted image at the first lookup; and my tests in the plain cell system
were unsound twice - reading NAMEBUF at the prompt, after the interpreter's
own lookups had overwritten it, and compiling S" inside a definition, which
that kernel cannot. Left open, not shipped: 14 of seed 10's 15 front
designs have byte headers. Also caught before running: the dump loop
chose its overlay by a comprehension variable that does not leak.

## Iteration 50 - 2026-10-05 - Claude

**FILL and CMOVE as opcodes** - the kernel's byte loops, 12-14 dispatches
a byte: format-10 opcodes in OPS10_POOL, engine handlers a byte at a time
ascending (CMOVE's overlap as the loop's), the converter's expected bodies
written from its own reading (SOD16_SHOW=FILL,CMOVE). With the opcode,
the colon word's body becomes the opcode and EXIT, so code compiled at run
time - the sieve's FILL - gets it too; only these two, which never read
their caller's return address, and no recorded design has them.

On 96f2d8bfd7 with kfast, two pairs displaced: kernel 0.865, parse 0.944,
corpus 0.917, the held-out sieve 0.848 (still 1899 primes), 32 bytes less;
alive; recorded designs as recorded. With kfast, kernel is about 0.65 of
its dispatches of before, parse 0.69, corpus 0.66.

A stale link of mine - build/work/cv8-kfast.4, left dangling when the
cell-header attempt's file went - made the evolver's private work dir
fail; removed (a laptop run deletes build/ first).

## Iteration 51 - 2026-10-05 - Claude

**The thread walk as an opcode.** Attributed again after Iteration 50, the
dictionary search was most of what was left (about 63% of parse). kfast's
overlay factors the walk out of SEARCH-WORDLIST8 unchanged - THREAD-FIND
( nfa namebuf --- nfa' | 0 ) - and THREAD-FIND is a format-10 opcode: the
count, the bytes, NEXT-NFA8's three link forms in C; the converter checks
its body (from SOD16_SHOW); dormant without kfast. kfast had been in no
run, so its overlay could still change.

On 96f2d8bfd7: parse 0.489, corpus 0.631, kernel 0.799 more; alive in all
four engine forms; no bytes. From the design as recorded: parse 0.34,
corpus 0.42, kernel 0.53 of the dispatches, the selected workloads'
geometric mean about 0.60. NEXT-RUN: seed 11, then compare - the batch
timed on the laptop.

## Iteration 52 - 2026-10-05 - Claude

**Seed 11 and session 9 - the Forth sources' batch, timed.** 131 designs
carried in; the comparison (thirteen databases, 144 designs, calibration
1.007, ranks 1.00): **all 11 designs on the front of all runs are seed
11's - the fastest yet, 0.413 at 8,030 bytes (seed 8's 0.436 took
13,073), the smallest yet, 6,971, and 0.433 at 7,238** - 9-30% faster
than the fastest earlier design no larger at every size. kfast on 7 of
the 11 (46% of the living, none in generation 0), CMOVE on 10.

**But THREAD-FIND was never taken up** - the largest saving (parse 0.489
counted): 7 of 1,425 designs drew it from the pool of thirty format-10
names, 6 without kfast; the one where it worked was lost. On seed 11's two
best, first in the list: kernel 0.82, parse 0.49-0.51, corpus 0.63-0.65,
alive. **The gene `tfind`** (LATE, with kfast): THREAD-FIND first, sure of
a slot - a switch where the pool was a needle. Every recorded id kept; the
one pool-drawn design rebuilds as recorded.

A slip of mine, caught before the bundle went out: the record-keeping
script quoted GOALS.md with the wrong line breaks, its check stopped it
part way, and the shell committed anyway - without GOALS.md, NEXT-RUN
(still seed 11: a laptop would have run it again) or this entry. Amended;
the commit now waits on the script.

NEXT-RUN: seed 12, then compare.

## Iteration 53 - 2026-10-05 - Claude

**Seed 12 and session 10 - THREAD-FIND taken up.** 144 designs carried in;
the comparison (fourteen databases, 157 designs, calibration 0.994, ranks
1.00): **all 12 designs on the front of all runs are seed 12's - the
fastest yet, 0.326 at 9,014 bytes (seed 11's: 0.413 at 8,030), 0.331 at
7,958, 0.379 at 7,105, and the smallest yet, 6,941** - 17-32% faster than
the fastest earlier design no larger at every size.

THREAD-FIND expressed on 11 of the 12 (8 by tfind, 3 by the pool from
ancestors that had it), tfind first in generation 7, 37% of the living
with THREAD-FIND at the end against seed 11's 0%; parse at 0.21-0.28 of
s6's time, against 0.40-0.58. The record edits checked the files' text
first this time, and the commit waited on them.

NEXT-RUN: none.

## Iteration 54 - 2026-10-05 - Claude

The owner asked how much faster than the hand-made CV8 we are: the fastest
design 3.07x s6-cv8b on the selected workloads, head to head in session
10, 10% smaller; about 2.4x s5-cv8spec and 3.0x s4-cv8 bridged through
the stage ladder's laptop table. Then: proceed with the action items.

**The input side - the gene `kinput`.** Attributed again on seed 12's
fastest: REFILL, SCAN, PARSE, SKIP, WORD 27-36% of kernel, parse and
corpus; FILL 7.5% of kernel, in the pool and never taken up. kinput (with
kfast): forth/cv8b-kinput.4 - REFILL's tab loop factored out as TABS>BL,
REFILL8 calling it - and SCAN, SKIP, TABS>BL, FILL first among the
format-10 names, their colon bodies the opcode too. On dcbaf0e29f and
35135bde2f: kernel 0.72, parse 0.84, corpus 0.79, sieve 0.84; 31-40 bytes
less; alive in all four engine forms.

The evolver refused to run on a build older than the engine's sources -
its own check, as it should; rebuilt.

## Iteration 55 - 2026-10-05 - Claude

**kinput completed.** Attributed again with kinput on: lookup overhead
(FIND, SEARCH-WORDLIST, HASH, PLACE) 22-35% of kernel, parse and corpus;
PARSE's own stack work 9-14%; ?STACK after every word, with DEPTH and an
(ABORT") call each time, 8-10% of parse and corpus. kinput's overlay - in
no run yet - grew (PARSE) ( addr u c --- a1 len adv ) with PARSE8 around
it, and ?STACK8 (one unsigned compare, (ABORT") only on an error); kinput
puts (PARSE), HASH and PLACE first with its other four. HASH's handler is
the kernel's hash exactly.

dcbaf0e29f / 35135bde2f against them as recorded: kernel 0.62/0.63, parse
0.65/0.66, corpus 0.61/0.63, sieve 0.84/0.85, fib and loop 1.00 - the
selected geometric mean about 0.75; 63 bytes less; alive in all four
engine forms; recorded designs and ids untouched.

NEXT-RUN: seed 13, then compare.

## Iteration 56 - 2026-10-06 - Claude

**Seed 13 and session 11 - the input side taken up.** 157 designs carried
in; the comparison (fifteen databases, 173 designs, calibration 0.994,
ranks 1.00): **all 10 designs on the front of all runs are seed 13's -
the fastest yet, 0.284 at 7,799 bytes (3.5x s6; seed 12's best: 0.326 at
9,014), 0.297 at 7,246, and the smallest yet, 6,903 at 0.436** - 17-34%
faster than the fastest earlier design no larger at every size. kinput on
all ten, first in generation 1, 66% of the living. Nothing larger than
7,799 bytes is on the front any more.

NEXT-RUN: none.

## Iteration 57 - 2026-10-06 - Claude

**klookup - the whole lookup and the numbers.** Attributed on seed 13's
fastest: FIND and SEARCH-WORDLIST 28-31% of parse and corpus around the
opcodes; NUMBER?, >NUMBER, DIGIT? 12-21%. forth/cv8b-klookup.4: (FIND),
the kernel's FIND step for step with NAMEBUF, CONTEXT and #ORDER @ given,
and FIND8; (>NUMBER), the kernel's >NUMBER with BASE @ given, its Forth
body the kernel's loop (calling >NUMBER would recurse); WORD8 with one
HERE. The LATE gene klookup (with kinput) puts (FIND) and (>NUMBER) first.

The kernel has no search-order words and no workload changes the order,
so the handler's other paths were tested differentially - the kernel's
Forth against the opcode, identical outputs on two designs: one-entry and
three-entry orders, an empty wordlist first and last, long names; and
NUMBER? over signs, prefixes, points, overflow past 2^128, invalid input,
bases 2, 16, 36. Alive in all four engine forms. Counted on seed 13's
best: parse 0.53-0.57, corpus 0.60-0.65, kernel 0.80-0.81; selected
geomean 0.76-0.79; 40-44 bytes more.

Two slips of mine, both in test harnesses: a grep waiting on stdin when
its file list came back empty (the command timed out), and setting up one
build's private work dir twice. NEXT-RUN: seed 14, then compare.

## Iteration 58 - 2026-10-06 - Claude

The owner started seed 14. Meanwhile, the image's fixed costs: the
header's 353 bytes are 264 of thread count and heads, which only SOD16
reads - the CV8 loader reads them and returns before the word table they
serve. **The gene `thinhdr`** (LATE): --thin-header writes a count of 1
and a zero head. 248 bytes off every CV8 design (6,903 -> 6,655, 3.6%),
dispatches identical, alive; recorded designs and ids untouched.

NEXT-RUN unchanged - seed 14 is running; this commit goes out with its
analysis.

## Iteration 59 - 2026-10-06 - Claude

**The code compiled at run time, named.** fib, loop and the sieve run in
it (98-100%), and so does 39% of kernel. With the opcodes named
(stackops.py's naming): calls dominate - 19.5% of kernel's dispatches,
13.6% of corpus's; call>DOVAR, a variable called, 5.2% / 3.5% and the
sieve's 7.7%; fib's base-case test DUP 2 < IF three dispatches a call; the
loop's body DUP I + XOR (LOOP). And seed 13's fastest has only 6 pair
slots left - the format-10 opcodes the k-genes put first take the rest.

**Variables and constants as literals - built, measured, rejected.**
forth/cv8-fuse-lit.4 and a gene rtlit: an outermost COMPILE,8 link that
executes a variable or a constant at compile time - known by its body,
DOVAR, or one of LIT,'s four forms then EXIT (there is no VALUE or TO) -
and compiles the value through LITERAL. Correct: alive in all four engine
forms, the sieve's 1899. The held-out sieve 0.811 of its dispatches - but
kernel 0.984 and corpus 1.016: checking every word compiled costs a
compiling workload more than the calls saved; 132 bytes more; selected
geomean 1.000. Reverted, in the register. Kept as candidates: I + fused
in loops (a fifth of loop), DUP n < IF fused (fib's test).

## Iteration 60 - 2026-10-06 - Claude

The owner asked how much is left, and agreed to go on; the run (seed 14)
still going, the run-time code next - the plan and a stopping rule in
GOALS.md: the improvements end when two runs in a row each improve the
fastest by under ~5% and the smallest by under ~2%.

**rtiplus - I + fused in code compiled at run time.** The loop workload's
body is DUP I + XOR (LOOP), a fifth of it I then +. The run-time fuser
already fuses a pair SUPER-TABLE lists when LAST-OP points at the first;
rtloopall compiles I and clears LAST-OP. So: a format-10 opcode I+ (tos
+= RS; a pseudo name, no kernel word), the converter's SUPER-TABLE entry
(I, +) -> I+ placed with the tests (never cut), and forth/cv8-fuse-iplus.4
- one COMPILE,8 link pointing LAST-OP at I's byte; a branch target in
between clears LAST-OP as for any pair. The LATE gene rtiplus (with
rtloopall) puts I+ first among the format-10 names.

ad62971982: loop 0.801, the held-out sieve 0.967, kernel, parse and
corpus 1.007-1.012 - the link's one offset compare for every word
compiled; selected geomean 0.962, and 0.958 on top of klookup and thinhdr;
37 bytes; alive in all four engine forms. Caching I's xt in a variable
cut the compile cost to 1.004-1.008 for 37 bytes more - not kept.

## Iteration 61 - 2026-10-06 - Claude

**swapi - SWAP+I sure of a slot.** In the pool since Iteration 34, on none
of seed 13's front; fib's SWAP -2 + took two dispatches. The LATE gene
swapi (with 'imm') puts it first. On ad62971982 with klookup, thinhdr and
rtiplus: fib 0.944, corpus 0.995, kernel 0.998 - selected geomean 0.987 -
16 bytes less; alive with all four new genes; every recorded id kept.

The opcode budget: that design has 3 pair slots left, 2 with SWAP+I. This
is the fifth 'put X first' switch (tfind, kinput, klookup, rtiplus,
swapi) - the pool of format-10 names is too big for mutation to find a
good one by chance, and a general way to let evolution order them is on
the list. (My first try at this entry quoted GOALS.md with the wrong line
breaks; its check stopped the commit, as it should.)

## Iteration 62 - 2026-10-06 - Claude

**Seed 14 and session 12 - the whole lookup taken up.** 173 designs
carried in; the comparison (sixteen databases, 188 designs, calibration
1.000, ranks 1.00): **11 of the 12 designs on the front of all runs are
seed 14's - the fastest yet, 0.240 at 8,320 bytes (4.2x s6; seed 13's
best 0.284 at 7,799), 0.244 at 7,286, 0.245 at 7,172** - 15-20% faster
than anything earlier from 7.0 to 8.3 KB; the small end held at 6,903.
klookup on 8 of the 11, first in generation 2. By the stopping rule:
go on (the fastest 15% better).

**The comparison capped.** It re-timed every run's front - 188 designs,
twenty minutes, a minute more each run - though since carrying began the
front of all runs has come from the newest one or two. next-run.sh now
compares the newest COMPARE_LAST archived databases (default 4; 0: all);
compare-fronts.py leaves a carried design to the run that found it only
if that run is compared, so none goes unmeasured - checked on seed 14's
re-measured front: 15 kept and 2 left to seed 13 with seed 13 present
(as session 12 itself did), all 17 kept without it.

NEXT-RUN: seed 15 - thinhdr, rtiplus, swapi to choose - then compare.

## Iteration 63 - 2026-10-06 - Claude

**Seed 15 and session 13.** The first capped comparison: seed 15 and
seeds 11-14, 72 designs, eight minutes (twenty before), calibration
0.994, ranks 1.00. **13 of the 14 designs on the front of all runs are
seed 15's - the smallest yet, 6,654 bytes (thinhdr's 249), 0.239 at 6,940
where the best that small was 0.375, and the fastest yet, 0.230 at
7,958** (seed 14: 0.240 at 8,320). thinhdr on all 13 (70% of the living);
rtiplus on none - it needs rtloopall, on 3 - and swapi on one: counted
gains that did not pay in time. Stopping rule: go on - the fastest moved
4.2%, under 5%, but the smallest 3.6%, over 2%.

**Cleanup** (the owner: ~/forth-vm-evolution-runs holds a lot):
tools/clean-runs.sh keeps every pack tarball (each run's database, report
and logs), the newest four archives (the comparison and the carry read
them) and the newest run directory, and packs the rest - older archives,
older run directories - into records/NAME.tar.gz, each checked readable
before its directory goes. A dry run unless --yes; it takes the runs'
lock. Tested on a mock runs directory: seven archives, five run
directories, a tarball and a stray file - the right ones packed, the
rest untouched. next-run.sh now carries only the newest CARRY_LAST
archives (4), as the comparison compares - 188 carried designs cost
minutes of seed 15's first generation.

NEXT-RUN: none - the next run waits for the next batch.

## Iteration 64 - 2026-10-06 - Claude

The owner asked the winning design's maximum code space: **2 MB** - calls
name a byte offset from the image base, the three-byte form's 22 bits
less the one the 32 hot calls take; the engine's memory is 16 MB, and the
run-time compiler's CALL, has no reach check, so a call to a word past
2 MB would encode as a hot call to another word. The owner remembered a
different layout - two selector bits, 64 opcodes, a reserved four-byte
call - and asked for consistency with relf (github.com/kt97679/relf).

relf, cloned and read: its reference (docs/CV8.md 2.1) is the format this
repository uses - 128 opcodes, calls of 14 and 22 bits - with MEMSIZE cut
to 4 MB to match the reach (its Iteration 545); its decision A15 brought
the one-byte opcodes in use to 64 (539) but kept the calls ("don't
implement the 1 GB call range yet"); the two-bit tag - 00 an opcode,
calls of 14, 22, 30 bits, 1 GB - is its GOALS item 2 and Z5, priced at
0-0.7% by its Iteration 501.

**Decided with the owner, all in FORMAT-TAG2.md**: that tag; 64 one-byte
codes and ESC + selector; codes by measured rank; no hot calls; variable
length everywhere and full cells avoided - calls 2-4 bytes, links 1-4
read backwards, backward branches 8 or 16 bits, forward branches 16 in
the one-pass run-time compiler and 8 where the converter knows they
reach, CREATE reserving the four-byte DOES> call; the old CV8 kept for
recorded designs, new runs on the new format, the old front the
baseline. Next: T1, the engine.

## Iteration 65 - 2026-10-06 - Claude

**T1: the engine reads the two-bit tag.** Under TAG2, vm-lab.c fills a
256-entry table once: 0x00-0x3F this design's one-byte codes (from
vm-tag2-one.h, which the converter will write), 0x40-0xFF the call
handler of their width - so a dispatch is one byte and one indirect jump,
no opcode-or-call test. The escape goes through a 256-entry table (from
vm-tag2-esc.h). Each code names a LOGICAL operation - the table the engine
builds today, or an escaped primitive - so every handler, fold, pair and
format-10 word is reused unchanged; an unassigned code faults, not
no-ops. Calls of 14, 22 and 30 bits, byte offsets from the image base;
F_TAG2 in the magic (neither engine reads the other's images); #error
with hot calls, a scale, or another encoding.

The two handlers that walk the dictionary - THREAD-FIND's and (FIND)'s -
and their copies in both generators now decode a link through one macro,
PREVNFA: the old form, or the tag's (00 one byte of 6 bits, 0 ends the
thread; 01 two; 10 three; 11 four; read backwards). Unchanged for every
design: tests, the seven stages identical, klookup designs alive in all
four engine forms. TAG2 compiles in the base and cached-top engines. The
multi-state generator finds the dispatch fill by pattern and copies the
call path per cache state - its port is T1b. Next: T2, the converter.

## Iteration 66 - 2026-10-06 - Claude

**T2: the converter writes the two-bit tag.** sod16.py: the tag's state and
encoders - t2put (one byte, or the escape and a selector), t2call (2, 3, 4
bytes) - opcode_L, each operation's logical opcode as to_bytes_v8 decides
it, op_bytes re-costing every opcode by rank, and to_bytes_t2, a separate
emitter, the old one untouched. layout.py --tag2: every operation named
(t2_names) and ranked - NOOP at 0 (padding), the run-time compiler's
constants pinned, then a reference profile's weight (--tag2-rank, still
to make), then static use; 63 one-byte codes, the escape at 0x3F; links of
1-4 bytes with the tag; calls, and DOES> bodies always with the 4-byte
call; no hot calls; F_TAG2; the engine's map written beside the image. The
engine's DOVAR and DODOES at align(ip + 4) under TAG2. The evolver: the
LATE gene tag2 - converter before engine, -DTAG2=1, no hot calls, no
multi-state caching yet.

**Smoke test**: seed 13's fastest as tag 2 - 168 operations, 63 one-byte,
105 escaped - boots and interprets: 1 2 + . -> 3, 7 DUP * . -> 49, ' DUP
' SWAP < . -> -1. 8,018 bytes against 7,799 in the old format, with
static ranking only. Compiling needs T3.

**A regression of mine, caught**: the cached-top generator's DOVAR now
names TAG2, which spn-cv8.c did not define - the SPN engine stopped
compiling, and the test suite did not notice (it does not build it); the
stage build's last line said so. spn-cv8.c defines TAG2 0 - the same
constant as before.

## Iteration 67 - 2026-10-06 - Claude

**T3: the run-time compiler in the two-bit tag.** forth/cv8t.4 and
cv8bt.4 - copies, the originals frozen by the designs recorded with them:
CALL, in the shortest of three widths (aborting past 1 GB), COMPILE,8
knowing the escape by ESC-OP, backward branches one byte where the design
has the short form and it reaches, forward ones 16 bits, DOES> always the
4-byte call with CREATE reserving 4, links of 1-4 bytes with the tag.
cv8t-fuse.4 and cv8t-fuse-imm.4: ESC-OP for the old escape's 125. The
converter rewrites the run-time compiler's opcode constants - [LIT n][EXIT]
bodies - to the design's codes, writes its tables in one-byte codes
(dropping an entry with an escaped operation; run-time folds off - their
opcode was the fold base plus a position), pins LOOPTAB's eight. k64-bt
dumps for every overlay combination; tag2 needs byte headers.

**Seed 13's fastest as tag 2 passes the life test**: every workload, the
corpus and the kernel rebuild compiling at run time in the tag. By hand:
a colon word, BEGIN UNTIL, a VARIABLE, CREATE DOES> - 49, 5, 42, 99.
8,314 bytes against 7,799 in the old format, ranked statically. Next: the
price, design by design, and the reference ranking.

## Iteration 68 - 2026-10-06 - Claude

**The tag's price.** Seed 15's front as tag 2, ranked statically: size
+6.6-8.4%, dispatches +5-42% - operations code compiled at run time uses
are rare in the image, so they were escaped or dropped from the run-time
tables (8298ca5d59's loop 3.98x: rtloop's loop opcodes escaped, so it
called the colon words). Fixed: the loop opcodes pinned with either loop
table; and the reference ranking, lab/evolve/tag2-rank.py - four seed-15
designs profiled in the old format, each operation's share of each
selected workload, named by the converter's own t2_names (a debug hook,
SOD16_T2NAMES) - lab/evolve/tag2-rank-v1.json, 134 names, DUP + EXIT LIT8
DOVAR at the top. With it: fib and loop exactly 1.000, kernel, parse and
corpus +3-5%, selected geomean 1.023-1.030 - but size +9.1-10.6%: ranking
by weight escapes what the image uses often and runs rarely.

--tag2-hot W, the middle way: weighing at least W, hot, by weight; the
rest by static use. 0.02: size +8.0-9.1%, dispatches 1.032-1.049; static:
+7.0-8.4%, 1.053-1.134 - which way a design should go differs, so this is
for evolution to weigh. Where the fastest design's 638 bytes go: hot calls
130, escaped uses 194-357, and ~245 in the tag-2 compiler's own words -
CALL, +92, NEXT-NFA8 +51, LINK, +47, <BRANCH, 40.

## Iteration 69 - 2026-10-06 - Claude

**The tag-2 compiler made small.** CALL, LINK, and NEXT-NFA8 as one loop
each instead of a branch per width; the 1 GB check out of CALL, - an
ABORT" and its string - into vm-lab.c, which refuses at compile time a
MEMSIZE past what a call reaches. Seed 15's smallest and fastest as tag 2
(--tag2-hot 0.02): alive, the hand test 49 5 42 99, **7,041 bytes against
6,654 (+5.8%, was +9.1%) and 8,386 against 7,958 (+5.4%, was +8.0%)**. What
is left is the format's: the hot calls it has no room for (~1.6%), the
escaped uses (2.5-3.5%).

## Iteration 70 - 2026-10-06 - Claude

**T1b and T5: every engine form, and past 4 MB.** gen-tail.py turns the
tag's two computed gotos into tail calls through function tables;
gen-msc.py builds per-state tables for the tag (below 0x40 the variants
as ever, above them the per-state copy of the call handler for that
width), copies the three call handlers per state, and normalises through
the tag's table - the escape dispatches from state 1. Seed 15's fastest
and smallest as tag 2: alive with no cached top, cached top, tail calls,
multi-state caching; the search-order and NUMBER? differential tests
identical to the old format; and past 4 MB - a 5 MB ALLOT, words calling
and called across it, DOES> on both sides of it, a tick walking a link
across it - right in every form. The same program in the old format:
return stack overflow.

## Iteration 71 - 2026-10-06 - Claude

**T4: the evolver within the two-bit tag.** The gene t2hot (LATE, with
the tag): the ranking's hot threshold, 0.02 by default, 0, 0.05 or static
- the trade Iteration 68 found differs by design. --require tag2: every
design entering a run, the hand-made references excepted (s6 stays the
measure of speed), in the tag with byte headers; a carried design that
re-encoding gives a new id is the run's own ('tag 2 of ...'), so the
comparison measures it there. next-run.sh: 'seed N tag2'. A miniature
run carrying seed 15's front: 15 re-encoded and alive, the hand-made
untouched, 11 of 13 mutants alive.

NEXT-RUN: seed 16 tag2, then compare - the old front the baseline. Left
of the format: 32-bit cells (before the Tegra), the analysis tools'
opcode names.

## Iteration 72 - 2026-10-06 - Claude

**Seed 16, the first run in the two-bit tag**, and session 14 (seeds
12-16, calibration 1.001): the front of all runs stays the old format's;
seed 16's front is the old one moved ~370 bytes right at about its speed
- 1.03-1.08 of the best old design no larger from 7.2 KB up. The price,
as counted. t2hot chosen toward size.

**The aim, written down** (the owner: simplicity and minimalism are the
main goal; it was not stated anywhere): at the top of GOALS.md and
README.md - the smallest, simplest system that does the job; mechanisms
earn their place by measurement, behind genes, and come out if they buy
nothing; the simpler of two ways; and complexity counted - the fitness
does not see what a design adds to the ENGINE.

**A JIT as a gene** (the owner asked): possible - SPN proved copy-and-patch
here, on x86-64 and ARM - but SPN is not minimal (a 1,861-line engine copy,
~2,600 lines of Forth). The minimal version and its costs are in GOALS.md;
it waits for the owner's word.

NEXT-RUN: seed 17 tag2, then compare.

## Iteration 73 - 2026-10-06 - Claude

The owner: a lazy JIT, to keep the image small and gain speed - but no
significant growth in code complexity or memory: track them. **Tracked
now**: evaluate() records each design's engine code - its binary's .text
section, read from the ELF section table - and the peak resident memory
of its runs, per workload, from cputime.c's MAXRSS (printed all along,
never read); the run's report and the comparison's table show both.
First readings: seed 15's smallest and fastest in the old format, 37.2
and 39.9 KB of engine code, 1.43-1.44 MB peak; the fastest in the tag 45.5
KB - the tag's cost in the engine, 5.6 KB, mostly the multi-state copies
of its call handlers and tables - at the same peak.

**JIT.md** - the minimal lazy JIT planned: SPN's stencils, markers and
native convention borrowed, not its engine copy or translator; only
words compiled at run time, translated on their first call, all or
nothing per word; budgets - ~300 new lines of C, +15 KB engine code,
+1 MB peak memory, the image unchanged - and it must pay, or it comes
out. Phase 1, a prototype on the VM, next.

## Iteration 74 - 2026-10-06 - Claude

The owner: the budgets are reasonable - try it; a little over is fine,
optimise later or drop it on its numbers. The seed-16 packs sent again
are the same run (the clone had not pulled the bundle setting seed 17);
the comparison, run again on them, agrees with the first - 70 designs,
median 1.006, 10-90% 0.986-1.026, the front the old format's.

**The JIT begun.** engine/jit.c: SPN's rules for reading a stencil
(forth/spn.4) in C - the body from its address past an endbr64 to its
last jump to NEXT or JUMP (EXIT: its first ret); the holes found exactly,
a 32-bit relative field aimed at a marker or a magic constant (8-byte
literal, 4-byte literal, the return stack's address). tools/jit-check.sh
prints how this machine's compiler shaped every stencil: gcc -O2 and -Os
here - every one the prototype needs has the holes its source implies;
?DO's conditional exit does not, so ?DO would stay bytecode. Next: the
converter's per-design table, the translator, JIT? and NATIVE,
executable memory, the run-time compiler's header.

## Iteration 75 - 2026-10-06 - Claude

**Three objectives, equal** (the owner): the smallest binary + image, the
highest speed, the lowest memory - to catch logic moved into the engine.
Every evolved engine and the reference s6 now link without the C library
(engine/rt-linux-x86_64.c, mprotect added; no unwind tables): with it,
1.1 MB of 1.47 MB resident was the library, and its code was invisible
in the binary. binary = a stripped copy; memory = pages touched, from a
new MINFLT in cputime (faults counted one by one) - ru_maxrss failed
twice over: a 388 KB floor from fork's copy of a library-linked cputime
(the peak survives exec), then 0 KB for a static 30 ms run on Linux 6.18
(per-CPU counters, read approximately). cputime now links without the
library too. NSGA-II dominates and crowds over the three; the
comparison counts designs on the front by memory alone.

First readings: s6 39,521 (binary 29,456); seed 15's fastest, multi-state,
65,982 (binary 58,024 - 20 KB of cached-state handler copies); with tail
calls 45,526; 200-216 KB touched. A 2-generation run and a comparison
checked end to end (the comparison's row format fixed on the way); in
that small test one of five front designs was there by memory alone.
NEXT-RUN: seed 18 tag2, then compare. The JIT (phase 1) resumes after.

## Iteration 76 - 2026-10-06 - Claude

**Seed 17** (the tag's second run, the last under the old rules) and
session 15 (seeds 13-17, calibration 0.993): **the first designs in the
tag on the front of all runs** - a36dc45e12 0.233 at 7,283 bytes, 4.5%
faster than the best old design no larger, within 1.3% of the old
fastest at 675 bytes less; 5671742b27 0.233 at 7,690. The tag's front at
its fast end 4.1% faster than seed 16's and 425 bytes smaller; 9 of the
joint tag-2 front's 12. From 7.2 KB up the price is won back; at the
small end not yet. Both front designs: no multi-state caching - ~20 KB
less engine, which the new objectives count - and swapi, taken up for
the first time. NEXT-RUN stays seed 18, the first under three objectives.

## Iteration 77 - 2026-10-06 - Claude

**Seed 18, the first run under three objectives** (session 16, seeds
14-18, calibration 1.004, ranks 1.00). binary + image works: 35 of the
front's 39 are seed 18's, engines down to 25,280 bytes; bbab8560dd 0.258
at 40,786 total against the old fastest 3a96a12236's 0.249 at 65,982.
**Memory selects on noise**: 18 of 39 on the front by memory alone, each a
page or less from a design faster and smaller; with one page of tolerance
none. Told the owner; memory within 8 KB (EVOLVE_MEM_TOL) is now a tie,
speed and binary + image exact - the evolver's front on seed 18's records
56 -> 25, the speed-and-size front. A stopping rule for three objectives
proposed (GOALS.md).

Two converter deaths fixed, both through the tag: json unimported in
layout.py when no ops10/pairs/hot-calls file was given (7); rtloopall_on
checked the genome's list, not the slots the loop opcodes get after
kinput's and klookup's words (8) - ops10_order() split out of ops10_in()
so the check needs no recursion. Replayed: all 15 alive; all 1,246 living
designs keep their ids. NEXT-RUN: seed 19 tag2.

## Iteration 78 - 2026-10-06 - Claude

The owner adopted the stopping rule for three objectives. **Seed 19**
(session 17, seeds 15-19, calibration 1.009, ranks 1.00) is **small, the
first of two**: fastest 0.238 against 0.244 (+2.5%), smallest binary +
image 32,299 against 32,331 (+0.1%), least memory none. The memory tie
works: 0 of the front's 18 by memory alone (19 of 40 before). The
fastest of all runs no longer needs a large engine - cc0b1e2aeb, 0.238 at
42,512 bytes total, binary 33,448 - against seed 18's 0.244 at 74,548. No
converter deaths. NEXT-RUN: seed 20 tag2; if small, the gene set has
converged and the JIT comes before more runs.

## Iteration 79 - 2026-10-06 - Claude

**Seed 20 small too - two in a row: evolution stops** (session 18, seeds
16-20, calibration 1.000, ranks 1.00, 0 by memory alone): fastest 0.264
against 0.243, smallest total 32,299 against 32,299, memory 208 against
204 KB. The converged front: 32 designs, 16 of seed 20, 11 of seed 19, 5
of seed 18. The owner asked whether evolution can run here to spare the
laptop: processes on this VM are killed between Claude's turns (a
background heartbeat stopped at the turn's end; the files persist), so a
run here only advances during a reply - ~45 minutes of one; and the runs'
last generations still make front designs (of 64: 25% by generation 20,
50% by 30), so shorter runs would cost. NEXT-RUN: none - the JIT next.

## Iteration 80 - 2026-10-06 - Claude

**The lazy JIT, phase 1** (JIT.md), built and measured. Colon words
compiled at run time begin [JIT][four bytes] (forth/cv8t-jit.4, an
overlay only for the gene); the first call translates the word
(engine/jit.c): decode as the engine does, callees first, SPN's stencils
copied and patched - all or nothing, calls only to native words or
itself. The converter writes vm-jit-ops.h from the operations' names and
pins JIT to one byte. One bug on the way: inside a handler gen-tos.py has
no rule for, the stack is spilled - dsp at the top.

On seed 19's fastest design: fib 0.605 -> 0.221, loop 0.173 -> 0.070;
kernel, parse, corpus and sieve 8-13% slower (every run-time word's call
pays the JIT dispatch; most stay bytecode, calling kernel words); speed
0.229 -> 0.166. Binary +8,288 bytes, image +136, memory +4 KB - within the
budgets. The corpus, the tests and the hand-made stages pass. The gene
`jit` is in the evolver; NEXT-RUN: seed 21 tag2 - the stopping rule
starts again with a new gene.

## Iteration 81 - 2026-10-06 - Claude

The JIT, two fixes: its opcode is an operation of its own under the tag
(T2_JIT, a pinned one-byte code) instead of the first format-10 slot -
which had pushed a pair out (R> =); and a word that stays bytecode
re-points each call site past its header on the first call. The
overhead on kernel, parse and corpus did not move, and with translation
switched off it remained: CELLS pushed into the escaped band by the
pinned code, the engine's layout, the VM's noise - for the laptop to
weigh. Found: after the tag's call handlers gen-tos.py leaves a handler
unwrapped (no SPILL) - the JIT handler sits among the ordinary ones; and
the binary objective moves in 4 KB steps (page-aligned segments).

## Iteration 82 - 2026-10-06 - Claude

**Seed 21, the JIT's first run** (session 19, calibration 0.995): the gene
taken up in generation 6, active in 206 designs; the four fastest designs
of all runs carry it (6fd52398b1 0.204 at 45,560 bytes). On the laptop,
four designs with and without it: fib 0.17, loop 0.42, kernel/parse/
corpus 0.98, sieve 0.96 - the VM's 10-17% cost on bytecode workloads was
the VM's. Not small (fastest +19.6%, smallest total +13.4%).

**Engines without page padding** (the owner agreed): -Wl,-n, and -z
norelro and no build-id - RELRO's end on a page boundary left ~6 KB of
padding even under -n. The binary objective now counts bytes: s6 22,200
(was 29,456); the JIT's real cost 3.4 KB. The owner asked: a deep dive
into the JIT's slowdown? Not needed - the laptop shows none. Forth
sources reviewed? Yes, Iterations 49-57 (kfast, tfind, kinput,
klookup); number conversion and FIND's search-order loop left. Inlining
short words? Never built - to be priced next. NEXT-RUN: seed 22 tag2.

## Iteration 83 - 2026-10-06 - Claude

**Seed 22** (the first with binaries in bytes; session 20, calibration
1.005): small, the first of two - fastest 0.199 (+4.5%), smallest total
25,181 (+0.5%), memory none. 12 of the front's 39 by memory alone, by 16-20
KB: real pages now, not noise - the tie rule kept.

**The runs directory cleaned before every run** (the owner): tools/clean-
runs.sh rewritten - archives past the newest four, run directories whose
pack tarball exists, tarballs past the newest eight; the old tool missed
every run directory since commits grew to 9 hex digits. next-run.sh runs
it under its lock; a failure never stops a run. On a copy of the owner's
directory: 20 archives -> 4, 43 run directories -> 0, 45 tarballs -> 8.

The owner agreed the next genes, in order: inlining short words and tail
calls (priced first - lab/evolve/callsites.py's census and per-target
call counts are the tool), the rewrite-rule search, image compression,
the JIT's calls into bytecode, a wider flag pool. NEXT-RUN: seed 23 tag2.

## Iteration 84 - 2026-10-06 - Claude

**The runs directory moves into the clone** (the owner: all development
in one place): runs/, ignored by git, the default of next-run.sh and
tools/clean-runs.sh (RUNS still overrides). Once, under the runs lock, the
newest archives and pack tarballs move over from ~/forth-vm-evolution-runs
(a marker, runs/.moved-in, lists them); the rest of the old directory is
left for the owner to delete. Packs to send back are now in runs/.

## Iteration 85 - 2026-10-06 - Claude

Every pack lists the clone (the owner): repo-files.txt - every path but
the insides of .git, build/ and runs/ (summed), and git status --ignored.
The owner asked whether to start a new chat: GOALS.md now says how to
resume in one, with the next steps as agreed.

## Iteration 86 - 2026-10-06 - Claude

**Seed 23 small too - two in a row: evolution stops** (session 21, seeds
19-23, calibration 0.996): fastest none (0.212 against 0.195), smallest
total +0.2%, memory none. The gene set with the JIT has converged; the
front of all runs 35 designs, fastest 2cbcf427f6 0.195 at 42,816 bytes.
The runs directory in the clone worked on the laptop: the one-off move
brought 4 archives and 8 tarballs from ~/forth-vm-evolution-runs; the
clean-up removed the excess. The seed pack still carries the laptop's
stash of results/ from 2026-10-04 (a re-measured stage ladder) - old,
re-sent while the stash exists.

**Captured for a new chat** (the owner moves to one): GOALS.md "Resuming
in a new chat" - where it stands, the agreed next steps, the longer term
(the Tegra's prerequisites: 32-bit cells under the tag, an ARM libc-free
runtime, the JIT's ARM patching; the Forth sources' leftovers; the
article; GitHub the owner's), and how to work on the development VM. The
gene candidates and the reasoning on randomness: lab/evolve/GENES.md.
NEXT-RUN: none.

## Iteration 87 - 2026-10-06 - Claude

**The fronts' genomes in the repository** (the owner: the next chat should
not need a separate upload). The new chat could not rebuild a single front
design: the run reports in results/ name genes only where they differ
from s6-cv8b, pairs cut after four (14 of the 35 designs on the front of
all runs have 5-8), and even where nothing is cut the genome holds state
the report does not show (rtloop counts a loop word in the genome's
unslotted ops10 list) - 0 of 91 rebuilt from the reports matched their
ids. The databases live on the laptop; the owner sent a snapshot of the
clone.

Now `evolve.py --report` ends the report with "The front's genomes": one
JSON line per front design (and per design the front was measured again
with), its database record without the raw timings. The report goes to
results/ as always, so the genomes come with it; a tool that takes `--db`
reads a report as a database, the lines that are not JSON skipped.
Seeds 19-23's reports were filled in from the owner's databases, in the
same format: 158 designs, every id equal to its genome's, all 35 of the
front of all runs. Nothing else in the snapshot was missing from the
repository (its tree is HEAD's; ignored files, build/, runs/ and the old
results stash of 2026-10-04 aside). GOALS.md, "Resuming in a new chat",
says so.

## Iteration 88 - 2026-10-07 - Claude

**lab/evolve/callsites.py ported to the two-bit tag** (GOALS.md, the agreed
next step). What broke: the call map (CALLMAP, tools/layout.py) sized a
call 2 or 3 bytes from the old encoding; the tool decoded the old 10/11
forms with a scale; its audit rebuilt with the pre-Iteration-13 body check,
which today's designs fail; and its hot-call price has no place under the
tag (git history keeps it). Now:
- **the call map** sizes a call by its tag (2, 3 or 4 bytes) and also
  writes each operation's design-independent name, every branch target,
  every word's body and the tag's codes - images unchanged;
- **the profiler** (engine/vm-lab.c, PROFILE builds only - no design's
  engine changes) records every call under the tag by its return address:
  target, count, the byte after the call and the callee's first eight,
  read when the run ends. So calls compiled at run time - the kernel
  workload's cross-compiler, fib, the sieve - are seen too, which no census
  of the image can;
- **the tool** reads the genomes from results/ (Iteration 87) or any
  database, builds the design with the map and the profiler, and prices
  inlining short words and Forth tail calls, image and run-time code apart.
  Audits, each stopping it: the image is its recorded size; every site
  decodes to its target; dispatches by address equal dispatches by pair,
  calls by return address equal calls by pair; every call returning into
  the image is a census site, run as often as the site was dispatched. All
  hold on the 35 designs of the front of all runs (5 minutes on the VM).
  One trap on the way: profiling forces the plain dispatch (tail=0), and in
  e83972af52 that woke a JIT gene the tail-call engine kept dormant (+136
  bytes of image); the build keeps it dormant now.
The tests pass; the seven hand-made stages are identical.

## Iteration 89 - 2026-10-07 - Claude

**Inlining short words and Forth tail calls, priced** (GOALS.md's step 2;
`results/price-inline-tailcalls.md`), with callsites.py on the 35 designs of
the front of all runs. In the image neither pays: inlining finds 0-15 sites
and 0-11 bytes - the converter's tiny words, folds and format-10 words made
the short kernel words opcodes long ago; tail calls find ~50 sites and -4 to
+9 bytes, since a 16-bit BRANCH is as long as a 2-byte call and its EXIT.
Dynamically tail calls save at most 1.8% of a workload's dispatches. The
one lever is code compiled at run time: inlining saves 6.1-7.6% of the
kernel workload's dispatches on the faster designs (1.6-4.5% on the small
ones), and 85% of that is CHARS - `: CHARS ;`, an empty word the cross-
compiler calls for 12.6% of its calls. Constants (a literal and EXIT,
outside the agreed definition): 0 bytes, 0.1-2.2%. Nothing built. Not yet
priced: the JIT refuses every run-time word that calls a kernel word, so
inlining could let more code go native - next.

## Iteration 90 - 2026-10-07 - Claude

**What inlining at run time would do for the JIT: nothing** (the owner:
"continue"; results/price-inline-tailcalls.md, "The JIT"). The profiler now
logs every word the translator met and, for each left bytecode, its calls
and its first operation without stencils (engine/jit.c, profiling builds
only - no design's engine changes); callsites.py frees words by kind of
blocker as a fixpoint. On the five JIT designs of the front of all runs the
JIT leaves 44.5-46.6% of the kernel workload's dispatches in bytecode,
3.8-4.2% of the corpus's, 78.8-80.1% of the held-out sieve's. Inlining
short words alone frees 0.0-0.1%; data words and constants as literals
1.2-1.3% of the kernel's, with inlining 7.5-7.9%; every call translatable -
native code calling bytecode, SPN's st_interp, GENES.md candidate 5 -
9.8-10.2% of the kernel's and 78.8-80.1% of the sieve's, whose one word
PRIMES calls FILL, 1+, 2DROP and the run-time FLAGS and SIZE (no JIT
header: data and a constant). >R without stencils is first in words holding
30.1% of the kernel's dispatches. So candidate 5 is the lever; inlining is
not. Nothing built; the owner decides.

## Iteration 91 - 2026-10-07 - Claude

**A deep dive: what else could make it smaller and faster, ranked**
(lab/evolve/GENES.md, "Ranked (Iteration 91)"; the owner asked for
imagination, then a ranking). Measured for it, with one-off scripts: the
smallest engine's 14.7 KB of code is 8.1 KB interpreter and 6.3 KB other
functions - ~3-4 KB of them the shell's OS calls (getpwnam, setenv,
execvp, malloc, snprintf/vsnprintf ...), which no workload uses; on the
fastest design the workloads run 0.55-7.4 ms and a bare start costs
0.077-0.097 ms (18% of loop) against 0.042 for an empty process; inlining
the 10 hottest call sites, any callee, costs 26 bytes and saves 9.3% of
parse's dispatches and 8.8% of corpus's; a quarter of the fastest image
(1,977 bytes) never runs, led by the Forth bodies of words opcodes
replaced; factoring repeated code saves ~1% of an image at a speed cost.
Ranked first: hot-site inlining, the dead bodies behind opcodes, the OS
layer out, a cheaper start, the JIT's calls into bytecode. Three questions
for the owner: is the shell part of the job, should start count in speed,
may the tag drop its 3-byte call. Nothing built.

## Iteration 92 - 2026-10-07 - Claude

**The deep dive's first two, built behind genes** (results/hotinl-opbody.md;
the owner: "proceed"). `hotinl` (0, 10, 20, 40, designs in the tag): the
converter inlines the first K safe sites of lab/evolve/hotsites-v1.json -
the image's call sites ranked by the fastest design's profile
(lab/evolve/hotsites.py), named by caller, callee and ordinal - spliced in
before every rewrite (tools/sod16.py: read_ops split into raw_read and the
rewrites; hot_inline). `opbody` (0, 1): (FIND), (>NUMBER), THREAD-FIND, +!
and ?DUP get [opcode EXIT], as FILL and CMOVE did. On the fast designs
together about size-neutral (-16 and +16 bytes) for 9-10% fewer dispatches
on parse and corpus and 5% on kernel; on the smallest the list barely
applies (0.5%). Three faults, each caught by the gate: callers and callees
known by their names before the compiler's X8 swap (LITERAL's cell-format
body inlined crashed at the first literal); a body the converter patches
after reading copied (LIT8-OP); data told from code wrongly. With the genes
off all 35 front designs build to their recorded sizes and ids; the tests
pass; the hand-made stages are identical. NEXT-RUN: seed 24 tag2.

## Iteration 93 - 2026-10-07 - Claude

**A run for a night** (the owner: longer runs overnight, more combinations
and generations?). Measured first, on seeds 19-23's databases: the fronts
ended with 20, 27, 38, 46 and 42 designs against a population of 32 - since
three equal objectives the front outgrew the population, so part of it was
cut from breeding every generation; 29-52% of each final front was born in
the last 10 of 40 generations; the best speed and smallest total mostly
settled by generation 20-30 (seed 19's best speed moved at the end, 0.235 ->
0.217). So the population first, then the generations: `night` after the
seed (next-run.sh) runs 96 x 80, about 7,800 designs, ~3 hours at seed 23's
pace, then the re-measure and comparison as always (lab/evolve/RUNNING.md).
And NEXT-RUN gets back its comparison after the run (`then experiment
compare-fronts.py --rounds 10 --cpus 2,8`), which Iteration 92 dropped.
Seed 24 stays at the usual size, as the owner asked.

## Iteration 94 - 2026-10-07 - Claude

**Seed 24** (results/evolve-amd-ryzen-7-pro-8840hs-seed24.md), the first run
with hotinl and opbody, at Iteration 92's commit - so no comparison. 1,407
designs, 1,323 alive, no death but the reach limit's 84. **opbody taken up**
(23 of the front's 37; clean child/parent pairs -105 bytes, neutral in
time). **hotinl hardly tried and on no front design** (33 living): its 8
clean pairs give parse 0.970, as counted on the VM, but the whole design
1.017 - corpus, kernel, loop and the sieve within a pair's noise of +-5%
(loop and the sieve run almost no image code it changes): below what a
3-round median sees. The run's fastest, e22d91cd94, 0.175 re-measured
(seed 23's best 0.195-0.206), carries neither new gene; the smallest total
25,131 is opbody's 8 bytes on seed 23's smallest. Seen on the way: pairs
differing by one image-only gene show corpus ratios up to 1.34 - the corpus
runs ~1.5 ms on the fast designs. The owner: a couple more short runs, a
night run later. NEXT-RUN: seed 25 tag2, then the comparison (seeds 21-25).

## Iteration 95 - 2026-10-07 - Claude

**The gene t2wide: the tag without its 3-byte call** (results/t2wide.md;
the owner asked about calls as continuation bytes for 128 opcodes - priced
first, and the cheaper route agreed). The front's designs have 159-169
operations and 63 one-byte codes; escapes ran as 4.2-8.1% of the dispatches
of kernel, parse and corpus. Under t2wide `10xxxxxx` are 64 more one-byte
codes (127), calls `01` (2 bytes) and `11` (4 bytes, 1 GB); the engine's
table and profiler, the JIT's decoder and jit_repoint, the converter
(--tag2-wide, CALL,'s 3-byte limit patched in its body) and the evolver.
On the fastest, middle and smallest designs - cached top with the JIT,
tail calls, plain - all through the gate; escapes run 0.0%; images -208,
-302, -121 bytes; calls 5 MB out right. With the gene off all 68 designs
of both fronts at their recorded sizes and ids; tests pass; hand-made
stages identical. Not under multi-state caching yet (gen-msc.py). Found: the
smallest engine grew 288 bytes of sections but 4,352 of file - the
page-aligned memory area makes the file move in 4 KB steps when the code's
end crosses a page; a fix for the owner to decide. NEXT-RUN: seed 26 tag2,
then the comparison.

## Iteration 96 - 2026-10-07 - Claude

**Seed 25 and session 22** (results/evolve-amd-ryzen-7-pro-8840hs-seed25.md,
results/compare-fronts-amd-ryzen-7-pro-8840hs.md). Seed 25 at Iteration 94's
commit: 1,426 designs, 1,335 alive, only the reach limit's 91 deaths, 37
minutes. Session 22 measured seeds 21-25 together (calibration 0.998, cpu 2
0.998, cpu 8 1.001): **seed 24 small** (the first since the new genes:
fastest none, smallest total +0.03%, memory none); **seed 25 not small** -
the fastest +6.9%, 14b8775218 0.163 at 39,296 bytes. The front of all runs
34 designs, 18 of seed 25 and 13 of seed 24. opbody on 21 of seed 25's
front; hotinl on 3, at 10 sites - its first. The owner: the 4 KB steps in
the engine's file left for now, more data first; and the night run now:
NEXT-RUN seed 26 tag2 night (96 x 80, ~3.5 hours), the first run that can
choose t2wide, then the comparison.

## Iteration 97 - 2026-10-07 - Claude

**Seed 26, the first night run, and session 23**
(results/evolve-amd-ryzen-7-pro-8840hs-seed26.md). Population 96, 80
generations, at Iteration 96's commit: 7,718 designs, 7,268 alive, only the
reach limit's 450 deaths, 3 h 19 min (1.55 s a design). Session 23 measured
seeds 22-26 (calibration 0.998): **seed 26 not small** - fastest +10.3%
(70bc3ae6b5, 0.165 at 43,224 bytes), smallest total 24,964 (+0.66%),
memory none. **The night run took the front**: 29 of the 30 designs on the
front of all runs against four short runs; 33 of its 35 front designs born
after generation 40, the best speed still moving at 80 (0.163 by 40, 0.153
by 80). **t2wide everywhere**: all 35 of the run's front, 29 of 30 of all
runs; 25 clean pairs -104 bytes, kernel 0.986, parse 0.980, corpus 0.988.
hotinl on 11 of the run's front and on the two fastest of all runs (20
sites); opbody on all 35. Measured too: the same 137 designs 1.8% slower
than in session 22 at the median (10-90% -0.8% to +7.2%; seed 25's fastest
0.163 then, 0.184 now) - why the rule compares within one session.
NEXT-RUN: seed 27 tag2 night (or 96 x 160 for a whole night, RUNNING.md).

## Iteration 98 - 2026-10-07 - Claude

**Seed 27 and session 24** (results/evolve-amd-ryzen-7-pro-8840hs-seed27.md).
Night size (96 x 80) run by day, at Iteration 97's commit: 7,691 designs,
7,267 alive, only the reach limit's 424 deaths, 3 h 39 min. Session 24
measured seeds 23-27 (calibration 1.009): **seed 27 small, the first in a
row** - fastest none (0.185 against seed 26's 0.181), smallest total 24,923
(+0.16%), memory none. From seed 26's front it plateaued early: the best
recorded speed flat from generation 20, the smallest total from 40. The
front of all runs: 40 designs, 24 of seed 27 (the middle and the small
end), 16 of seed 26 (still the two fastest). t2wide on 39 of the 40,
opbody on all, hotinl on 20. The same 136 designs measured 3.0% slower than
in session 23 (10-90% -0.2% to +7.3%). NEXT-RUN: seed 28 tag2 night - if
small too, evolution stops for this gene set.

## Iteration 99 - 2026-10-08 - Claude

**Four cores and a 12-hour run** (the owner: plan the next run for 12 hours;
only one core was busy; four are fine). evolve.py `--jobs N`: N workers,
each pinned with its builds to its own physical core (free_cores),
pairing its timed runs with s6 on that core in its own copy of the
reference's work directory; a generation's children all made before any is
evaluated (get() asks, flush() evaluates in order), so decisions are as
before and a resumed run replays - checked: generation 0 identical with one
worker and two, a rerun on its own database evaluated nothing new. Found on
the way: the worker pool's first name, POOL, overwrote the fold pool of the
same name (line 70) - renamed WORKERS before anything ran with it.
`--until EPOCH`: no generation started after the deadline (checked: five
generations, then the report). `first_front()`: the front over every design
without comparing every pair - identical on seeds 25-27's databases, 0.07 s
against 130 s - for the report, the re-measure and the carry; a 12-hour
run's ~90,000 designs would have taken hours. next-run.sh: JOBS (default 4)
and a size in hours, `12h`: population 256, generations until 50 minutes
before the end. Tests pass, hand-made stages identical.

The owner's compound quality Q = (binary + image) x run time x memory,
discussed: on the front of all runs its best is a middle design
(2766152e23: 0.200 at 34,872 bytes, 200 KB; Q 0.230 of s6's), the fastest
0.27, the smallest 0.56 - speed spans 3.6x on the front, size 1.7x, memory
1.1x, so Q is mostly speed. Suggested: keep the three-objective front for
selection, Q for naming a champion and judging runs; memory in 8 KB steps;
not before the 4 KB binary steps are fixed. Not built - the owner decides.

NEXT-RUN: seed 28 tag2 12h, then the comparison.

## Iterations 100-103 - 2026-10-08 - Claude

The owner's answers to the ranked list: Q for information, never selection;
one SYSCALL primitive (agreed in principle - Linux calls take at most six
register arguments, so one primitive serves all; the shell's speed rests on
fork and exec, not on wrappers); longer workloads; rtempty; the trims; the
JIT's next step priced first; packed names later.

**Iteration 100 - longer workloads.** evolve.py program(): the BENCH line
repeated (fib 2x, loop 10x, the sieve 3x), parse 3x, the corpus 5x - each
pass followed by an empty line, which its ACCEPT test reads (without it,
each pass swallowed the next pass's INCLUDED line: 5 of 10 ran). The kernel
workload stays single: cross.4 included twice in one process does nothing
the second time. Memory keeps its meaning: the corpus's from one run of the
single corpus. On the fastest design (VM) 3.5-17 ms a workload, a start ~1%;
s6 349 ms a round. bench/ untouched; long files made at setup.

**Iteration 101 - the gene rtempty** (forth/cv8t-empty.4): a word whose
body is EXIT alone compiles to nothing. Through the gate on the fastest and
the smallest design; kernel workload dispatches -4.0% and -2.3%; image +32
and +40 bytes.

**Iteration 102 - the CPU's divide for UM/MOD** (engine/vm-lab.c, x86-64):
libgcc's __udivmodti4 (430 bytes) gone from every engine; equal to the C on
2,000,000 cases, overflowing quotients included. The engines' files: the
fastest 35,000 -> 30,704, the smallest 18,032 -> 17,960 - the page padding
again (the owner: later). Tests pass; hand-made stages identical.

**Iteration 103 - the JIT's next step, priced** (results/jit-kernel-
words.md): kernel words translated once each (76 of 296 made of operations
with stencils) free nothing alone, 8.2% of the kernel workload's dispatches
with data words as literals; the sieve waits on FILL's stencil. callsites.py
learned the wide tag (its audit read 0x80-0xBF as calls).

NEXT-RUN: seed 28 tag2 12h (the deadline 80 minutes before the end: the
long workloads' comparison takes ~1 hour).

## Iteration 104 - 2026-10-08 - Claude

**Input as relf reads it** (the owner: ACCEPT should read a byte at a time on
descriptors that cannot seek - fixed in relf). relf's KEY reads one byte off
descriptor 0 and its READ-LINE reads a seekable descriptor a block at a time,
seeking back past the newline, anything else a byte at a time: descriptor 0
is shared with every child, and a byte read ahead is taken from whatever
runs next. This engine still read stdin 4 KB ahead (t_ibuf) and gave every
file descriptor, pipes included, a 4 KB read-ahead slot whose seek-back fails
on a pipe. Now (engine/vm-lab.c, images unchanged): READ on descriptor 0
hands over at most a line as before, from a seekable one a block and a seek
back, from anything else a byte per read(2); READ-LINE on descriptor 0 a byte
per read; a file descriptor that cannot seek is marked raw when it gets its
slot. Proven both ways: `printf '1 2 + . CR BYE\nREST\n' | sh -c 'engine
img; cat'` leaves REST to cat, and READ-LINE on /dev/stdin takes only its
line - both FAIL on the previous engine, rebuilt for the purpose. Found on the
way: a macro reading its argument four times (T_EDIT(p[k++])) lost whole
lines on a pipe - the test suite passed it (every input it gives is a file),
the hand-made stages' check (a pipe) caught it. Not the cause of the corpus's
repeated passes (Iteration 100): its ACCEPT test reads the next line of
terminal input by design, unbuffered or not - the empty line stays. Tests
pass; hand-made stages identical; front designs in three engine forms
through the gate.

**The Paleocomputing article** (Habr, 2026: Wirth's RISC5 and Project Oberon
rebuilt by AI agents in nine days - in the browser, QEMU, KubeVirt). Its
technical subject does not carry over; its method does, and matches this
project's own failures. The prompts library: **15-checks-that-can-fail**
(plant faults; a check that cannot run is red; no verdict from a log line;
the changed path covered), **16-premortem** (role reviewers attack a plan
before it is built; a ceiling for every claimed gain; "first" is a search
result; stopping points; the boring-result line), **17-variants-as-data**
(the next variant a row, a fictional one in the tests); 03 gains step 9,
null rewrites (meaning-preserving changes as the noise floor - our 4 KB
steps), and in step 4 the disappointing result audited too. Carried back to
relf through prompts/UPSTREAM.

## Iteration 105 - 2026-10-08 - Claude

The owner asked to confirm that KEY and EMIT are colon words: they are - in
forth/kernel.4 and in every image (checked on the fastest and the smallest
design), KEY is KEY-BYTE 1 READ 0= IF BYE THEN KEY-BYTE C@, EMIT is
EMIT-BYTE C! EMIT-BYTE 1 WRITE, TYPE is WRITE; no design has an opcode of
either name. They rest on the primitives READ and WRITE - not yet on one
SYSCALL, which is agreed in principle but not built; with it, READ and WRITE
would become colon words too, and WRITE's output buffer (4 KB in C, flushed
before reads, fork and exit) would have to move into Forth, not go: one
write(2) a character made relf's runs 5x slower. NEXT-RUN: the long run 9
hours, not 12 (seed 28 tag2 9h).

## Iteration 106 - 2026-10-08 - Claude

**Seed 28 and session 25** (results/evolve-amd-ryzen-7-pro-8840hs-seed28.md):
nine hours on four cores (workers on cpus 4, 8, 6, 12), the long workloads,
rtempty; population 256, 158 generations before the deadline, 39,985 designs
(2.7 s each for a worker); deaths only the reach limit's 2,305 and one
old-format design that does not convert. 8 h 42 min with the comparison.
Session 25 measured seeds 24-28 with the long workloads (calibration 0.993):
**seed 28 not small, by a hair** - the fastest +5.0% (679fdd08a1, 0.132 at
38,560 bytes), smallest total 24,874 (+0.20%), memory none. The front of all
runs 67 designs, 66 of seed 28. **Four workers measured as tightly as one**:
a front design's speed in the run against its re-measured speed, 10-90%
0.900-0.955 (seeds 26 and 27, one worker: 0.896-0.990, 0.848-0.992).
Still improving at the end: 60 of its 86 front designs born after
generation 120, the best recorded speed 0.124 by generation 10, 0.119 by
158. On the front of all runs: t2wide 63, opbody 66, hotinl 37, the JIT 18,
rtempty 17. Q (information): best fc52c18d76, 0.151 at 34,464 bytes; the
fastest 1.04 times it, the smallest 2.79 times. NEXT-RUN: seed 29 tag2 9h.

## Iteration 107 - 2026-10-09 - Claude

**How long a run should be** (results/run-length.md; the owner's guess:
long runs lose efficiency at the end). Measured on seeds 26-28 by hours
elapsed, with the run's own measurements (noisy: a run keeps its luckiest)
and with the final front re-measured (honest): seed 28 had ~80% of its gain
in the first hour, ~89% in three, the last five hours ~10% - though its one
real speed jump (0.141 -> 0.133) came between hours 4 and 5. With new genes,
9 hours; with nothing new, ~4-6 hours gets ~90-95% of it. **The day** (the
owner: 6am to 9pm free, a 9-hour run from 9pm): seed 30 for 6 hours - the
convergence check - its comparison, then knockouts of its front, each gene's
worth in each design (evolve.py --knockout, never yet run on t2wide, opbody,
hotinl, rtempty). The knockout now finds the front with first_front, not
fronts() - every pair of a long run's ~40,000 designs would have taken half
an hour. NEXT-RUN: seed 30 tag2 6h, then the comparison, then the knockouts.

## Iteration 108 - 2026-10-09 - Claude

**The gene jitx** (results/jitx.md; the owner: "proceed" with batch 1). On
top of `jit`, the parts priced in Iteration 103 that only pay together:
variables as literals (DOVAR's align8(body + 5)); words without the JIT
header - kernel words, run-time constants - translated once each, kept by
address, their end the first EXIT no branch reaches past; >R, R> and R@ with
SPN's stencils, in words whose return stack balances in order (native words
return through the C stack, so a word reading its own return address stays
bytecode); a FILL stencil without a call (rep stosb). VM counts on two JIT
designs: kernel workload bytecode dispatches 0.900, corpus 0.997, the
held-out sieve 0.001 - its PRIMES native, 3.4x faster on the VM. Checked
where it changed: the gate, the sieve's output against s6's, FILL's bytes on
the translating call and the next, a balanced >R word; tests pass,
hand-made stages identical, the gene expressed only with the JIT. Cost: +368
bytes of code, a 4 KB BSS table; the engine file +4,288 - the page padding's
step. With the gene off images are identical, the JIT engines' code 48 bytes
larger. Not in this batch: the two engine trims - until the page padding is
fixed their bytes are invisible or a 4 KB lottery. NEXT-RUN: seed 31 tag2 9h,
into ~/Downloads after the day's chain.

## Iteration 109 - 2026-10-08 - Claude

**Seed 30, session 27 and the knockouts** (results/evolve-amd-ryzen-7-pro-
8840hs-seed30.md, results/knockouts-seed30.md). Seed 30 - the first run with
jitx, 6 hours from 13:15 (seed 29 never ran): 24,230 designs in 95
generations, no death but the reach limit's. Session 27 (calibration 1.001)
measured seeds 25-28 and 30: **seed 30 small** - fastest +1.5% (4ddd323cee,
0.135), smallest total and memory none; the front of all runs 75, 54 of seed
30. jitx on 12 of its 89 front designs: its knockout is 2.6% of the selected
workloads' speed, its 3.4x on the held-out sieve unseen by selection, against
an engine file 4.3 KB larger through the page padding. **The knockouts** -
each gene undone in each of 22 front designs: kfast +175%, escape +123%,
kinput +68%, ops10 +51%, rtloop +51%, the JIT +47%, klookup +27% carry the
speed; t2wide 8.4% and 203 bytes; opbody 128 bytes; hotinl 1.9% for 56;
rtloopall (with 424 bytes), t2hot, tracer, tfind and spec ~0 - candidates to
retire, for simplicity; tail ~9% slower for 125 bytes, a size trade.
NEXT-RUN unchanged: seed 31 tag2 9h.

## Iteration 110 - 2026-10-09 - Claude

**The engine's file without page padding** (results/link-N.md; the owner:
choose between the padding fix and retiring the genes worth nothing). The
padding fix first: it is a measurement problem, it misleads selection on
every design, it is checkable exactly on the VM, and it unblocks the trims;
retiring genes needs the loop column first (the knockout's speed leaves loop
out) and changes the genome's identities. The cause, found: not the
page-aligned memory area (.bss takes no file room) but the default linker
script's page alignment of the data sections under -n. Linked with -N: the
data sections end to end. The front of all runs, built both ways: 16
engines unchanged, 59 smaller (median -160, up to -2,528 bytes), none larger;
15 designs of every engine form through the gate; tests pass, hand-made
stages identical. Sizes changed for every design - the stopping rule counts
afresh. NEXT-RUN: seed 32 tag2 6h (hours to fit the day), then the
comparison.

## Iteration 111 - 2026-10-09 - Claude

**Seed 32 and session 28** (results/evolve-amd-ryzen-7-pro-8840hs-seed32.md):
the first run with engines linked under -N, 6 hours from 21:53, 25,016
designs in 98 generations, no death but the reach limit's (seed 31 never
ran). Session 28 rebuilt every run's designs under -N (calibration 0.998):
**seed 32 not small** - the smallest binary + image +3.8% (333b2c6807, 22,342
bytes, 889 below anything before: the page padding had hidden the small end),
the fastest +1.5% (67c070bd47, 0.131), memory none. The front of all runs:
111 designs, 96 of seed 32. **jitx with honest sizes**: 30 clean pairs, +456
bytes (it had looked like ~4.3 KB), kernel 0.883, the held-out sieve 6.5x; on
18 of the run's 149 front designs. NEXT-RUN: seed 33 tag2 9h.

## Iteration 112 - 2026-10-09 - Claude

**Seed 33 and session 29** (results/evolve-amd-ryzen-7-pro-8840hs-seed33.md):
8 hours from 04:41 (the owner's choice), 35,862 designs in 141 generations,
no death but the reach limit's. Session 29 (calibration 0.996) measured
seeds 27, 28, 30, 32 and 33: **seed 33 small** - fastest +0.8% (caeb3d97ac,
0.132), smallest +0.39% (ffe6038baf, 22,254 bytes), memory none; the front
of all runs 138, 102 of seed 33. The comparison measured 520 designs in
2 h 18 min - the fronts have grown to ~150 a run since sizes are honest -
so the 8 hours were ~9 h 15 min: comparisons now run 6 rounds (the rule's
bars are 2% and 5%), ~40% less. NEXT-RUN: seed 34 tag2 9h, then the
comparison at 6 rounds.

## Iteration 113 - 2026-10-09 - Claude

**Dead code out of every engine, and two flag genes**
(results/flags-gcsections.md; the owner: new genes for tonight). The two
engine trims priced first and left: 16-bit dispatch tables (~768 bytes) need
the table's text changed in the engine, three generated headers and the
tail-call and multi-state generators - too wide to prove in an afternoon;
cold escaped operations overlap crossjumping. Instead six compiler flags
priced to the byte: --gc-sections takes 1.9-3 KB off every engine - dead
runtime code (vsnprintf, execvp, snprintf, syscall ...; vsnprintf was dead,
not the shell's) - so it is every engine's, not a gene: the front of all runs
(138) all smaller, 1,888-3,392 bytes, median 2,112. alignfn and noinls (~1.1
and ~1.3 KB on -O2 engines, nothing on -Os) are genes. A slip: the flag genes
were looked up as g[k], and the hand-made stages' non-CV8 genome had no such
key - --validate caught it; now g.get(k). Gate: 23 front designs (plain,
tail, the JIT with jitx), cached-top and tail designs with the genes, four
with everything; tests pass; hand-made stages identical. Sizes changed for
every design: the stopping rule counts afresh. NEXT-RUN: seed 35 tag2 9h.

## Iteration 114 - 2026-10-09 - Claude

**Seed 35 and session 30** (results/evolve-amd-ryzen-7-pro-8840hs-seed35.md):
6 hours from 14:40, 25,189 designs in 98 generations, no death but the reach
limit's. Session 30 (calibration 0.998), every engine under --gc-sections:
**seed 35 small** - fastest +1.5% (e5193642ef, 0.133), smallest +0.08%
(585376cf49, 20,318 bytes, ~2 KB below seed 33's: the dead code gone),
memory 2 KB inside the tie: the second small in a row since sizes last
changed - this gene set has converged. alignfn and noinls on ~56% of its
front at once. The front of all runs 151, 121 of seed 35.

**A run from scratch** (the owner: "proceed as you suggested", the anchoring
question): next-run.sh `nocarry` - no archived front carried in; travels to
the detached run in the environment (NEXT_RUN_NOCARRY) and is part of the
run's identity, so a resume keeps it. **A thinner comparison**: the session
had 660 designs, 2 h 4 min at 6 rounds, past the hours' 80-minute reserve;
compare-fronts.py --frontier keeps of each run one design per box of 1%
speed, 64 bytes and 8 KB, plus its three bests - seeds 33 and 35: 82 of 160,
85 of 178. A first version (each run's speed-size frontier) kept ~70%: a
run's own noisy numbers make a staircase where nearly every design survives
by a hair. NEXT-RUN: seed 36 tag2 4h nocarry, then the comparison with
--frontier.

## Iteration 115 - 2026-10-09 - Claude

**Deep dive 2** (results/deep-dive-2.md, lab/evolve/GENES.md "Ranked
(Iteration 115)"; the owner: add the primitive-set gene, find more gene
ideas, make "SOD32 from nothing" possible). **The primitive-set gene priced**:
each demotion turns one-byte opcodes into two-byte calls, adds a body and
dispatches - OVER (38 uses, 2.5% of dispatches) and ROT (up to 5.8%) larger
and slower, UM* a loop that would double the kernel workload's time; no
demotion pays alone: recorded as the floor of an instruction set evolution
builds, with promotion by synthesis (gen-super.py's composition generalized)
as its ceiling. **New ideas with numbers**: ?STACK and (ABORT") are 17.8% of
parse's dispatches (kstack, next), NUMBER? 19.1% (knum). **Built**: `fbuf` -
a file's read-ahead buffer 4096, 1024 or 512 bytes: the kernel workload's
memory 200 -> 172 -> 168 KB on the smallest, 216 -> 180 -> 176 on the
fastest - the first lever on memory, whose front spans 186-200 KB; and
`fromzero` - evolve.py --fromzero, next-run.sh `fromzero` (implies nocarry):
the first generation all random genomes (a VM run: 8 random, 4 alive, the
report and re-measure fine without s6 in the database). Gate: two designs
at three buffer sizes; tests pass; hand-made stages identical. A slip: the
first commit of this iteration missed these two notes (an edit anchor one
word off) - amended.

## Iteration 116 - 2026-10-10 - Claude

**Improving the Forth sources** (results/forth-sources.md; the owner: start
with kstack in Forth and verified rewrites; collect other Forths). kstack.4
(?STACK8, swapped into ?STACK) first made the fastest design slower: the
image's ?STACK already was the kernel input gene's guarded one-compare body,
and the overlay replaced it - deep dive 2 had read kernel.4's ?STACK, not
the one that runs, and (ABORT")'s calls come from INTERPRET (48,000 in
parse) and REFILL (12,021), not ?STACK. Corrected: kstack is kinput's
?STACK8 alone, expressed only without kinput - the smallest design's parse
and corpus -0.7%, same image size, same error message. The real waste is
ABORT" itself: a guarded ABORT" would take the fastest design's parse -4.3%,
corpus -2.3%, for ~20 bytes - the owner's decision (kernel.4 and cross.4,
every image). Verified rewrites of stack-word runs: 2-4 shorter patterns in
two images, at most 0.09% of dispatches - not worth a superoptimizer. Seven
Forths fetched (/tmp only; licences noted): gforth and lbForth compile
ABORT" guarded, gforth's ?stack one compare. Tests pass; hand-made stages
identical. NEXT-RUN: seed 37 tag2 9h with fbuf and kstack.

## Iteration 117 - 2026-10-10 - Claude

**The guarded ABORT" as a gene: abortif** (results/forth-sources.md section
5; the owner: "can we add this as a new gene?"). tools/sod16.py
guard_aborts, switched by layout.py --guard-abort: every compiled call to
(ABORT") with its message gets `?BRANCH` to past the message and `-1` before
it, spliced in right after hot-site inlining and before the specialisations
and fusers (which then fuse the ?BRANCH with its test, and -1 is the one-byte
literal); sites guarded by hand and words with a DOES> entry left alone;
moved branches moved back. Fastest design: parse -5.6% of bytecode
dispatches, corpus -3.0%, kernel -1.0%, image +56 bytes; smallest: -0.8%,
-0.7%, -0.3%, +72 bytes. "Undefined word" and "Not found" exactly as before;
through the gate; tests pass; hand-made stages identical; the gene expressed
in random and mutated genomes. The owner offered a ~100 MB collection of
Forth material (relf's history, SOD32, eForth, 3-instruction Forth, gforth
0.6.2, SP-Forth, test suites, books) - to look through once uploaded.
NEXT-RUN: seed 37 tag2 9h with fbuf, kstack and abortif.

## Iteration 118 - 2026-10-10 - Claude

**The owner's Forth collection** (results/forth-collection.md): 138 MB,
~1,100 source files, examined in /tmp. RelF's origin (SOD32 sped up,
relative offsets), its early superinstruction counts and a todo with
primitive-set decisions; minimal cores (eForth's 31 primitives, FIRST/THIRD,
Itsy, 3ins4th); optimizers to learn from (gforth 0.6.2, SP-Forth's
macroopt); benchmarks. Licences noted: SOD32, gforth, bigForth GPL - ideas
only. **The ANS test suite** (Hayes, Jackson; freely distributable) added as
tests/ans with tools/ans-upper.py (the files are lowercase) and a prelude. Its
first run was vacuous - core.fr's ACCEPT swallowed the next file's INCLUDED,
the corpus's trap of Iteration 100 again; with an empty line it runs:
coreplus and memorytest pass, the rest stop at missing word sets (:NONAME, D-,
CATCH, COMPARE, ONLY, AHEAD), double literals read as singles. **It found the
stack-guard gene killing the engine on underflow**: "relf: return stack
overflow", exit 1, buffered output lost - s6 and the design without the gene
print "Stack error DROP" and go on. The corpus never underflows.

## Iteration 119 - 2026-10-10 - Claude

**The stack guard fixed** (the owner: proceed). The guard's data stack began
two cells below the return stack's guard page, so one DROP too many trapped
there and was reported as "return stack overflow", the process killed with
its output unflushed. Now: 64 cells of slack, so a shallow underflow is
?STACK's - "Stack error DROP", as in s6; the handler names the stack and the
direction by the edge of the page the access hit, recognises the C stack
(the JIT's native recursion killed the engine with a bare SIGSEGV - found
while testing this), runs on its own stack (sigaltstack, added to the
libc-free runtime), flushes the output and exits 70. Gate, tests, hand-made
stages pass; non-guard engines unchanged (--gc-sections drops the new code).

**The held-out check** - lab/evolve/ans-check.py: the ANS suite (tests/ans)
on each design, every file's output against s6's. Twelve front designs (six
with the guard): all ten files identical.

**The collection catalogued** (results/forth-collection-catalog.md): every
top-level item, its licence and use - pForth (public domain) and FICL
(freeware) usable as code; Koopman, Moving Forth, eForth, FIRST, strongForth
for ideas. relf_dev/relf-0.3 holds the owner's 2009 JIT base: t1.asm copies
precompiled machine-code snippets per opcode into a buffer and runs it - the
template idea the project's stencil JIT uses - and relf2.c pre-decodes
threaded code into handler pointers.

## Iteration 120 - 2026-10-10 - Claude

**What doc/ gives the project** (results/docs-reuse.md; the owner: anything
to reuse from the docs?). Koopman's Stack Computers, section 6.3: on the RTX
32P instruction combining cut instructions by ~25% - op+EXIT (here folds),
call+EXIT (tail calls), op+op (supers), literal or variable + op
(specialisations), and op+call, which no gene has: priced on this project's
designs with the profiler - an operation right before a call is 2.7-6.6% of
the fastest design's dispatches (LIT8, ?BRANCH8, (PARSE), PLACE, DROP, 0=), 2.7-
3.8% of the smallest's - the gene candidate opcall (GENES.md). Moving Forth
part 5: Rodriguez's rules for which words are primitives, and the spectrum
13 / eForth 31 / CamelForth ~70 - a prior for the instruction-set search.
Knaggs's thesis: a stack-effect algebra, for checking fused sequences and
genetic improvement's edits. The rest: theory for expression compilers,
background, learning.

## Iteration 121 - 2026-10-10 - Claude

**The gene opcall** (results/opcall.md; the owner: proceed). An operation
followed by a call becomes `X;CALL`: X's handler copied by tools/gen-opcall.py
with NEXT() made CALLNEXT() - the call's first byte, a compare, a direct jump
into the call's code - and the call left in place after it. The converter's
last pass (sod16.py opcall_rewrite) on operations without an operand; the
pool of 16, each offered where the design has its handler. The two target
designs had no slot left in the 128-entry table, so the fused operations are
logical 0xFE00 + k with their own table, as the JIT's opcode. A first build
died in the converter's format-10 body checks, which ran with opcall on -
they now switch it off, as they do pairs. Fastest design, 16 ops: parse
-3.8%, corpus -3.4%, kernel -1.6% of dispatches, +768 bytes of engine;
smallest, 14: -2.5%, -2.5%, -1.6%, +656. Gate, the ANS suite as s6 on both,
tests, hand-made stages; all 945 recorded ids unchanged. NEXT-RUN: seed 37
tag2 9h.

## Iteration 122 - 2026-10-10 - Claude

**The handoff, checked** (the owner: last time a new chat found files
missing - fixed?). Fixed in Iteration 87 (the fronts' genomes in results/);
checked now from a fresh clone of the bundle: it builds, tests pass,
hand-made stages identical; all 151 designs of the front of all runs have
their genomes in results/ (945, every id right); eleven rebuilt from results/
alone - the fastest and smallest among them - pass the gate with their
recorded image bytes; the working repository holds nothing uncommitted
(build/ and caches ignored). GOALS.md "Resuming in a new chat" now opens with
a short HANDOFF: the state, the pending runs, the open threads in order,
where to look.

## Iteration 123 - 2026-10-10 - Claude

**Seed 36 and session 31 - the anchoring test** (results/evolve-amd-ryzen-
7-pro-8840hs-seed36.md). 4 hours with nothing carried in (2 h 40 min of
evolution, 53 generations, 13,508 designs): the best speed 0.812 -> 0.148 by
generation 20 -> 0.141; the smallest 25,369 -> 20,425. Session 31 (calibration
1.007; with --frontier: 362 designs in 63 minutes, inside the reserve): seed
36's fastest 0.146 against the carried 0.130, smallest 20,425 against 20,318,
memory 188 against 186; 2 of the 90 on the front of all runs, both in the
middle; the same gene choices as the carried runs. **The owner's question -
does adding genes one at a time skew the search? - answered no**: a fresh
start reaches the carried runs' neighbourhood and no further. NEXT-RUN
unchanged: seed 37 tag2 9h with the new genes.

## Iteration 124 - 2026-10-10 - Claude

**Set up from the Iteration 123 bundle, the checks shown to fail first**
(prompts/15): run-tests.sh's negative control caught on all 16 corpus runs;
--validate's image comparison caught one bit flipped in the build's s6 image
(DIFFERENT, exit 1; s5 still IDENTICAL; restored, hash checked); alive()'s
corpus half caught one wrong case ("died: corpus"), its kernel half a
workload that never writes kernel.img and a written kernel one bit off. The
handoff prompt's clone fails where /home/claude belongs to root: make the
directory and chown it first (HANDOFF-PROMPT.md, GOALS.md).

**Seed 37 confirmed, then started by the owner.** next-run.sh traced: the
deadline is fixed at the start (evolution to 7 h 40 min), but the re-measure
is serial (~7 s a design) and session 32 (seeds 32-37 by --frontier, ~400
designs at 10.4 s) is larger than 31 - the chain ~9 h 10-30 min, the seed pack
~8 h in. The code of Iterations 115-121, new to the laptop, rehearsed on the
VM: the carry as main() does it (0 of 604 recorded ids changed); 22,000+
children through crossover, borrow and mutate, no exception; the run's
evaluate() on the fastest and smallest of seeds 32, 33, 35, 36 with all four
new genes on - 8 of 8 alive; fbuf's memory per design -32 to -40 KB.

**The Forth 2012 test suite** (results/forth-standard-tests.md; the owner:
reuse tests from the Forth Standard committee's suite?). tests/ans is now that
suite (commit 4c87e56; Hayes's files "distributed freely", Jackson's public
domain) - 963 tests on s6 against the old copy's 821; doubletest alone covers
less (5 against 32: it opens with number prefixes). ans-check.py rewritten:
s6's own result against the suite first (a fault every stage shares is
invisible to a comparison with s6), sentinels inside each file, every test
counted, a negative control, an exit status. **It found five faults**, alike
on all 14 systems, not on RelF: +LOOP exits early at the wrap-around
boundaries (Haley's tests; the kernel's sign-flip rule from SOD32, checked
three ways - s6 128 where RelF and the standard give 256); FILE-POSITION
leaves 2 cells, not ( ud ior ); READ-LINE into a 0-length buffer says end of
file; an empty S" " or ." " swallows the rest of the line (`34 WORD`); and
**DELETE-FILE segfaulted on every call** - the handler stored unlink's result
over the name's address, then restored the byte at result + u (0xc, the
address SPN's handler named), in six engine sources since the baseline;
nothing called it, the suites stop before their test. **Fixed**: images
identical, binaries +0 on 76 of 98 designs and +32 on 22; a check in
run-tests.sh on every stage, failing on all 14 old binaries. The rest are the
owner's decision (each changes every image or engine). The 90 designs of the
front of all runs and 8 with the new genes say what s6 says on all 14 files.

**tests/core/tester.fr restored.** ans-check.py copied the suite's tester.fr
into the work directories, whose files are symlinks into build/work - and
build/work/tester.fr is tests/core/tester.fr: from Iteration 118 to 123 it was
the 56-line ANS tester, not the 1,022-line tester and core tests the locals
check loads (that check passed either way; the corpus and the gate never read
it). Restored byte for byte; ans-check.py replaces files instead of writing
through them. NEXT-RUN: none - seed 37's packs first.

## Iteration 125 - 2026-10-10 - Claude

**RelF's fixes, taken** (results/relf-reuse.md; the owner: reuse what RelF
upstream has, then fix). This project forked from RelF at e8440ed - kernel.4,
extend.4, cross.4 and the tester byte for byte - so RelF's 140 later commits
were the list. Each fix below was a fault on s6 and right on the vendored RelF:
**+LOOP** (gforth's test, ((x XOR x+n) AND (x XOR n)) < 0, in all six places:
kernel.4, sod16.py's expected body, the opcode in vm-lab.c, gen-tos.py and
gen-msc.py, SPN's st_ploop); **PARSE** skipped leading delimiters, as SOD32's
does - so S" " and ( ) took the rest of the line; it is standard now, its old
body kept as PARSE-WORD for WORD and klookup's WORD8 (kinput's PARSE8 is
PARSE-WORD8, its opcode unchanged; hotinl's sites renamed) - RelF put the skip
into WORD, which would cost ~15 dispatches a token; S" ." ABORT" and cross.4's
on 34 PARSE STRING,, ABORT = WARM (it printed " ;"); **the file words'** doubles
and iors (REPOSITION-FILE returned the position as its ior, FILE-SIZE always
0) and READ-LINE into 0 bytes, in all six engines; **CONVERT** (`1+`, not `-1 +`);
**names over 31** refused in the three header words; **IF outside a definition**
refused (it segfaulted) - ?COMP in 95 bodies, every copy of the 15 compile-only
words. shell.4's one comment that leaned on the old PARSE, `( ) )`, is `\ )` -
found by the shell image failing to build. Bootstrapped by tools/reseed.sh:
the 8-byte kernel a fixed point at 25,640 bytes (was 25,144).

**Tests**: RelF's coreplus-loop.fth (the standard suite's +LOOP sections) and
a new tests/core/fixes.fth run on every stage from run-tests.sh, in one file
with the sentinel at its end and a copy with one wrong case, plus the two
refusals; on Iteration 124's build all 14 stages fail them (8 cases each; the
refusals a segfault). run-tests.sh passed a build that had stopped half way -
a missing stage was a SKIP; now a stage missing where its width was built
FAILs (s3 hidden: the suite fails). **Cost**, the 98 designs rebuilt: none died,
all as s6 on the standard suite (ans-check.py on the 90: 0 differ); images
+120-160 bytes, binaries mostly +64 or +96; dispatches kernel +1.8-2.5%, corpus
+0.1-1.5%, parse 0-0.7%. s6 fails 4 of the standard suite (the double
literals) where it failed 14. Not taken: RelF's ext/ tests need its newer
extend.4 and kernel (and extend.4 is in the kernel workload); the shell suites
wait on whether the shell is part of the job. A job started in a tool call
dies when the call returns: run it inside one call (GOALS.md).

## Iteration 126 - 2026-10-10 - Claude

**Seed 37 processed** (results/evolve-amd-ryzen-7-pro-8840hs-seed37.md; session
32 in results/compare-fronts-amd-ryzen-7-pro-8840hs.md). 9 hours at d5917cd,
the first run of fbuf, kstack, abortif and opcall: the fronts of seeds 32-36
carried in, 165 generations, 42,225 designs, 40,132 alive; the chain 9 h 08
min (estimated 9 h 10-30). **Not small: memory 184 -> 156 KB** against the
earlier runs in the session (fastest 0.134 against seed 33's 0.133, smallest
20,430 against 20,468 - both small), as predicted before the run; 90 of the
107 on the front of all runs are seed 37's. On its front (242): fbuf 123 (121
at 1 KB, 2 at 512 B; 152-184 KB, the rest 184-220, the fastest among the
rest), abortif 79, kstack 17 (of the 19 without kinput), opcall 13. The
held-out check at Iteration 125's code: all 242 as s6 on the Forth 2012 suite
(58 with the guard), the control caught. Proposed: seed 38, 9 hours, the same
genes - the first run on the fixed kernel (NEXT-RUN; the owner's call).

## Iteration 127 - 2026-10-10 - Claude

**The measurement changed, alone** (the owner: both, before seed 38). The
gate: tests/corpus/core.fth ends with the +LOOP sections of the Forth 2012
suite's coreplustest.fth (tests/core/coreplus-loop.fth, RelF's) - 661 cases;
every stage passes them; upstream SOD32, the ancestor, fails exactly those 7
(GD8, GD9) and run-tests.sh checks that it is those and no others, its
negative control then needing an eighth. The selection: kernel, fib, corpus,
loop, bubble, ackermann; held out sieve and parse. bench/bubble.fth is the
owner's (RelF's bench/langs/bench.4, 300 cells), bench/ackermann.fth A(3,5) -
the collection's RelF/bench Ackermann is not in the repository (a re-upload
would let it replace this textbook one). Both run alike on every kind of
stage (cell, pack, SOD16, CV8, CV8b, SPN, RelF: 30836742192 and 253); K = 8
and 20 for ~11 ms on the fastest design. That design, seed 37's fastest:
0.229 under the new selection (0.130 before) - bubble 0.44 of s6, ackermann
0.57, against loop 0.06. Speeds are not comparable with earlier records; the
stopping rule counts afresh. evolve.py's knockout report named the old
workloads by hand; it reads the list now.

**And the plan** (results/word-audit-plan.md): the todo genes' status - built
since Iteration 115: kstack, abortif, fbuf, fromzero, opcall; open: the JIT
stencils (first now: bubble and ackermann are where the front is weakest),
one SYSCALL (not built), 16-bit dispatch tables, packed names, knum,
promotion by synthesis. The owner's audit of every word against other Forths:
weigh, collect (permissive sources only), compare in this VM's terms, land as
overlay genes; its premortem puts the ceiling at ~3% of speed and ~1.7% of
size, with stopping points.

## Iteration 128 - 2026-10-10 - Claude

**Bubble and ackermann are the owner's own** (he sent his collection,
forth.tgz): RelF/bench/bubble.4 and ackermann.4, their words as they were -
bubble's CELL +LOOP over addresses, 2@ and 2!, VERIFY-LIST; ackermann's -ack
with 1 -1 D+ for A(x-1,1) - sized for a timed run (ELEMENTS 300, not 6000;
NUM 5, not 3) and given a BENCH word that prints (65505 0; 253, alike on every
kind of stage). K = 12 and 23, ~11 ms on the fastest design. Seed 37's fastest
under the selection: 0.224 - bubble 0.32 of s6, ackermann 0.71. Still before
any run of Iteration 127's measurement, so part of it. Runs of 6 hours now
(the owner: two in a day): seed 38, then 39, the same genes.

## Iteration 129 - 2026-10-10 - Claude

**Seed 38's first start failed at the tests**, ten minutes in: run-tests.sh's
two sections from Iteration 125 (DELETE-FILE, the fixes) listed every stage
at both cell widths, and SPN's s7 and s8 exist at 8 bytes only - their native
code is x86-64. The laptop builds the 4-byte half, so the five showed as
"not built" there and failed the suite; this VM, without a 32-bit compiler,
never built that half, so the check had passed only where it could not fail
that way (prompts/08). Everything else on the laptop's 4-byte side passed,
the new sections included on the ten stages that exist. Fixed: stages_for
lists a width's stages as the corpus section does. And the VM now has
gcc-multilib, so it builds both halves: next-run.sh's four checks - build,
tests, validate, jail - reproduce the laptop's failure at Iteration 128's
commit and pass with the fix; a 4-byte stage hidden fails the suite. The
HANDOFF-PROMPT's set-up installs it. The jitloop work stays stashed until it
works (bubble faults with the gene on).

## Iteration 130 - 2026-10-10 - Claude

**The gene jitloop, built and dormant.** Why the front is weak on the new
workloads (the JIT's own log, profiling builds of seed 37's fastest design):
bubble's inner words stay bytecode at (+LOOP), which has no stencil mapped,
and ackermann's -ack at D+. Mapping SPN's (+LOOP) stencil crashed the corpus
and bubble - and the cause was the JIT's scanner, not the mapping: it reads a
stencil to the next table function or 64 bytes, and (+LOOP)'s is 87 bytes
(since Iteration 125's rule; 55 before, missing its exit even then), (?DO)'s
76 - cut after its fall-through, its skip lost, so a (?DO) with equal bounds
would have jumped into the next stencil. No stencil any recorded design uses
reads differently at 160 bytes, so none carried the fault. Under JITLOOP: the
read 160 bytes, and both exits required of PLOOP and QDO, else bytecode
(slower, never wrong). On five JIT designs with the gene on: the gate, bubble
65505 0 and ackermann 253, the Forth 2012 suite as s6 on all 14 files. On the
fastest: bubble's dispatches 13.29 M -> 197 k, its long run 13.2 -> 7.9 ms
(VM), the corpus -1.1%, the rest unchanged. A D+ stencil made -ack native
(dispatches -99.9%) and ackermann no faster (12.8 ms both) - the call is the
cost, and the native call costs what the bytecode one does; left out. With the
gene off, ids, images and engines are byte-identical (two JIT designs and the
smallest). Dormant: in LATE, not in EXPRESSED - 0 of 20,000 mutations set it -
and the build reads the expressed genome, so a forced value cannot build
under an old id. The four checks pass at both widths. NEXT-RUN none while
seed 38 runs.

## Iteration 131 - 2026-10-10 - Claude

**The audit's first step** (results/word-audit.md). The sources, newer online
where they exist (the owner): pForth (0BSD-style), FICL 4.x from its author
(BSD-3), ueForth for eForth (Apache-2.0), jonesforth (public domain), zForth
(MIT), Retro (ISC); lbForth GPL-3 and the standard's repository (no licence
stated) for ideas; F83, cmFORTH, FIRST/THIRD and the GPL Forths from the
collection - fetched to the VM, the commits recorded. The weights, exact on
profiling builds: kernel words carry 60% of s6's dispatches over the six
selected workloads; 17 words carry 90% of that on s6 and on the smallest, 41
on the fastest (its interpreter only - the JIT runs the rest natively); the
union is 51 words, the audit's order. Seen already: every dictionary lookup
zero-fills a 32-byte name buffer a byte at a time (NAME>BUF's FILL - 35% of
s6's kernel workload, 27% of its corpus; kfast avoids it, and s6 does not have
kfast).

## Iteration 132 - 2026-10-10 - Claude

**The audit's batch 1, and SYSCALL priced** - two decisions for the owner,
nothing in the kernel or the engine yet (seeds 38 and 39 run the same code).
NAME>BUF zero-filled 32 bytes a byte at a time for every lookup; the cell-wise
search needs two cells - eForth's PACK$ zeroes one, for the same reason. In a
scratch clone (reseeded, both widths, run-tests PASS, 7 of 7 IDENTICAL), the
two-cell NAME>BUF cut s6's dispatches 28% on the kernel workload and 27% on
the corpus; NAMEBUF needed a cell more - the old code read past it for a
31-character name, and the new one, writing there, broke the 4-byte build
until it had room (results/word-audit.md). The other heavy words are minimal
already; COLD is noise (2,649 dispatches of start-up on s6). SYSCALL, exact by
source-line attribution of s6's engine: the 29 OS handlers are 3,153 bytes and
the runtime 3,400 - ~3-3.5 KB net smaller for every design if built
(results/syscall-pricing.md).

## Iteration 133 - 2026-10-10 - Claude

**The owner's go: NAME>BUF into the kernel after seed 39, SYSCALL built as a
gene.** NAME>BUF waits as results/pending/namebuf-after-seed39.patch (it
applies to master; not applied - seeds 38 and 39 run the same code).
**SYSCALL, phase 1 - the engine half** (the gene sysc, not yet wired into
the evolver). A design's image is the kernel only - the evolver never loads
the shell - and neither the kernel nor extend.4 calls the shell's process and
environment primitives, so with SYSC the engine keeps one SYSCALL in FORK's
slot, ( block num --- r ), and the other seventeen and the runtime's
environment and getpwnam compile out (x86-64 only, by #error). s6's engine:
20,248 bytes as built, 15,568 with SYSC - 4,680 smaller, 23% (the linker
drops what only those handlers used, too). Without SYSC every hand-made engine
is identical; with it the gate passes on s6's image, the profiling build
compiles, and SYSCALL 39 through FORK's slot returns the pid. Next: the
shell's half - its seventeen words in Forth on SYSCALL - tested by the shell
suite removed in 5c87022, which still runs (6 s, 8 assertions in 2 files fail
on today's shell, the baseline); then the gene, dormant.

## Iteration 134 - 2026-10-10 - Claude

**The shell suite, back.** tests/shell - the parent project's 57 files - was
removed in 5c87022 as unrun; it still ran, and its 8 failing assertions in 2
files were the tests' own assumptions, not the shell: run-comments expected
HOME=/root (len=5, trim=root), run-engine-stacks the parent's relf,
kernel.img and fib.4 at its top. Fixed (HOME given; this repository's cell
stage and kernel; fib computed inline) - the engine's own diagnostics were
already the expected ones ("relf: data stack overflow", exit 70). run-tests.sh
runs every file through the cell stage's shell and s5's (s6 is not built with
one): 554 assertions each; the negative control, a shell that ignores its
command, fails 468. The suite is what the gene sysc's shell half must pass.

## Iteration 135 - 2026-10-10 - Claude

**SYSCALL phase 1, the shell half.** forth/shell-sysc.4: the seventeen
process and environment words over SYSCALL, with their old stack effects
and results. On a SYSC s5 engine with a shell image built through the cell
stage and the converter, as build-stages.sh builds s5's, tests/shell passes
all 554 assertions, as the plain shell does, and ~user, ulimit -f, export,
unset, the child's environment and cd agree line for line
(tools/test-sysc-shell.sh, not yet in run-tests.sh). Two things the converter
taught: ?DO is not translated in cell-compiled code (the shell never used
it - the overlay's loops are BEGIN WHILE REPEAT), and the cell kernel has no
NIP. Next: the gene sysc, dormant (after seed 39, with NAME>BUF).

## Iteration 136 - 2026-10-10 - Claude

**The gene sysc, wired and dormant.** In LATE, expressed on CV8 designs only
(SYSC is vm-lab.c's; the cell family is relf.c), the build flag from the
expressed genome - not in EXPRESSED until seed 39 has run. Forced on: eight
front designs of seed 37 through the gate, engines 2,880-3,848 bytes smaller
(its smallest -14% in all); tail-call threading -6,568 and msc -3,728 on s6's
genome (the tag carries neither). Off: ids, images and engines as Iteration
130's. The shell's environment table is ALLOCATE'd on first use - not 4 KB
of zeros in the image; tests/shell still passes on the SYSC shell. The four
checks pass at both widths. Waiting for seed 39 to have run, together: the
NAME>BUF patch, jitloop and sysc into EXPRESSED, tools/test-sysc-shell.sh
into run-tests.sh.

## Iteration 137 - 2026-10-10 - Claude

**Cheaper native calls, priced and built: the gene jitinl, dormant.** Why
native -ack was no faster (Iteration 130): not the depth - a native call
costs 2.5-2.8 ns at depth 10 and at depth 500 alike, against 6.6-10 ns
bytecode on s6 - but the calls to one-operation words: -ack calls 0=, 1+ and
1- as words, and a native call and return to one cost ~0.7 ns, a quarter of a
small recursive word's time (1- 2.92 ns a call, -1 + 2.21). jitinl: the JIT
makes such a call the operation itself (jit_inl1 - not one that branches,
ends the word, or touches the return stack or the interpreter; anything else
stays a call), and D+'s stencil comes back with it. On seed 37's fastest
with jitloop: ackermann's 12.7 M dispatches native and its long run 10.1 ->
5.0 ms (VM); bubble's 11.0 -> 5.4 with jitloop; together roughly a fifth off
the speed score, for the laptop to measure. Five JIT designs with both: the
gate, the answers, the Forth 2012 suite as s6. Every new gene off: ids,
images and engines identical to Iteration 130's.

## Iteration 138 - 2026-10-10 - Claude

**The owner: the kernel holds core words only; the size objective stays the
kernel's.** The shell is used here for correctness alone - tests/shell in
run-tests.sh and tools/test-sysc-shell.sh - never timed: no workload, gate or
design image contains it (checked). A census of kernel.4 under that principle
(results/word-audit.md): 269 words, 180 standard; 20 non-standard words only
the shell uses or nothing does - its seventeen, SYSTEM, A/O, CHAR- - some
300-400 bytes of every kernel image. Their move out waits on one model for
the OS words (SYSCALL in every engine) - the owner's decision.

## Iteration 139 - 2026-10-10 - Claude

**?DO and LEAVE in extensions.** The converter refused both (BAD_WORDS):
their operand had been an absolute address. The kernel has since stored
leave addresses as offsets from the cell that holds them, like every other
branch (RESOLVE-LEAVE; run-tests.sh saves and reloads a skipped ?DO and a
LEAVE) - the refusal was stale, and it had made the shell's overlay rewrite
its loops. They are loop words now, like (LOOP). Every image the build makes,
63 of them at both widths, byte-identical; four words using them (a skipped
?DO, a LEAVE, a running ?DO, a LEAVE in a nested loop), compiled on the cell
stage before shell.4, translate and run right on s1, s3, s4 and s5
(tools/test-ext-loops.sh) - and the old converter refuses all four on all
four stages, the negative control. The test joins run-tests.sh after seed 39.

## Iteration 140 - 2026-10-10 - Claude

**libc leaves the 4-byte half too, and the switch found a shell bug.** The
owner had thought libc gone; only the evolver's engines were - build-stages.sh
linked glibc by default (ENGINE_RT=libc), and every 32-bit engine always.
engine/rt-linux-i386.c: int $0x80 system calls (a function of their own, ebp
being the frame pointer), i386's numbers (mmap2, wait4, ugetrlimit), its
signal struct and rt_sigreturn, an entry point 16-aligned at the call; the
portable rest is rt-linux-x86_64.c's, included with RT_PORTABLE_ONLY - one
copy. Evolved designs' engines byte-identical after that file's edit. The
4-byte cell engine without libc: the corpus, the fix tests and Haley's +LOOP
tests byte-identical to glibc's, both stack overflows diagnosed.
ENGINE_RT=nolibc now covers 32-bit (RT_FLAGS32). **With every hand-made
engine libc-free, tests/shell failed**: 8 nested for loops crashed. The
shell's DO-FOR-ITERATE measured its current word through an arena address
after running the body - and a nested loop's capture had RESIZEd the arena
away from it: a use-after-free, invisible under glibc (a freed block stays
mapped, its bytes right by luck), fatal under the libc-free allocator (over
32 KB, unmapped). Found with strace (the fault address inside the unmapped
block). Fixed in shell.4 - advance before the body runs; depth 8 and 10 run
whole. Everything passes both ways: the four checks at both widths, the shell
suite, the SYSC shell, ?DO and LEAVE in extensions. The libc-free default is
a pending patch, for after seed 39.

## Iteration 141 - 2026-10-10 - Claude

**SYSCALL: -errno, and both widths** - the first steps of the single-SYSCALL
model (the owner agreed: SYSCALL in every engine, the kernel declaring it
alone - opcode slots kept, -errno, x86-64 and i386). SYSCALL returns the
kernel's -errno, not -1 (chdir("") gives -2): the shell can tell EINTR from
ENOENT; the overlay's 0< tests are unchanged. At 4-byte cells the engine maps
the overlay's x86-64 numbers to i386's (eleven calls; any other ENOSYS), and
the overlay reads a C int with SYSC-I@ at either width (PIPE's descriptors,
WAITPID's status). tools/test-sysc-shell.sh runs at both widths: the shell
suite, all 554 assertions, and the targeted paths as the plain shell - with
glibc and libc-free alike. Without SYSC every engine as before: evolved
designs identical, the four checks pass. Next: SYSCALL in relf.c, pack4.c,
pack8.c and the SPN engines; then, after seed 39, the kernel's names.

## Iteration 142 - 2026-10-10 - Claude

**SYSCALL in the cell engine.** relf.c takes the same transformation as
vm-lab.c - now a script that checks an engine has what SYSCALL needs before
changing it (it refused relf.c until PROFDUMP, the profiler's, was made
optional). Without SYSC the cell engine is byte-identical at both widths;
with it, a shell built as build-stages.sh's cellshell builds the cell
stage's, the overlay loaded first, passes tests/shell (554 assertions) and
matches the plain cell shell at both widths, with glibc and libc-free. The
libc-free cell engine: 28,552 -> 24,120 bytes at 8-byte cells, 32,092 ->
27,964 at 4. tools/test-sysc-shell.sh covers s5 and the cell stage. Left:
pack4.c, pack8.c and the SPN engines; then, after seed 39, the kernel.

## Iteration 143 - 2026-10-10 - Claude

**SYSCALL in every engine: the single model's engine half done.** pack4.c,
pack8.c, spn.c and spn-cv8.c take tools/sysc-xform.py's transformation, as
vm-lab.c and relf.c did. Without SYSC all nine pack and SPN engines the build
makes are byte-identical. With every 64-bit engine built SYSC
(ENGINE_CFLAGS=-DSYSC=1), run-tests.sh fails only where a shell built without
the overlay boots - the corpus on all fifteen 64-bit stages, DELETE-FILE, the
fixes, locals all pass - and getpid through FORK's slot answers on every
stage: the cell stage, both pack engines (at both widths, i386's number
mapped), s1-s6, SPN's s7 and s8s. The kernel part waits for seed 39 to have
run (results/syscall-pricing.md).

## Iteration 144 - 2026-10-10 - Claude

**The audit's batch 2** (results/word-audit.md). SKIP and SCAN, under every
parsed word, move on with `1 -1 D+` (the owner's idiom) and keep the
delimiter on the return stack: on s6 after NAME>BUF, the kernel workload
-2.3%, the corpus -1.7%, parse -1.4%, the image 8 bytes smaller - a pending
patch for after seed 39. CMOVE, CMOVE>, ?STACK, NUMBER? and DIGIT? read and
counted, not worth a kernel change; REFILL's tab pass (7.3% of s6's kernel
workload) removable only by changing what a delimiter is - the owner's call.

## Iteration 145 - 2026-10-10 - Claude

**Tab-free parsing, a pending patch** (the owner's: a tab is a space to the
parser). No source here holds a tab, yet REFILL passed over every line for
them. SKIP and SCAN take any control character for a space delimiter - in the
kernel and in the C operations, which live in three places (vm-lab.c,
gen-tos.py, gen-msc.py) - and REFILL and kinput's REFILL8 make no tab a
space. Building seed 37's fastest found what the plain SKIP/SCAN patch had
missed: a body unlike the converter's expected one kills a kinput design -
it would have killed most of the front after seed 39; the expected bodies
are updated, and that patch is replaced. The tab test (tests/core/tabs.fth)
is right on 22 hand-made stages and 20 front designs, with a negative
control; on s6 the kernel workload -11.3%, the corpus -5.4%, parse -3.7%.
Its run-tests section first reported "ok, 0 stages" - run before stages_for
existed; now after it, and no stage tested is a failure.

## Iteration 146 - 2026-10-10 - Claude

**The after-seed-39 batch, rehearsed.** A scratch clone with the pending
patches in order - NAME>BUF, parsing, the libc-free default - the dormant
genes jitloop, jitinl and sysc expressed, and tools/test-sysc-shell.sh and
tools/test-ext-loops.sh as run-tests.sh sections: the kernel's fixed point,
then the four checks at both widths, libc-free - every section run (the SYSC
shell 8 checks, extension loops 4 stages, tabs 22 stages and the control),
7 of 7 IDENTICAL, the jail. A short tag2 run (138 designs, the VM's one CPU):
119 alive, 18 refused by the reach limit (seed 37: 5% of its 42,225), one
layout that dies as it does on master; the six carrying sysc all alive. The
five JIT front designs with all three genes: the gate, bubble and ackermann's
answers, the tab test, the Forth 2012 suite as the batch's s6. The genes'
switch and the two sections are the fourth pending patch; the four, applied
to a fresh clone of master, give the rehearsal's files exactly.

## Iteration 147 - 2026-10-10 - Claude

**The single-SYSCALL model's kernel part, a pending patch** (the fifth of the
after-seed-39 batch). cross.4 gains PRIMITIVE-SLOT - an opcode advanced past
with nothing made in the target; kernel.4 declares SYSCALL in FORK's slot and
the other seventeen and SYSTEM as `PRIMITIVE-SLOT (NAME)` - every position kept,
so the old seed bootstraps the new kernel and the tools that read kernel.4's
PRIMITIVE lines (the converter's opcodes and escaped band, the evolver's folds)
keep their numbers; A/O moves to the shell, CHAR- goes. Every engine is SYSC by
default and the gene sysc retires; every shell loads forth/shell-sysc.4; the
shell suite runs at both widths; the jail test attacks through SYSCALL. The
first attempt lost REPOSITION-FILE - a pattern's \s matched a newline and ate
the next line, so ALLOCATE's token fell on a reserved slot and the dump
exited 70; now the list is checked position for position against master's.
Kernels: 25,152 bytes at 8-byte cells (25,640 at Iteration 125), 13,868 at 4.
The four checks at both widths: the shell suite 554 assertions on four SYSCALL
shells, the jail - one fork refused, one allowed, the bomb contained - 7 of 7;
20 front designs through the gate with the tab test right. The five patches
on a fresh clone of master give the tested tree, file for file.

## Iteration 148 - 2026-10-10 - Claude

**The next JIT stencil, priced: none.** On seed 37's fastest with jitloop and
jitinl, the JIT's own blocker log, each blocker weighted by the dispatches the
words it blocks execute: PLACE blocks 11% of bubble's remaining interpreted
work (197 k dispatches - ~2% of its time), SYS-ARGC 4% of the kernel
workload's (gone with the single-SYSCALL model); * blocks nothing - the guess
that RANDOM waited on it was wrong. What the corpus, kernel and parse
workloads still interpret (3.9 M, 1.7 M, 8.0 M dispatches) is the outer
interpreter - INTERPRET, the parse, FIND, NUMBER? - bytecode because the
interpreter loop is, not for a missing stencil. The k-genes and the batch's
kernel patches are what reach it.

**TABS>BL gone - the batch's sixth pending patch.** Dead since the parsing
patch, it still claimed a format-10 slot: 214 of seed 37's 242 front genomes
name it, and kinput put it first. Out of kinput, the evolver's lists and maps,
the engine and both generators, the converter's expected bodies and opbody's
list; an old genome naming it builds without it, the slot passing on. 20
front designs - 18 naming it - through the gate, the tab test right, none
built with it; the four checks at both widths. tools/sysc-xform.py retired with
it (its six engines done). The six patches, in order, on a fresh clone of
master give the tested tree's code exactly.

## Iteration 149 - 2026-10-10 - Claude

**SmithForth reviewed; the engine as it ships** (results/smithforth-review.md).
No licence - ideas only - and machine code that would not fit C engines. Its
lesson is the executable that is only its headers and its loaded bytes; ours
already were one RWE segment, but carried the section headers, their names and
.comment past the strip the size objective measures - 616-620 bytes in every
engine. tools/elf_tight.py drops them; build() returns the tight engine - it
is what runs, is gated, timed and measured - and keeps engine.full for
analysis. 20 front designs pass the gate and the tab test tight; the
four checks pass; the carry re-measures every carried design, so the change is
consistent within a run (sessions before and after the batch are not
comparable). The batch's seventh pending patch; the seven on a fresh clone of
master give the tested tree's code exactly.

## Iteration 150 - 2026-10-10 - Claude

**The size review of the kernel's long tail** (results/word-audit.md, batch
3). On the after-seed-39 batch: the smallest image's bytes are 62% word bodies
and 38% headers; the code no workload runs is 151 bytes (lean leaves the rest
out); the rarely-run words are already 20-60 bytes in a dense encoding. 21
words are named by no loadable source - headerless, ~150 bytes; half-width
thread entries ~128 - priced, not built (2% each, with converter work). The
batch itself: the smallest design 20,630 -> 17,610 bytes (-14.6%), the fastest
33,512 -> 29,976 (-10.6%), the same genomes. No code from the permissive
Forths taken: their compact words are primitives in C or assembler; ours are
already short colon definitions.

## Iteration 151 - 2026-10-10 - Claude

**Seed 38, processed: small** (results/evolve-amd-ryzen-7-pro-8840hs-seed38.md;
session 33 in results/compare-fronts-amd-ryzen-7-pro-8840hs.md). The first run
of the selection with bubble and ackermann: 21,395 designs, 20,396 alive, the
only deaths the reach limit's 999; 83 generations in 4 h 42 min; the chain 6 h
49 min (the comparison 1 h 47 - the longer workloads). Session 33 (seeds 33-38,
calibration 1.008): the front of all runs 88, 69 of them seed 38's; against
seed 37 the fastest is a tie (0.236 against 0.241 on cpu 2, seed 37 ahead on
cpu 8), the smallest 0.04% smaller, memory 4 KB less - small on all three. All
165 front designs as s6 on the Forth 2012 suite. The laptop's pack also carried
results-measured-here.patch: an old local difference in three stage-benchmark
tables (30 September), not this run's - left out. NEXT-RUN: seed 39, the same
genes and measurement; the batch after it.

## Iteration 152 - 2026-10-10 - Claude

**A run ends when it says** (the owner: the 6-hour run took ~7). The evolution
had stopped on time; what follows it - the front re-measured, the comparison
- was given a fixed 80 minutes, right until the longer workloads (Iteration
127): seed 38's took 126 (18 min 39 s and 1 h 47 min), the chain 6 h 49 min.
next-run.sh now records each later phase's duration in runs/phase-times (the
re-measure with its rounds, the comparison with its rounds and CPUs) and
reserves the last chain's, scaled to this one's rounds and CPUs, plus a tenth
and 10 minutes for the builds, checks and packing; seed 38's times until a
chain records its own; the evolution keeps at least 40% of the hours; the
plan is said at the start. Tested on the functions themselves, five cases,
against the arithmetic by hand. The trade-off it exposes: with the two-CPU
comparison of 6 rounds a 6-hour chain evolves ~3 h 32 min (seed 38: 4 h 42);
a comparison of 4 rounds on one CPU would leave ~4 h 44.

## Iteration 153 - 2026-10-10 - Claude

**Seed 39 runs 7 hours** (the owner asked which to choose). It is seed 38's pair:
the same genes and measurement, so the same evolution budget and the same
comparison too. With the reserve now honest, 6 hours would leave ~3 h 32 min of
evolution against seed 38's 4 h 42 - a weaker seed 39 could not be told from a
shorter one; a cheaper comparison would measure the very verdict the pair is
for less precisely, and one CPU would lose the cross-check that showed seed
38's speed a tie. 7 hours: ~4 h 32 min of evolution, the same comparison, the
chain ending at 7 hours as it says. The regular length is chosen after the
batch - 6 hours with a two-CPU comparison of 4 rounds would leave ~4 h 10.

## Iteration 154 - 2026-10-10 - Claude

**While seed 39 runs: the batch on seed 38's front, and predictions.** All 165
of seed 38's front designs rebuilt on the after-seed-39 batch: all alive, the
tab test right on all, 146 with new ids (TABS>BL left their operations), each
smaller by a median 3,148 bytes - the smallest 20,622 -> 17,594 (-14.7%). And
a finding: none of the 47 JIT designs carries jitloop or jitinl - dormant
through seed 38, the genes must be found by mutation after the batch, jitinl
two steps away for the 41 without jitx. results/predictions.md: what seed 39
and the first run after the batch should show, written before either.

## Iteration 155 - 2026-10-10 - Claude

**Founders for the JIT's new genes - the batch's eighth pending patch** (the
owner). Dormant through seed 38, jitloop and jitinl are in no genome, and
jitinl needs jitx too - two mutations from 41 of seed 38's 47 JIT front
designs. Two founders join the first generation of every run not from zero:
seed 37's fastest with both (its record read from results/ - recorded_genome;
left out, said so, if absent) - bubble's interpreted dispatches 13.29 M -> 197
k, ackermann's 12.69 M -> 15.6 k; and s6 with the JIT, jitx and both - a carrier
any tree can make (ackermann -99.4%; bubble unchanged: s6's loop words are
calls, not the operations jitloop translates). Both built as get() builds
them under --require tag2: the four genes expressed, the gate, the answers.
The eight patches on a fresh clone of master give the tested files.

## Iteration 156 - 2026-10-10 - Claude

**Every Forth definition audited - the batch's ninth pending patch** (the owner).
Every definition on a measured path read, with each word's dispatches and calls
measured on the batch; the rule: a change removes operations in every encoding
(call overhead is the genes' to remove). Built: INTERPRET checks the stack only
where it can have changed; CMOVE, CMOVE>, FILL by D+; 2SWAP, 2!, WORD,
SEARCH-WORDLIST's constants; SUPER-OP's first opcode first; cross.4's 8 * as
3 LSHIFT (the same kernels, byte for byte); the converter's expected bodies for
FILL and CMOVE; tests/core/audit.fth with a control. Kernel workload -6.2% on s6
and -38.8% on the JIT founder (the cross-compiler's loops now translated), the
corpus -2.6% and -2.7%. run-tests PASS, 7 of 7 IDENTICAL, the jail; all 165 of
seed 38's front designs and both founders alive on the nine patches. Open:
ABORT"'s run-time check, compiled at run time where abortif cannot reach it.
results/word-audit.md, Batch 4.

## Iteration 157 - 2026-10-10 - Claude

**ABORT" guarded where it is compiled - folded into the ninth pending patch.**
The audit's open question: abortif guards (ABORT") in the converter, which sees
only the kernel image; a program's ABORT" is compiled at run time, as a bare
call. ABORT" now compiles IF -1 (ABORT") "ccc" THEN - abortif's shape, and
kinput's ?STACK8's. Bubble's check on the JIT founder: 3,588 calls to (ABORT")
before, none after, its interpreted dispatches -12.6%; the kernel 64 bytes
larger at 8-byte cells (the audit's net: -104), the kernel workload +0.3%.
run-tests PASS, 7 of 7 IDENTICAL, the jail; all 165 of seed 38's front designs
and both founders alive, tabs and audit right. The whole audit on the JIT
founder: kernel workload -38.6%, bubble -13.3%, corpus -2.7%, sieve -6.6%.

## Iteration 158 - 2026-10-10 - Claude

**Code far from the image base: the gate and cv8's refusals - the batch's tenth
pending patch** (the owner: long addresses). tests/core/far.fth puts code and
data past 64 KB, then 8 MB more; tools/farcheck.py: every answer right, any
missing one refused out loud. All 165 of seed 38's front designs and both
founders: every answer. The ladder broke - crashed, hung, lost words, stopped
silently; cv8 now refuses (CALL, past 21 bits, DOES>8 out of its form's reach,
cv8b's links past 4 MB), so s1, s5, s6 and the s8 stages refuse where they
broke. Still broken, listed and shown in run-tests.sh: s4 (no far form in its
engine), s0, pack4, pack8, s7 (crash), s2, s3 (hang). The gate: alive() runs
far.fth on every evolved design; hand-made stages and --validate exempt.
run-tests PASS, 7 of 7 IDENTICAL, the jail; 167 of 167 alive through the gate.
results/far-addresses.md.

## Iteration 159 - 2026-10-10 - Claude

**Every stage answers far code or refuses it - folded into the tenth pending
patch** (the owner: proceed). s4: the converter writes CV8-VARCALL-V for every
cv8 design and CALL, refuses a far call without VARCALL; cpt16 (s2, s3):
CALL,, !CALL and DOES>16 refuse past one token; relf.c, pack4.c, pack8.c and
spn.c hold 16 MB, as vm-lab.c - s0, the pack stages and s7 then give every
answer. FAR_KNOWN empty. The seeds unchanged; run-tests PASS, 7 of 7
IDENTICAL, the jail; 167 of 167 alive. Open: ALLOT past an engine's memory.

## Iteration 160 - 2026-10-10 - Claude

**Engine coverage measured; the untested handlers given a test - the batch's
eleventh pending patch** (the owner: every execution path tested). gcov over
the whole suite on --coverage builds of every stage: READ-FILE, RESIZE run by
no test anywhere; FREE, ALLOCATE, WRITE-FILE, SYSCALL by none on most stages.
tests/core/paths.fth closes them on every stage at both widths (with a
control); lines run rose to 82-93%. What is left has a reason or is listed as
a gap (s6's locals, s1's near DODOES). The front's engines are not measured
yet: their copied stencils break under --coverage. tools/covsum.py,
results/coverage.md. The far workload for compare-fronts is written but held
back: its output did not match fib's on a first check.

## Iteration 161 - 2026-10-10 - Claude

**The remaining action items; the coverage patch merged into the tenth** (the
owner: proceed; use gdb on segfaults). The far benchmark verified (output fib's
but for the gap line's OK) and added to compare-fronts.py as a held-out
workload. The front's coverage measured with the copied stencils left
uninstrumented: jit.c 98-100%, vm.c 80-82%; WRITE-LINE run by none - paths.fth
writes a line. The dictionary full: gdb showed a byte store past memory; ALLOT
refuses past the data stack's room (S0), , and C, by DP +!; full.fth in
run-tests and the gate. far.fth now checks its gaps were taken - RelF had
refused one and run the rest near. run-tests PASS, 7 of 7 IDENTICAL, the jail;
167 of 167 alive. results/coverage.md, results/far-addresses.md.

## Iteration 162 - 2026-10-11 - Claude

**The tracer - the batch's eleventh pending patch** (the owner: a profiler in
the engine, with stack context). vm-lab.c at -DPROFILE=2: a shadow call stack
resynchronised by rp (returns need no hook), the first run of every
instruction recorded with its call path, the top three cells and the input
line, dispatches per call path as folded stacks. tools/vmtrace.py builds a
trace engine for any design, names what the input compiled through the
design's own dictionary, and reports coverage and contexts; its self-test is
in run-tests.sh. The profiler's 1 MB address mask removed. Measured engines
untouched (12 stage engines byte for byte); run-tests PASS, 7 of 7
IDENTICAL, the jail. First use, s6 under the suite: 73.4% of instructions,
?DO never, the cv8 compiler's own names never (dead copies?), NUMBER?'s
prefixes never. results/tracer.md.

## Iteration 163 - 2026-10-11 - Claude

**The tracer's second use; two genes measured** (the owner: a gene for call
offsets from the base or the call site; a hybrid stack/register design; the
remaining items). The standard suite runs by ans-check.py (a correction: I had
said it never ran): on s6 991 tests, four files of fourteen whole, the rest
stopping at words the kernel lacks - which also hides the tests of ?DO and
ABORT". Traced: s6 76.2 percent of instructions under the suite and
run-tests.sh's files. s6's never-run compiler words are copies --cv8-compiler
leaves behind: 26 words, 733 bytes of code. Measured for the genes: a one-bit
"base or call site" choice keeps every workload at 2.00-2.10 bytes per call
and takes far from 3.00 to 2.00; stack shuffles are 23-46 percent of the
smallest design's dispatches. results/tracer.md.

## Iterations 164-165 - 2026-10-11 - Claude

**164: the gene callrel - a draft outside the batch.** The owner: tag-2 calls
from the base, from the call site, or either by a bit; can 13 bits do? Measured:
the kernel images' calls cost +0 bytes at 13 bits from the base or either (the
images are under 8 KB), the call site alone +35 and +41. Built in the engine
(byte for byte the same at 0), the JIT, the converter (either: the base form,
the low bit 0) and the run-time compiler (the shortest form, none of 3 bytes
under t2wide - 140 of 165 front designs); base and either work on three kinds
of design, and the corpus compiled past a 4 MB ALLOT (the owner's trick) gives
the same output. Not in the batch: the run-time encoder adds ~400 bytes to
every tag-2 image, used or not - it goes to its own overlay first.
results/drafts/callrel.md.

**165: the standard words as an extension - the batch's twelfth pending
patch.** forth/coreext.4 and extend.4 load before each suite file: 991 tests
-> 1,194 on s6, no new failure. results/forth-standard-tests.md.

## Iteration 166 - 2026-10-11 - Claude

**s5 and s6 lean - the batch's thirteenth pending patch** (the owner: yes).
The gene lean's --drop-x8 and --drop-dumptool on the hand-made s5 and s6 (HUMAN
and build-stages.sh in step): s6's image 10,385 -> 8,761 bytes at 8-byte cells,
s5's 13,784 -> 12,104. And s6's dispatches fell - parse -5.0 percent, corpus
-2.2, kernel -0.9: the copies' entries lengthened the hash threads every lookup
walks. The SPN sources and the tracer named NAME>8, now dropped: NAME> instead.
run-tests PASS, 7 of 7 IDENTICAL, the jail, the standard suite unchanged, 167
alive; the thirteen patches on a fresh clone of master, reseeded, the same.
results/tracer.md, results/predictions.md.

## Iteration 167 - 2026-10-11 - Claude

**callrel packaged, still a draft; the standard's words and numbers - the
batch's twelfth (regenerated) and fourteenth pending patches.** CALL, reaches
callrel's encoder through a cell the converter writes; without the gene it is
left out (56 bytes, not ~400) - but 23 of 167 designs, those with images past
8 KB, do not convert with the gene on: the converter must place kernel calls
by distance first. coreext.4: waves two and three, a standard COMPARE; the
kernel's NUMBER? and INTERPRET as the standard reads numbers. The standard
suite on s6: 1,599 tests, 6 failed (CREATE-FILE). The fourteen patches on a
fresh clone, reseeded: run-tests PASS, 7 of 7 IDENTICAL, the jail, 167 alive.

## Iteration 168 - 2026-10-11 - Claude

**Seed 39 processed - small, the second in a row: the gene set has converged
under the selection with bubble and ackermann.** Session 34 (seeds 35-39,
calibration 0.996): seed 39's fastest 0.239 against seed 38's 0.237, smallest
and memory equal (20,622 bytes, 152 KB); 71 of the joint front's 119 designs
its, 39 seed 38's. 74 of the 119 are JIT designs, the fastest among them - the
prediction "fastest still not JIT" was wrong. The chain: 6 h 28 min of 7. The
held-out check: 0 of seed 39's 186 front designs differ from s6 on the Forth
2012 suite. results/evolve-amd-ryzen-7-pro-8840hs-seed39.md, session 34 in
results/compare-fronts-amd-ryzen-7-pro-8840hs.md, results/predictions.md.

**CREATE-FILE with R/W - the batch's fifteenth pending patch** (the owner:
respect the standard, tolerate the size). It was 1 AND OPEN-FILE: a file
created R/W could only be written. The engines' open-flags table takes two
more entries (create, read and write), CREATE-FILE maps R/W to them: the
standard suite on s6 1,599 tests, 0 failed.

## Iteration 169 - 2026-10-11 - Claude

**The after-seed-39 batch applied - fifteen patches; seed 40 runs 9 hours.**
On master in order (results/applied-after-seed39/), reseeded - the 8-byte
kernel a fixed point at 26,080 bytes, the 4-byte identical from either seed -
then the four checks: build, run-tests PASS, 7 of 7 IDENTICAL, the jail PASS.
Seed 39's 186 front designs, rebuilt on it: 186 alive. NEXT-RUN: seed 40 tag2
9h then the two-CPU comparison - the batch's first run, not comparable with
the runs before it. Predictions: results/predictions.md (Iterations 154, 166,
169).

## Iteration 170 - 2026-10-11 - Claude

**The standard's words, waves four to six - a draft: the held-out check says
not yet.** coreext.4 grew by CS-PICK SLITERAL M*/ RESIZE-FILE MARKER VALUE
2VALUE TO C" N>R UNESCAPE FILE-STATUS and others; on s6 the suite runs 1,817
tests, 4 failed (doubletest and searchordertest whole). Found: extend.4's
SET-ORDER with 0 ran down through memory; M*/ floors as this system's /; .(
is missing; RECURSE in :NONAME calls LAST's word - its fix crashes under the
runner only (results/drafts/recurse-noname.md). But over seed 39's 186 front
designs all 186 now differ from s6 - searchordertest on every one - so the
waves stay a draft (results/drafts/coreext-after-seed40-draft.patch) until
that difference is understood. Master's code is unchanged: seed 40 runs it.

## Iteration 171 - 2026-10-11 - Claude

**The standard's words ready, and the exception wordset in the kernel - the
after-seed-40 batch's first two pending patches.** The 186 differences were
ORDER printing addresses (names now) and :NONAME's bare-HERE xt, wrong for a
tag-2 design's COMPILE, (now the design's own :, which mends RECURSE in
:NONAME too). The kernel: CATCH and THROW (input source restored), ABORT and
ABORT" through THROW, -13 for an undefined word under a CATCH, every message
as before without one. s6: 1,821 standard tests, 0 failed (exceptiontest
whole); the checks; seed 39's 186 designs alive and none differing from s6.
Master's code unchanged - seed 40 runs it.

## Iteration 172 - 2026-10-11 - Claude

**The hybrid stack/register design, priced again - and a measurement bug.**
The owner's request of Iteration 163 had stopped at measuring the shuffles.
Priced now on every executed dispatch, run-time code included: moves are
17-27% of the dispatches of s6, the fastest and the smallest alike; a move
feeding the next operation is 4-12% on the image-heavy workloads, little on
fib, loop and bubble - whose moves feed literals first, which only triples
see. regprice.py names opcodes wrongly on today's designs (its order of
primitives has moved); the converter's CALLMAP names are right and now used.
results/price-hybrid.md: the plan - triples, then the gene, in the run-time
compiler too.

## Iteration 173 - 2026-10-11 - Claude

**Seed 40 processed - the batch's first run, not small: the JIT genes halve
the time.** Session 35 (seeds 36-40, calibration 0.988): fastest 0.187
(d9247d19b0: jit, jitloop, jitinl) against 0.280; bubble at 24% of the best
carried design's ratio, ackermann 58%; smallest 17,762 bytes (nolibc and the
tight ELF: ~2.9 KB off every design), memory level. 89 of the joint front's
97 designs are seed 40's. Every prediction right, the image growth only
roughly (~170 bytes). The held-out check: 0 of 218 differ from s6. The five
corpus deaths reproduced: the gene opcall (results/opcall-deaths.md). The
hybrid priced with triples: 14-15% of the selection's dispatches on the
interpreted designs, 5% on the fastest - built next, for them
(results/price-hybrid.md).

## Iteration 174 - 2026-10-11 - Claude

**The after-seed-40 batch applied - seed 41 runs 9 hours.** coreext (the
standard's words), exceptions (CATCH and THROW in the kernel; ABORT and ABORT"
through them), triples (the profiler; profiling builds only) - results/
applied-after-seed40/. Reseeded (26,904 bytes), run-tests PASS, 7 of 7
IDENTICAL, the jail; seed 40's 218 front designs alive on it; held-out: 0 of 218 designs differ from s6 somewhere.

## Iteration 175 - 2026-10-11 - Claude

**The hybrid's first step: rtimm=2 - run-time immediates without pairs.**
Before building new opcodes, the counterfactual: seed 40's smallest already
carried rtimm, unexpressed behind the pair overlay, rtfuse and pairs it has no
slots for. rtimm=2 gives it the immediates overlay alone: +662 bytes, fib
-13.6% of its dispatches, the compile-heavy workloads +0.4-1.1%. All 218 of
seed 40's front designs alive with it; the held-out check clean on the two
checked. Pending after seed 41: results/pending/rtimm2-after-seed41.patch.
Next on it: the forms the price asks for - `-` and `<` immediates, DUP n <.

## Iteration 176 - 2026-10-11 - Claude

**The hybrid's keeping forms: fib -36.3%, the price met.** DUP+I and DUP<I in
every layer (engine, both generators, converter, JIT steps, run-time fusion),
pinned to one-byte codes where the run-time immediates' table is - escaped,
they did nothing (found by probing what the run-time compiler wrote). On seed
40's smallest with rtimm=2: fib 59.27 M -> 37.74 M dispatches for +726 bytes;
218 of 218 front designs alive with them; the held-out check clean on the two
ans-check took (it keeps its database's front - the rest to check). Pending
after seed 41, after rtimm2: results/pending/keepforms-after-seed41.patch.

## Iteration 177 - 2026-10-11 - Claude

**Seed 41 runs 6 hours, not 9** (the owner). NEXT-RUN changed; the command
with the plan given explicitly does the same with any bundle.

## Iteration 178 - 2026-10-11 - Claude

**The keeping forms checked by the suite; a founder; regprice fixed; opcall's
two bugs located.** Eight front designs with rtimm=2 and the forms (six
interpreted): 14 of 14 standard files as s6. Pending after seed 41, in order:
rtimm2, keepforms, founder, regprice-names - the four reproduce the tested
tree on a fresh clone. The five wrong corpora are two bugs: run-time pair
fusion under the escape with DROP;CALL, and the JIT with 1+;CALL
(results/opcall-deaths.md). Next: those, then the return stack - the
hybrid's tail (41% of loop's image dispatches).

## Iteration 179 - 2026-10-11 - Claude

**opcall's two bugs narrowed; the loops looked at.** Bug 1 needs one pair,
`DUP C@`, fused at run time with DROP;CALL under escape 2 - four mechanisms
excluded. Bug 2 needs the tiny specialisation: 1+;CALL copies L_onep, which
tiny's 1+ may not be. The fastest's loop: I then + a fifth of its dispatches
(I+ exists, behind three genes); the smallest's: NOOPs executed, 8.4%. No
patch this time: findings, results/opcall-deaths.md, results/price-hybrid.md.

**Corrected (Iteration 179):** bug 2's "tiny" is no clue - tiny makes 1+ an
opcode; without it 1+ is never fused, so tiny off is opcall off. What is left:
1+;CALL with the JIT, t2wide and tos.

## Iteration 180 - 2026-10-11 - Claude

**opcall's wrong answers contained.** Both "bugs" are one pattern: every
X;CALL of the five dead designs had its code outside the base one-byte band
(escaped, or t2wide's 0x80-0xBF), and each gene that fixed one moved it in. The
converter now writes X;CALL only in the base band: all five right, all 48 of
seed 40's opcall front designs alive. The mechanism outside the band is still
unexplained - a containment, recorded as such. Pending after seed 41, fifth:
results/pending/opcall-band-after-seed41.patch.

**And the loops' padding (Iteration 180):** LOOP8's NOOPs sit inside the loop
body - every iteration, not "once per loop" as the comment has it: 8.4% of the
smallest's dispatches on loop. Next: price a wider call or an unaligned-safe
operand read (results/price-hybrid.md).

## Iteration 181 - 2026-10-11 - Claude

**The loops' padding removed where it runs; the standard's seventh wave.**
Priced: executed NOOPs 8.0-8.3% of loop's dispatches on interpreted designs
without a run-time loop compiler (27 of seed 40's front). cv8t.4 no longer pads
loop operands in a design without the JIT ((LOOP) reads them unaligned): the
smallest's loop -8.3% of dispatches, bubble -3.4%, sieve -6.9%; 218 of 218
alive; the suite on six interpreted designs as s6. The seventh wave - SYNONYM,
INCLUDE, REQUIRED, REQUIRE, SAVE-INPUT, RESTORE-INPUT - and two case faults of
the test conversion (file names, PARSE-NAME's token): s6 1,862 tests, 0
failed. Pending after seed 41, sixth and seventh: loopalign, coreext-w7.

**The whole batch, held out (Iteration 181):** all seven pending patches on seed 40's 218 front designs - 0 of 218 designs differ from s6 somewhere.

## Iteration 182 - 2026-10-11 - Claude

**The standard's eighth wave: s6 1,988 tests, 1 failed; stringtest whole.**
DEFER and its words, S\", REPLACES, SUBSTITUTE, HOLDS, two transient buffers
for S" - and my CHAR-AT's R@ inside a DO loop, found by the suite. Pending
after seed 41, eighth: coreext-w8. callrel's draft no longer applies (the
batches since changed evolve.py and layout.py): rebase first, then the
converter's placement by distance - its own session.

**Held out with the eighth wave (Iteration 182):** all eight pending patches on seed 40's 218 front designs - 0 of 218 designs differ from s6 somewhere.
