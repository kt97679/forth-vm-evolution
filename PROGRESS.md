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
