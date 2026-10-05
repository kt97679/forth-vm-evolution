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
