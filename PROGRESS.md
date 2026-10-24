# Progress log

Append-only: one entry per session, newest last. A wrong entry is
corrected by a later one that says so, not edited (prompts/12-progress-log).
History before this log: the git log, `FINDINGS-*.md`, `lab/*/README.md`.

**A new chat starts at the HANDOFF entry at the end of this file (Iteration 213):
the state, the routine, the owner's standing decisions, the open items.**

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
gene.** NAME>BUF waits as results/applied-after-seed39/namebuf-after-seed39.patch (it
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
checked. Pending after seed 41: results/applied-after-seed41/rtimm2-after-seed41.patch.
Next on it: the forms the price asks for - `-` and `<` immediates, DUP n <.

## Iteration 176 - 2026-10-11 - Claude

**The hybrid's keeping forms: fib -36.3%, the price met.** DUP+I and DUP<I in
every layer (engine, both generators, converter, JIT steps, run-time fusion),
pinned to one-byte codes where the run-time immediates' table is - escaped,
they did nothing (found by probing what the run-time compiler wrote). On seed
40's smallest with rtimm=2: fib 59.27 M -> 37.74 M dispatches for +726 bytes;
218 of 218 front designs alive with them; the held-out check clean on the two
ans-check took (it keeps its database's front - the rest to check). Pending
after seed 41, after rtimm2: results/applied-after-seed41/keepforms-after-seed41.patch.

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
results/applied-after-seed41/opcall-band-after-seed41.patch.

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

## Iteration 183 - 2026-10-11 - Claude

**The stacks' place (the owner's question): a gene, dskew.** The stacks
already sit 16 MB from the dictionary in the same block; a separate block
would change neither speed nor memory and would need the kernel's dictionary
limit moved. What placement can change is 4K aliasing between the two stacks'
top cells - they share page offsets whenever the return stack is one cell
deeper. On the VM an A/B is lost in noise (rounds differ by 9%); the gene
dskew (data stack 2 KB lower) lets the laptop judge. Every recorded id kept;
validate's KeyError on hand-made genomes found and fixed. Pending after seed
41, ninth: dskew. results/stack-placement.md.

**coreexttest whole (Iteration 183):** its "X32X32" was the test conversion
ending an S\" string at an escaped quote; it steps over escapes now - 383
tests, 0 failed. s6 1,989 tests, 1 failed; ten of fourteen files whole. Ten
patches pending after seed 41, held out clean on seed 40's 218 designs.

## Iteration 184 - 2026-10-11 - Claude

**The stacks apart, the dictionary growable (the owner).** The stacks in a
chunk of their own; the dictionary in a 256 MB reservation that never moves -
addresses are absolute everywhere, so growth must be in place, not a realloc.
Three faults found by the checks: s1-s3's encodings crashed apart (they keep
the old layout); ALLOT's HERE + n wrapped in a 32-bit process placed high (n
against the room left now); and that unsigned compare refused negative ALLOT
(35 designs wrong, fixed). All 218 front designs alive; evolved designs grow
past 16 MB and run code there. Pending after seed 41, eleventh: stacksep.

**Held out with the stacks apart (Iteration 184):** all eleven pending patches on seed 40's 218 front designs - 0 of 218 designs differ from s6 somewhere.

## Iteration 185 - 2026-10-11 - Claude

**callrel rebased; its drift found and fixed; the next blocker named.**
The draft rebased onto the eleven pending patches (two evolve.py conflicts,
both sides kept). The drift: tag-2 calls are sized 2 bytes before any offset
exists and re-encoded at emission against the true one - at 13 bits, longer
past 8 KB. Hybrid calls are now sized from an upper bound of their target's
offset, the same at both passes, emitted at that length. Next: the short-branch
pass still assumes 2-byte calls ("short branch out of range" on part of the
front). Still a draft: results/drafts/callrel-draft-rebased.patch.

## Iteration 186 - 2026-10-11 - Claude

**callrel: the short branches explained - it needs a real fixed point.** The
branch-shortening pass sizes with non-tag-2 sizes (it runs before the tag-2
map exists); and Iteration 185's bound, measured from the 27 KB cell dump,
sizes nearly every call long - correct, and larger than base mode. The fix is
a layout rerun to a fixed point: its own session (results/drafts/callrel.md).

**And the standard (Iteration 186):** the block word set (two buffers over
blocks.fb) and TRAVERSE-WORDLIST with the name tokens (on the byte headers'
NEXT-NFA8): blocktest and toolstest whole - s6 2,068 tests, 1 failed; twelve
of fourteen files whole. Pending after seed 41, twelfth: coreext-w9.

**Held out with the twelve (Iteration 186):** seed 40's 218 front designs - 0 of 218 designs differ from s6 somewhere.

**The return stack, priced (Iteration 186):** 31.8% of loop's dispatches on
the founder configuration - the colon-word loop runtime. And rtloop, one
mutation from it, is inert there: +582 bytes, not one dispatch saved - a
run-time DO LOOP still compiles calls to (DO), I and (LOOP). Next first: why
(results/price-hybrid.md).

## Iteration 187 - 2026-10-11 - Claude

**Corrected: rtloop works - my test of it ran on the founder, which had lost
the loop opcodes.** Two keeping forms first among format-10 names pushed I and
(LOOP) out of the smallest's 10 slots; measured against four other choices, it
is still the founder's best (kernel +0.9%, corpus +1.9%). rtloop on the
recorded smallest: +568 bytes, loop -77% of dispatches, bubble -13.5%, sieve
-27.7% - the size end declines it, as the front intends. Next worth pricing: a
cheaper rtloop.

**A cheaper rtloop, priced (Iteration 187):** of its 568 bytes, ~160 are
headers of overlay-internal words nothing reads at run time - dropping them
would serve every overlay - and ~50-100 the lookup and leave-chain machinery:
roughly 320-370 left. The next build for the small end.

## Iteration 188 - 2026-10-11 - Claude

**Weighing the objectives (the owner).** Selection keeps the good trade-offs -
seed 40's small end has designs 1-2% larger and 23-29% faster, Q 0.62-0.63 of
the smallest's. The judging could miss them: the stopping rule sees only the
extremes. On sessions 34-35 hypervolume and best Q agree with it (seed 39 small
by all, seed 40 big by all), but nothing guarded. And I had anchored on the
extremes - the founder built on the smallest, the worst Q of its neighbourhood.
Proposed: the rule to include hypervolume and best Q; reports to name the Q-best
design; founders from the knee. results/weighing.md - the owner decides.

## Iteration 189 - 2026-10-11 - Claude

**Selection: demote, don't delete (the owner).** The thirteenth after-seed-41
patch (weighing-after-seed41.patch): demoted designs carrying gene values no
survivor has kept in an attic (128), one parent in ten and borrowed genes from
there; the 8 best by Q always survive; compare-fronts.py judges a run by five
measures (the extremes, hypervolume, best Q) and names the Q-best design; the
founder from the small end's knee (d99e3d9ed9, JIT; alive, 0.980 of s6). A
scratch run: the attic held 42 lost gene values by generation 4, its children
alive and among the notable. run-tests PASS. results/weighing.md.

## Iteration 190 - 2026-10-11 - Claude

**The cheaper rtloop: rtloop=2.** The converter learned headerless words
(tools/layout.py --headerless: code kept, header dropped, on no chain; a name
defined once only); rtloop=2 builds cv8-fuse-loop.4's eight internal words that
way. 96-108 bytes a design: rtloop costs +460 bytes on seed 40's smallest
instead of +568, for -72% loop time. 128 of seed 40's recorded designs carry
rtloop=1; ten rebuilt with rtloop=2, all alive. A fib/bubble slowdown seen with
rtloop on the knee founder was noise - probes show the forms compile the same
with and without the loop overlay. run-tests PASS. The fourteenth after-seed-41
patch: rtloop2-after-seed41.patch. results/drafts/rtloop-cheaper.md.

## Iteration 191 - 2026-10-11 - Claude

**opcall's root cause found and fixed.** Padding between an X;CALL and its
call: a call taking an inline operand ((LOOP), (POSTPONE)) is padded in front
so its operand is aligned, and CALLNEXT read the first padding byte as the
call - a call to the image's start. Bisected to one DROP;CALL in SUPER-OP, its
bytes read. One cause for all five of seed 40's wrong corpora; the base band
was a coincidence. Fix: no X;CALL before such a call; the base-band containment
removed - every band open. 30 of 30 opcall designs alive (seed 40's front 25,
the five dead), run-tests PASS. The fifteenth after-seed-41 patch:
opcall-fix-after-seed41.patch (supersedes the fifth's containment).

## Iteration 192 - 2026-10-11 - Claude

**filetest whole.** Its stop at SI_INC was the harness: SI_INC, SI1 and S$ come
from coreexttest, which upstream runs first in the same session; ans-check.py
now defines them before filetest. And RESTORE-INPUT now returns to a file's
earlier line: SAVE-INPUT records where the line starts (verified by reading it
again), RESTORE-INPUT repositions and reads it again - coreext.4 only. On s6:
2,069 tests, 0 failed; thirteen of fourteen files whole (localstest waits on
the owner's decision on a kernel hook). 0 of 12 front designs differ from s6.
The sixteenth after-seed-41 patch: coreext-w10-after-seed41.patch.

Also: results/applied-after-seed57/ORDER.md - the sixteen patches' order and the checks
after; the callrel draft rebased onto them (results/drafts/
callrel-draft-rebased16.patch), its fixed point planned as two converter runs
(results/drafts/callrel.md).

## Iteration 193 - 2026-10-11 - Claude

**callrel: the fixed point built, the gene measured - not worth it.** Calls
sized from the pass before (two converter runs or more; the short branches
sized as emission sizes them): every design alive with the gene. On four of
seed 40's designs callrel=2 is worse on all: +300-400 bytes of image, +400-800
in all, interpreted designs 10-17% slower (a flag tested on every call). Kept
as a draft (results/drafts/callrel-draft-twopass.patch), not in the batch.
**Found on the way:** the batch carries no binaries - after applying it, the
reseed must come first, or every stage is built from the old kernel (every
tag-2 design died "dictionary full" on a fresh clone). results/applied-after-seed57/ORDER.md
corrected: reseed (27,120 bytes, as tested), then the build and the checks.

**Locals need no kernel hook.** The kernel's FIND walks the search order, so a
wordlist of local names, first in the order while a definition compiles, is
found by the ordinary interpreter; the names' headers go into a scratch area
(HERE, LAST, CURRENT saved and restored). Prototyped on a built tag-2 design:
a local made mid-definition compiles, is gone after the scope, the dictionary
intact. The owner's decision is not needed: coreext.4 only, like every wave.
results/drafts/locals-plan.md - the next turn's work.

## Iteration 194 - 2026-10-11 - Claude

**The standard suite whole: 2,119 tests, 0 failed, fourteen of fourteen files.**
The locals word set in coreext.4 - no kernel hook (Iteration 193's finding): a
wordlist of the definition's local names, first in the search order while it
compiles, headers in a scratch area; values on a stack of their own; {:
(LOCAL) TO, ; DOES> EXIT ending the scope; ENVIRONMENT? (#LOCALS) and .S.
localstest 50 tests, 0 failed. 0 of 12 front designs differ from s6. The
seventeenth after-seed-41 patch: coreext-w11-after-seed41.patch (ORDER.md).

**regprice.py rerun** on s6 and four of seed 40's designs (results/price-
hybrid.md): the register stage would remove 20-26% of the image's dispatches
on the interpreted smallest (corpus, parse), 7-12% on the JIT designs; the
largest patterns there (DUP before ?BRANCH, OVER before C@) are the next
keeping-form candidates. Every action item of the list is now done or
measured; what stays open is for the owner (callrel's two-decoder variant)
and the laptop (dskew, seed 41).

## Iteration 195 - 2026-10-11 - Claude

**The GP process, a deep dive (the owner): results/gp-deep-dive.md.** Our data
first (seed 40's database): mutation-only children made 73% of the final front
from a quarter of the children - crossover, 60% of variation, is 12 times less
productive per child; varcall and doesfar never help (3.5% of evaluations);
the JIT genes, tos-msc and escape-rtloopall are linked on the front but split
by crossover; corpus, parse and kernel correlate 0.90-0.99 (three votes for
one behaviour); noise +-2.6% (5-95%). Literature weighed against it: operator
bandits (OpenTuner), learned linkage (GOMEA), surrogates, age (AFPO/ALPS),
racing (irace), lexicase, islands (FunSearch/AlphaEvolve); new genes from
deep-parameter sweeps (fbuf is one), instruction replication, PGO, two stack
registers. Proposed for seed 42: crossover 0.25, the learned blocks, the dead
genes slowed, speed ties within 2% - the owner decides.

## Iteration 196 - 2026-10-11 - Claude

**Other Forths surveyed (the owner): results/forth-implementations-survey.md.**
Much is ours already (superinstructions, TOS register, tail calls, stencil JIT,
thinned headers, sized operands - Nga's bundles and zForth's variable cells
included). New, ranked: pinned VM registers (Gforth's build tuning - our engine
pins none); primitives demoted to Forth (sectorforth's eight primitives; the
interpreter function is 10.7 of a JIT design's 21.1 KB, and no gene moves
primitives out of C); packed names (colorForth); run-time folding of literal
expressions (Mecrisp); single-use words inlined in the image (Mecrisp-Across);
optimal superinstruction choice (Gforth - ours is greedy); stack caching for
the hottest primitives only (Gforth's peeprules); tail-call threading (Clang
19+ only).

## Iteration 197 - 2026-10-11 - Claude

**The GP process changes and regpin built** - the 18th and 19th after-seed-41
patches. Process (for seed 42 against seed 41): crossover 0.25; the genes
linked on seed 40's front inherited whole (crossover was uniform gene by gene,
splitting them); varcall/doesfar drawn one time in ten; speed within 2% a tie
in the ranking, fronts guarded against non-transitive cycles. regpin: VM
registers pinned, three assignments - on this VM bigger and no faster except
the fastest JIT design (160-320 bytes smaller, equal speed); the laptop
decides. Run-time folding not built: one constant expression in all the
benchmarks. run-tests PASS; hand-made stages identical; nineteen patches apply
in order (ORDER.md).

**The surrogate, tested offline** (results/drafts/surrogate-offline.md): random
forests on the genes, trained on seed 40's first half, predict the second
half's speed within 3.1% (median) and size within 0.74%. Replayed as a screen
against the front of what was measured before: skipping children predicted 30%
slower and 5% bigger skips 34% of them and loses none of the final front's 163;
20%/2% skips 58% and loses 6 (random skipping: 95). Proposed: built into the
evolver, conservative at first - the owner decides, and on the dependency.

## Iteration 198 - 2026-10-11 - Claude

**Seed 41 processed - small.** 18,213 designs in 6 hours (14:45-18:50, session
36 by 20:54). By the five measures against seeds 37-40: fastest +1.6%
(9e2a6f1307 0.183), smallest +0.00% (f0aeaeb237, 17,938), memory -4 KB,
hypervolume +1.2%, best Q -0.2%. The run's own fastest (28677d13b1, 0.174) was
0.185 in the session - the winner's curse. Deaths: 858 reach limit, 37 short
branch out of range (new: the converter sizes branches before the tag-2 map;
all tag-2 with hotcalls - a targeted fix is next), 12 corpus (all opcall 1+,
fixed in the batch). Predictions: four of five, the fifth half
(results/predictions.md); seed 42's written.

**The after-seed-41 batch applied to master** - nineteen patches in order
(results/applied-after-seed41/ORDER.md), the run's measured results first:
the reseed's fixed point at 27,120 bytes (identical to the tested seed), the
stages rebuilt, the hand-made stages 7 of 7 IDENTICAL, run-tests PASS, every
front design alive (126: seed 41's 75 and the joint front - two from seed 39's
database), the held-out check 0 of 12 of seed 41's front differing from s6
(2,119 tests, the suite whole). NEXT-RUN: seed 42, 6 hours - the process
changes against seed 41 on equal time.

## Iterations 199-202 - 2026-10-11 - Claude

**Seed 41's 37 converter deaths fixed.** The converter decides which
branches can be short before the tag-2 map exists (escaped opcodes 1 byte,
calls 2), and a loop body near 128 bytes encoded a few bytes past reach
(-131 to -135). Now the encoding records each such branch (word, cell offset -
stable from shorten() to the encoding: only opcall_rewrite comes between, one
token for one), layout.py writes them (--long-branches) and exits 4, and
evolve.py converts again with them kept long. All 37 of seed 41's dead genomes
alive with the batch's code; the smallest's and the knee's images byte for
byte as before; 7 of 7 stages identical; run-tests PASS. The first
after-seed-42 patch (results/applied-after-seed42/shortbranch-after-seed42.patch).

**The surrogate without scikit-learn** (results/drafts/surrogate-offline.md):
a pure-Python additive model (22 s to fit) predicts speed within 8.2% and size
within 1.2% (the forest: 3.1%, 0.74%), and at the conservative 30%/5% screen
skips the same third of children, losing 1 of 163 front designs (the forest
none); at 20%/2% it is overconfident (46 lost) - it cannot see gene
interactions. Parents predict poorly (25.7%): a child is not like its parents.
The choice is the owner's: the forest with scikit-learn, or the additive model
at the conservative margins only. (Iteration 200, the second after-seed-42
patch: the additive model's screen, at 30%/5%, one child in ten audited -
results/applied-after-seed42/screen-after-seed42.patch. Iteration 201 had no
commit of its own; this entry, re-headed at Iteration 366, covers 199-202.)

**The gene fsys built** - the third after-seed-42 patch. Six file words and
RESIZE in Forth over SYSCALL in an -fsys dump, their seven handlers out of the
engine. Without the gene, designs byte for byte as before (engine and image,
three designs); with it, the smallest 104 bytes smaller in all (engine -608,
image +504), the fastest 328, the standard suite 14 of 14 as s6 on all three.
Two faults found: the dump-making system has no NIP or TUCK (the library had
stopped after READ-FILE), and my first check of the kernel's uses had hidden
every line with a stack comment.

## Iteration 203 - 2026-10-11 - Claude

**The loop audit (the owner): results/loop-audit.md.** 42 of the image's 276
colon definitions loop, 16 never run. Profiled per word on the smallest
design: the name lookup (NEXT-NFA8, SEARCH-WORDLIST, NAME=?) is ~60% of
corpus and parse, 22% of the kernel; the loop runtime dominates loop, bubble
and sieve; FILL 15% of sieve. Most already have a gene that moves them into C.
Two assumptions refuted on the way (thinhdr is not one chain; FIND skips the
duplicate FORTH). NAME=? a cell at a time tried and measured - no gain (most
compares end at the first character), reverted. What would cut the lookup:
fewer entries a lookup - more chains as a gene, or a lookup cache.

## Iteration 204 - 2026-10-12 - Claude

**The gene threads** - the fourth after-seed-42 patch. The loop audit's
lever: the converter files the dictionary into 16, 32, 64 or 128 chains (32 as
built: byte-identical). Counted on the smallest: 64 chains cut corpus 28%,
parse 27%, kernel 9% for ~240 bytes; 128 chains 41%, 43%, 14% for ~700; 16
save 128 bytes and cost +49%. The suite whole at every count; run-tests PASS.
And the single-SYSCALL family designed with the owner
(results/drafts/fsys/single-syscall.md): fsys 2 - every I/O word over SYSCALL,
the kernel's compiled uses rebound by the converter, WRITE's buffer on the
heap - beside fsys 0 (all native) for evolution to weigh.

## Iteration 205 - 2026-10-12 - Claude

**The single-SYSCALL family, stage A** - the fifth after-seed-42 patch. fsys
2: OPEN-FILE, CLOSE-FILE, WRITE-FILE, ALLOCATE and FREE in Forth over SYSCALL
too; the converter rebinds the kernel's compiled uses (INCLUDED, SAVE-SYSTEM)
to them, so their handlers - and the C allocator - leave the engine. The
smallest 628 bytes smaller in all (fsys 1: 104), the fastest 1,039; the full
gate and the standard suite whole. fsys 0 byte-identical. Patch 5 regenerated
once: it had carried patch 4's hunks (patch 4 never committed in the working
tree). Stage B next: WRITE on a heap buffer, READ, READ-LINE, BYE.

## Iteration 206 - 2026-10-12 - Claude

**The single-SYSCALL family, stage B** - the sixth after-seed-42 patch. fsys
3: WRITE, READ, READ-LINE and BYE in Forth over SYSCALL, as the owner set it -
no output buffer, no read-ahead from what cannot seek; the engine's I/O is
SYSCALL alone. The smallest 1,217 bytes smaller in all, the fastest 1,921; the
I/O workloads slower (kernel +37-89%, corpus +23-88% - the unbuffered output
and three calls a line), fib and bubble not; the standard suite whole. A
fault found by instrumenting L_nosys: TYPE (`WRITE ;`) looked like a primitive
stub and kept the dropped opcode - stub-shaped colon words are rebound now.

## Iteration 207 - 2026-10-12 - Claude

**fsys 4: the output buffered, and tests that it breaks nothing** - the seventh
after-seed-42 patch. Gforth's rule (the standard leaves it open): no input
buffering, no output buffering to a terminal, buffering to a pipe or file -
WRITE asks once (ioctl TCGETS); its 4 KB heap buffer is registered with the
engine, whose t_flush empties it at every native flush point.
lab/evolve/outbuf-check.py against native: ten programs on one pipe with
stderr byte for byte (a SIGFPE death where native loses output 3 and 4 keep),
the prompt before a blocking read, a terminal shown at once (native holds it).
Speed about fsys 3: the workloads' I/O cost is READ-LINE's line scan (FS-LF,
1.9M dispatches of the corpus) and calls a line - the next step.

## Iteration 208 - 2026-10-12 - Claude

**READ-LINE at fsys 3 and 4 faster** - the eighth after-seed-42 patch: the
line's end by SCAN (native under kinput), whether a file can seek remembered
per descriptor (OPEN-FILE and CLOSE-FILE forget). The fastest design (kinput)
went from 27% to 16% slower than fsys 2; designs without kinput gain the
system call only. The standard suite whole at both levels, outbuf-check.py
PASS, run-tests PASS. Read-ahead on seekable files - allowed by the owner's
rule - is what would close the rest.

## Iteration 209 - 2026-10-12 - Claude

**Seed 42 processed - not small.** 15,352 designs in about 5 hours (21:15-
02:21 with session 37). The comparison judged itself by the five measures
for the first time: fastest -7.0%, smallest +0.18%, memory +6 KB, hypervolume
+4.8%, best Q +0.5% - not small; by the extremes alone it would have been
small. The Q-best of all runs is seed 42's 9a3de58ebe (0.211 at 26,472 bytes).
111 deaths (seed 41: 907), none on the corpus. Predictions: five of seven
(results/predictions.md); seed 43's written.

**The after-seed-42 batch applied to master** - eight patches
(results/applied-after-seed42/ORDER.md), no reseed (kernel.4 untouched); the
laptop's results patch was the same stash as seed 41's, on master already.
Stages rebuilt, 7 of 7 identical, run-tests PASS, every front design alive
(101: seed 42's 59 and the joint front's 89), 0 of 12 of seed 42's front
differing from s6 (2,119 tests). NEXT-RUN: seed 43, 6 hours.

## Iteration 210 - 2026-10-12 - Claude

**Seed 43 for 9 hours (the owner)** - NEXT-RUN `seed 43 tag2 9h then experiment
compare-fronts.py --rounds 6 --frontier --cpus 2,8`; the hours include the
re-measure and the comparison, as for seed 40. Seed 43's prediction about the
screen now per hour (seed 42: ~3,000 designs an hour).

## Iteration 211 - 2026-10-12 - Claude

**fsys 5 - read-ahead where a file can seek - and a converter fault found.**
The after-seed-43 batch begun (results/applied-after-seed57/ORDER.md). fsys 5: READ-LINE
reads 4 KB ahead on seekable descriptors (never stdin or pipes), given back
before every other use; measured between fsys 4 and native. On the way, two
faults: file-sysc5.4 did not load (remarks outside comments) and the gate hid
it; and --rebind took the OLDEST redefinition, so fsys 4's buffered WRITE was
never bound since Iteration 207 - seed 43 runs with that (its fsys 4 is fsys
3 with dead bytes). Fixed; outbuf-check.py now tests real buffering and
passes; the standard suite whole at fsys 4 and 5; run-tests PASS.

## Iteration 212 - 2026-10-12 - Claude

**The dump guard (the owner)** - the third after-seed-43 patch. Each dump is
checked as setup makes it: no load error among its messages, every name each
loaded file defines present, and each present as often as the bare kernel
and the loaded files define it - the count catches a failed redefinition an
older definition hides (fsys 5's READ-LINE behind fsys 3's). Tested both ways:
the original remark stops the run (FS-FILL, FS-TAKE missing); READ-LINE alone
broken stops it (READ-LINE 2 of 3). All 2,666 dumps pass; 7 of 7 stages.

## Iteration 213 - 2026-10-12 - Claude: HANDOFF - start here in a new chat

Read this entry whole, then `prompts/` (the project's conventions), then the
entries it points to. Everything needed is in the repository; nothing from
earlier chats or uploads is needed - the owner's Forth collection (forth.tgz)
is kept in `reference/forth-archive/` (README there), the packs' results are in
`results/`. Earlier chats' transcripts will not be there: this log and
`results/` are the record.

### What this is

An evolutionary search over the design of a Forth system: the engine
(`engine/vm-lab.c`, computed-goto C), the kernel (`forth/kernel.4`, cross-
compiled by `forth/cross.4` in the cell system), the converter (`tools/layout.py`
with `tools/sod16.py`: the cell-threaded dump into the byte-coded CV8 / tag-2
image), and the evolver (`lab/evolve/evolve.py`: NSGA-II over genes; three
objectives - speed: the geometric mean of median cpu time over the selection
workloads against the hand-made s6; size: engine plus image bytes; memory:
rss). The owner, Kirill Timofeev, runs the seeds on his laptop (AMD Ryzen 7 PRO
8840HS, "fury") per `lab/evolve/NEXT-RUN` and sends back two packs: the run
(`forth-vm-evolution-seedN-<commit>-fury-<time>_tar.gz`) and the comparison
(`...-compare-fronts-...`). Commits are authored `Kirill Timofeev
<kt97679@gmail.com>`; deliveries are git bundles (`sh tools/make-bundle.sh
/mnt/user-data/outputs`, then present the file).

### The state now

- master: Iteration 213 (this entry). The after-seed-42 batch is applied
  (Iteration 209: `results/applied-after-seed42/ORDER.md`).
- Seed 43 is RUNNING on the laptop (started 2026-10-12 ~03:00, 9 hours - the
  owner's choice - including the re-measure and the comparison), at Iteration
  210's commit: `seed 43 tag2 9h then experiment compare-fronts.py --rounds 6
  --frontier --cpus 2,8`. Its predictions: `results/predictions.md`.
- The after-seed-43 batch, pending in `results/pending/` (ORDER.md): (1)
  rebind - the converter rebinds a primitive to its NEWEST Forth redefinition;
  (2) fsys 5 - READ-LINE reading ahead where a file can seek; (3) the dump
  guard. No kernel change: no reseed.
- **Seed 43 caveat:** it runs with the rebind fault (Iteration 211): its fsys
  4 is fsys 3 plus dead bytes (the buffered WRITE was never bound), so fsys 4
  will look strictly worse than fsys 3 - seed 43's front says nothing about
  buffering. Its fsys 3/4 designs work.

### Processing a returned seed (the routine - seeds 41 and 42 were done so)

1. Unpack both packs into /tmp. Check `pack/tests.log` (PASS), `jail.log`,
   `validate.log`; `report.md`'s count; `next-run.log` times.
2. The comparison judges itself (`compare-fronts.md`, "Judging the runs"):
   fastest, smallest, memory (+-8 KB), hypervolume, best Q - a run is small
   only if all five are. Note the Q-best design of all runs.
3. From the run's `db.jsonl`: deaths by cause, corpus deaths, crossover share,
   children and front designs "via the attic", the final front by how made,
   the new genes on the front (`E.first_front`, `E.express`).
4. Score the seed's predictions in `results/predictions.md`; write the next.
5. Write `results/evolve-amd-ryzen-7-pro-8840hs-seedN.md` (a heading of the
   verdict and facts, then the pack's report.md) - `ans-check.py` and other
   tools find genomes through these files.
6. The pack's `results-measured-here.patch` has so far been the same laptop
   stash every time, already on master: check with `git apply -R --check`.
7. Apply the pending batch per `results/applied-after-seed57/ORDER.md` (reseed first with
   `tools/reseed.sh` only if a patch changes `forth/kernel.4`), then
   `LAYOUTS=1 bash tools/build-stages.sh`, `bash tools/run-tests.sh` (PASS),
   `python3 lab/evolve/evolve.py --validate` (7 of 7 IDENTICAL).
8. Every front design alive with the new code: the run's front and the joint
   front from compare-fronts.md, genomes from the run's db (earlier runs' for
   the joint front) - build and run the corpus (seed 42: 101 of 101).
9. Held out: `python3 lab/evolve/ans-check.py --ids <12 of the front>` - 0
   differ from s6, s6 2,119 tests, 0 failed, 14 of 14 whole.
10. `git mv results/pending results/applied-after-seedN`; append the session to
   `results/compare-fronts-amd-ryzen-7-pro-8840hs.md`; set `lab/evolve/NEXT-RUN`
   (the next seed, the owner's hours); a PROGRESS entry; commit; bundle.

### The owner's standing decisions

- Judging by five measures (Iterations 188-189): hypervolume and best Q count
  with the extremes; the stopping rule counts small runs. Seed 42 showed why:
  small by the extremes, not small by hypervolume (+4.8%).
- Demote, don't delete: the attic (demoted designs with gene values no
  survivor has; a tenth of parents from it); the 8 best by Q always survive.
- Offer trade-offs to evolution as genes rather than deciding: a small size
  cost for a large speed gain is welcome (threads, fsys levels, rtloop...).
- Noisy timing questions go to the laptop; here (a VM, +-10%) decide by the
  profiler's dispatch counts, which are deterministic.
- The surrogate screen: pure Python, 30%/5%, one screened child in ten audited.
- I/O (Iterations 202-211): keep both families - native I/O primitives
  (fsys 0) and the single SYSCALL primitive (fsys 1-5) - "to ensure we are not
  losing anything". No buffering of input from stdin, pipes or anything that
  cannot seek; output buffers on the heap, never in the dictionary; output to a
  terminal unbuffered (Gforth's rule; the standard leaves it open); read-ahead
  only where a file can seek, given back before any other use.
- From the Forth collection: code only from public-domain, permissive or the
  owner's own sources; GPL ones (SOD32, gforth, SP-Forth, bigFORTH) ideas only.
- Run lengths: seeds 41-42 6 hours, seed 43 9 hours - ask for the next.
- Every patch: tested, then verified to apply in order on a fresh clone and to
  reproduce the tested files; batches wait in `results/pending/` with ORDER.md.

### Open items (roughly by value)

1. Seed 43: process (above); mind the fsys 4 caveat; check the crossover share
   (33% recorded at XOVER 0.25 in seed 42 - explained as remade repeats, which
   are mostly mutation-only: verify from the db).
2. The after-seed-43 batch: apply; NEXT-RUN seed 44 (ask the hours).
3. fsys follow-ups: READ (stdin) finds the editing character in a Forth loop
   (SCAN can find one character; the four need care); level 5's bookkeeping
   costs more dispatches than level 4 (6.95M against 6.76M, the kernel
   workload) for fewer system calls - tighten; shared loops in the libraries.
4. Packed names (colorForth): `reference/forth-archive/colorforth-chars.md` -
   our names need characters colorForth lacks: an escape code or our own
   frequency table; NAME=? and the chain walk as cell compares.
5. A lookup cache beside the threads gene (results/loop-audit.md): name to
   word, cleared on every definition and order change.
6. The next keeping forms: DUP before ?BRANCH, OVER before C@ (regprice.py,
   results/price-hybrid.md).
7. Instruction replication; a sweep of the engine's constants.
8. Engine findings, not yet acted on: `1 0 /` kills every engine with SIGFPE
   (the standard leaves it ambiguous; THROW -10 would be kinder); the native
   engine loses buffered output on a signal death and buffers terminal output.
9. Settled, not to redo: callrel (worse, results/drafts/callrel*), PGO (not a
   gene, results/drafts/pgo.md), run-time folding (one constant expression in
   all workloads), NAME=? a cell at a time (no gain - Iteration 203),
   regpin (in, the laptop decides), dskew (the laptop judges).

### Lessons - how faults got in, and the checks that now catch them

- A passing gate does not prove the intended code ran: twice a fallback of the
  same name answered (fsys 5's READ-LINE never loaded; fsys 4's WRITE never
  bound). Profile and look for the new words; the dump guard (Iteration 212)
  now stops a run whose libraries do not load whole.
- The dump lists words NEWEST first; Forth remarks must be in comments; the
  cell system has no NIP or TUCK; the kernel never uses ?DO (the translator has
  no case for it); a colon word shaped like a stub (TYPE is `WRITE ;`) is read
  as a stub - rebinding handles it.
- Patches: commit each locally before diffing the next (a patch once carried
  the one before); verify the whole batch in order on a fresh clone.
- Tool calls run /bin/sh (no bash-only syntax); about 300 s a call - run-tests
  takes ~4 min alone, ans-check ~2.5 min a design at one setting; split.
- After changing `forth/` or `engine/`, rebuild the stages - the evolver's
  freshness check refuses a stale build.

### The environment

Work as user `claude` (`runuser -u claude`) in
`/home/claude/forth-vm-evolution` (clone the bundle there); scratch in /tmp. A
scratch tree for a batch in progress: clone master, apply the pending patches,
build stages there. Uploads arrive in `/mnt/user-data/uploads`; deliver to
`/mnt/user-data/outputs`.

### Where things are

- The log: this file; the goals: `GOALS.md`; conventions: `prompts/`.
- The evolver and its tools: `lab/evolve/` (README.md: every gene and process
  change by iteration); `evolve.py`, `compare-fronts.py`, `ans-check.py`,
  `outbuf-check.py`, `regprice.py`, `loopwords.py`, `surrogate-*.py` (in
  results/drafts), `NEXT-RUN`.
- Results: `results/evolve-amd-ryzen-7-pro-8840hs-seed*.md` (each run),
  `results/compare-fronts-amd-ryzen-7-pro-8840hs.md` (every session),
  `results/predictions.md`, `results/gp-deep-dive.md`, `results/weighing.md`,
  `results/loop-audit.md`, `results/forth-implementations-survey.md`,
  `results/forth-standard-tests.md`, `results/drafts/` (designs and negative
  results: fsys/single-syscall.md, pgo.md, callrel*, surrogate-offline.md).
- Batches: `results/applied-after-seed41/`, `results/applied-after-seed42/`,
  `results/pending/` (after seed 43).
- The Forth collection: `reference/forth-archive/` and
  `results/forth-collection-catalog.md`.

## Iteration 214 - 2026-10-12 - Claude

**Set up from Iteration 213's bundle while seed 43 runs.** The checks as handed
over: the build 23 s, run-tests PASS (99 s here, not ~4 minutes), 7 of 7 stages
identical. Iteration 213's environment, corrected forward: install gcc-multilib
as root and make the clone's directory belong to claude before cloning (HANDOFF-
PROMPT.md had both; it is rewritten to point to the last HANDOFF entry); a job
started with `&` dies when its tool call ends - the first run-tests was killed
silently - so a long job runs under `setsid nohup` and is polled; and one such
job did not outlive the end of a reply (its log stops there; /tmp kept its
files). Nothing executable changed between seed 43's commit (9b96930) and 213,
and a chain pulls once (its second half runs with NEXT_RUN_PULLED=1): a newer
bundle in ~/Downloads cannot touch a running chain.

**fsys 5 tightened - the after-seed-43 batch's fourth patch
(results/applied-after-seed43/fsys5fast-after-seed43.patch).** Searched first (prompts/12:
PROGRESS, GOALS, the fsys notes - bookkeeping, read-ahead, FS-FILL, FS-TAKE,
6.95): no earlier attempt, only Iteration 211's count. Priced first
(prompts/10): lab/evolve/fsys-count.py - the profiler's per-address counts
summed, strace -f -c for the system calls, the same build but for the level:
counted, nothing removed - reproduced 211's 6,754,946 and 6,947,095 exactly:
the prize 192,149 dispatches (2.8%), the kernel workload on seed 42's smallest.
READ-LINE now takes a line whose LF is already in the buffer, within the
caller's room, at once: one SCAN, one CMOVE, no seek test (an entry holding
unread bytes belongs to a file that seeks - every open, close and other use
empties it), no variables, next and end as addresses; the rest goes the general
way with two variables where there were six. Predicted ~110 dispatches a line
against fsys 4's ~155; counted, fsys 4 -> 5 (Iteration 211's in brackets):

| design | kernel | corpus |
|---|---|---|
| be1620e346, seed 42's smallest | -2.2% (+2.8%) | -0.4% |
| a0c7010722, without kinput | -2.3% (+2.8%) | -0.4% (+2.2%) |
| 28677d13b1, seed 42's fastest | -12.5% (+3.8%) | -9.7% (+2.8%) |
| 9a3de58ebe, the best by Q | +44.8% (+62%) | +21.1% (+33%) |

System calls as in 211 (kernel 4,441 -> 135, corpus 12,755 -> 439); images
33-53 bytes smaller than 211's fsys 5. Profiled: the seek test 40,700
dispatches -> 192 - the new path is the one taking the lines.

**Found: the copy, where CMOVE has no opcode.** 9a3de58ebe lists CMOVE among
its format-10 words but realizes 14 of its 31, and not CMOVE: 90% of its fsys 5
cost is copying lines out with the kernel's byte loop. A copy a cell at a time
priced, NOT built: there -28% kernel, -17% corpus; where CMOVE has its opcode
+2.2% to +11.7% and +0.8% to +6.5% - and evolution can give CMOVE its slot
already (GOALS.md's register; results/drafts/fsys/single-syscall.md).

**lab/evolve/readline-check.py** (in the patch): READ-LINE at fsys 3, 4 and 5
against native, byte for byte - every kind of line, a 10-character room, a CR
and its LF on either side of the 4 KB boundary, the position words between
lines, two files in turn, a number reused, u1 = 0, the end met again, a
5,000-character line, INCLUDED nested, /dev/stdin opened as a file (no read-
ahead from a pipe: the next line must be left to the interpreter). PASS on
three designs. Shown to fail (prompts/15): a planted fault in the new path (a CR
kept before the LF) and one in the general way (its LF left unconsumed) - each
caught at fsys 5 alone; and before that on my own wrong expectation ("XX" and
its LF cover three bytes, not four). **A native fault:** WRITE-LINE's handler
never gives back the read-ahead (no t_fdrop, where CLOSE-FILE, READ-FILE,
WRITE-FILE, REPOSITION-FILE, FILE-POSITION and FILE-SIZE all call it), so after
a READ-LINE on a file opened R/W native writes after the 4 KB it read; fsys 3,
4 and 5 write at the file position. Judged by the file's bytes, not against
native. Not fixed: an engine change to every fsys 0 design - open item 8, with
the other engine findings, the owner's call.

**Tested** (master and patches 1-4): run-tests PASS; 7 of 7 stages identical;
the gate at fsys 5 on four designs (the corpus, kernel.img byte for byte, far);
readline-check PASS; outbuf-check.py PASS; the standard suite at fsys 5 14 of
14 as s6 on two designs, the negative control caught. Verified: the four
patches apply in order on a fresh clone and reproduce the tested files.

**Open items, Iteration 213's list changed so:** 2 - the batch is four patches.
3 - fsys 5's bookkeeping done; READ from stdin's editing characters and the
shared loops remain. 8 - native WRITE-LINE's missing give-back added.

## Iteration 215 - 2026-10-12 - Claude

**Seed 43 processed - not small; the after-seed-43 batch applied.** Both packs
at 9b96930b (Iteration 210): tests PASS, the jail PASS, 7 of 7 identical. The
evolution 02:44-09:34 (6 h 51 min, generations 0-153): 38,796 designs made,
31,957 measured, 6,839 screened; the chain 8 h 30 min. The comparison's own
verdict (session 38): fastest -1.9%, smallest +12.26%, memory +4 KB,
hypervolume +22.4%, best Q +9.3% - not small. The Q-best of all runs is seed
43's fc09f6373d (0.203 at 25,964 bytes, 180 KB, Q 0.210 of s6's); the smallest
of all its add5ec8937 (16,136 bytes); the fastest still seed 42's 28677d13b1.
All 73 designs of the front of all runs are in seed 43's database.
results/evolve-amd-ryzen-7-pro-8840hs-seed43.md.

From the database: 182 deaths, every one "reach limit at scale 0 - not run"
(none from a short branch, none on the corpus); the screen skipped 18.4% of
the children from generation 5, and of the 805 audited none is on the front;
threads at 16 chains on 121 of the 165 - never 64 or 128: the bytes won over
the lookup's dispatches; fsys 2 on 84 (49 of the fast third: it moves only the
file words), 3 on 44 (the small end), 4 on 4 (unbuffered in this run), 0 on 33.
**The crossover share, verified** (Iteration 213's open item 1): the children
kept are 31.4% crossover at XOVER 0.25; one try from the final front against
the run's designs repeats 24.6% of the time mutation-only, 0.5% crossover, and
the loop remakes repeats - which predicts 30.6%. Predictions scored
(results/predictions.md): 1 and 5 right, 2 and 4 half, 3 wrong; seed 44's
written.

**The batch applied** (results/applied-after-seed43/, four patches; no kernel
change, no reseed): run-tests PASS, 7 of 7 identical. Every front design alive
with the new code - the run's 165 and the joint front's 73, 175 in all: 175 of
175 (the corpus, kernel.img byte for byte, far). Audited, since 175 took 201 s:
the builds are real (0.8-1.6 s each here), the 4 fsys 4 designs' images 8-16
bytes smaller than recorded - their buffered WRITE bound at last - and the
fsys 0 and 3 ones byte for byte as recorded. The standard suite on 12 of the
front (fsys 0, 2, 3 and 4; threads 16 and 32): 0 differ from s6, s6 2,119
tests, 0 failed, 14 of 14 whole. The pack's results-measured-here.patch is
already on master (reverses cleanly).

**NEXT-RUN: seed 44, 9 hours like seed 43 - proposed, the owner's to choose.**

**Open items, Iteration 213's list changed so:** 1 and 2 done. 3: READ
(stdin)'s editing characters; the shared loops. 4-9 as listed (8 with native
WRITE-LINE's missing give-back, Iteration 214). fsys 5's cell-wise copy in
GOALS.md's register.

## Iteration 216 - 2026-10-12 - Claude

**Seed 44 for 6 hours, not 9 (the owner).** lab/evolve/NEXT-RUN: `seed 44
tag2 6h then experiment compare-fronts.py --rounds 6 --frontier --cpus 2,8`.
next-run.sh keeps the last chain's re-measure and comparison time (seed 43's:
18 + 79 minutes) plus a tenth and 10 minutes, so the evolution gets about 4
hours - seeds 41 and 42 ran 6-hour chains too; the comparison measures every
front again in one session, so a shorter run is judged on equal terms. Seed
44's predictions (results/predictions.md, Iteration 215) stand as written.

## Iteration 217 - 2026-10-12 - Claude

**A survey of JITs and VM speed elsewhere (the owner, seed 44 running):
results/drafts/jit-vm-survey.md.** Read against what the project has and has
rejected first (JIT.md, GENES.md's candidates, GOALS.md's register), so it
re-proposes nothing. The strongest finding is new this year: RPyForth (Izawa
and Hakamada, arXiv 2609.23759, September 2026), a Forth on RPython's
meta-tracing JIT, gained 1.44-1.60x from letting the compiler name a window of
top stack cells, beat gforth-fast and SwiftForth, and beat VFX on kernels but
not on call-heavy applications. CPython's copy-and-patch JIT added the same
thing in 3.15 as stencil variants per cached-register state. Ranked: (1) stack
state in the JIT's translator - stencil variants by cells in registers, with
constants tracked as Liftoff does - priced first with stackops.py over the
words the JIT translates; (2) native code calling byte code (candidate 5,
priced); (3) the handlers as the stencils (candidate 11, Deegen's way); (4)
hot/cold splitting of stencils; (5) the IP/sp dependence chain on loops (Ertl
and Paysan, ECOOP 2024) - perf on the laptop first; (6) replication only if
(5) shows mispredictions; (7) folding literal inputs at compile time
(Mecrisp's n-foldable). Not borrowed: tracing JITs, a register byte code for
the interpreter, preserve_none.

## Iteration 218 - 2026-10-12 - Claude

**Stack state in the JIT's translator, priced: results/price-jit-stack.md**
(the survey's item 1; the owner: proceed). Searched first: FINDINGS-SPN.md
named it SPN's next step, never attempted. Built to count, not to run: a
profiling-only switch, `JIT_PRICE` (engine/vm-lab.c, engine/jit.c, evolve.py
by environment) - the JIT translates as it would, native code never runs, so
every operation of every translated word is counted and the translator lists
their stencils and branch targets; lab/evolve/jitstack.py simulates a K-register
cache with constants, canonical at branches, targets, loops, calls and EXIT,
costed by each stencil's own machine code (objdump). Checked: four designs'
engines and images byte for byte as built from Iteration 217's tree, 7 of 7
stages; the loop's hot word audited operation by operation. **The prize** on the
fastest design of all runs (the others alike): native instructions -27% fib,
-27% loop (K=3), -17-21% bubble, -12-14% ackermann, -17-25% kernel, -43-45%
the held-out sieve; data-stack memory accesses -50 to -100%; the corpus and
parse barely run translated code. **Into time once**
(lab/evolve/jitstack-inner.S): the loop's hot word today 1.01-1.03 ns an
iteration, three cells cached 0.72-0.76 (25-30% less, as the 27% instructions
said), the loop's index in registers too 0.62-0.65. Estimated: the selection's
geometric mean ~15% better on JIT designs. Not yet priced: the engine bytes -
stencil variants or an emitter.

## Iteration 219 - 2026-10-12 - Claude

**Stack state in the JIT, the cheapest form built and priced; Iteration 218's
time corrected** (results/price-jit-stack.md). Correction forward: the 25-30%
measured on the loop's hot word was one build's placement. Swept over eight
loop-head offsets (lab/evolve/jitstack-inner-sweep.sh, the VM's Intel core):
today 1.03-1.21 ns an iteration; three cells cached with free renames 0.68 at
two offsets, 1.61-1.96 at six; the loop's index in registers too 0.61-0.65 at
all eight. The data stack's memory traffic removed alone is not reliably faster
here: the index's load-add-store through memory remains, and the core's
speculation and alignment decide the rest. The proxy (instructions, stack
accesses) did not see that chain. **Engine bytes**: lab/evolve/jitvariants.py
builds the fixed-register form (cells always in %rsi, %rdx, %rcx; a stencil
per data operation per state; immediate forms; canonicalisers) with the
fastest design's flags - 113 stencils, 2,072 bytes at K=2; 151, 2,813 at K=3;
today 43, 1,007: ~+1.4 KB and ~+2.1 KB. Simulated with those stencils
(jitstack.py --variants): instructions -4.5% loop, -12% fib, +4% bubble, +4-13%
kernel, -22% sieve - fixed registers turn shuffles into moves; memory traffic
-24% to -100%, which alone did not pay on this core. Loops whose index could
live in registers (bodies calling nothing): 99.9% of the loop workload's, none
of bubble's or the sieve's. **Deferred, not built**: the laptop's sweep decides
(`sh lab/evolve/jitstack-inner-sweep.sh` on the Zen 4). Also: the JIT_PRICE
switch and jitstack.py's loop count stay for that.

## Iteration 220 - 2026-10-12 - Claude

**Native code calling byte code (the survey's item 2, GENES.md candidate 5),
priced again: not built** (results/price-jit-interp.md). The JIT_PRICE dump
now lists every call of every word the JIT met (`K` lines; two designs'
engines and images byte for byte as before). On the fastest design, the words
the JIT leaves because of a call alone hold 9.3% of the kernel workload's
dispatches, 4.1% of the corpus's, 0.5% of bubble's and nothing elsewhere
(Iteration 90's 80% of the sieve went to jitx) - and they would cross back
into the interpreter every 3-4 operations (44,675 crossings for 180,846
operations on the kernel workload). Recorded in GOALS.md's register. Of the
survey's list: 1 deferred to the laptop's sweep, 2 not built; 3 and 4 are
bytes (~1.3 KB of stencils, a few cold paths), 5 and 6 need the laptop's perf.

## Iteration 221 - 2026-10-12 - Claude

**A name-lookup cache (the handoff's open item 5), priced: not built**
(results/price-lookup-cache.md; results/drafts/lookup-cache-model.py). Over
the corpus's and parse's own token streams, the dictionary growing as they
define, on seed 43's smallest design at the 16 chains most of its front chose:
a 16-entry cache cuts the entries visited per lookup 22% (corpus, 23.5 -> 18.3)
and 48% (parse, 22.7 -> 11.8); doubling the chains halves both, 64 chains cut
three quarters - for 128-384 bytes, which evolution declined at the small end.
Half the walk is names not found (57% and 49% of the visits), which a cache of
found names cannot serve; a per-chain filter would - noted, not priced in
bytes. Register updated. Open items now: 3 (fsys: READ's editing characters,
the libraries' shared loops), 4 (packed names), 6 (keeping forms), 7-8; the
JIT survey's 1 waits for the laptop's sweep, 5-6 for its perf.

## Iteration 222 - 2026-10-12 - Claude

**The next keeping forms (open item 6) and packed names (open item 4), priced:
neither built; a better size lever found** (results/price-keepforms-next.md,
results/price-names.md). regprice.py on seed 43's smallest: the largest
absorbable pattern is still DUP before a short ?BRANCH (5.4% kernel, 6.3%
corpus, 6.4% parse of image dispatches) - which has its form, DUP?BRANCH8,
listed by 121 of the 165 front designs and realised by 28: the small designs
realise 10-14 of the 31 format-10 names they list; codes are what is short
there, and new forms (OVER C@ 1.4-3.0%, DUP C@ 1.3-2.9%) would queue for them.
Packed names: all 58 characters fit six bits; -292 to -384 bytes before the
code, a kernel change and a reseed - not built. **The names nobody uses**
(results/drafts/hidden-names.py): the names no program here writes, made
headerless with the converter's existing switch - the overlays' compiler
helpers and constants, NAME=? and NEXT-NFA8 - the smallest of all runs 16,136
-> 15,688 bytes (-2.8%), seed 43's fastest -936 (-2.7%), both alive; no
standard word among them. A candidate for the after-seed-44 batch, as lists
kept by hand per overlay; gene or default, the owner's call.

## Iteration 223 - 2026-10-12 - Claude

**Iteration 222's "costs nothing", corrected: hiding the unused names does hurt**
(results/price-names.md). The owner asked whether it could; the standard suite
had not been run. Run on three designs with the lists hidden: 13, 13 and 0 of
14 files as s6 - the third (5f4a21fbdb, JIT) crashing on every file. Causes:
coreext.4, INCLUDEd at run time by the suite's harness, builds
TRAVERSE-WORDLIST from NEXT-NFA8, and the scan had not read it (read, the tools
test matches); and LEAVE8 alone (bisected) crashes that design at its first
INCLUDED - defined in four overlays, POSTPONEd by one, reached in a way no
source scan shows. A derived list is unsafe; only hand-kept, reviewed lists
per overlay, checked on every gene combination, could carry the -2.7%.
**Inlining instead** (the owner's question), priced from the call map: the
opcode constants are 2-byte bodies (~28 bytes as literals), words called once
~3 bytes each (36 and 15 bytes), and the words no call reaches are not dead -
reached through headers, tables and POSTPONE. The bytes are in the headers.

## Iteration 224 - 2026-10-12 - Claude

**The owner: capture the hidden-names findings, do nothing more on them now.**
Recorded in GOALS.md's register as deferred, with what a safe form would need
(hand-kept lists per overlay, LEAVE8's crash understood, every gene combination
through the gate and the standard suite). On to the other action items.

## Iteration 225 - 2026-10-12 - Claude

**Two engine changes for the after-seed-44 batch (results/pending/, ORDER.md).**
(1) **Native WRITE-LINE gives back the read-ahead** (open item 8, found by
readline-check.py in Iteration 214): one line, `t_fdrop` before the write, as
WRITE-FILE and the positioning handlers already did; readline-check.py now
holds native to the right bytes too. (2) **The native file buffers' slots,
state apart from buffers** (open item 7, "a sweep of the engine's constants",
by pages touched - cputime's MINFLT, the memory objective): t_fslot's scan of
the slots' fd fields touched one page a slot, 32 KB at 4 KB buffers, the first
time any file was read. With the state in one array, d3149e10c6 (fbuf 0): fib
144 -> 116 KB, loop 144 -> 116, corpus 168 -> 144, kernel 204 -> 168 - what
512-byte buffers cost before (112-164), without their reads; fbuf 2 itself
0 to +8 KB, within the tie. 30 of seed 43's native designs have full buffers,
83 the 1 KB ones. Tested together: readline-check PASS on two designs, run-tests
PASS, 7 of 7 identical, outbuf-check PASS, every native front design of seed
43 alive (117 of 117), the standard suite 0 of 2 differ; engines and images of
three designs the same sizes as master's; both patches apply in order on a
fresh clone and reproduce the tested files.

**Left for the owner** (open item 8): `1 0 /` kills every engine (SIGFPE) - a
THROW -10 needs a way for a handler to raise a Forth exception, which the
engine has not (it reports and exits); native output held when the terminal
should see it at once, and lost when a signal kills the engine - each fix
adds bytes to every native engine. Open items now: 3 (fsys: READ's editing
characters - pipes read a byte at a time, so the workloads would not see it -
and the libraries' shared loops), 7 (replication: the laptop's perf), the JIT
survey's 1, 5 and 6 (the laptop).

## Iteration 226 - 2026-10-12 - Claude

**The fsys follow-ups (open item 3), as seed 44 runs: the third patch of the
after-seed-44 batch (results/applied-after-seed44/fsysread-after-seed44.patch).** READ finding
its editing characters in a Forth loop: not made faster - only a stdin that is a
file takes that path (a block read, the rest given back), and every workload
reads its input through a pipe, a byte a read(2) (the owner's rule), so
evolution would not see it. What it lacked was a check: readline-check.py now
gives the interpreter its input from a stdin that is a file - CR LF, a
backspace and a delete inside a line, a line past ACCEPT's room, KEY, no newline
at the end - every level against native: fsys 3, 4 and 5 as native; shown to
fail with READ's block path not stopping at the first editing character. The
libraries' shared loops: READ asks whether stdin seeks as every file is asked
(FS-SEEKS?, its bit cache), and its own FS-SEEK0 goes - 40 image bytes at fsys 3
(8,680 -> 8,640 on the smallest of all runs). The rest priced and left: READ's
and READ-LINE's byte-a-time loops share a few tokens (a helper would save ~4
bytes); fsys 5's seven give-back wrappers (~100 bytes there) could fold into
FS-DROP if the converter rebound its compiled uses - a converter change, not
done. Tested: readline-check PASS on two designs, outbuf-check PASS, run-tests
PASS, 7 of 7 identical, the 48 seed 43 front designs with fsys 3 or 4 at each
of fsys 3, 4, 5 alive (144 of 144), the suite at fsys 3 on two designs 0 differ;
the three patches apply in order on a fresh clone and reproduce the tested files.

## Iteration 227 - 2026-10-12 - Claude

**The owner's guidance on words, recorded in GOALS.md ("The aim"):** core words
in the base kernel; helper words where convenient, in a reasonable balance with
size - developer friendly, so reusable non-standard words keep their names;
splitting a long word for understanding, testing and extending counts as a plus
beside the bytes. The hidden-names entry in the register notes it.

## Iteration 228 - 2026-10-12 - Claude

**The fourth after-seed-44 patch: 32 KB of stack nobody used, on every run of
every design** (results/applied-after-seed44/stackheads-after-seed44.patch; open item 7, the
engine's constants swept by memory). Found by reading which pages a design
still has present after a workload (/proc/pid/pagemap, mapped to the engine's
symbols): 9-11 pages of C stack in a libc-free engine. load_image keeps
`heads[MAX_THREADS]` - 4,096 cells, 32 KB - on the stack, and Ubuntu's gcc
compiles with -fstack-clash-protection, which probes every page of a frame
that large: 8 pages written at each start, for the 16 to 128 heads an image
has. Static, in BSS, only the pages written count. With patch 2, memory by
pages touched against master: seed 43's smallest -28 to -40 KB on every
selection workload (fib 112 -> 80, kernel 172 -> 132), d3149e10c6 (full file
buffers) -52 to -60, seed 43's fastest -24 to -44, the Q-best of all runs -16
(-4 and 0 on bubble and ackermann). Tested on master and patches 1-4: run-tests
PASS, 7 of 7 identical, all 165 of seed 43's front designs alive, the standard
suite 0 of 2 differ; engines +-32 bytes, images unchanged; the four apply in
order on a fresh clone and reproduce the tested files. load_image is the only
function the compiler probes page by page (objdump: one probe loop).

## Iteration 229 - 2026-10-12 - Claude

**A zero divisor is -10 THROW (the owner approved; the fifth after-seed-44 patch,
results/applied-after-seed44/divzero-after-seed44.patch - it changes kernel.4: reseed).** The
converter writes THROW's body into every CV8 image header, as it writes the
locals words'; the engine's UM/MOD calls it with -10 where the divisor was -
through macros, so the handler stays one line for gen-super (a superinstruction
must not run its second operation after the throw) and gen-tos (the cached top
refilled first). SAVE-SYSTEM and the SPN save write the cell; spn-cv8.c reads
it. The kernel's THROW, uncaught, names the code first: "Division by zero" for
-10, "Error n" for the rest but -1 and -2. outbuf-check.py has a DIVZERO case.
Checked on every engine kind (multi-state, tail, JIT, cached top, fsys 5) and
the stages; run-tests PASS, 7 of 7, outbuf-check and readline-check PASS, all
165 of seed 43's front alive, the suite 0 of 3 differ. Cost: engines +96 to
+192 bytes, images +64 - five times the estimate on the engine side; a slimmer
form (no message for the header's absence, "Error -10" only) is possible.
Found on the way: s6's bare-kernel image (s6-cv8b-k64.img) dies on any input -
on master too, unused by the tests; s6's system image is fine. Also: the owner's
standing decisions already say "output to a terminal unbuffered" - native's
buffering of terminal output (Iteration 214) is a defect against them, not a
question; open.

## Iteration 230 - 2026-10-12 - Claude

**Seed 44 processed: small, the first** (results/evolve-amd-ryzen-7-pro-8840hs-
seed44.md). The comparison: fastest -0.6%, smallest +0.00%, memory +0 KB,
hypervolume +0.9%, best Q -0.2%. Q-best of all runs seed 43's 0af26c8e89 (0.206
at 25,779, 180 KB, Q 0.211); smallest still add5ec8937, matched by seed 44's
dde890d478 (16,136); fastest still seed 42's 28677d13b1. Run: 4 h 05 min of
evolution, generations 0-89, 22,785 made, 18,094 measured, 4,691 screened; 106
deaths (reach limit), none on the corpus; crossover 32.2% (35.5% late); the
attic 3,364 children, 7 of 120 on the front; fsys 5 on 15 (from 17,769 bytes;
the smallest tenth all fsys 3), fsys 4 on 3; threads 16 on 85. Predictions 3 of
5 (fsys 4 wrong - fsys 5 took its place; "not small" wrong). Seed 45's written.
The pack's results patch already on master. **The after-seed-44 batch applied**
(results/applied-after-seed44/, five patches, reseeded for patch 5): run-tests
PASS, 7 of 7 IDENTICAL, every design of seed 44's front and the joint front
alive (161 of 161: 120 and 82, 41 in both), the standard suite on 12 of the
front 0 differ (s6 2,119 tests, 0 failed, 14 of 14 whole). NEXT-RUN: seed 45, 6
hours, proposed - by GOALS.md's rule a second small run stops the evolution
until new genes exist; the batch has none. The owner chooses.

## Iteration 231 - 2026-10-12 - Claude

**The after-seed-45 batch begun, as seed 45 runs (results/pending/, ORDER.md).**
(1) **Native output to a terminal unbuffered** - the owner's standing rule,
which the native engine broke (Iteration 214 found it, Iteration 229 named it
a defect): the first WRITE asks isatty(1) - a small isatty added to the
libc-free runtimes (ioctl TCGETS) - and a terminal gets every WRITE at once.
outbuf-check.py's terminal case holds native to it now: "A" at 0.00 s, "B" at
0.88 s. +132 engine bytes on native designs (the generic syscall() measured
+68 and +100 - a trim before applying). (2) **The SPN engine throws -10 too**:
s8 read THROW's cell (Iteration 229) but still died of SIGFPE - now as
vm-lab.c; s8-full and s8-spncv8 checked. Both: run-tests PASS, 7 of 7, 161 of
161 front designs alive, the suite 0 of 2 differ, a fresh clone reproduces the
files. **A correction to Iteration 229:** s6's bare-kernel image dying on any
input is known and documented (build-stages.sh: "for the size column ONLY. It
does not boot" - the kernel's own word-list search assumes cell headers);
confirmed here - the same conversion without --bytehdr runs. Not a defect.

## Iteration 232 - 2026-10-12 - Claude

**UTF-8 word names compile right (the owner asked how they behave; the third
after-seed-45 patch, results/applied-after-seed45/names-after-seed45.patch).** >NAME finds a
header by scanning back from the body for bit 7 - the count byte's mark - and
COMPILE, reads bit 5 there to inline a primitive. With the name between the
count byte and the body, a UTF-8 byte (bit 7 set) stopped the scan; with bit 5
set too (BF, A9, A0...) the word read as a primitive: `: суп 5 . ;` ran,
`: обед суп суп ;` printed nothing, `café` crashed. Byte headers now carry the
count byte after the name, right before the body: the scan stops there at
once, whatever the name holds. Three more repairs on the way: REVEAL8 (the
kernel's REVEAL hashed the name after the count byte - every new word went to
the wrong thread), the converter's expected THREAD-FIND body (75 of 161 designs
died "no exact body match" until sod16.py's list matched), the tracer's way of
naming run-time words. New check: lab/evolve/names-check.py. All checks pass
(ORDER.md); images +16 bytes, +56 with kfast. **Found, not fixed:** the cell
headers have the same fault - the kernel's own COMPILE, asks >NAME; s0 crashes
on `café`. The owner decides on that, and on packed names after this.

## Iteration 233 - 2026-10-12 - Claude

**The owner: fix the UTF-8 fault in the cell-header designs too; capture packed
names' benefits, do not build them now.** Packed names recorded in GOALS.md's
register with the plan and the numbers (images ~300-380 bytes fewer before
~100-150 bytes of code; UTF-8 names unchanged under it; a Cyrillic table would
cut a program's Cyrillic names ~60%). The cell headers next.

## Iteration 234 - 2026-10-12 - Claude

**UTF-8 names in the cell-header systems too (the owner approved; the fourth
after-seed-45 patch, results/applied-after-seed45/cellnames-after-seed45.patch - it changes
kernel.4: reseed).** The kernel's own COMPILE, asked >NAME for a primitive's
flag the same way, so s0 (the build host), SOD16, CPT16, s4-s5, pack4/pack8 and
s7 had the fault - s0 crashed on `café`. Cell headers are now [link cell]
[zeros][name][count byte], the count byte last, right before the cell-aligned
body: the kernel's HEADER, SEARCH-WORDLIST (a byte compare), REVEAL, NAME>
(1+) and a new PRIOR-NFA; cross.4 lays the target's headers the same way; the
dump tool, the converter's cell path, the SOD16 tables, sod16.4 and the cell
SPN follow; NAME=? moved into the kernel (one copy in byte images), REVEAL8
dropped. names-check.py judges all 14 hand-made stages now: all right, as every
evolved design given. Two faults found and fixed on the way (PRIOR-NFA's name -
NEXT-NFA collided with the converter's X8 swap and broke s8; LINKC kept the dump
tool in the images, +662 bytes, until the converter's DUMPTOOL listed it). All
checks pass (ORDER.md); images +32 bytes, engines unchanged. The after-seed-45
batch: four patches, one reseed.

## Iteration 235 - 2026-10-13 - Claude

**The benchmarks in C - a native baseline (the owner's idea).** bench/c/bench.c
does exactly the work of fib, loop, sieve, bubble, ackermann and parse
(BENCH repeated as the long versions do; 64-bit wrapping cells; inputs through
volatile reads, results printed - the same answers as the Forth: sieve 1899,
bubble 65505 0, ackermann 253). lab/evolve/c-baseline.py times C -O2 and -O0
against s6 and given designs with the evolver's own CPU-time wrapper, the
median of N runs, start-up subtracted. On the VM (noisy, ~10%), as multiples of
C -O2: s6 27.1x; the fastest of all runs (28677d13b1) 3.9x - loop 1.7x, parse
1.9x, bubble 3.4x, sieve 3.5x, fib 5.1x, ackermann 16.8x; the knee 4.7x; the
smallest 29.3x; C -O0 3.2x. Calls and returns are where the fast end is
furthest from C: ackermann and fib, recursion, 16.8x and 5.1x, against 1.7-3.5x
for the loops - the outside reviews' return-path ideas aim there.
results/c-baseline-*.md; the laptop should run it for real numbers.

**The outside reviews triaged** (five models, the owner's brief): new and
worth pricing - the dispatch table as offsets in the engine file (-768 bytes
on the smallest, no cost per dispatch: the tag-2 tables are built at start-up),
dropping stencils a design never uses, a Bloom filter for failed lookups
(half of all lookup work, Iteration 221); compressing image and engine (-37% and
-51% with xz) - a question for the owner, as it changes what size means.
Already ours or not applicable otherwise (GOALS.md register).

## Iteration 236 - 2026-10-13 - Claude

**Compressed image and engine: captured, not built (the owner).** The owner's
point holds for memory - the code runs decompressed, so memory does not shrink,
and start-up pays the decompression. On disk it would: a tiny LZSS (a
~150-300-byte decompressor) takes the smallest design's image 8,704 -> 6,659
bytes and engine 7,680 -> 4,605 (deflate and xz pack tighter but their
decompressors are kilobytes). Recorded in GOALS.md's register, with the open
question whether on-disk bytes that do not run should count as size at all.

## Iteration 237 - 2026-10-13 - Claude

**The dispatch table as offsets (the fifth after-seed-45 patch; the owner: no
new limits for developers).** Every CV8 engine file carried its dispatch table
as 128 8-byte addresses. It now holds 32-bit offsets from L_noop; at the first
entry the addresses are made once into a BSS copy that all the code reads as
before - cv8_tab, esc_tab, the tag's t2tab, the dispatch - so no dispatch pays.
384-448 bytes off every design's engine (the smallest of all runs 7,680 ->
7,240: -2.7% of its binary + image). 32 bits, not 16: 16 would save 256 bytes
more and cap the interpreter at 32 KB - the kind of limit the owner ruled out.
The generators (gen-super, gen-fold, gen-msc, and evolve.py's format-10 table)
read and write a DSP() entry; gen-tail's tables of functions and the SPN engine
keep addresses. A first form converted at every read and grew the code by 400
bytes - replaced. All checks pass (ORDER.md). Not taken: the two 16-bit opcode
maps as 8-bit (would cap the opcode space - the op;CALL codes are 0xFE00+k).

## Iteration 238 - 2026-10-13 - Claude

**The other two outside ideas priced (results/price-stencils-bloom.md).**
Dropping unused JIT stencils: 50-170 bytes of ~1,000 - not built. A Bloom
filter for names not found: the lookup is 66% of the smallest design's corpus
dispatches (69% of parse's, 36% of the kernel's) and misses half its walk, but
64 chains already cut three quarters of it for about the same bytes, a trade
evolution declines at the small end - not built. **Found on the way:** a JIT
engine's extra bytes are its translator (jit_body 3,456 bytes), which runs once
per word; compiled -Os it saves 416-800 bytes on JIT engines built -O2/-O3,
alive - proposed as a gene `jitos`, translation speed the trade.

## Iteration 239 - 2026-10-13 - Claude

**A new gene, `jitos`: the JIT's translator compiled for size (the sixth
after-seed-45 patch).** engine/jit.c under GCC's optimize ("Os") - a pragma
around its #include in vm-lab.c - on JIT designs not built -Os. In LATE, so
every recorded design keeps its id; expressed for CV8; linked with jit, jitx,
jitloop and jitinl in crossover; GENES.md has its row. On: cc6d168e0a -800
bytes, 28677d13b1 -416, both alive; an -Os design is the same build and id.
Mutation reaches it about as often as any binary gene (89 of 4,000). The
translator runs once per word, so the trade evolution weighs is translation
speed on the kernel and corpus against the bytes. All checks pass (ORDER.md).
The after-seed-45 batch: six patches, one reseed (patch 4).

## Iteration 240 - 2026-10-13 - Claude

**Seed 45 processed: not small** (results/evolve-amd-ryzen-7-pro-8840hs-seed45.md).
The comparison: fastest +0.9%, smallest +0.54%, memory +4 KB, hypervolume +6.2%,
best Q -1.6%. The after-seed-44 batch's memory fixes moved the landscape - full
4 KB file buffers now cost no memory, so 46 of the front's native-file designs
chose them (seed 44: 23) and designs earlier runs dropped as memory-dominated
returned: the reason Iteration 230 named if it were not small. Q-best of all
runs seed 44's cc678c891d (0.204 at 26,108, 168 KB). Run: 3 h 51 min, 17,797
measured, 115 deaths (reach limit), none on the corpus; crossover 31.5%; the
front 105 (fsys 2 on 53, 3 on 27, 5 on 11; memory 124-188 KB against seed 44's
160-224). Predictions 4 of 5 ("small" wrong); seed 46's written. **The
after-seed-45 batch applied** (results/applied-after-seed45/, six patches,
reseeded): run-tests PASS, 7 of 7 IDENTICAL, every design of seed 45's front and
the joint front alive (128 of 128), the standard suite on 12 of the front 0
differ (s6 2,119 tests, 0 failed, 14 of 14 whole). NEXT-RUN: seed 46, 6 hours,
proposed.

## Iteration 241 - 2026-10-13 - Claude

**Seed 46 for 10 hours (the owner).** NEXT-RUN: `seed 46 tag2 10h then
experiment compare-fronts.py --rounds 6 --frontier --cpus 2,8` - about 8 hours
of evolution after the re-measure's and the comparison's reserve (seed 45's
chain: 12 min and 1 h 17 min). The first run with jitos, the dispatch-table
offsets and the UTF-8 name fix. Seed 46's predictions stand.

## Iteration 242 - 2026-10-13 - Claude

**Primitives first, and the classic headers back (the owner: primitives belong
together at the start of the dictionary; the first after-seed-46 patch).** The
UTF-8 fault was COMPILE, finding the primitive bit through >NAME's scan back
from the code, across the name. kernel.4's second primitive block (file words,
SYSCALL and its slots, memory words) now follows RP! - order, so tokens,
unchanged - then a marker variable, (PRIMITIVES-END), and PRIMITIVE? ( xt ---
flag ): below the marker. A variable, not a ticked literal: the cross-
compiler's ['] gives a START-relative number the converter could not know for
an address (the first try - every primitive read as not one, and the second
seed crashed). Every COMPILE, asks PRIMITIVE?, so the count byte need not move:
Iterations 232-234's layout reversed - names are counted strings again, and the
walk's 6-8% (found in Iteration 241) is gone: the smallest design's corpus
58.90M dispatches (seed 45's code 58.95M, master 63.43M). names-check PASS on
every design and all 14 stages; all checks pass (results/applied-after-seed57/ORDER.md).
Bit 7 of the count byte is now read only by >NAME, which no compiler uses -
freeing it (an exact >NAME by the dictionary walk) is the next step if wanted.

## Iteration 243 - 2026-10-13 - Claude: HANDOFF - start here in a new chat

Read this entry whole, then Iteration 213's HANDOFF for what it says that is
still true (what this is, the routine for a returned seed, the environment),
then `prompts/`. Everything needed is in the repository.

### The state now

- master: Iteration 243. The after-seed-45 batch is applied (Iteration 240,
  `results/applied-after-seed45/ORDER.md`, six patches, reseeded).
- **Seed 46 is RUNNING** on the laptop: `seed 46 tag2 10h then experiment
  compare-fronts.py --rounds 6 --frontier --cpus 2,8` (the owner's 10 hours; about
  8 of evolution), at Iteration 241's commit (bf966d9). The first run with the
  gene jitos, the dispatch table as offsets, the UTF-8 name fix. Predictions:
  the end of `results/predictions.md`.
- The stopping rule counts afresh: seed 44 small, seed 45 not (hypervolume +6.2%
  - the memory fixes moved the landscape).
- **The after-seed-46 batch, pending in `results/pending/` (ORDER.md):** (1)
  primfirst - every PRIMITIVE together at the start of the dictionary,
  PRIMITIVE? by address in every COMPILE,, the classic [link][count][name]
  headers back (Iterations 232-234's layout reversed; the walk's 6-8% regained).
  **It changes kernel.4: reseed after applying.** More may follow (below).

### Processing a returned seed

Iteration 213's ten steps, unchanged, with: the gate script takes the run's front
and the joint front ("The front of all runs together" in compare-fronts.md);
`lab/evolve/names-check.py` (every design kind and all 14 stages) belongs with
run-tests after applying a batch; reseed when a patch changes kernel.4.

### The owner's standing decisions (added since Iteration 213)

- **No limits a developer could hit** (Iteration 237): e.g. 32-bit dispatch
  offsets, not 16; opcode maps not narrowed to 8 bits.
- **Developer friendly** (Iteration 227): core words in the kernel, helpers where
  convenient in balance with size, reusable non-standard words keep their names;
  splitting a long word for understanding, testing, extending is a plus.
- **Primitives together at the start of the dictionary** (Iteration 242);
  headers stay link-name-code (Iteration 243: the walk reads the link at a fixed
  place).
- UTF-8 word names must work (Iterations 231-242).
- A zero divisor is -10 THROW, an uncaught THROW names its code (Iteration 229).
- Deferred, captured in GOALS.md's register: packed names, hidden internal
  names, a compressed image (on-disk bytes that do not run - should they count?).
- Run lengths: seeds 44-45 6 hours, seed 46 10 hours - ask for the next.

### Open items (roughly by value)

1. Seed 46: process (the routine), apply the after-seed-46 batch (reseed).
2. Bit 7 of the count byte: read now only by >NAME, which no compiler uses -
   an exact >NAME (the dictionary walk) frees it (the owner wants the bit).
3. Calls and returns at the fast end: the C baseline (results/c-baseline-*.md)
   puts the fastest design 16.8x C on ackermann, 5.1x on fib, against 1.7-3.5x on
   loops - price a cheaper call/return in JIT code by instruction counts.
4. Trim the zero-divisor cost (+96-192 engine bytes, +64 image).
5. The laptop's: `sh lab/evolve/jitstack-inner-sweep.sh` (the JIT stack cache,
   Iteration 219), `perf stat` on IP-update chains and branch misses (Ertl &
   Paysan), instruction replication, `python3 lab/evolve/c-baseline.py`.
6. The owner's decisions above; search-method ideas from the outside reviews (a
   higher-mutation run instead of stopping; a gene-interaction study).

### Lessons added since Iteration 213

- A background job dies when the chat's turn ends - finish and poll within it.
- Never run two evolver processes on one tree at once (E.setup races on
  build/evolve/reference).
- In cross-compiled kernel code `[']` compiles a START-relative number, which the
  converter cannot know for an address - use a variable's address instead.
- The converter swaps every X8 body into X: a new kernel word X collides with an
  overlay's X8 (NEXT-NFA vs NEXT-NFA8) and --drop-x8 then drops X8's name.
- New dump-tool words must be in layout.py's DUMPTOOL, or the dump tool stays in
  every image (+662 bytes once).
- After a header or lookup change, count dispatches (the profiler is
  deterministic): a "correct" fix cost the small designs 6-8% unseen by the gate.
- Engine size changes hide in the code: a table halved can come back as code
  (the first DISPOFF form, +400 bytes) - measure the file, not the table.

### Where things are (added)

- `lab/evolve/names-check.py` (UTF-8 names, all stages), `lab/evolve/c-baseline.py`
  with `bench/c/bench.c` (the benchmarks in C), `results/price-*.md` (priced
  ideas: names, lookup cache, stencils and Bloom filter, JIT stack...),
  `results/c-baseline-x86-64.md`.
- Batches: `results/applied-after-seed43/` .. `applied-after-seed45/`,
  `results/pending/` (after seed 46).

## Iteration 244 - 2026-10-13 - Claude

**Bit 7 of the count byte freed, and a POSTPONE fault found on the way (the
second after-seed-46 patch).** With no compiler asking >NAME (Iteration 242),
its scan for the marker bit was the only reader of bit 7 - but not the only
user of >NAME: the kernel's (POSTPONE) read the IMMEDIATE bit through it every
time it ran. So Iteration 242 left a fault: POSTPONE of an immediate word with a
UTF-8 name (`ёж2`: the scan stops on 0xB6, bit 6 clear) compiled it instead of
running it. Now POSTPONE decides when it compiles, by FIND's flag, and
(POSTPONE) only compiles. The kernel's own POSTPONEs are compiled by cross.4,
whose target POSTPONE now reads the target header's flag: T-IMMEDIATE? walks
the thread the name hashes to (all 32 threads cost the kernel workload 7.7%,
one 0.6%). Nothing sets bit 7 any more (HEADER, HEADER8, cross.4's "HEADER, the
converter masks it).

>NAME itself: exact means a walk of the word lists, so it was measured both
ways - in the kernel (+32 bytes on byte-header designs, kernel workload +2%) or
out of it, in coreext.4 beside NAME>STRING and TRAVERSE-WORDLIST (images 64-136
bytes smaller than patch 1 alone, corpus -0.26%). Out of it: no compiler needs
it, the standard's name tokens are in coreext.4, and the tracer (TRWALK names
every word past the image) and the SPN diagnostic walk for themselves. The
owner's choice was invited: keeping it in every image costs about 100-230
bytes. names-check now checks bit 7 clear (through LAST) and POSTPONE of UTF-8
words; every check passes (results/applied-after-seed57/ORDER.md). Lesson: when a fix
removes a reader of a header bit, grep every reader of the word that read it.

## Iteration 245 - 2026-10-13 - Claude

**Calls and returns at the fast end, priced (results/price-jit-calls.md).** The
JIT already calls with the machine's call and ret (eight instructions a pair,
returns predicted); its 16.8x C -O2 on ackermann and 5.1x on fib match C -O0
(13.4x, 5.2x) - the gap is what an optimizing compiler does around calls (tail
calls into jumps, registers), not the call. A JIT tail call - a call to a native
word followed by EXIT, or a BRANCH chain to it, translated as a jump - would
remove about 9 of ~35 instructions a -ack call runs (two of its three calls):
an estimated 15-25% on ackermann, nothing on fib, 3-4% on the geometric mean
for JIT designs. Proposed as a gene, jittail, for the owner to decide.

## Iteration 246 - 2026-10-13 - Claude

**The gene jittail (the third after-seed-46 patch).** Iteration 245's pricing,
built: in engine/jit.c a call to a native word followed by EXIT, or by a BRANCH
chain to one, is translated as S_BRANCH aimed at the callee - its ret returns to
our caller. The first form cost +352 engine bytes (the tail test inlined in two
loops); decided once per call and remembered, +256. Timing needed care: short,
unalternated runs read -5% and then +3%; alternated over 15-25 rounds,
ackermann is 15-18% faster and fib, corpus, loop, bubble within noise - about
3% on the speed objective for JIT designs. Checks: the suite 14 of 14 on two JIT
designs with the gene; a 3-million-deep tail recursion runs in place; builds
without jitx, without jitloop, with jitos; off, the engine byte-identical. The
price write-up has the measurement. Lesson: on the VM, time two engines
alternately, many rounds, before believing a difference.

## Iteration 247 - 2026-10-13 - Claude

**The zero-divisor check, measured (open item 4).** Built with DIV0_CHECK
emptied, the engines are smaller by 160 bytes (add5ec8937), 96 (cc6d168e0a,
28677d13b1, f20de05a64) - UM/MOD's test of the divisor and THROW's set-up,
whose dispatch is inlined (FILLNEXT with the cached top); no superinstruction
copies it in these designs. A trim would route that dispatch through a shared
one instead (and share the set-up with LSAVE's fallback where SPEC loc has
it): an estimated 30-60 bytes, 0.2-0.4% of the smallest designs' total. Not
built: small, and it touches the generators' dispatch macros (gen-tos.py,
gen-super.py) - the owner's call.

## Iteration 248 - 2026-10-13 - Claude

**Seed 46 processed; the after-seed-46 batch applied; seed 47 set for 6 hours
(the owner).** Both packs clean (tests PASS, 7 of 7 IDENTICAL, the jail PASS).
The evolution ran 8 h 10 min, generations 0-186, 46,498 designs. The
comparison's verdict: fastest -1.1%, smallest +0.15%, memory +2 KB,
hypervolume +6.4%, best Q -3.4% - not small. Predictions three of five (jitos
on none of the front; not small) - `results/predictions.md`, with seed 47's.
`results/evolve-amd-ryzen-7-pro-8840hs-seed46.md` has the facts.

**The run's real news: every tail design died** - 222 "engine did not
compile", all with the gene tail. Iteration 237's dispatch offsets: gen-tail.py
reads the source after `cc -E`, where its own `#ifndef DISPOFF` guard is
already gone, so the tail engine's table was differences between functions,
which C cannot initialize. My gate then had no tail design on the fronts, and
the suite's tail design was a multi-state one (another generator). Fixed as the
batch's fourth patch: build_tail preprocesses with -DDISPOFF=0; two of the dead
designs (cb0545f94f, c1591d9cf8 - the second with jitos) now pass the suite.
Lesson: an engine change is tested on every generator's engine (tail, tos, msc,
super, JIT), whether or not the front has one.

Applied in order (results/applied-after-seed46/ORDER.md): primfirst, nobit7,
jittail, tailfix; reseeded (the cell kernel 27,264 bytes, a fixed point; the
4-byte kernel identical from both seeds). Build, run-tests PASS, 7 of 7
IDENTICAL; seed 46's front and the joint front alive with the new code, 148 of
148 (127 and 72, 51 in both); the suite on 12 of seed 46's front (smallest,
fastest, least memory, Q-best, and across the fsys levels) and the two tail
designs: 14 of 14 each, 0 differ from s6 (2,119 tests, 0 failed).

NEXT-RUN: `seed 47 tag2 6h then experiment compare-fronts.py --rounds 6
--frontier --cpus 2,8`. The state for a new chat: Iteration 243's HANDOFF, with
seed 47 now the run, the after-seed-46 batch applied, and results/pending
empty.

## Iteration 249 - 2026-10-13 - Claude (entry written at Iteration 366, from its commit)

**lab/evolve/engines-check.py**: s6 taken down every engine generator's path (19), each built and
its corpus run; part of run-tests, so a broken generator stops the laptop before a run rather than
costing the run's tail, as seed 46's was lost.

## Iteration 250 - 2026-10-13 - Claude

**A gene-interaction study, from seed 46's own mutations**
(`results/gene-interactions-seed46.md`, `lab/evolve/gene-interactions.py`): the
6,547 single 0/1 flips that change nothing else expressed, each gene's effect
split by every other gene in the parent. The JIT is a regime - rtloop is 33%
faster without it and 62% with it, -fno-gcse costs 18% without it and nothing
with it, interpreter genes are nearly neutral under it; within the interpreter
interactions are weak (t 6-8, all with ipaclone). The crossover links stand:
the JIT's genes must inherit together, and the one other synergy, rtloop, is
fixed already (all 45 JIT designs on the front). The zero-divisor trim stays
priced and unbuilt: one copy of a short path, shared only by restructuring the
cached-top engine's spill convention - not worth its risk for 30-60 bytes.

## Iteration 251 - 2026-10-13 - Claude

**The stack header captured, not built (the owner): GOALS.md's register.** And
the last engine finding of open item 8, measured: output lost when a signal
kills the engine. A zero divisor is -10 THROW now and UM/MOD's quotient
overflow cannot trap (udiv reduces the high cell first), so SIGFPE is gone; what
is left is SIGSEGV - `0 @`, a runaway pointer. The guard gene's handler flushes
the engine's output and reports (status 70) - but guard is on 13 of seed 46's
127 front designs: the other 114 die of a bare SIGSEGV, and those whose engine
buffers output to a pipe or file lose what they wrote before it (fe3c9c3940,
3bb2087f9d: "before the fault" gone; 3456ac1e5e at fsys 3 writes through and
keeps it). guard costs 448 bytes on the smallest design, 256 in the middle, none
at the fast end - it brings guard pages and five messages, and the objectives
never see a crash, so evolution drops it. A handler that only flushes and
reports, in every engine, would be ~100 bytes (an estimate); the Forth-side
buffers of fsys 4-5 would still be lost. The owner's call: leave it to the gene,
or make the minimal handler mandatory as the zero divisor was.

## Iteration 252 - 2026-10-13 - Claude

**A fault handler in every engine (the owner: as most reasonable; the first
after-seed-47 patch).** Iteration 251's choice, made: mandatory, as the zero
divisor's THROW was - the objectives never see a crash, so a gene would be
dropped (guard is), and a program's output surviving its own bad pointer is
what a developer expects. Without the guard gene the engine now catches SIGSEGV,
flushes (t_flush - the engine's buffer and fsys 4-5's Forth-side one), reports
and exits 70. The first form, through the runtime's general sigaction, cost
+384 bytes - nearly guard's own 448; the runtime's new rt_fault fills the
kernel's struct in place, SIGSEGV alone (the engine maps no file, so no
SIGBUS), and the handler uses the exit already linked: +128 to +160. Checks:
run-tests (19 generator paths), validation, the gate 148 of 148, the suite on
four front designs. Pending in `results/pending/` until seed 47 is processed.

## Iteration 253 - 2026-10-13 - Claude (entry written at Iteration 366, from its commit)

**lab/evolve/progress-table.py and results/progress-by-run.md**: every run's extremes (fastest,
smallest and the rest, run by run) in one table - the data behind the progress charts.

## Iteration 254 - 2026-10-13 - Claude

**Factoring repeated code into helper words, priced: not worth it (GOALS.md's
register).** From the converter's call map of the smallest design (every
operation and call with its offset, every branch target), each word's body was
cut into runs with no branch, branch target, EXIT or return-stack word, and
repeated runs were factored greedily, a helper costing its header (~8 bytes),
its body and EXIT, each use a 2-byte call. By opcode names alone: 146 bytes
(0= with ABORT", POSTPONE patterns) - but byte for byte, with the literals and
inline messages that must match too: 12 bytes, 4 helpers. The image has no
real repetition left to fold. Also: lab/evolve/progress-table.py and
results/progress-by-run.md (Iteration 253) keep the per-run extremes behind the
progress charts; and the standard suite went over the rest of seed 46's front
on master's code: 115 more designs, 14 of 14 each, 0 differ from s6 - with
Iteration 248's twelve, all 127 of the front.

## Iteration 255 - 2026-10-13 - Claude

**Where the fast end's speed is held back, and a proposal for the owner.** The
fastest design's per-workload times against s6: bubble 0.076, loop 0.092, fib
0.137, corpus 0.189, kernel 0.322, ackermann 0.436 - ackermann (jittail, in
seed 47) and the kernel workload are the weak ones. The kernel workload,
profiled without the JIT: 56% of its dispatches in cross.4's own words, mostly
@-T and !-T moving cells a byte at a time. A fast path (the host's @ and ! when
the target's cell is the host's, little-endian) cuts the workload's dispatches
37% (1.73M -> 1.09M) and its time on the fastest JIT design 9%, building a
byte-identical kernel. It changes a selection workload - s6 gains most, so every
design's kernel ratio moves - so it waits as a draft:
`results/drafts/crossfast.md` and `.patch`.

## Iteration 256 - 2026-10-13 - Claude

**The routine's ad-hoc scripts, tracked.** Steps 3 and 8 of processing a
returned seed ran from scripts in /tmp, rewritten each time and lost with the
chat. Now: `lab/evolve/seed-facts.py DB RESULTS` (step 3 - statuses, deaths by
cause with the gene values a cause's designs share and the living lack, the
screen, children by how made, the attic, the front's thirds and main genes, the
repeat rates) and `lab/evolve/gate.py RESULTS COMPARE` (step 8 - the run's front
and the joint front built and run). On seed 46 the facts tool names the tail
loss by itself: "died: engine did not compile - 222: shared, and rare among the
living: tail=1 (222 of 222; alive with it: 0 of 36705)". The routine, for a new
chat (Iteration 213's ten steps, with these): step 3 `seed-facts.py`; step 7's
run-tests now builds every generator's path (engines-check, Iteration 249);
step 8 `gate.py`; step 9 `ans-check.py --ids` (it ran the whole of seed 46's
front in minutes - all 127 is affordable).

The smallest engine audited for bytes (3456ac1e5e, 7,112): the interpreter
3,448, main with load_image 791, the dispatch and escape tables 512 each, the
runtime's wrappers 25-101 each (syscall 101, open 95 - variadic). Nothing
large to cut without design changes: a 32-bit magic compare instead of memcmp
(~35 bytes) and a non-variadic open in the runtime (~60) are the visible ones,
left for a batch that touches load_image anyway.

## Iteration 257 - 2026-10-13 - Claude

**The cross.4 fast path left (the owner agreed: it changes the yardstick, not
the designs - GOALS.md's register), and the fault handler paid for (the second
after-seed-47 patch).** Iteration 256's audit named two runtime costs; both
built: the image's magic as one 32-bit compare and a byte, so memcmp - its only
caller - drops out (42 bytes); the engine's opens through a three-argument
rt_open (x86-64 and i386 runtimes), so no va_list and no register save area
(open was 95 bytes). A first form aliased the variadic open to a three-argument
function - GCC warned of an uninitialised mode where it inlined a two-argument
call: undefined behaviour, replaced by an explicit OPEN3 in the engine. With
patch 1, engines are +56, 0 and -32 bytes against today (smallest, Q-best,
fastest). All checks pass (results/applied-after-seed57/ORDER.md).

## Iteration 258 - 2026-10-13 - Claude

**A gap check: options missed so far?** (`results/missed-options-2026-10.md`)
The inventory (genes, the register's 35 rows, the pricings) against current
interpreter literature, with an experiment where a gap showed. Found:
link-time optimisation across the engine and its runtime - 1.0-2.4% off
engines (-72 to -512 bytes), corpus right, interpreters' speed within noise -
but it changed the JIT's stencils (the JIT stopped translating: fib 2.5x, loop
3.9x slower), so a gene would compile spn-stencils.c outside LTO. Clang as a
compiler (CPython 3.14's tail-calling interpreter needed musttail and
preserve_none; the laptop and the VM have GCC 13.3, which has neither) - the
owner's call. Not worth it: -march=x86-64-v3 (sizes mixed), nibble-packed
operation runs (27 bytes). Everything else checked was covered already.

## Iteration 259 - 2026-10-13 - Claude

**The JIT's stack cache, a gene: jitk (the owner; the third after-seed-47
patch).** The hybrid stack/register design (Iteration 163) was priced twice and
built where its value was - run-time immediates and the keeping forms (fib
-36%); its JIT half, keeping the top cells in registers across copied code, was
deferred for the laptop's sweep (Iteration 219). The research sweep ranked it
first, so it is built as a gene instead. tools/gen-jitk.py (from Iteration 219's
jitvariants.py) writes, per build, a stencil for each of 16 hot data operations
in each cache state 0..K - the top in %rsi, the next in %rdx, the third in %rcx
- and a canonicaliser per state; engine/jit.c scans them with the base stencils
(each bounded by both tables) and plans every operation in one function both
passes share, so sizes and copies agree: a variant where there is one, else the
canonicaliser and the base stencil; every branch target in state 1. Checks: the
corpus and hand tests; the suite on three JIT designs at K=2 and 3, 14 of 14, 0
differ; run-tests (21 generator paths); 7 of 7. +2.3 KB (K=2), +2.8 KB (K=3).
On the VM: loop -9%, bubble -5%, corpus -4%, ackermann flat, fib +16% at K=2 and
flat at K=3 - this core disagreed with the papers before; seed 48 measures it
where it counts.

## Iteration 260 - 2026-10-13 - Claude

**The research sweep's findings, worked through (the owner): two more build
genes, the rest priced or covered** (`results/missed-options-2026-10.md`,
GOALS.md's register). Built - the fourth after-seed-47 patch: lto (the engine
and its runtime as one; the JIT's stencils compiled outside it, or the JIT
stops translating) - -32 to -160 bytes now that patch 2 took memcmp and the
variadic open; gotodup (GCC's max-goto-duplication-insns: default, 32, 128) -
interpreted engines +704-800 bytes for dispatch copied into more handlers, the
laptop to say whether it predicts better. Priced: the echo instruction - 283-427
bytes (3.3-4.9%) of the smallest image, new semantics in every engine, the
owner's call; mutation weighted by regime - ~1.4% of evaluations, not built.
Deferred: the IP-update loop form (the laptop's timing). Covered: JIT code apart
from written data, no section headers, the 6.17 kernel's exact peak memory.
The owner's: Clang or GCC 16 for preserve_none. All four after-seed-47 patches:
run-tests (25 generator paths), 7 of 7, 148 of 148 alive, a fresh clone
reproduces them.

## Iteration 261 - 2026-10-13 - Claude

**Clang beside GCC, tried (the owner asked whether both can live together).**
clang 18.1.3 installed on the VM (`apt-get install clang`; the laptop has GCC
13.3 only). The engine source needs no change for clang: interpreted designs
built and ran the corpus as they are; the JIT designs failed only on a GCC flag
clang rejects (-fipa-cp-clone, the ipaclone gene) - with the nine GCC-only
flags left out they built, and the JIT translated (fib 13-14 ms, as with GCC):
the stencils' shapes hold. -Oz first failed to link: clang turns memcmp() == 0
into bcmp, which the runtime lacks - after-seed-47 patch 2 removes the memcmp.
Engine bytes (3456ac1e5e, fe3c9c3940, 3bb2087f9d): GCC 7,112 / 16,828 / 21,276;
clang at the designs' own levels 10,256 / 17,868 / 25,788; clang -Oz (patch 2
applied) 8,624 / 17,772 / 20,396 - larger at the small end, 4% smaller at the
fast end. So a compiler gene is feasible and the results are design-dependent:
GCC-only genes (ipaclone, tracer, peel, nogcse, nocrossjump, align1, noreorder,
gotodup, jitos's optimize attribute, regpin's register variables) unexpressed
under clang; clang-only ones (-Oz; preserve_none with musttail for the tail
engine, clang 19+) unexpressed under GCC. Not built: it needs clang on the
laptop.

## Iteration 262 - 2026-10-13 - Claude

**The compiler as a gene (the owner; the fifth after-seed-47 patch).** compiler
(0 GCC, 1 clang): CC(g) names it at every engine compile - the tail engine's
preprocessing too, LTO's stencil objects - and ccflags gives clang -Oz for -Os
and only the flags it knows; express() drops GCC's own genes under clang, so
they cannot make look-alike designs. Offered only where clang is installed
(shutil.which at import): a design that names clang cannot be built without
it. clang is a build tool to the jail (BUILD_TOOLS), or it would be limited as
an engine. A bcmp in the runtime. Checks: engines-check 29 paths (clang plain,
JIT, tail, -Oz); run-tests; 7 of 7; the suite on two clang-built designs, 14 of
14. The laptop needs `sudo apt install clang` before seed 48 for the gene to
take part.

**A slip caught:** Iteration 260's commit took tools/gen-jitk.py into master
(created there, then `git add -A`) - so patch 3, which adds it, no longer
applied: the fresh-clone check of all five found it. Removed from master.
Lesson: write files for a pending patch in the scratch tree, never in master.

**An assembly engine (the owner asked):** not now. What it could buy is size at
the small end - the smallest engine's interpreter is 3,448 bytes of GCC -O2,
~27 a handler with the dispatch copied into each; hand-written handlers sharing
one dispatch might halve that (an estimate, ~1.5 KB, ~10% of the smallest
design). What it costs: a family of its own outside every generator - the
genes work by generating C (gen-tos, gen-msc, gen-tail, gen-super, the folds,
the JIT's C stencils), so an assembly engine starts with almost none of them,
and every engine change must be made twice. And the speed side is reachable
from C: Deegen's interpreter generated through LLVM with the GHC calling
convention beats LuaJIT's hand-written assembly interpreter by 31% - clang's
preserve_none with musttail is that convention, for the tail engine. So: the
compiler gene first, preserve_none next (clang 19); if the small end then
still wants bytes, price an assembly interpreter by writing its dispatch and a
dozen handlers and extrapolating, before building a family.

## Iteration 263 - 2026-10-13 - Claude

**The two small items revisited.** The zero-divisor throw path's own dispatch
replaced by a jump into NOOP's (DROP's in the cached-top engine, which pops the
-10 into the top as FILLNEXT did): engines -64, -32, +32 bytes - noise around a
15-byte saving, and the smallest got larger; -10 still caught. Not kept.

**The echo instruction, priced against its cheaper cousin.** An echo needs the
interpreter to know where a replayed fragment ends: a per-dispatch check, or a
second dispatch table switched in while echoing - a cost on all code, or a
second copy of every handler. The same bytes are mostly reachable without a new
opcode: the converter factoring repeated runs into headerless shared bodies
(Iteration 254's analysis, which found 12 bytes, charged each helper an 8-byte
header; bodies the converter makes and never names need none). Greedily, on the
smallest image: 154 bytes with 2-byte calls (40 helpers), 359 with 1-byte calls
where slots allow - against the echo's 283-427 before its handler. No engine
change; the price is a call and a return where a body is used, so the reference
profile keeps it off hot code. The next size candidate (GOALS.md's register):
a converter gene, `factor`.

## Iteration 264 - 2026-10-13 - Claude

**The gene factor, planned (results/drafts/factor-plan.md).** Where the pass
goes (layout.py, between the token fill and placement), how a factored body
becomes a word (a synthetic key past the dump, in Iteration 190's headerless
set, appended after (PRIMITIVES-END)), what stays out (branches and their
targets, EXITs, the return stack, aligned or relocated operands, words the
run-time compiler reads, hot words by the reference profile), and the checks.
Not built yet: the converter keys every map by a word's dump address, and the
change wants a session of its own rather than the end of this one.

## Iteration 265 - 2026-10-13 - Claude: HANDOFF - start here in a new chat

Read this entry, then Iteration 213's HANDOFF for what it says that is still
true (what this is, the environment), then `prompts/`. Everything is in the
repository.

### The state now

- master: Iteration 265. The after-seed-46 batch is applied (Iteration 248).
- **Seed 47 is RUNNING** on the laptop: `seed 47 tag2 6h then experiment
  compare-fronts.py --rounds 6 --frontier --cpus 2,8`, at Iteration 248's commit
  (c0bf29d) - the first run with jittail, tail working again, primitives first,
  bit 7 free. Predictions: the end of `results/predictions.md`.
- **The after-seed-47 batch, pending in `results/pending/` (ORDER.md), five
  patches, no reseed:** (1) faulttrap - a fault handler in every engine without
  guard; (2) lean-open - memcmp and the variadic open out of the engine; (3)
  jitk - the JIT's stack cache gene (adds tools/gen-jitk.py); (4) buildgenes -
  lto and gotodup; (5) compiler - GCC or clang. Checked together on a fresh
  clone (Iterations 252-262).
- **The laptop has clang now** (the owner, Iteration 265) - the compiler gene is
  offered only where `clang` is on the PATH. `apt install clang` on Ubuntu 24.04
  is clang 18; clang-19 (and 20) exist as packages - preserve_none needs 19+.

### Processing a returned seed

Iteration 213's ten steps, with the tracked tools: step 3
`python3 lab/evolve/seed-facts.py <pack>/db.jsonl <results file>` (it names a
death cause's shared genes - seed 46's tail=1 was found that way); step 5 the
results file first (the gate reads genomes from it); step 7 `run-tests.sh`
builds every generator's path (lab/evolve/engines-check.py, 29 paths with
clang); step 8 `python3 lab/evolve/gate.py <results file> <compare pack>/
compare-fronts.md`; step 9 ans-check on as many of the front as wanted (all 127
of seed 46's took minutes). Apply the after-seed-47 batch per ORDER.md, then
`lab/evolve/progress-table.py > results/progress-by-run.md` for the charts.

### The owner's decisions since Iteration 243

- Primitives together at the start; headers link-name-code; bit 7 free; >NAME
  in coreext.4 (Iterations 242-244). A fault handler mandatory (252).
- The kernel workload (cross.4) left as it is - a yardstick, not a design (257).
- Small gains count: size savings are exact - take them; speed ones as genes
  (261). GNU_STACK kept (251). The echo instruction priced; factoring first.
- Clang as a gene (262); an assembly engine not now (262's reasoning).

### Open items (roughly by value)

1. Seed 47: process; apply the after-seed-47 batch; NEXT-RUN for seed 48.
2. Build the gene `factor` (results/drafts/factor-plan.md): repeated code in
   headerless shared bodies, 154-359 bytes of the smallest image, converter only.
3. A tail engine with preserve_none + musttail (clang 19+): gen-tail.py's
   handlers and their table in that convention - after the compiler gene runs.
4. The laptop, after seed 47 (timing-sensitive, not during a run): `perf stat`
   (IP-update chains, branch misses); `python3 lab/evolve/c-baseline.py`.
5. The register (GOALS.md "Rejected or deferred"): packed names, hidden names,
   compressed image, the stack header, cross.4's fast path - the owner's.

### Lessons added since Iteration 243

- Files for a pending patch are written in the scratch tree, never in master:
  a stray new file there makes the patch that adds it fail (Iteration 262).
- An engine change is checked on every generator's engine (engines-check, now in
  run-tests) - seed 46 lost every tail design to one that was not.
- On the VM time two engines alternately, many rounds; single runs mislead.
- A compiler gene must be offered only where the compiler exists, and the jail
  must know it as a build tool (BUILD_TOOLS).

## Iteration 266 - 2026-10-13 - Claude

**Set up from the Iteration 265 bundle; engines-check shown to fail
(prompts/15).** A fresh VM (one CPU, dash as /bin/sh, the C locale) set up per
HANDOFF-PROMPT.md, gcc-multilib, clang 18.1.3 and clang-19 installed: the build
at both widths; run-tests PASS (661 cases on 26 stage runs, every negative
control caught; the generators 19 paths - master's count, 29 after patch 5
where clang is installed); 7 of 7 IDENTICAL. The after-seed-47 batch applies in
order on this master (its ORDER.md says after 252); patch 1 applied twice
fails.

engines-check (Iteration 249) had never failed: it was written after 248 fixed
the fault it exists for. On a scratch clone with that fix reversed (`git apply
-R --include=lab/evolve/evolve.py
results/applied-after-seed46/tailfix-after-seed46.patch`, then the build):
"tail calls (gen-tail) DIED died: engine did not compile", FAIL 1 of 19, exit
1 - seed 46's loss, caught; run-tests reads that exit status. --validate not
run broken again: its image comparison caught a flipped bit in Iteration 124
and has not changed since (169 added far=False to its corpus run). Shown red
by nothing yet, having no control of their own: ext-loops, the tracer's
self-test, DELETE-FILE, locals, the two saved-image checks.

Noted for seed 48: Iteration 248 set NEXT-RUN's seed 47 line without its
history comment; it goes in with seed 48's.

## Iteration 267 - 2026-10-13 - Claude

**The gene factor built, as a draft patch (results/drafts/factor-after-seed47-
draft.patch, on the five after-seed-47 patches); its first number audited; the
trade-off counted.** tools/layout.py's pass (between the tag's ranking and the
token fill), sod16.py's GAP, lab/evolve/hotwords.py and hotwords-v1.json, the
gene in evolve.py, two engines-check paths.

How a use is replaced: the call, then a GAP - an operation of the run's
remaining cells and no bytes (sod16 op_cells, op_bytes). Branch, loop-operand,
xt and DOES>-entry offsets are all old cell offsets and the locals literals are
found by adjacency, so nothing else in the word moves; one call in place of the
run would have shifted every offset after it (the plan did not say how).

A run: two to sixteen operations, none of them a branch, branch target, inline
operand, string, alignment, LITOFF, EXIT or RA word (I, J, EXECUTE, the loop
words), no call to a word that reads its caller's return address (sod16
ra_safe), neither half of a locals pair, the return stack balanced inside it
(rs_walk, superinstruction pairs expanded). Left out: primitives, the words
layout.py patches after reading (HOT_PATCHED), words with a DOES> entry, the
dump tool's, bss. Greedy by k x (len - 2) - (len + 1), lazily re-evaluated.

The first number - 16 image bytes against Iteration 263's 154 - audited on
3456ac1e5e by lifting one exclusion at a time (converter estimate / image): as
built 31 / -16; hot words in 124 / -120; the swapped compiler bodies in 38 /
-17; both 147 / -127; EXECUTE allowed, no change; calls reading the return
address allowed (not safe) 150 / -128; the return stack and loop words too (not
safe) 186 / -173. The hot-word filter was the gap; the safety rules cost 3
bytes beyond 147. The estimate runs ahead of the image (31 against 16, 147
against 127) - not explained yet; image bytes are what count.

Hot is a trade-off, counted (the profiler, deterministic; 3456ac1e5e, the six
selection workloads, geometric mean of dispatches): words below 0.01% of the
dispatches -17 bytes, +0.001%; below 0.1% -41, +0.007%; below 0.3% -65,
+0.028%; below 1% -95, +0.17%; every word -127, +1.98% (kernel +4.3%, loop
+4.3%, corpus +1.6%, bubble +1.7%). So four levels (FACTORV): 0 off, 1 below
0.1%, 2 below 1%, 3 every word - evolution weighs it. The swapped compiler
bodies take part: their xts resolve from the source's address plus an old cell
offset, which a GAP keeps; corpus and kernel workload right with them.

The reference profile: hotwords.py on five of seed 46's front that hold every
kernel overlay between them (3456ac1e5e, 5d7c8449aa, f179c75c01, d1ac6c88d8,
3bb2087f9d, the JIT off): 299 code words, 177 below 0.01%, 221 below 0.1%. A
word missing from the table keeps its code.

Checked: with the gene off, 14 front designs of different kinds convert to
byte-identical images and ids, master's converter against the patch's; the
draft applies after patches 1-5 on a fresh clone and reproduces its six files.
Not yet: run-tests with the two new paths, 7 of 7, names-check, the suite and
the corpus with the gene on - so a draft, not results/pending. prompts/17: the
gene touches evolve.py in six places and two constants; the gene table that
prompt asks for (Iteration 104) is still owed.

## Iteration 268 - 2026-10-13 - Claude

**The gene factor checked and pending: after-seed-47 patch 6
(results/applied-after-seed47/factor-after-seed47.patch, ORDER.md).** On patches 1-5, clang
18 installed: run-tests PASS (the generators 31 paths - the tag and the JIT
with factor=3); 7 of 7 identical; names-check PASS; the suite on 3456ac1e5e at
factor 1, 2 and 3 and on d1ac6c88d8 and 3bb2087f9d at 3: 14 of 14 each, 0 differ
(its negative control caught); at factor=3 all 127 of seed 46's front alive, at
1 and 2 the 14 of different kinds. The six apply in order on a fresh clone and
reproduce the tested files; the draft is out of results/drafts.

Image bytes against the gene off, 14 of seed 46's front (every kernel overlay,
fsys levels, engine families, the JIT): level 1 mean -52 (-39 to -74), level 2
-96 (-67 to -182), level 3 -133 (-88 to -269) - smaller at every level, every
design. Dispatches were counted on the smallest only (Iteration 267); the
laptop's timing decides the rest, through evolution.

The batch is six patches now; no reseed. Open: why the converter's estimate
runs ahead of the image; the gene table prompts/17 asks for (six touch points
for this gene); seed 47's routine when its packs come.

## Iteration 269 - 2026-10-13 - Claude

**Seed 47 processed; the after-seed-47 batch applied (six patches); seed 48 set
for 6 hours (the owner).** Both packs clean (tests PASS, 7 of 7 IDENTICAL, the
jail PASS); the measured-here patch is the laptop's usual stash, already on
master. The evolution ran 4 h 14 min, generations 0-89, 22,642 designs (18,549
alive, 3,968 screened). The comparison's verdict: fastest +2.5%, smallest
+0.05%, memory -2 KB, hypervolume +1.4%, best Q -2.1% - small, the first since
seed 44. Predictions three of five (tail on none of the front; small) -
results/predictions.md, with seed 48's. results/evolve-amd-ryzen-7-pro-8840hs-
seed47.md has the facts: no engine or corpus death (125 refused before running),
626 tail designs alive and none on the front, jittail on 27 of the front's 44
JIT designs, the smallest 7535695a36 at 15,808 bytes (-64), the fastest
e141550b9a at 0.164.

Applied in order (results/applied-after-seed47/ORDER.md): faulttrap, lean-open,
jitk, buildgenes, compiler, factor - no kernel change, no reseed. On master:
build, run-tests PASS (the generators: 31 paths), 7 of 7 IDENTICAL; the gate
152 of 152 alive with the new code (seed 47's front 124 and the joint front 77,
49 in both); the standard suite on 33 of seed 47's front (every fourth by size,
the smallest, fastest, least memory and the Q-best), 0 differ from s6, its
negative control caught.

NEXT-RUN: `seed 48 tag2 6h then experiment compare-fronts.py --rounds 6
--frontier --cpus 2,8`, with the comment Iteration 248 left out. New genes: the
stopping rule counts afresh. For the laptop: clang on the PATH before the run,
or the compiler gene stays dormant. The comparison is session 42 of
results/compare-fronts-amd-ryzen-7-pro-8840hs.md; results/progress-by-run.md
regenerated. The state for a new chat: Iteration 265's HANDOFF and the entries
after it - seed 48 running at this commit, results/pending empty.

## Iteration 270 - 2026-10-13 - Claude: HANDOFF - start here in a new chat

Read this entry, then Iteration 213's HANDOFF for what it says that is still
true (what this is, the environment), then `prompts/`. Everything needed is in
the repository: nothing from this chat or its uploads is - the seed 47 packs
are processed into results/, and the scripts this chat measured with are
tracked (below).

### The state now

- master: Iteration 270. The after-seed-47 batch is applied (Iteration 269, six
  patches: faulttrap, lean-open, jitk, buildgenes, compiler, factor -
  results/applied-after-seed47/ORDER.md); results/pending does not exist.
- **Seed 48 is the laptop's next run** (or running): `seed 48 tag2 6h then
  experiment compare-fronts.py --rounds 6 --frontier --cpus 2,8`, at Iteration
  269's commit (9029848) or this one - they differ in documents and two tools
  only. The first run with jitk, lto, gotodup, compiler (where clang is on the
  laptop's PATH) and factor; the stopping rule counts afresh. Predictions: the
  end of results/predictions.md.
- Seed 47 was small by all five measures (Iteration 269).

### Processing a returned seed (as done for seed 47, Iteration 269)

Iteration 213's ten steps, with the tracked tools; on this VM about 20 minutes
of machine time for build, tests and gates:
1. Unpack both packs (they arrive as `..._tar.gz`) into /tmp; tests.log PASS,
   validate.log 7 IDENTICAL, jail.log PASS, next-run.log times; `git apply -R
   --check` the pack's results-measured-here.patch (the laptop's stash, on master).
2. The comparison's "Judging the runs" verdict and the Q-best of all runs.
3. `python3 lab/evolve/seed-facts.py <pack>/db.jsonl <pack>/report.md`.
4. Score the predictions and write the next (results/predictions.md).
5. results/evolve-amd-ryzen-7-pro-8840hs-seedN.md: the verdict and facts, a
   `---`, then report.md - the gate and ans-check read genomes from it.
6. Apply the pending batch per its ORDER.md (reseed only when kernel.4 changes),
   then ONE background chain: build, run-tests (31 generator paths), --validate,
   `gate.py <results file> <compare pack>/compare-fronts.md` (152 of 152 for
   seed 47), `ans-check.py --ids <every fourth of the front by size, and its
   extremes>` (33 designs, 2.5 minutes).
7. `git mv results/pending results/applied-after-seedN`; the session appended to
   results/compare-fronts-amd-ryzen-7-pro-8840hs.md ("## Session K - Iteration
   I: seed N and seeds ...", the verdict line, then the pack's compare-fronts.md);
   `lab/evolve/progress-table.py > results/progress-by-run.md`; NEXT-RUN (the
   owner's hours, and a comment for the iteration); the PROGRESS entry; commit;
   `sh tools/make-bundle.sh /mnt/user-data/outputs`; present the bundle.

### The owner's decisions since Iteration 265

- Seed 48: 6 hours. The gene factor's four levels apply the standing rule
  (trade-offs as genes): its price was counted (Iteration 267) and evolution
  weighs it.

### Open items (roughly by value)

1. Seed 48: process (above). No batch is pending.
2. Why the converter's factor estimate runs ahead of the image (31 against 16,
   147 against 127) - explain it or drop the estimate line.
3. The gene table prompts/17 asks for: a gene now touches evolve.py in six
   places. Convert with every recorded id unchanged, checked over all results
   files before and after.
4. A tail engine with preserve_none + musttail (clang 19+), once seed 48 shows
   what clang engines do on the laptop.
5. The laptop between runs (timing-sensitive): `perf stat` (IP-update chains,
   branch misses), `python3 lab/evolve/c-baseline.py`.
6. The register (GOALS.md "Rejected or deferred"): packed names, hidden names,
   a compressed image, the stack header, cross.4's fast path - the owner's.

### Lessons added since Iteration 265

- A turn has a budget of tool calls (about fifty here): commit and bundle a
  checkpoint before long work - twice a turn ended with work only in /tmp
  (Iterations 267-268).
- Look in lab/evolve/ before writing a script: image-ab.py already measures an
  image change on one engine, with --set. A script that produces a recorded
  figure is tracked: lab/evolve/factor-price.py (267's curve) and gate.py --set
  (268's forced-gene check) are now; 263's /tmp/factor.py was lost with its chat.
- A check that had never failed was made to fail first (266: engines-check
  against 248's fault, reversed). Measure the artifact, not a tool's estimate of
  it (267: the converter's count against the image's bytes).
- A first number far below its price is audited by lifting one restriction at a
  time before anything is concluded (267: the hot-word filter, not the safety
  rules).
- When a family of engines is fixed, check that its designs live, not only that
  they compile (seed 47: 626 tail designs alive, none on the front).

### Where things are (added)

- lab/evolve/hotwords.py and hotwords-v1.json (factor's reference profile),
  lab/evolve/factor-price.py (factor's price on one design), gate.py --set,
  results/applied-after-seed47/.

## Iteration 271 - 2026-10-13 - Claude

**The handoff checked end to end (the owner asked).** From the Iteration 270
bundle, with HANDOFF-PROMPT.md's commands as written (in /tmp/hand for
/home/claude): the packages, the clone, the identity (a test commit carried the
owner's name, then was reset away), the build, run-tests PASS (31 generator
paths), 7 of 7 IDENTICAL. The newest HANDOFF a new chat finds is Iteration 270;
NEXT-RUN is seed 48 for 6 hours.

The chat's tools, run from that clone: `gate.py --set factor=1` on seed 47's
front and the joint front - 152 of 152 alive, the gene's first check on seed
47's designs; `factor-price.py 3456ac1e5e --shares 1e-3` - -41 image bytes as
Iteration 267 recorded, dispatches +0.008% against its +0.007% (the last digit,
not traced). Nothing from this chat is needed by the next: the packs are in
results/, the scripts behind recorded figures are tracked.

## Iteration 272 - 2026-10-13 - Claude

**The handoff made hard to lose (the owner asked).** Three ways information went
missing between chats, each with its fix:

- Work outside the repository: Iteration 263's /tmp/factor.py was lost with its
  chat; 267-268's work sat in a scratch tree when a turn ran out of tool calls.
  Now `tools/handoff-check.py` fails on uncommitted work, on a scratch git tree
  holding changes or commits master does not, and on any script, patch or Forth
  source in /tmp or /home/claude that matches no tracked file - unless listed in
  /tmp/handoff-disposable.txt with a reason.
- A handoff that goes stale: Iteration 265's entry said seed 47 was running after
  it was processed, and the prompt named that entry by number. Now HANDOFF.md:
  one self-contained file kept current (what 213, 243, 265 and 270 said,
  consolidated), the present beside this log's past. The check fails when its
  "master: Iteration N" is behind the last commit that changed NEXT-RUN,
  results/pending, an applied batch, a seed's results file or the prompt.
- Steps in nobody's file: the git identity (Iteration 270 put it in the prompt).
  HANDOFF-PROMPT.md now holds two messages: one to close the old chat (commit,
  track or discard, HANDOFF.md, the check, the bundle), one to start the new.

`tools/make-bundle.sh` runs the check and refuses a bundle a new chat could not
start from; `--checkpoint` makes one mid-work, named ...-checkpoint - not a
handoff point. From now on chats keep HANDOFF.md current; the HANDOFF entries in
this log remain its history. The previous chat's machine held one file not in
the repository (/tmp/factor.py), needed for nothing now: open item 6, optional.

The check shown to fail (prompts/15), one planted fault per rule in a throwaway
clone: an uncommitted change (1), a subject without "Iteration N:" (2),
HANDOFF.md saying 270 after a state change at 272 (3), the prompt without
HANDOFF.md (4), a scratch tree with an uncommitted change and with a commit
master lacks (5), a stray script (6), a pending patch ORDER.md does not apply
(7), NEXT-RUN without a line (8) - each failed alone, on its own rule; the clean
clone passed, and so did 5 and 6 with the item listed disposable with a reason;
a disposable line without a reason failed. (A first round was contaminated by
its harness - root-owned files in claude's clone survived the resets - and was
redone.) On this chat's real state it failed as it should: /tmp/fx, the factor
scratch tree, and eleven files. /tmp/fx-ident.py, behind Iteration 267's 14-of-14
identity figure, is tracked as results/drafts/image-identity.py; the rest are
listed disposable with reasons - superseded by factor-price.py and gate.py
--set, or one-off chains of tracked checks.

## Iteration 273 - 2026-10-13 - Claude

**The previous chat's leftovers filed, as found: results/drafts/chat-to-iter265/
(the owner asked that chat; its MANIFEST.md).** The chat that ended at
Iteration 265 still had its machine. It sent 51 scripts mapped to the
iterations and figures they produced (Iterations 241-264), its check jobs and
logs (244-262), its 23 /tmp patches (every one already in the repository, byte
for byte) and its 33 scratch trees as patches with their status. Among them
/tmp/factor.py - as found it is the exact-bytes version behind 254's 12 bytes;
the opcode-name version behind 146 was overwritten in place - and factor0.py and
factor1.py behind 263's 154 and 359. Nothing reconstructed: that chat said so
file by file. GOALS.md's register row and the factor plan point to them now.

My request had asked for Iterations 244-265, but that chat ran from 213: its
/tmp listing (the manifest's section 5) shows 84 more scripts and sources, of
Iterations 213-243 (facts43.py, gate44*.py, pages.py, job1-52.sh,
vm-lab-jitos.c ...), not packed. Asked for (HANDOFF.md, open item 6).

## Iteration 274 - 2026-10-13 - Claude

**The second archive filed, as found: results/drafts/chat-to-iter265/part2/
(its MANIFEST.md), and an index for both (README.md there).** Every one of the
85 scripts and sources of that chat's /tmp the first archive lacked (Iterations
213-243) arrived, with 11 more (source copies with other suffixes, three pk2-*.py
scripts), 47 job scripts and the 130 logs they wrote; 24 of its 226 files were
already tracked. Its notes: nothing is gone; elf.py (Iterations 250-251, behind
GOALS.md's 176 stack-header bytes) belonged in the first archive; names-check.py
there is the pre-fix copy the tracked tool grew from. It found iterations and
figures in two earlier transcripts its machine kept in /mnt/transcripts - on
this machine that directory is empty, so the repository stays the only record
that carries over. Nothing more is owed by that chat.

## Iteration 275 - 2026-10-13 - Claude

**The documentation audited (the owner asked): one home per fact, every document
indexed, the indexes checked.** 187 tracked documents. What changed:

- **GOALS.md, 922 lines to 155.** Three sections were snapshots of the state and
  the plan, written in Iterations 60-272 and never brought up to date ("Where
  things stand" stopped at seed 28, Iteration 106; "Next" pointed back at
  "Resuming in a new chat", Iteration 86). Moved out verbatim to
  results/drafts/goals-snapshots.md. What was still live stayed in GOALS.md,
  brought to date: the measures (the selection workloads of Iteration 127, the
  kernel-only size of Iteration 138), the five-measure rule of Iterations
  188-189 (the section still stated Iteration 78's three), the conventions (the
  handoff check, checkpoints, where things are written), the owner's later
  plans (the Tegra session, the article). The runs/ directory and the VM's four
  checks were already in RUNNING.md and HANDOFF.md.
- **Indexes.** README.md's new "Documents" section lists every document once;
  results/README.md (was: the stage runs and seed 1) every measurement, analysis
  and per-run record, by topic, with each file's own title; lab/evolve/README.md
  opens with its 36 tools, each from its own docstring. HANDOFF.md's "Where
  things are" points to them instead of keeping a list of its own, and its
  judging rule points to GOALS.md. A new chat now reads GOALS.md too
  (HANDOFF-PROMPT.md). README.md's corpus count was 616; it is 661.
- **The handoff check, rules 9 and 10**: every tracked document in an index and
  every indexed document there; every script of the evolver among its README's
  tools. On its first run it found two gaps (the second archive's manifest, and
  its own matching of seedN), fixed.
- **The VM's fourth check** - lab/evolve/test-jail.py, which the laptop runs
  before a run - is in HANDOFF.md's routine now; Iteration 269 ran three of the
  four before seed 48's bundle.
- **The prompts** (prompts/UPSTREAM, to carry back to relf): 07 - a session ends
  without warning, so every turn that changed the repository is a possible end;
  the present in one checked file; losing work a failing check; closing the old
  session before opening the new; recovering from a closed one, for its whole
  range. 12 - one home for the present. 15 - a planted fault must trip only its
  own check (the contaminated first round of Iteration 272). INDEX and README rows.

Left as they are, said so: lab/evolve/README.md and GENES.md both describe each
gene - the README as history, GENES.md as the reference - and overlap by design;
PROGRESS.md's old HANDOFF entries are history now; the article (on the
backburner) predates the evolution's results.

Rules 9 and 10 shown to fail (prompts/15, each fault planted from a clean state
in a clone owned by the user claude): a document in no index (9), an index
entry for a document that is not there (9), an evolver script missing from its
README's tools (10) - each failed alone on its own rule; the clone passed before
and after. lab/evolve/test-jail.py on master: PASS - with run-tests, --validate
and the build, all four of the laptop's checks have now passed on the code
seed 48 runs. bench/README.md's corpus count brought to 661; the findings,
GENES.md's iteration notes, the rehearsal and the article keep their 616 - they
are dated measurements, made when the corpus had 616 cases.

## Iteration 276 - 2026-10-13 - Claude

**Three open items closed (the owner: in the order that seemed right).**

**Why the factor gene's estimate ran ahead of the image: placement.** The
converter now encodes each changed word before and after the pass and reports
that, not a sum of operation sizes. On 3456ac1e5e at the cheapest level the
words' code is 141 bytes smaller and the bodies take 95: 46 before placement,
and placement gives 5 back (word starts realigned to cells, links resized):
-41 in the image. Every word factored: 355, 198, 157 before placement, 30
back, -127. factor-price.py prints the split. The last digit of Iteration 271
(+0.008% against 267's +0.007%): the dispatch counts are deterministic - two
full runs here identical on all six workloads, --raw - and the geometric mean is
+0.0075%, on the rounding edge; today's run prints +0.007%.

**The gene table (prompts/17).** A gene is one row - `gene(name, values, show,
family, late, needs, convert)` - read by LATE, EXPRESSED, mutate(),
random_genome(), express() and the converter's options; factor is the first,
its seven touch points one. The thirteen older genes with more than two values
have their values once, in GENE_VALUES, where mutate() and random_genome() each
had a copy; their express() rules and build code stay code (open item 4).
Nothing changed: 2,876 recorded genomes keep ids and expressions; 3,000
mutations, 1,000 random genomes and 1,000 crossovers, seeded, identical before
and after (the old evolve.py beside the new; two helpers that read build data
stubbed alike in both). gene-table-test.py: a fictional gene - values 0, 5, 7,
the tag only, a converter option - works with no code change (ids, expression,
90 mutations reaching it, every value drawn, its option), and its control (the
same row without a rule) is caught.

**The previous chats' scratch trees, sorted**
(results/drafts/chat-to-iter265/trees/SORTED.md): by the share of the lines
each tree's patches add that master holds today, 19 reached master, 2 mostly,
1 added nothing, 10 did not - three of them trivial, seven from Iterations
231-238 (names, a compressed image, unused stencils), unread. GOALS.md's
register points to them.

Checked on master with the table: run-tests PASS (the generators: 31 paths -
factor's two now built through the row's converter option), 7 of 7 IDENTICAL,
`gate.py --set factor=3` on seed 47's front 124 of 124 alive.

The handoff check refused the bundle on four scripts in /tmp - its job. The
equivalence test behind this entry's figures is tracked now, generalised:
lab/evolve/gene-equiv.py REV (the evolver against itself at an earlier commit,
read from git; a control reorders one gene's values and must be caught) - run
against HEAD~1 it reproduced the figures above and caught its control. The
other three are listed disposable with reasons.

## Iteration 277 - 2026-10-13 - Claude

**The ten unmerged scratch trees read (the owner asked): no lost work.**
Iteration 276 sorted the trees of the chats of Iterations 213-265 by the share
of their added lines in today's master, and ten came out under half. Measured
against the batches as applied instead, and read
(results/drafts/chat-to-iter265/trees/SORTED.md): seven are the after-seed-45
batch in the making - base45, fresh45b and p13 the names patch, fresh45c and
fresh45d the cell headers' fix, fresh45e and fresh45f later - every added line
in that batch but fresh45c's seven, a variant left for the X8 collision its own
comment names; primfirst (after seed 46) reversed their header layout, which is
why today's master shares little of them. ff is cross.4's fast path,
results/drafts/crossfast.patch line for line; ansall its first draft. ec is
Iteration 248's tail fix reversed beside engines-check.py being written
(Iteration 249).

**Corrected forward:** Iteration 266 said engines-check "had never failed: it
was written after 248 fixed the fault it exists for". The tree ec shows that
chat planted that very fault while writing it; no job, log or entry records the
run, so the true statement is that it had never been *recorded* failing -
Iteration 266's run is the first on record. Also corrected: Iteration 276's
GOALS.md note that the trees might hold prototypes of deferred ideas - none
does. HANDOFF.md's open item 5 is closed.

## Iteration 278 - 2026-10-13 - Claude

**The laptop's measurements made runnable (the owner asked what they are).**
Open item 3 named `perf stat` - no tool did it - and c-baseline.py, which
`next-run.sh experiment` would have broken: it passes every database as an
argument, and c-baseline read them as design ids; its default designs dated
from Iteration 235. Now: lab/evolve/counters.py - perf's user-space cycles,
instructions, branches and branch misses for the newest front's fastest designs
with and without the JIT, its smallest, and s6, on the six selection workloads:
instructions per cycle and misses per thousand instructions - dispatch
mispredictions against the chain of instruction-pointer updates (Ertl & Paysan;
the IP-update loop form deferred in Iteration 260; gotodup's question). It
refuses, saying why, when perf is missing or a counter unreadable - shown here,
where there is no perf and a Firecracker guest has no counters; its parser
checked on perf's own output. c-baseline.py ignores database paths; both pick
their designs from evolve.newest_front(). RUNNING.md, "Between runs": install
perf once, `sudo sysctl kernel.perf_event_paranoid=2` each boot, then `sh
lab/evolve/next-run.sh experiment c-baseline.py then experiment counters.py`.
Running c-baseline as next-run.sh runs it found newest_front without its glob
import - fixed before any laptop met it.

**31 older genes into rows** (GENES.md, "Adding a gene", says which, and what
stays code). gene-equiv.py now also judges by id and expression every genome it
makes - 3,000 mutations, 1,000 random genomes, 1,000 crossovers. Its first run
against the commit before: 875 recorded designs changed id - all rtfuse=0 leaving
the identity: gene() put rtfuse, older than LATE, into it by default. Fixed
(late=False), and gene() now refuses an already-listed gene whose row misstates
its late-ness. Then: every id, expression and seeded draw the same; the fictional
gene's test PASS.

Checked: 24 front designs' images byte-identical built before and after the
conversion (the five converter flags moved; results/drafts/image-identity.py in
both trees), ids too; c-baseline.py run exactly as next-run.sh runs it, with two
database paths, picked today's designs itself (e141550b9a, 037722ab8a, the
smallest) and finished; run-tests PASS (31 generator paths), 7 of 7 IDENTICAL.

## Iteration 279 - 2026-10-13 - Claude

**perf's setting changed for the measurement only (the owner: linux-tools
installed, no global sysctl change).** counters.py now raises
kernel.perf_event_paranoid itself: it reads the value; if above 2 it asks sudo
once - the prompt and its messages on the terminal, since next-run.sh sends the
tool's output to files - sets 2, keeps sudo's credentials fresh between designs
so the restore needs no password, and puts the old value back when it ends,
reading it back to check: normally, on an error, on Ctrl-C, SIGTERM or SIGHUP.
A restore that fails is said on the terminal with the command that does it; a
reboot restores it anyway (the setting is not saved). The chain now runs
counters.py first, so the prompt comes at the start: `sh lab/evolve/next-run.sh
experiment counters.py then experiment c-baseline.py` (RUNNING.md).
lab/evolve/counters-test.py, as root with a stand-in sudo, from Ubuntu's 4: a
normal end, an error, SIGTERM, SIGHUP, Ctrl-C (2 during, 4 after, exit 143, 129,
130), the setting already 2 (no sudo), sudo refused at the start (nothing
changed), a restore that fails (said, with the command) - 8 of 8; the VM's own
setting put back.

## Iteration 280 - 2026-10-14 - Claude

**Housekeeping while seed 48 runs (the owner asked).** Checked: no tracked file
an ignore rule matches, no caches, objects or editor debris tracked; 1,321
tracked files, 26 MB, the history packed to 5.5 MB - everything large is records
(the comparison history 2.2 MB, the per-seed results, the owner's Forth
collection), so nothing to delete for size, and deleting would not shrink the
bundle anyway: the history keeps every version. The living documents scanned
for paths no tracked file satisfies: of ten, eight point outside the repository
or are placeholders; two corrected - stages/STAGES.md's ENCODING-COMPARISON.md
is said to be a note this repository never held (the log does not say whose),
and GENES.md's tools/test-sysc-shell.sh is said to be gone since Iteration 169,
run-tests.sh's shell suite running every SYSC shell. The laptop's clone (seed
47's pack, repo-files.txt): runs/ 125 files, 138 MB - the only copies of each
run's database; old bundles in ~/Downloads can go, every one but the newest.

## Iteration 281 - 2026-10-14 - Claude

**The Forth sources audited again (the owner asked): one missed opportunity,
priced; size nothing new** (results/source-audit-2.md). Searched, not recalled:
each hot word of the five-design profile against what a gene can reach. 2@, 2!
and DEPTH reach nothing - in no ops10 pool, tiny family or opbody list, though
Iteration 131 counted on "the opcode genes" for 2@ and 2!. Counted exactly with
a new tool, lab/evolve/word-cost.py: in bubble, 2@ and 2! take 16.3% of the
dispatches on s6, 16.1% on the smallest, 41.6% on c9369657e4 (seed 47's fastest
without the JIT); DEPTH 0.8%, 0.5%, 5.2% of the corpus. bench/bubble.fth's inner
loop calls 2@ three times and 2! once; tester.fr DEPTH ten times - code compiled
at run time, so through opbody's [opcode EXIT] two thirds of it: bubble -11% to
-28%, about -5% of c9369657e4's geometric mean in dispatches. A patch for after
seed 48 (HANDOFF.md, item 2). Rechecked and standing: the lookup (threads,
klookup), the loop and scan words (ops10), > 0= 1+ 1- (tiny), INTERPRET's
control flow; NUMBER?'s digit table, rejected in 144 for its 256 bytes, reopens
as a possible gene under "trade-offs as genes". Size: the smallest image is
32% headers and padding (2,765 of 8,696 bytes) - the register's packed and
hidden names, the owner's; its largest bodies are needed words; 42 words never
run (672 bytes) are error paths and file words. prompts/02: fifteen recalled
optimizations, every one already built, priced or in the register; the search
found the one new.

## Iteration 282 - 2026-10-14 - Claude

**counters.py's first laptop run failed, safely; the chain fixed.** The owner ran
`next-run.sh experiment counters.py then experiment c-baseline.py`: build,
run-tests (31 generator paths), 7 of 7 IDENTICAL and the jail all passed at
Iteration 281's code; then sudo, asked from inside the chain, "unable to read
password: Input/output error", and counters.py stopped saying "nothing changed" -
the setting untouched, c-baseline.py never started. The cause: next-run.sh runs
its chain detached (nohup, stdin /dev/null, an orphaned job); Iteration 279 had
said the tools ran in the foreground, from a grep that found no nohup - wrong.

Now next-run.sh, before it detaches, when counters.py is in the chain and the
setting is above 2, runs lab/evolve/perf-hold-start.sh: sudo asks once, at once,
and lab/evolve/perf-hold.py is left as root (sudo -b; hang-ups ignored from the
fork, a session of its own). It changes nothing until counters.py writes its pid;
sets 2; restores when counters.py says done or its process is gone (kill -9
included), after two hours at most; gives up unchanged if counters.py never
starts within four. counters.py's PerfHold speaks that protocol in the chain;
run in a terminal it still asks sudo itself (PerfAccess). Shown:
counters-test.py 14 of 14 (the eight of 279, and the chain - the helper with
PerfHold, kill -9, a chain that failed first, perf-hold-start.sh with the setting
already 2, with no terminal, in a terminal by script(1)); and counters.py itself
end to end, for the first time anywhere, as the chain runs it - detached, no
terminal, a stand-in perf: every design built and run, its table written, the
setting 2 for eight seconds (04:05:54-04:06:02) and 4 after.

Three faults of mine on the way, each caught: `pkill -f perf-hold.py` killed the
shell running it, its pattern in that shell's command line; tests run alongside
each other moved the one global setting under each other and killed each other's
helper; the stand-in sudo let a pty's hang-up kill its child before it ran,
where real sudo -b keeps the command apart from the terminal's foreground group.
HANDOFF.md's lessons have the first two.

## Iteration 283 - 2026-10-14 - Claude

**counters.py's second laptop try: the setting held and restored, perf itself
failed - and its words were lost.** The owner's log: sudo asked before the chain
detached, the checks passed again, perf-hold.py raised and restored the setting
("kernel.perf_event_paranoid is 4 after the measurement") - Iteration 282's fix
works on the laptop. Then "s6 on kernel exited 2": perf's very first run. Not the
engine or the workload - run-tests and --validate had run s6 on the kernel
workload minutes before - but perf: Ubuntu's perf is a wrapper that exits 2,
printing which package to install, when the tools for the running kernel are
missing; counters.py captured that message and reported only the code.

Now perf is tried first: perf-hold-start.sh runs `perf --version` in the
foreground, before sudo or anything detaches, and on a failure shows perf's own
lines and `sudo apt install linux-tools-$(uname -r)` - nothing started;
counters.py runs `perf stat` on `true` before it builds any design, and every
perf failure it reports carries perf's own output. Shown with a stand-in for
Ubuntu's wrapper: perf-hold-start.sh refuses before sudo with perf's words;
counters.py stops before building anything (0 designs) with the same.
counters-test.py now carries a stand-in perf, working or broken: 15 of 15.
Unconfirmed until the owner runs `perf --version`: that the tools for the
laptop's running kernel are what is missing.

## Iteration 284 - 2026-10-14 - Claude

**perf on the laptop: the running kernel's tools have none.** Iteration 283's
guess confirmed by the owner: `perf --version` - "perf not found for kernel
6.17.0-1032", the running kernel 6.17.0-1032-oem. apt: linux-tools-6.17.0-1032-oem
"already the newest version" - installed, and the wrapper still finds no perf where
it looks (/usr/lib/linux-tools/$(uname -r)/perf); the cloud-tools and "oem"
meta-packages it names do not exist for that kernel. So counters.py's find_perf
(also `counters.py --find-perf`, which next-run.sh now asks in the foreground
and exports as PERF for the whole chain): $PERF if it runs; else `perf` if it
runs; else any perf binary under /usr/lib's linux tools, the running kernel's
first, then the newest - for user-space counts another kernel's perf does. Each
one tried and why it failed is said; the table names the perf used.
counters-test.py, 19 of 19: no perf anywhere (fails, saying what it tried and
the apt line), the broken wrapper with another kernel's perf installed (that
one), the running kernel's before a newer, PERF given (first). Still unknown:
what the OEM tools package installs, and whether any perf binary is on the
laptop at all - asked of the owner.

## Iteration 285 - 2026-10-14 - Claude

**The laptop's two measurements, in (the owner).** Both packs clean (tests PASS,
7 of 7, the jail PASS); perf 6.8.12, found by counters.py's search past Ubuntu's
wrapper (the OEM kernel's tools have none), counted on kernel 6.17 - the owner's
check showed it would; the setting 2 only while counters.py measured (05:13:50-
05:14:54), 4 after.

results/c-baseline-amd-ryzen-7-pro-8840hs.md: the fastest design (e141550b9a)
3.7x C -O2 on the geometric mean (2.8-5.1x), the knee 4.2x, s6 24.2x, the
smallest 29.1x - and 50x on parse, held out, where it has none of the parsing and
lookup operations; the engines start as fast as C.

results/counters-amd-ryzen-7-pro-8840hs.md: on compute work (fib, loop, bubble,
ackermann) every interpreted design mispredicts at most 0.54 per thousand
instructions - dispatch is predicted; yet the evolved interpreted designs run at
1.7-2.9 IPC to s6's 2.75-3.9: something serial - the IP chain or the stack through
memory, which four counters cannot split - so the IP-update loop form stays open.
New: on kernel and corpus the evolved designs mispredict 3.5-9.1 per thousand
instructions to s6's 0.4-0.7 - an estimated 9-24% of their cycles at 12-18 a miss,
s6's 1-3% - most likely the C operations evolution chose for that work, whose
loop exits depend on the data; which handlers is the next laptop measurement.
And the JIT mispredicts 1.5% of ackermann's branches - returns, probably. HANDOFF.md:
the owner's item done; items 4 and 5 new.

## Iteration 286 - 2026-10-14 - Claude

**Seed 49 set for 8 hours (the owner), before seed 48 is processed.** Seed 48 has
finished on the laptop; its packs have not come back yet, and they are safe there:
clean-runs.sh removes pack tarballs only past the newest eight, and the laptop has
made two since (the counters and C-baseline packs), seed 49 and its comparison two
more. Seed 49 carries its fronts from the laptop's own archives, so it needs nothing
from the processing; it runs the same genes as seed 48 (no batch between), longer.
NEXT-RUN: `seed 49 tag2 8h then experiment compare-fronts.py --rounds 6 --frontier
--cpus 2,8`. Its predictions are written now, before its run and without seed 48's
results (results/predictions.md). The 2@, 2! and DEPTH patch moves to after seed 49.

## Iteration 287 - 2026-10-14 - Claude

**Seed 49 started (the owner) - and two small confusions it showed.**
`the evolution stops at 04:34` looked like a stop before the start: next-run.sh
prints that one time in local time (the laptop's: US Pacific) where every log line
and file name is UTC - 04:34 Pacific is 11:34 UTC, 8 hours less the 113 minutes
kept, from 05:28 UTC. Now it says both. And next-run.sh stashed
results/c-baseline-x86-64.md: c-baseline.py named its file by platform.processor(),
'x86_64' on any Linux PC, so the laptop wrote over the VM's. Now it names it by the
CPU's model, as results/ does (on the laptop: c-baseline-amd-ryzen-7-pro-8840hs.md,
the file Iteration 285 filed). Seed 49's results-measured-here.patch will carry that
hunk; HANDOFF.md says to leave it out.

## Iteration 288 - 2026-10-14 - Claude

**Seed 49 processed; seed 50 set for 12 hours (the owner).** Both packs clean (tests
PASS, the generators 31 paths, 7 of 7 IDENTICAL, the jail PASS); the measured-here
patch the laptop's usual stash (it reverse-applies) and the c-baseline-x86-64.md
hunk left out, as Iteration 287 said. The evolution ran 6 h 03 min, generations
0-146, 36,868 designs (28,022 alive, 8,643 screened); 203 deaths, all refused
before running. The comparison's verdict: fastest -4.1%, smallest +0.00%, memory
-4 KB, hypervolume +4.0%, best Q -3.9% - not small. The Q-best of all runs is seed
48's 4599c1f454 (Q 0.216); in the run the fastest 0.128, the smallest 15,672 (-136
under seed 47's), the least memory 116 KB, the least of any run. Seed 48's genes
took the front: factor on 161 of 172 (level 3 on 96; on 56 of the small third's
57), lto on 111 of the 154 GCC-built, clang on 18, jitk 3 on 23 JIT designs,
gotodup on 24. Predictions three of four (not small, where "small" was said);
seed 50's written.

Seed 48's packs have still not come back. Its database is in this comparison as an
archive and its front's genomes in seed 49's as carried records, so gate.py now
takes --db FILE for genomes no results file holds yet; its results file waits for
its pack, which clean-runs will remove when seed 52 starts. On this master: the gate
220 of 220 alive (seed 49's front 172, the joint front 109, 61 in both); the
standard suite on 37 of the front, 0 differ from s6, its negative control caught.
NEXT-RUN: `seed 50 tag2 12h then experiment compare-fronts.py --rounds 6 --frontier
--cpus 2,8`; the comparison is session 43; results/progress-by-run.md regenerated.

## Iteration 289 - 2026-10-14 - Claude

**Seed 50 started (13:49 UTC; the evolution stops 23:55 UTC, "16:55 here" - the
two-clock message works). Seed 48 left without a record, the owner's choice.** The
owner had not run what NEXT-RUN called seed 48 as such, he thought that iteration
the perf measurements' - yet a run went from Oct 13 21:01 UTC to about 03:00,
archived as runs/archived-20261014-052835, and seed 49's comparison holds it, the
Q-best of all runs among its designs; seed 49's pack cannot say which seed it ran
(repo-files.txt lists no runs/). Nothing is re-run: its designs live on in seed 49's
database and the comparisons; its own pack, results file and predictions' score
are given up.

## Iteration 290 - 2026-10-14 - Claude

**2@ and 2! as opcodes, pending as the after-seed-50 batch's patch 1
(results/applied-after-seed57/ORDER.md) - the second source audit's finding built.** Their
handlers in vm-lab.c, gen-tos.py and gen-msc.py (gen-tail.py takes them as it finds
them; the JIT leaves a word with an opcode it cannot translate to the interpreter),
their kernel bodies in sod16.py's table as the converter reads them (SOD16_SHOW: 2@
`DUP CELL+ @ SWAP @`, 2! `SWAP OVER ! CELL+ !`), the pool, the labels and opbody's
list, five engines-check paths. DEPTH left out: its handler would have to agree with
the kernel's S0 through ABORT and saved images, for the corpus's few per cent.
Measured: c9369657e4's bubble 12,759,474 -> 9,572,364 dispatches (-25.0%), its
corpus -0.3% - about -4.7% on the geometric mean. Checked in a scratch tree:
engines-check 36 paths and run-tests PASS; gene-equiv.py - every recorded id and
expression the same, random draws and four mutations different, as a longer pool
must make them; the gate with the opcodes first in every list, seed 49's front: 172 of
172 alive. The patch applies on a fresh clone and reproduces the tested files.

On the way, gate.py's --set learned lists, and the first try built nothing: appended
to lists that already filled their designs' opcode slots, the two words got none
(ops10_in hands the slots out in the list's order) - so a forced list's members now go
first, in gate.py and in word-cost.py (now with --set too); and a gate left running
when the turn ended came back empty. HANDOFF.md has both lessons.

## Iteration 291 - 2026-10-14 - Claude

**The pending 2@ and 2! patch gets the JIT's stencils.** Looking at item 1 of the
waiting list - the run-time compiler compiling an [opcode EXIT] word's opcode in
place of the call - showed a fault in the patch itself: jit.c translates a word only
if every operation in it has SPN stencils ("all or nothing"), and the two new opcodes
had none. A JIT design taking them would have left every word holding one to the
interpreter - 2@ and 2! themselves among them, which its JIT had compiled natively
as colon words - slower, never wrong, so engines-check could not see it. layout.py's
stencil table now has them: 2@ DUP ADDI FETCH SWAP FETCH, 2! SWAP OVER STORE ADDI
STORE, CELL+'s ADDI the one constant (8). Checked in a scratch tree: the fastest JIT
design, 927064f127, 70 of 129 operations translatable with them (69 without);
engines-check PASS; the gate on seed 49's front, the opcodes first, 172 of 172 (99 JIT
designs); run-tests PASS. The patch is regenerated and ORDER.md says so. Item 1 itself
- the converter putting the [opcode EXIT] words among the primitives, so that
PRIMITIVE? lets COMPILE,8 copy their opcode - is still to do.

## Iteration 292 - 2026-10-14 - Claude

**The gene opinline, pending as the after-seed-50 batch's patch 2: the [opcode EXIT]
words compiled as their opcode at run time.** PRIMITIVE? asks by address - below
(PRIMITIVES-END) - and every COMPILE, copies a primitive's body: the cv8 and cv8t
overlays one byte or the escape's two, cpt16 one token; cv8t-empty.4's PRIMITIVE? 0=
leaves primitives alone. So layout.py --op-inline places the words its [opcode EXIT]
loop made - the base list, and opbody's - before the marker, a word defined once only (a
later definition of a name must stay the one FIND finds). A gene, late, off at 0: moving
the base list's words unasked would change what recorded designs build under their ids.
It is expressed only where a design has such a word. Measured on c9369657e4 with patch
1's opcodes and opbody: bubble 9,572,364 -> 7,448,901 dispatches (-22.2%), 0 left inside
2@ and 2! - -41.6% from the 12,759,474 before patch 1, as the audit priced; the corpus
-0.2%. Checked in a scratch tree on patch 1: engines-check 41 paths PASS (five with
opinline), run-tests PASS, gene-equiv - recorded ids and expressions identical, every
made genome different (a new gene's key); the gate, seed 49's front with both opcodes
first and both genes on: 172 of 172.

## Iteration 293 - 2026-10-14 - Claude

**The gene tailpn, pending as the after-seed-50 batch's patch 3: the tail-call engine
with clang 19+'s preserve_none and musttail** (the owner: clang-20 on the laptop). gen-tail
.py --preserve-none marks the handler type and every handler preserve_none and every
handler-to-handler call musttail - not the entry, an ordinary C function that only calls
in; evolve.py's clang_pn() finds the newest clang that compiles a line of both (clang-19
here), CC() takes it for a tailpn design, and the gene is expressed only on a clang tail
engine, only where such a clang is. The first try "did not compile" - yet tail.c compiled
by hand, and so did the exact command: the jail. A program not in BUILD_TOOLS is run as an
engine, with no new process allowed, so clang-19's driver could not start the linker; a
versioned clang is a build tool now. Checked in a scratch tree on patches 1 and 2:
engines-check 42 paths PASS, the new one clang-19's (225 preserve_none, 223 musttail; s6's
engine 14,232 bytes, 14,680 without); run-tests PASS; gene-equiv - recorded ids and
expressions the same; the gate, tail, clang and tailpn forced on 20 of seed 49's front: 19
of 19 alive, one unable to express a tail engine. No speed figure: a rough VM timing's
script ran the engines wrongly, and the VM could not judge it; seed 51 on the laptop will.

## Iteration 294 - 2026-10-14 - Claude

**missmap.py - which handlers mispredict - ready for the laptop; the JIT's ackermann
misses explained.** For the 9-24% of the interpreter's cycles the counters put down to
branch misses: perf record samples each design's user-space branch misses on kernel and
corpus, perf report gives each sample's source line, and the line is charged to the
handler whose label (L_x:, or a tail engine's H_x) comes last before it; samples outside
the engine's source - the JIT's code - are counted apart. The engine is built with -g for
it (evolve.py's EVOLVE_CFLAGS, a measurement's only; debug information changes no
instruction); perf and the paranoid setting as counters.py's (next-run.sh asks sudo for
missmap.py too). Tried end to end here with a stand-in perf that runs the engine for
record and answers report with real label lines of s6's source: exit 0, the samples on
L_t2call2-4 as placed, the outside line in the JIT's bucket. On the way: evolve.build()
returns the engine's and image's paths - assumed names were why the two rough timings of
Iteration 293 ran nothing (exit 2). The JIT's ackermann, read in jit.c: native call and
ret, A(3,5) deeper than the return predictor - a candidate gene (EXIT as pop and jmp), in
results/counters-amd-ryzen-7-pro-8840hs.md, not built.

## Iteration 295 - 2026-10-14 - Claude

**The gene knumber, pending as the after-seed-50 batch's patch 4: NUMBER? as one
opcode; counters.py --extra; the IP-update loop form planned, not built.** Pricing the
digit table first showed it aimed wrong: DIGIT? is under 1% of the corpus where it runs
at all, and the fast designs convert digits in C already ((>NUMBER), Iteration 57) - but
NUMBER?'s own Forth around it was 10.1% of c9369657e4's corpus dispatches and 13.3% of
927064f127's. knumber: forth/cv8b-knumber.4 under a stage tag of its own - a gene, since
klookup's overlay and forced list would have changed what recorded designs build -
(NUMBER?), the kernel's NUMBER? with BASE @ and DPL given, its two failure paths 0 0 0
(only INTERPRET calls it, and aborts or throws), and NUMBER?8; numberq in vm-lab.c, the
same steps in C with (>NUMBER)'s umul, for the plain, cached-top and multi-state engines;
the expected body, 170 operations, generated from the converter's own reading. Measured:
c9369657e4's corpus -10.2% (NUMBER? 10.1% -> 0.9%); 927064f127's corpus -4.9% and its
kernel +5.3% - its slots full, the opcode displaced a word: evolution weighs it.
Checked in a scratch tree on patches 1-3: engines-check 47 paths, run-tests, gene-equiv
(recorded ids and expressions the same), the gate - 55 of 55, every klookup design on seed
49's front. Patch 1's handlers carry no #if, and need none: three recorded designs build
byte for byte the same with it.

counters.py --extra EV,EV counts more events, each a column as a share of cycles, an
event the CPU cannot count n/a (tried with a stand-in perf). results/drafts/iploop-plan
.md: three explanations of the evolved designs' lower IPC - the IP chain, the stack
through memory, the front end - and the laptop measurement that tells them apart
(front- and back-end stalls), then a hand variant; only then a gene.

## Iteration 296 - 2026-10-15 - Claude

**Seed 50 processed - small - and the after-seed-50 batch applied; seed 51 set for 12
hours (the owner).** Both packs clean (tests PASS, the generators 31 paths, 7 of 7, the
jail PASS); the measured-here patch the laptop's stash again, the c-baseline-x86-64.md
hunk left out. The evolution ran 10 h 03 min, 47,033 designs measured (46,744 alive),
14,337 screened; 289 deaths, all refused before running. The verdict: fastest -0.1%,
smallest +0.16%, memory -2 KB, hypervolume +0.4%, best Q +0.2% - small, the third run
of seed 48's genes; the Q-best of all runs now this run's ed821c2edc (Q 0.216). The
front 187: factor on 174 (level 3 on 121), lto on 117 of 159 GCC-built, clang 28, jitk
48, gotodup 24, the JIT on 109; the smallest 15,647 (-25), the least memory 116 KB again.
Predictions three of five (not small, and 30 bytes off the smallest, were wrong).

The batch - 2@ and 2! as opcodes, opinline, tailpn, knumber - applied in order, then on
master: run-tests PASS (47 generator paths), the gate 266 of 266 (seed 50's front 187,
the joint front 128), ans-check 0 of 35 differ. New genes: the stopping rule counts
afresh. NEXT-RUN: `seed 51 tag2 12h then experiment compare-fronts.py --rounds 6
--frontier --cpus 2,8`; its predictions written; the comparison is session 44. Before
seed 51 the owner runs missmap.py and counters.py --extra, each its own command.

## Iteration 297 - 2026-10-15 - Claude

**The two laptop measurements before seed 51: the front end, and a missmap.py that ran
the wrong binary.** counters.py --extra (front- and back-end stalls; this CPU counts only
the front end's): the evolved interpreted designs stall in the front end about half
their cycles on compute work - the fastest without the JIT 48.9% on fib, 56.8% on bubble,
mispredicting 0.16 and 0.39 a thousand there; the smallest 48-56%; s6 18-36%; the JIT
1-6%. The IP-update loop form, a back-end chain, is not what bounds them: set aside
(results/drafts/iploop-plan.md). Next: which part of the front end (Zen 4's cache and TLB
events), and a gene aligning handler entries - align1 only takes alignment away.
missmap.py attributed nothing - every sample without a source line: build() strips the
engine and keeps engine.full, and the tool ran the stripped one. It runs engine.full now,
tried against a stand-in perf that refuses a stripped engine. Nothing found asks for a
change before seed 51; seed 51 set to 10 hours (the owner).

## Iteration 298 - 2026-10-15 - Claude

**Seed 51 started (10 hours); the gene alignhot pending for after it; counters.py
--extra per 1k instructions.** The owner's `perf list` gave Zen 4's names
(ic_tag_hit_miss.instruction_cache_miss, op_cache_hit_miss.op_cache_miss,
de_src_op_disp.op_cache); counters.py --extra now gives a stalled-cycles event as a share of
cycles and any other per 1k instructions - the next between-runs measurement asks which
part of the front end the evolved interpreted designs wait on. alignhot - GCC's
-falign-jumps, -labels, -functions at 32:11, 32 or 64 - is the cheap lever on it: GCC's
labels align every branch target, so full alignment costs much (s6's engine +5,216 bytes
at 32, +12,192 at 64), 32:11 - only where it costs at most 10 bytes - +1,280. Checked in a
scratch tree: engines-check 52 paths, run-tests, gene-equiv (3,235 recorded ids and
expressions the same), the gate at 64 on seed 50's front: 20 of 20 - the other 167 build
with clang or carry align1 or alignfn: evolution has taken alignment away on most of the
front. A new batch, results/pending: applied after seed 51.

## Iteration 299 - 2026-10-15 - Claude

**While seed 51 runs: seed-facts.py reports every gene; source audit 3; > and 0= pending
as the after-seed-51 batch's patch 2.** seed-facts.py printed a fixed list of thirteen
genes - seeds 48-50's factor, lto, clang, jitk and gotodup were counted by hand - and now
prints every late gene the front carries (val() gives strings: '0' is off; the genes off
on every design on one line) and every format-10 word with the designs expressing it.
Audit 3 (results/source-audit-3.md; hotwords.py and word-cost.py, exact counts, seed 50's
fastest, smallest and Q-best designs): 2@, 2! and NUMBER? at the top, all handled by the
batch applied before seed 51; new, > 11.7% of bubble's dispatches and 0= 7.7% of
ackermann's on 658ed9b9f8 - kernel colon words the benchmarks' compiled code calls - and
?STACK 7.4% of the corpus's, which needs S0 as DEPTH does: a gene for later. > and 0= as
pool words and opbody's: handlers L_x_gt and L_x_zeq (the engine's L_gt is <, the name
historical); their kernel bodies were in sod16.py's table already, and the JIT has
stencils for both. With them first, opbody and opinline, on 658ed9b9f8: bubble -11.7%,
ackermann -7.7%, the kernel +5.5% and the corpus +8.7% for the two words they pushed out of
a full list. Checked in a scratch tree on patch 1: engines-check, run-tests, gene-equiv
(recorded ids and expressions the same), the gate - 187 of 187 on seed 50's front. The
gate had finished as the last turn ended; its log said so.

**?STACK, looked at and deferred.** It was worked on twice already - kinput's ?STACK8
(Iteration 54) and kstack's (Iteration 116), one unsigned compare on DEPTH, in Forth -
and what is left is about a dozen dispatches a check, 7.4% of 658ed9b9f8's corpus. An
opcode given S0 @ would take most of it, about 1% of the geometric mean, at the price of an
overlay tag on every design (the stage dumps doubled) and of reproducing DEPTH exactly -
SP@ is PUSH(dsp + CELL_BYTES), its value dsp before the push because the macro moves dsp
first. HANDOFF.md item 5a: worth it if seed 51 shows the corpus still weighs.

## Iteration 300 - 2026-10-15 - Claude

**Seed 51 processed - small, the fastest +4.9% - the after-seed-51 batch applied, and
HANDOFF.md's routine repaired.** Both packs clean (tests PASS, the generators 47 paths, 7
of 7, the jail PASS); the measured-here patch the laptop's stash again. The evolution ran
7 h 32 min of the owner's 10 hours, 34,690 designs measured, 10,684 screened, 217 deaths
all refused before running. The verdict: fastest +4.9% (just under its 5%), smallest
+0.00%, memory +0 KB, hypervolume +1.7%, best Q +0.8% - small; the Q-best of all runs
seed 51's f6b175f69c (Q 0.216). What the first run of the after-seed-50 batch took
(seed-facts.py, generic since 299): opinline on 64 of 162; 2@ on 52 - the JIT designs,
five of the six fastest (the JIT translates it since 291), but 8 of the 69 without the JIT;
knumber 8 of 69 klookup designs; tailpn and tail engines none. Predictions two of six -
every miss on how widely a new gene would be taken: a full format-10 list makes a new
opcode cost an interpreted design a slot.

The batch - alignhot; > and 0= - applied, then on master: run-tests PASS (57 generator
paths), the gate 241 of 241 (seed 51's front 162, the joint front 131), ans-check 0 of 35
differ. NEXT-RUN: `seed 52 tag2 10h then experiment compare-fronts.py --rounds 6
--frontier --cpus 2,8` - 10 hours, seed 51's, for the owner to confirm; the comparison is
session 45; its predictions written.

HANDOFF.md, found broken while updating it: from Iteration 293 my edits found open items
by `index('\n3. ')` and the like - and the routine, numbered too, comes first: its steps
3-5 had been overwritten with open-item text, and the open items left stale since 290.
The routine's steps restored from Iteration 292's text; the open items rebuilt from the
texts the edits had written; a lesson added.

## Iteration 301 - 2026-10-15 - Claude

**The two measurements before seed 52, and seed 52 set to 6 hours (the owner).** missmap.py,
running engine.full at last, on seed 51's front (results/missmap-amd-ryzen-7-pro-8840hs.md):
(FIND) in C the largest single source of the interpreter's misses, 9-13% on kernel and
corpus - its chain walk, the fast designs all with the fewest threads (16); calls and returns
15-25%; the JIT design's runtime C about 20%; s6's L_t2bad most likely GCC's merged dispatch
jump. counters.py with Zen 4's cache events: on compute work the caches hardly miss (under
0.2 a thousand instructions) while the front end stalls half the cycles - the dispatch's
taken indirect jump itself; fewer dispatches is the lever, alignment not (alignhot, applied,
unlikely to pay). Next for seed 53: a branch-light (FIND) chain walk, as a gene.

## Iteration 302 - 2026-10-15 - Claude

**The collaboration protocol, agreed with the owner, and captured in the prompts
library.** One command on the laptop, one archive back with every step's results and
every log; made even when a step fails, a failed step not costing the others;
privileges asked at the start, and anything needing them later done by a root helper
forked at the start that polls for its condition and chowns what it creates (the
owner's rule: no root-owned files in his home); the code pulled once; the checks once
per chain; the measurements first. HANDOFF.md: a standing decision, and open item 0 to
build it. prompts/: 08 - what comes back from the other machine, items 11-14 (one
archive with every log; privileges at the start and the forked helper; the code pinned;
a failed step not costing the others) and the artifact; 11 - the dropped perf message,
item 7 (everything in one archive); 15 - step 6, a stand-in refuses what the real one
refuses (the stand-in perf that invented source lines; the stand-in sudo that let a
hang-up kill its child). INDEX, README, USAGE rows; UPSTREAM, to carry back to relf.

## Iteration 303 - 2026-10-15 - Claude

**The protocol's stop and cleanup (the owner): a clear way to stop a run, cleanup on
every exit, and at every start a repair of what a crashed or killed run left.** Read
first in next-run.sh: it detaches with plain nohup, no session of its own, and the
evolver starts every engine and build with start_new_session=True - a signal to the
runner's process group would miss them, so a stop goes by the process tree; the flock
dies with its holder; the state file already makes stop-then-start a resume of the seed
run; and perf-hold.py creates runs/perf-hold.log as root - a root-owned file in the
owner's home, against his rule. results/drafts/runner-protocol.md specifies the rebuilt
runner: start, status, stop; the start's recovery; the trap that always archives
(written as .partial and renamed); root that chowns and watches the chain; the tests
(a miniature chain, a stop in mid-run, a kill -9 as a crash). prompts/08 item 15 and
its why; UPSTREAM; HANDOFF's decision and open item 0.

## Iteration 304 - 2026-10-15 - Claude

**A monitor command (the owner).** next-run.sh monitor follows the chain's log from its
start, read-only - Ctrl-C ends the watching, never the run - and ends by itself when the
chain does, with how it ended and where the archive is. It asks for two things the
current runner lacks: one log for the whole chain (each step writes its own today), and
progress lines in the seed run (five-minutely: generation, designs, the front, the time
left), so the hours of evolution do not show as silence. Each command names the others.
results/drafts/runner-protocol.md, prompts/08 item 16, UPSTREAM, HANDOFF.

## Iteration 305 - 2026-10-15 - Claude

**Generalization - the owner's three concerns: this CPU, small programs, and whether
bigger code would do much worse.** Measured now: the held-out workload. lab/evolve/
heldout.py (columns by their header's name - a first inline try read "re-measured", the
selection's own speed measured again, and gave 0.999; the error caught before it was
reported): on seeds 49-51 the selection speed and sieve's agree with Spearman 0.939-0.943,
the fastest keep their places, and a steady group of designs is 2.5-2.7 times better on
the selection than on sieve. Not measured: any CPU but the laptop's - every selection's
speed is Zen 4's - and any program much larger than the cross-compiler and the test suite;
the counters' cache misses under 0.2 a thousand instructions on compute work say the hot
code fits. results/generalization.md: what carries to any CPU and what may not, and the two
checks to build - a held-out workload whose footprint grows, and the joint front on a
second CPU. heldout.py in the processing routine; HANDOFF item 5b.

## Iteration 306 - 2026-10-15 - Claude

**Two more machines for the generalization check (the owner): dream.lan, an Intel Core
i7-6700 (Skylake), and rage.lan, the Tegra (ARMv7, 32-bit) - both reached from the laptop
by ssh, both slower.** The plan, in results/drafts/runner-protocol.md: remote checks
alongside every seed run, on the front that just finished, so they add no hours - dream
24 designs of the joint front and s6, the selection workloads and sieve, 3 rounds (about
20-30 minutes, estimated); rage 12 designs without the JIT and s6, 2 rounds (1-1.5 hours) -
on a 32-bit host a design builds with 4-byte cells and the C library, and the JIT does not
express there. Each check a hard limit, its host's environment and a feasibility check on
first contact, a host that fails skipped and named; the Spearman correlation with the
laptop's speeds, as heldout.py does for workloads. Part of open item 0.

## Iteration 307 - 2026-10-15 - Claude

**xcheck.py - the remote checks' measuring side - and the hosts' facts (the owner): dream
and rage idle during runs, GCC on both, neither clang nor perf.** So a design built with
clang (compiler, tailpn) is not itself there, and on 32-bit rage neither is a JIT design.
xcheck.py reuses the evolver's own steps rather than copying them - E.build, E.alive,
E.measure (the design and s6 back to back each round), the comparison's geometric mean of
the selection's ratios: --sample picks a front's designs that can be themselves on the
host (the fastest, about the best Q, the smallest, between); the host's run records its
environment, checks s6, and for each design compares its expression there with the
laptop's before building, checking and measuring it, keeping what it has at --until;
--report gives the Spearman correlation with the laptop's speeds, where the laptop's
fastest rank, and the designs that moved most. Tried here, the VM as the host: 8 sampled,
one given a false expression on purpose and reported "not itself here (compiler)", 7
measured, the report made. The VM's numbers are no evidence - virtual, one core, not quiet -
but on it the fast designs ran 1.8-1.9 times slower relative to s6 than on the laptop, and
the small ones slightly faster: what dream will show properly.

## Iteration 308 - 2026-10-15 - Claude

**The laptop's binaries to dream (the owner's suggestion).** No build uses -march or
-mtune - the x86-64 baseline, the JIT's stencils too - and the engines are static with raw
system calls: the laptop's engines and images run on the i7-6700 unchanged. So
xcheck.py --sample --bundle builds the sampled designs and s6 on the laptop into one
tarball (four and s6: 70 KB), and --prebuilt measures those very binaries on the host:
what moves there moves for the microarchitecture alone, clang-built designs are themselves
without clang, and dream builds nothing. Tried here with the VM as both: three clang-built
JIT designs and the smallest measured from the bundle. It found a fault first: a design's
directory left by an earlier run (a design recurs from run to run) made private_work
refuse it - each directory is now cleared before use, and the rerun, the old directory
still there, measured 4 of 4. For the Tegra, cross-building on the laptop (the owner's
other suggestion) means a second target in the evolver's build; native builds first, timed
by the first run, cross-building if they are too slow. On the VM again - no evidence, but
the same shape - the smallest design's ratio to s6 was the laptop's (1.473, 1.480) and the
JIT designs' doubled (0.254, 0.129).

## Iteration 309 - 2026-10-15 - Claude

**Two new prompts (the owner: capture the reusable ideas).** 18-does-it-generalize, from
Iterations 305-308: a search finds what its benchmarks reward, on the machine it ran on -
held-out workloads looked at every round (rank correlation 0.94, and a group of designs
the selection flatters 2.5-2.7 times), a held-out machine measured with the same binaries,
a design counted only where it expresses the same, the program grown past the caches, the
checks run alongside the search under a time limit, a perfect number distrusted (the 0.999
read from the wrong column). 19-address-by-name, from four faults of one week with one
cause - a part of a document found by where it was: open items edited in the routine's
numbered list, a table row's end counted into the next row, a held-out column read by
position, an insertion with no place to go - find by heading, item text or header; scope
the search; one match or stop; read the changed unit back with its neighbours; name the
edges. The index tables edited as 19 says - each by its anchor, unique, read back - and
USAGE's table, which stopped at 13, completed for 14-19 from each prompt's own "produces"
line. UPSTREAM, to carry back to relf.

## Iteration 310 - 2026-10-15 - Claude

**Seed 52 processed - small - and a JIT fault it found.** Both packs clean (tests PASS,
57 generator paths, 7 of 7, the jail PASS); the measured-here patch the stash again. The
evolution 3 h 19 min, 15,246 designs measured, 4,440 screened. The verdict: fastest +1.8%,
smallest +0.00%, memory +0 KB, hypervolume +0.5%, best Q -1.9% - small. The batch's genes
barely taken: alignhot on none of the front, > on 3, 0= on none; 2@ on 77. heldout.py: 0.937,
the ten fastest by selection the ten fastest on sieve. Predictions four of five.

Two designs died on the corpus - the first in these runs. Reproduced here: with the JIT
off both live; opinline and opbody are innocent (my first guess, wrong); reverting any one
of folds, ops10, rtloop or tag2 makes each live, and nothing else of the 26-28 genes they
differ from s6 by does; the corpus output ends inside the loop tests (16 lines of 788). An
older JIT fault, most likely, reached now. results/drafts/jit-loop-crash.md keeps the two
genomes, what is known and the next steps; HANDOFF item 0a. NEXT-RUN: seed 53, the same
genes, 6 hours as a placeholder - the owner's hours, and whether to wait for new genes.

**The JIT fault, narrowed further (Iteration 310).** A segmentation fault (the engine's
handler, exit 70) on the corpus's first loop test, `: GD1 DO I LOOP ; 4 1 GD1` - a
micro-program reproduces it in milliseconds. It needs (DO), I and (LOOP) as format-10
opcodes: dropping any one stops it, dropping any of the design's ten other words does not.
They are one-byte opcodes (95, 88, 87) - my guess of a misread operand after an escape
pair was wrong; and folds' part is indirect - reverted, the loop words are not format-10
opcodes at all. Left: the JIT's translation of that run-time-compiled loop (results/drafts/
jit-loop-crash.md).


## Iteration 311 - 2026-10-15 - Claude

**Seed runs paused (the owner, agreeing): the JIT fault first, then the new runner with the
remote checks, then the (FIND) gene.** The fault's condition found: GD1's compiled bytes
are right - (DO), I, (LOOP) and a 16-bit -2 back to I, the JIT's operand kind 7 exactly -
and the crash needs jitloop off and the top of the stack cached: with jitloop on, or tos
off, the micro-program prints 3 2 1. On seed 52's front 88 of the 89 JIT designs carry
jitloop; the evolution had kept out of a region where designs die, and the two deaths are
where it went back in. Next: the JIT's loop translation without jitloop, and the cached top
across it (results/drafts/jit-loop-crash.md). NEXT-RUN says paused.

## Iteration 312 - 2026-10-15 - Claude

**The JIT fault fixed, pending as the after-seed-52 batch.** The cause: jit.c read each
stencil at most 64 bytes in a build without jitloop (160 with it), taking the stencil's end
at the last jump to NEXT or JUMP in that window; the dead design's st_loop is 72 bytes (nm -S
on engine.full), so the scan found the fall-through and missed the loop-back - a (LOOP)
stencil recorded short, with no jump hole, its inner branch pointing past the copy. The
both-exits check covered (+LOOP) and (?DO) only, and only with jitloop. The design with
jitloop on lived with the same st_loop, read in 160; and "tos off" lived because without tos
there is no JIT at all (jit_on) - my Iteration 311 reading of that probe was wrong. The fix:
160 in every build; every branching stencil - 0BRANCH, (LOOP), (+LOOP), (?DO), DUP n > ?BRANCH
both exits, BRANCH and LEAVE their jump - or not used, every build; and lab/evolve/
regressions.json, designs that once failed, which engines-check builds and runs on the corpus
every time. Tested in a scratch tree: both designs live (3 2 1, the corpus right), 59 paths
with the two regressions, run-tests, the gate 252 of 252; three JIT designs' speed unchanged -
one that looked 40% slower on loop from 2 rounds measured 0.043 on master and with the fix,
twice, from 5.

## Iteration 313 - 2026-10-15 - Claude

**The new runner, its chain layer built (results/drafts/runner-protocol.md, "Built so far").**
lab/evolve/chainctl.py and nine edits to next-run.sh; each step's own logic unchanged. A chain
- every step of a NEXT-RUN line - is one session (setsid) with one directory: its line,
commit, session, status, a line a step, the one log, and packs/. `next-run.sh status`,
`monitor` (read only) and `stop` (TERM, then KILL after 60 s, and packed). One archive at the
end, whatever happened: forth-vm-evolution-chain-HEAD-HOST-TIME[-STATUS].tar.gz, .partial
until whole. A measurement that fails does not stop what follows; a seed run's failure skips
the comparison, recorded. The tests, validation and jail once a chain. A progress line every 5
minutes during the evolution. At start: a chain that ended without finishing archived as
interrupted, stale partial archives removed, root-owned files given back with sudo in the
foreground.

Tested on the VM in a scratch clone with two stand-in tools: a failure going on (one archive,
done-some-failed, the failed tool's own error kept - after a design gap the first test showed:
a later success had packed as plain done); checks once (23 s, the tests not run again); status
and monitor; stop in the middle of a build (five processes, none after; a stopped step first
recorded FAILED - now STOPPED); a crash, every process killed -9 - archived as interrupted by
the next start. A bug found by reading before testing: the pack line's expansion gave a path
"chain.log" plus the chain's path. Not yet: the seed step under the chain (a miniature seed
chain), the root-owned files path; perf-hold for every measurement; the remote checks.

## Iteration 314 - 2026-10-15 - Claude

**The runner: the seed path tested, root's files, perf-hold for every measurement.** A
miniature chain of the real shape on the VM - a measurement step, `seed 99 tag2 nocarry`
(population 4, 2 generations), a comparison step: done, one archive; the fresh seed archived
the previous records and rebuilt in 22 s, the tests kept from the first step; its pack has every
file the processing reads. The test found a fault: the ticker read build/evolve/evolve.log,
next-run.sh writes the clone's own - "no generation yet" through the run; fixed, and checked
against the test's log. Root-owned files: found, sudo refused, nothing started; given back, the
start went on (a second chain, which also tested the changed detach and stop).

perf-hold.py now takes the chain's directory: it holds for each measurement in turn, the old
value back after each, and ends when the chain does - its status final or its session gone; it
gives its log to the directory's owner after every line, and counters.py's PerfHold clears an
earlier measurement's DONE. The chain's directory is made before perf-hold starts. Tested for
real on the VM: two measurements, 2 during each and 3 after; the chain done - the helper gone;
the chain killed with its status left running - gone too; the log claude's. Left before seed
53: the remote checks.

The remote checks designed (results/drafts/runner-protocol.md, "The remote checks - the design
to build"): lab/evolve/REMOTES a line a host, remote-checks.sh start/gather/stop/clean driving
xcheck.py from the chain - sampled from the previous front, run in parallel with the seed run
under its own deadline, gathered before the one archive, never costing the chain; tested with a
stand-in ssh and scp that refuse what the real ones do. Built next.

## Iteration 315 - 2026-10-15 - Claude

**The remote checks built and tested - the runner complete.** lab/evolve/REMOTES (dream.lan
prebuilt 24 designs 3 rounds 30 minutes; rage.lan native 12, 2, 90, --no-jit --gcc-only) and
lab/evolve/remote-checks.sh probe/start/gather/stop around xcheck.py; hooked into next-run.sh
(probe in the first step's foreground, start in the seed step before the evolution) and into
chainctl.py (gather in pack - every chain's end - and stop). Tested on the VM with stand-in ssh
and scp that refuse what the real ones do: a seed chain with a missing host (skipped, said at
start), a native host (cloned, built, measured, gathered), a prebuilt host - which failed on
the host: evolve.py's setup refuses an incomplete build/, so prebuilt needs the stages built
too; my design said it needed nothing, and dream's first run would have failed. Recorded with
its reason, the chain done all the same; fixed - every host builds the stages - and the
prebuilt path then measured the laptop's binaries and was gathered. stop with a host
mid-build: its process group killed (by pid file - a pkill by name would match its own shell),
the directory removed; a stopped chain's pack with a host still running: 1 s, no wait,
cleaned. Before the first real run: ssh keys from the laptop to both hosts.

## Iteration 316 - 2026-10-15 - Claude

**The gene bfind begun - THREAD-FIND's and (FIND)'s walk branch-light; in progress, not on
master (results/drafts/bfind-wip.patch, HANDOFF item 0c).** Per candidate the walk had a
data-dependent length test, a byte loop entered on equal lengths, and PREVNFA's switch on the
link's form (1-4 bytes in TAG2, 1-3 in CV8). bfind: the count and first seven characters as one
masked 64-bit compare - almost always unequal, so predicted - the rest of a longer name only on
a match; the link read without a branch (the four bytes ending at its tag as one word, shifted
by its length). Expressed when (FIND) or THREAD-FIND is a format-10 opcode: on seed 52's front
(FIND) on 61 designs, THREAD-FIND on 67, never both - klookup's (FIND) walks itself. The first
build failed: the helpers stood above BYTE and UNS64's definitions; moved below, not yet built.
Three slips of mine on the way, none in the gene: a test filter that wanted both words; a
`< /dev/null` that replaced a heredoc script, so two "checks" ran nothing; git run as root on
claude's repository, refused, and `set -e` ending the command there.

## Iteration 317 - 2026-10-15 - Claude

**bfind verified and pending - the after-seed-52 batch complete (results/applied-after-seed57/ORDER.md).**
Built on patch 1 in a scratch tree, as the batch applies in order. The four cases right on the
corpus; gene-equiv against patch 1: every recorded genome's id and expression the same (its
FAIL the operator draws, as for any new gene); run-tests, 63 paths with four for bfind; validate
7 of 7; 32 of seed 52's front forced to bfind - 32 alive. The first form - each handler's label
twice, under #if/#else - broke the multi-state generator (5 of 63 paths), which would have
broken every msc design with the gene off; one label each, the condition inside the body, and
all 63 passed. On the VM no speed past the noise either way (kernel 0.951 for a (FIND) design,
perhaps a small cost) - the gene is for the laptop's predictor. My slips this turn: a test
script's syntax; a pkill -f matching its own command line - the pitfall remote-checks.sh was
built around. Both patches apply in order on a fresh clone and reproduce the tested files.

## Iteration 318 - 2026-10-16 - Claude

**The after-seed-52 batch applied - seed 53 is next.** The JIT fix (a stencil read short in a
build without jitloop; regressions.json and its engines-check paths) and the gene bfind, in
order, on master: run-tests PASS with 63 engine paths, validate 7 of 7, the gate 252 of 252
(results/applied-after-seed52/ORDER.md). With the new runner and the remote checks in, NEXT-RUN
is seed 53 again - 6 hours until the owner says, the comparison after; the pause lifted. Its
predictions revised (results/predictions.md): the Iteration 310 ones assumed the same genes; now
no corpus deaths, bfind on at least 20, small, dream's ranking at least 0.90 and rage's lower,
crossover 30-38%. Before the run: ssh keys from the laptop to dream.lan and rage.lan.

## Iteration 319 - 2026-10-16 - Claude

**Seed 53 for 3 hours (the owner).** Seed 52's laptop phases: the evolution 3 h 19 min, the
re-measure 19 min, the comparison 1 h 53 min at 6 rounds on 2 CPUs. At 3 hours with the
comparison unchanged, the reserve (the last chain's phases, a tenth and 10 minutes more) would
hit its cap of 60%: the evolution ~72 min and the chain ~3.5 h all the same. So the comparison
at 3 rounds - ~1 h, its verdict noisier: the evolution ~1.5 h, the chain ~3 h. NEXT-RUN: seed 53
tag2 3h then experiment compare-fronts.py --rounds 3 --frontier --cpus 2,8.

## Iteration 320 - 2026-10-16 - Claude

**Seed 53 processed - small - the first chain through the new runner.** One archive, status
done: both hosts answered at start; seed 53 and its comparison packed in it; dream's results
gathered; rage's recorded as failed with its reason - the chain unharmed, as designed. The
ticker's lines through the run. Both packs clean (63 paths, 7 of 7, the jail). The verdict at 3
rounds: fastest -5.8% (80 minutes of evolution), smallest +0.00%, memory -4 KB, hypervolume
+0.3%, best Q -5.3% - small. No corpus deaths (the JIT fix); bfind on 17 of 172; heldout 0.948.
Predictions three right, one wrong (bfind 17, not 20), one half (rage no data).

**The first remote check** (results/xcheck-dream-seed53.md): dream.lan, an i7-6700, measuring 24
of seed 52's front from the laptop's binaries - Spearman 0.959 with the laptop, the laptop's six
fastest its first six; the slow designs the same against s6 on both (1.01-1.02), the JIT
designs' lead smaller there - 0.128 of s6's time on the laptop, 0.223 on dream. rage.lan failed:
build-stages.sh compiles a stage with the gene sysc, x86-64's system calls, which relf.c refuses
on ARM - my plan assumed the stages built everywhere (HANDOFF item 0). NEXT-RUN: seed 54, the
same genes, 3 hours.

## Iteration 321 - 2026-10-16 - Claude

**Seed 54 for 9 hours (the owner).** The comparison back to 6 rounds - with 9 hours there is
room: the reserve from seed 53's phases (the re-measure 16 min, the comparison 44 min at 3
rounds, scaled to 6) about 2 hours, so the evolution about 7 - against seed 53's 80 minutes.
Seed 52's comparison at 6 rounds took 1 h 53 min, more than that scaling says: the chain may run
past 9 hours by some minutes. rage.lan's check is left failing (recorded, harmless) until item 0
is fixed properly - its sample must leave out designs with sysc too, not only its stages.

## Iteration 322 - 2026-10-16 - Claude

**rage.lan out of the remote checks - it cannot build the evolved designs at all.** Its first
check failed in build-stages.sh on relf.c's sysc guard, but the same log said why no fix there
would do: "8-byte cells DISABLED: this is a 32-bit host". Every evolved design is an 8-byte-cell
one - evolve.py's build needs the k64 dumps, made by running s0-cell-64 - and relf.c's cell width
is the host's pointer width. My REMOTES plan ("native, no JIT") missed it, as did the planning
that chose rage. REMOTES keeps rage's line commented with the reason; another architecture wants
a 64-bit host (aarch64: native, --no-jit). A configuration change: on master, read by the next
chain.

## Iteration 323 - 2026-10-16 - Claude

**Where the dispatches go now - the search for the next genes begun (results/drafts/
next-genes.md).** price.py on seed 53's three fastest interpreted designs: calls and returns
the largest share of dispatches (21-37% outside loop), but folds, tail, hotinl, factor, opinline
and rtempty are their genes already; more pairs priced at 8-21% but measured before at 0.2-2.4%
(their overlap, the slots); triples negligible. My idea of fusing returns was folds, which
exists. The frontier is the JIT's: a word it cannot translate whole stays interpreted, and no
tool counts what that leaves - jitleft.py is next. rage.lan out of REMOTES earlier this turn.

## Iteration 324 - 2026-10-16 - Claude

**The Tegra back, as the owner wants - 8-byte cells on a 32-bit host, begun
(results/drafts/cell64-wip.patch, HANDOFF item 0).** Running only on the laptop is the skew they
feared; rage is the check that differs most. The engines tied the cell to the pointer
(UINTPTR_MAX); CELL64 keeps it 64-bit on a 32-bit host, cells and pointers through uintptr_t,
CELL unaligned-safe for ARMv7. evolve.py: CCV(g) - the real compile of every evolved design
names the gene's compiler through CC(g), not cc: my first hooks were in build_other, the old
encodings', and my first "32-bit" test printed success over a 64-bit engine - it now checks the
ELF it built. Tests here: gcc -m32 runs, ARM under qemu-arm (no binfmt: a wrapper); installing
the cross compiler removed /usr/include/asm, which broke the 32-bit stages - restored, noted in
HANDOFF's setup. x86-64 builds unchanged. The s6 reference at -m32 -DCELL64=1: one error -
__int128 (UM*, UM/MOD), which 32-bit targets lack. Next: those in 32-bit halves, then the corpus.

## Iteration 325 - 2026-10-16 - Claude

**32-bit x86 with 8-byte cells works - 14 of 14 designs alive; the owner adds a 32-bit x86 check
to the runs (results/drafts/cell64-wip.patch, HANDOFF item 0).** UM* and UM/MOD in 32-bit halves
(no __int128 on 32-bit targets) - s6 built as a 32-bit engine and right on the corpus. One design
of seed 53's front died on the kernel workload; the bisect, all 27 genes: fsys alone. The cause:
the image's system-call numbers are x86-64's, and the table mapping them for 32-bit hosts held
only the shell's calls (Iteration 141) - none of the file overlays' (read, write, open, close,
lseek, mmap...); my first guess, varargs, was wrong (every argument is cast to long). Mapped for
i386 and 32-bit ARM, mmap through libc, results zero-extended unless an errno - an address past
2 GB is no error. And every engine is SYSC (Iteration 147): its guard stopped every design on
ARM, which rage met first. Then 14 of 14 at -m32: s6, the fsys design, twelve across the front.
ARM's first try: the cross compiler jailed by sh() as an engine (no new processes) - EVOLVE_CC's
compiler is a build tool now, as clang-19 became. The ARM run under qemu-arm next.

## Iteration 326 - 2026-10-16 - Claude

**Native cell width for the 32-bit checks - the owner's rule (results/drafts/cell32-wip.patch).**
The owner asked why a 32-bit build had 8-byte cells: it should have 4. Right - and a universal cell
would cost either the 32-bit hosts (double-word arithmetic) or the 64-bit ones (offsets for every
address, WebAssembly's way - every design on the laptop changed). Nothing was lost: one Forth
source, cross.4's TARGET-CELL-BYTES, gives both kernels; what was always 64-bit only is the
evolver's layer - its kernel variants, made in setup from kernel.img alone. The 8-byte-cells mode
dropped; evolve.py's cellw() makes the variants, the converter's width and the references follow
the host's width; the kernel workload at 4 bytes builds the 4-byte kernel, as reseed.sh does.
The first 32-bit variant dump failed: "out of memory" - file-sysc.4's ALLOCATE maps with mmap,
which on 32-bit x86 returns an address past 2 GB, a negative 4-byte cell, and the overlay tests
results with 0<. Not the port: the overlays were written for 64 bits. Without [IF] in the kernel,
and with the 64-bit images to stay the same, the engines keep such memory below 2 GB on a 32-bit
host - Linux's legacy layout, set at start and re-executed once (raw system calls: the runtimes
without the C library have no wrappers). The dump then whole: 342 names. Endianness: all hosts
little-endian; cross.4 says images are native-endian - no parameter needed.

## Iteration 327 - 2026-10-16 - Claude

**The 32-bit layer at 4-byte cells: the variants made, two blockers found (HANDOFF item 0).** Setup at
EVOLVE_CELL=4: all 3,314 k32 variant dumps in 127 s, every overlay loading at 32 bits. Then 0 of 14
designs alive, for two reasons. (1) The 4-byte kernel workload: a 32-bit Forth running the cross
compiler segfaults - s6 at -m32 and the hand-made 32-bit cell engine alike, so not a design's bug.
extend.4 and cross32.4's definitions run clean; bisecting kernel.4 by line (a cut that leaves it
compiling hangs instead of crashing - counted as no crash), the first crashing line is the target's
DO, and in it `POSTPONE (DO)` alone. The cross compiler has only ever run on a 64-bit host -
reseed.sh makes even the 4-byte seed there. The lead: its name hash or T-IMMEDIATE?'s thread walk
assuming 64-bit wraparound. (2) tag2 at 4-byte cells: the converter refuses it ("64-bit cells for
now - a DOES> body's 4-byte call must fit its first cell"), and every design on the fronts has tag2.
Both are real ports; the draft patch (results/drafts/cell32-wip.patch) is unchanged.

## Iteration 328 - 2026-10-16 - Claude

**The cross compiler on a 32-bit host - fixed: a 32-bit Forth now builds the 4-byte kernel,
byte-identical to kernel32-seed.img.** POSTPONE (DO)'s crash, followed into T-IMMEDIATE?'s thread
walk and its @-T: the sign extension ran "when the target cell is narrower than this host's own",
says its comment - the code said narrower than 8. On a 32-bit host building the 4-byte kernel it
extended anyway, and -1 32 LSHIFT on a 4-byte cell is a full-width shift, which x86 masks to
nothing: every negative link read -1, and the walk ran into unmapped memory. The fix, [ 1 CELLS ]
LITERAL, is invisible on a 64-bit host - the same HERE after the cross compiler (4,344,888), the
same kernel-seed.img - and on the 32-bit cell engine the whole 4-byte kernel built, 14,976 bytes,
identical to the seed a 64-bit host makes. Next: tag2 at 4-byte cells - the converter writes a
CREATE'd word's first cell as opcode + 4-byte call (5 bytes); the port is a two-cell code field
there, agreed between the converter, the engine's DOVAR and DODOES, the run-time compiler's CREATE
and >BODY, and the kernel's - FORMAT-TAG2.md's "left: 32-bit cells - before the Tegra".

## Iteration 329 - 2026-10-16 - Claude

**tag2 at 4-byte cells - and 32-bit x86 at native 4-byte cells: 14 of 14 designs alive.** The
converter refused tag2 below 8-byte cells: a CREATE'd word's first cell held the DOVAR or DODOES
opcode and the 4 bytes a DOES> call needs - 5 bytes. The engine (DOVAR's and DODOES's TAG2
branches) and the run-time compiler (CREATE8, >BODY8) already put the body at align(body + 5);
only the converter assumed one cell. cfd(): align_up(5, CELL) - 8 at both widths, so the 64-bit
images are the same bytes (3 of 3, old converter against new) and at 4-byte cells the code field
is two cells - at the seven places that size it or find its body. Then the sweep at 4-byte cells
as 32-bit x86 engines: s6 and 13 of seed 53's front, every one tag2 - the corpus right, and each
rebuilt the 4-byte kernel byte for byte with its own run of the cross compiler (Iteration 328's
fix). The draft patch (results/drafts/cell32-wip.patch) now carries tools/layout.py too. Next: ARM.

## Iteration 330 - 2026-10-16 - Claude

**ARMv7 at native 4-byte cells: 5 of 5 alive under qemu-arm.** s6 and four tag2 designs of seed
53's front, built by arm-linux-gnueabihf-gcc as EABI5 engines, run through qemu-arm: the corpus
right and the 4-byte kernel rebuilt byte for byte. One fix: MAP_32BIT is x86's - 32-bit x86's
headers have it, which is why -m32 compiled - and ARM's do not; 0 where the host has none, every
address below 4 GB there anyway. The harness wraps each ARM engine for qemu and, in itself only,
lifts sh()'s jail (qemu maps past its 1 GB) and multiplies the CPU limits. What qemu cannot say:
whether a Cortex-A9 faults on an unaligned 64-bit load - the Tegra's own run will. Next: the
checks - dream's 32-bit line and rage native - and the batch through run-tests and the gate.

## Iterations 331-332 - 2026-10-16 - Claude

**The 32-bit checks wired, tested, and pending as the after-seed-54 batch.** dream.lan cannot link a
32-bit binary ("4-byte cells DISABLED" in its build log), so its 32-bit check measures the laptop's:
-m32 builds linked with the static i386 runtime, run where no 32-bit library is; and the 4-byte
references it cannot make (the 32-bit cell engine and its image, the base k32 dumps), shipped in
the bundle; setup() takes the shipped s6 (EVOLVE_PREBUILT_REF). xcheck --sample --cell 4 takes a
design only once it builds and lives as a 32-bit engine on the laptop. remote-checks.sh runs several
checks a host, one after another under the host's lock (flock on a descriptor in run.sh itself, so
stop still kills its group), each deadline from its own start. Every host's byte order and cell
width recorded - measured, not assumed. Tested with stand-in hosts: 64-bit prebuilt, 32-bit
prebuilt (after a bug of mine: `; rp = private_work(rd)` left on the else branch's line), a simulated
32-bit native host - all measured and gathered, the lock holding the second check back. Then 64 bits
proven unchanged: six designs' engines and images byte-identical against a clean clone, gene-equiv
PASS with every operator draw, run-tests 63 paths, validate 7 of 7, the gate 245 of 245.

## Iteration 333 - 2026-10-16 - Claude

**Seed 54 processed - small - and the 32-bit checks applied; seed 55 next, 6 hours.** The chain
done in 8 h 40 min of its 9: the evolution 6 h 47 min, the comparison at 6 rounds 1 h 18 min. The
verdict: fastest +3.6%, smallest +0.05%, memory -2 KB, hypervolume +1.1%, best Q +0.9% - small, the
second in a row: the stopping rule's end of these genes. bfind on 67 of the 195 of the front, from
17 after seed 53's 80 minutes - the laptop's selection keeping what the VM could not measure. No
corpus deaths; one converter death, a new kind - "call target 1390 not 8-aligned", one of 41,406
(results/drafts/convert-align-death.md). heldout 0.953, though one of the ten fastest by selection
is 27th on sieve. dream.lan: Spearman 0.941, the laptop's six fastest 3 4 2 10 1 5 there. Predictions
five of five. Then the after-seed-54 batch applied - run-tests, validate 7 of 7, the gate 259 of 259
on seed 54's own front. Seed 55 (the owner: 6 hours) runs the same genes a third time, for the
checks: the laptop, dream.lan at 64 and at 32 bits, and the Tegra - all four, for the first time.

## Iteration 334 - 2026-10-16 - Claude

**Seed 55 processed - small, the third of these genes - and the first checks at both widths: the
skew the owner feared, measured.** dream.lan at 64 bits agrees with the laptop at Spearman 0.940;
at 32-bit x86 with 4-byte cells (the laptop's static builds of 24 interpreted designs), 0.694, the
laptop's six fastest 8th to 13th there. The slow designs keep their place; the fast ones lose about
half their lead over s6 (one: 0.368 of s6's time on the laptop, 0.700 there). It mixes machine and
width - the two samples shared only 8 designs, nearly all slow and within 5% of each other, their
ranks noise - so the next check takes the 64-bit sample from the 32-bit one's pool. The Tegra failed
again: build-stages.sh compiles four hand-made engines the 32-bit work had not ported (pack4.c
first); ported now - each compiles for ARM with build-stages' flags, the 16 64-bit binaries are
identical, run-tests and validate pass - pending as the after-seed-55 batch. bfind on 80 of 168,
heldout 0.959, predictions four of five (the Tegra's). NEXT-RUN: none - the stopping rule.

## Iteration 335 - 2026-10-16 - Claude

**Seed 56 for 6 hours, and both of the owner's: the run, then selecting at both widths.** The
after-seed-55 batch applied - the Tegra's four engines (run-tests, validate 7 of 7, the gate 248 of
248). dream.lan gets a third check, prebuilt64 --from prebuilt32: xcheck --sample --ids takes exactly
the 32-bit check's designs and builds them at 64 bits, so the next run measures the same designs at
both widths on one machine - the width alone, which seed 55's two samples (8 designs in common,
nearly all slow) could not. Tested with stand-in hosts: the two samples the same ids, both measured,
one after the other under the host's lock, 4-byte and 8-byte cells recorded. Selecting at both
widths drafted (results/drafts/two-width-selection.md): a design's interpreter measured at 4-byte
cells on the laptop as a second speed objective - the JIT designs judged at 32 bits by the
interpreter under their JIT; not one combined score, which would let a weakness hide. Its decisions
are the owner's before it is built - after seed 56 starts.

## Iteration 336 - 2026-10-16 - Claude

**Selecting at both widths, begun - the first two-width evolution ran through (results/drafts/
two-width-wip.patch).** The owner agreed to the draft's decisions: the JIT designs judged at 32 bits
by the interpreter under their JIT, speed32 a fourth objective. evolve.py --widths 8,4: setup at
4-byte cells first, its four width-dependent globals kept and swapped in by at_width() for each
design's 32-bit measurement (the design, jit off, as a 32-bit x86 engine, after its 64-bit one);
dominance and crowding with speed32. A scratch run - population 4, one generation - gave 20 designs,
all alive at 64 bits, 12 with speed32. The other 8 say what the 32-bit measurement is for: four
converter assertions ("call target ... not 8-aligned") - the one that killed a design of seed 54's
at 8-byte cells, far more often at 4 - and a corpus death at 4-byte cells. Faults to fix before the
selection leans on speed32, or it would steer away from call encodings for the converter's sake.

## Iteration 337 - 2026-10-16 - Claude

**The converter's call alignment, two of its faults fixed (in results/drafts/two-width-wip.patch).**
Both "call target ... not aligned" assertions are scaled calls (--cpt S reaching multiples of 2^S).
Word starts: bodies aligned to the cell, 4 at 4-byte cells, where S = 3 wants 8 - now aligned to
max(cell, 2^S), the same at 8-byte cells. SKIPPAD's shortcut (the CPT16 family's call landing past a
data word's pad, body + CELL - 2) is never reachable for S >= 2: that was seed 54's one converter
death (1390 = 6 mod 8) - now taken only where reachable; that design converts and lives. The second
two-width scratch run: 13 of 20 with speed32; left, 5 mid-word targets (DOES> tails, aligned only for
S > 1) and a CPT16 one, and the corpus death at 4-byte cells. Next: their S, then the tails, then the
corpus death's bisect.

## Iteration 338 - 2026-10-16 - Claude

**Selecting at both widths - built, tested, pending as the after-seed-56 batch.** The last two
32-bit failures of the scratch runs: the converter's ordinary-header padding of Iteration 337 made
images convert but run-time definitions (aligned to the cell) out of a scale-3 call's reach - 7
corpus deaths; taken back out, and the 32-bit build caps the call scale at 2 instead (nothing is
8-aligned at 4-byte cells). And the cell family copied s0-cell-s64.img at any width - a 4-byte engine
refused it before printing a byte. Then 20 of 20 designs with speed32. NEXT-RUN's word `widths`; the
report's 32-bit column and seed-facts' lines from the data; compare-fronts still at 64 bits. 64 bits
unchanged: six designs byte-identical, gene-equiv PASS over 4,096 genomes, run-tests, validate 7 of
7, the gate on seed 55's front.

## Iteration 339 - 2026-10-16 - Claude

**What the JIT leaves to the interpreter - lab/evolve/jitleft.py, and the next genes' direction.**
Each JIT design profiled with the JIT off (all its dispatches) and on (what the JIT left: translated
words dispatch nothing). Seed 55's two fastest: fib, loop and ackermann translated whole, bubble 98%;
**kernel 56% interpreted, corpus 99.7%**. The benchmarks' run-time words are translated (fib, loop),
so the corpus's - each run once or a few times - stay below what makes the JIT translate. The rest
is the outer interpreter: INTERPRET, PARSE-WORD, REFILL, WORD, ?STACK. Two genes to look for: the
outer interpreter made translatable (which operation keeps each out - next), and when the JIT
translates code compiled at run time (results/drafts/next-genes.md).

## Iteration 340 - 2026-10-16 - Claude

**Why the JIT leaves what it leaves - jitleft.py --why, and the next genes named.** engine/jit.c
gained a -DJITLOG=1 build (analysis only: a normal JIT engine byte-identical) logging each refusal -
the operation, the return stack's order, a stencil, a callee, the memory - and jitleft.py --why
follows each word through refused callees to the root. On seed 55's fastest JIT design: 62.6% of
what the JIT leaves was **never tried** - the outer interpreter (INTERPRET, PARSE-WORD, REFILL,
?STACK) is the image's own code, and the JIT tries only words with its header (those compiled at run
time) and their callees: not blocked, not a candidate. The rest: operations with no mapping - vf
(5.1%: WORD, HERE), UM* (1.8%: *), WRITE, vs, 0<?BRANCH8, SP@, DUP?BRANCH8, UM/MOD. The genes: the
image's words as JIT candidates (the large one), and stencils for those operations (small ones).

## Iteration 341 - 2026-10-16 - Claude

**The gene jitimg built - and the next blocker found (results/drafts/jitimg-wip.patch).** Built on
top of the pending two-width batch (both change the converter): the image's plain code words given
the JIT header run-time words get. Level 1 (the outer interpreter's words) alive, 64 bytes larger;
level 2 (every plain word) dies on the corpus - to bisect. jitleft.py --why --set=jitimg=1: kernel
54.7% left to the interpreter (55.9%), "never tried" 48.1% of it (62.6%); PARSE-WORD now tried and
refused for vf - the engine's getstatic, VARIABLE @ fused - which keeps WORD and HERE out too, and
which the JIT has no stencil for; INTERPRET still excluded (its inline aligned data). So jitimg pays
only with stencils for vf and vs: next.

## Iteration 342 - 2026-10-16 - Claude

**jitvar - vf and vs given the JIT - and where the staircase leads.** vf (getstatic) and vs
(putstatic) mapped as a literal of the slot's address then @ or ! - no new stencil; two operand kinds
in jit.c's decoder under JITVAR (no other engine changes). With jitimg 1, both alive; jitleft --why:
INTERPRET now tried (refused for PLACE), PARSE-WORD and WORD refused for (PARSE), "never tried" down to
32.9% of what is left from 62.6% - but the totals unmoved (kernel 54.7% left): each word still
refused, one step on. The next blockers are C primitives - PLACE, (PARSE), (FIND) - which a stencil
cannot be: translating the outer interpreter needs helper calls, native code calling a primitive's C;
the JIT has none, its handlers labels in one threaded function. jitimg and jitvar saved as one draft
(results/drafts/jit-genes-wip.patch).

## Iteration 343 - 2026-10-16 - Claude

**jitimg and jitvar pending - patch 2 of the after-seed-56 batch - and helper calls designed.** The
owner approved both steps. jitimg offered at 0 and 1 (2 killed on the corpus); three engine paths -
jitimg with jitvar, jitvar at each slot encoding - 66 in all; off, six designs byte-identical; forced
on, 16 of 16 JIT designs of seed 55's front alive; the gate 248 of 248. Helper calls designed: the
stencils' ABI (spn_st f(cell *sp, cell tos)) lets a C function be called from native code as a
stencil is; spn-stencils.c's function-pointer hole (IMM_FN) and one stencil, CALLC, calling through
it; jit.c to patch that hole as it patches the literal's; the converter's table with the helper's
address for the linker; first h_place, written from PLACE's handler. Next turn: build it.

## Iteration 344 - 2026-10-16 - Claude

**Helper calls work - and a latent bug in pending patch 2, found before it shipped.** Building the
helper calls meant reading how jit.c fills literal holes: only for operand kinds 1-5, while jitvar's
slots are 8 and 9 - a translated vf would have fetched from address 0. Latent, since no word with vf
was translated yet; it would have struck as soon as helpers unblocked one. Fixed with a macro that,
without JITVAR, is the original tokens exactly (a parenthesized first form changed three JIT designs'
engines: GCC built a different && tree; builds proved deterministic). The helper calls: st_callc
through spn-stencils.c's function hole, jit.c patching it, h_place from PLACE's handler - all under
JITHELP. With them INTERPRET gets past PLACE and stops at COUNT - which is DUP 1+ SWAP C@, a table
entry. Drafts saved; the corrected patch 2 to re-verify and stage before the batch is applied.

## Iteration 345 - 2026-10-17 - Claude

**Pending patch 2 corrected and re-verified; the helper calls two steps further.** The token-exact
JIT_LITOPND re-verified - six designs byte-identical to patch 1's, the three the parenthesized form
had changed among them; the behavioural checks (66 engine paths, validate 7 of 7, forced 16 of 16, the
gate 248 of 248) hold for it, the JITVAR expansion being the same - and it replaces the pending patch
2. The helper-call draft re-cut against it, with h_parse and COUNT as a table entry: with all three
JIT genes the design lives, and INTERPRET gets past PLACE and COUNT to (FIND), PARSE-WORD past (PARSE)
to +!. +! is five lines; (FIND) reads the engine's own internals - the hard step.

## Iteration 346 - 2026-10-17 - Claude

**Interpreter re-entry built - and its first run crashes.** Modelled on SPN's spn_interp: jit_interp
spills the stack, pushes a sentinel, runs a nested virtual_machine() under the compiler's own setjmp
(no libc in an engine: the C library's would not link); the sentinel is a fake JIT word whose native
code is a trampoline that longjmps back - no new opcode. The JIT calls it through SPN's st_interp,
as an ordinary operation the converter adds (INTERP), so a refused callee no longer refuses its
caller. It builds and links; the design dies with the fault handler's exit 70 right after the banner.
Until now no word with a helper call, an interpreted call or vf had ever run natively - so this is
the first execution of all of them. Next turn: bisect them one at a time; QUIT - RP!, CATCH - the
likeliest. The draft saved (results/drafts/jitre-wip.patch).

## Iteration 347 - 2026-10-17 - Claude

**The bisection: helper calls proven, two faults named.** Run-time words, each variant's output
against the JIT off: with jitvar and jithelp, identical - PLACE's and (PARSE)'s helpers and COUNT run
natively and right. With image headers, exactly one of the outer interpreter's 18 words breaks it,
(PARSE): a one-operation word, which the compiler inlines by copying its body's first operation -
the JIT opcode, with a header there. And re-entry faults even in the simplest case, startup fine -
so not QUIT; one hazard fixed on the way (an interpreted callee entered at its header repointed its
"caller", the sentinel), not enough. gdb cannot run the engine; next, its fault handler made to print
the faulting address.

## Iteration 348 - 2026-10-17 - Claude

**The re-entry fault located - and a doubt about last turn's proof.** gdb cannot run these engines;
their own fault handler, given SA_SIGINFO in a scratch build (the lab's runtime installs it), printed
the faulting rip, the landmarks and the native code's bytes. Execution jumped into the dictionary:
U1's bytecode called as machine code. The disassembly shows why - U1's native code is an ordinary
S_CALL stencil aimed at a bytecode address, not the interpreter call: some path sends a refused
callee to S_CALL past the rewrite. And if helper stencils compile alike, last turn's "helper calls
proven" may only mean those words ran as bytecode - to check with JITLOG before it is claimed again.

## Iteration 349 - 2026-10-17 - Claude

**Interpreter re-entry works.** A scratch log of every callee decision and every translation, and
the stencils compiled by hand and disassembled, closed it: the converter numbered the INTERP row
max(t2_names()) + 1 = 0xFFFE - the translator's marker for "a call resolved" - so every interpreted
call became a native call into bytecode. Now numbered just above the operations. With refused
callees no longer stopping their callers, the decoder read past (S") into its string; jit_rtouch
refuses a caller whose callee pops the caller's return address. The test programs now give the
JIT-off output exactly, status 0, and the log shows the helper words really translated - last
turn's claim, now with its evidence. Next: (PARSE)'s header again, the corpus, the gates, the speed.

## Iteration 350 - 2026-10-17 - Claude

**All four JIT genes run correctly together - and have not yet moved the numbers.** The kernel
workload's fault, reported by the crashing build's own handler and mapped with nm, was in the
translator: with refused callees no longer ending a translation, it went on to decoded garbage calls
in the data after a (.") - and jit_rtouch had trusted callees it could not read. Now conservative,
with every callee address bounded. All variants pass the corpus and the kernel. But jitleft: kernel
54.6% left to the interpreter against 55.9% with none of the four, corpus 99.6% - INTERPRET stops at
(FIND), PARSE-WORD at +!, operations without a stencil, which re-entry for callees does not reach.

## Iteration 351 - 2026-10-17 - Claude

**Seed 56 first, 10 hours (the owner).** NEXT-RUN: seed 56 tag2 10h, the comparison at 6 rounds - about
8 hours of evolution after the reserve. Master as it is: the Tegra's engines (applied after seed 55)
and dream.lan's paired check - the same designs at 64 and 32 bits. The pending batch (selecting at
both widths, jitimg and jitvar) is applied after it; the JIT drafts (helper calls, re-entry) wait,
parked - their payoff so far unmeasurable (kernel 54.6% left against 55.9%).

## Iteration 352 - 2026-10-17 - Claude

**While seed 56 runs: why designs lose at 32 bits, and the comparison at both widths.** Thirty of
seed 55's front measured here at both widths (each design's interpreter): r = 32-bit / 64-bit speed,
each against s6 at its width - median 1.30, up to 2.44. Knockouts, one gene at a time, on the fastest
and on one from the slow end: the two-bit tag (tag2) helps at 64 bits and hurts at 32 (without it the
fastest is 22% faster at 32); the compiler gene's 35% is 64-bit only; and fsys 3 - the Forth file
layer over SYSCALL - is the slow design's whole 32-bit loss (2x). Two of these read like engine
inefficiencies at 4-byte cells rather than trade-offs (results/drafts/skew-32.md). And compare-fronts
--widths 8,4: a section "At 32 bits", tested on two small databases - pending as patch 3.

## Iteration 353 - 2026-10-17 - Claude

**tag2 at 32 bits, and what two widths cost.** tag2's cost at 32 bits holds up - three repeats: 16%
faster at 64 bits, 36% slower at 32. It lies in every operation's dispatch (the counted loop loses
most), not in the call path; the cell type shrinks with the host, so not that; and the 32-bit engines'
position-independent code (a base register spent in every dispatch) is real but not tag2's own cost -
built -fno-pie, the ratio did not move. And selecting at both widths costs x1.86 the evaluation time
(the draft guessed 1.2-1.5): a two-width run needs nearly twice the hours.
**And a correction.** fsys 3's 2x at 32 bits looked like a file layer seeking at 4-byte cells; strace
counted the same calls at both widths (a read and a seek back for every line, by design) - my first
reading had taken strace's time-sorted table for counts. The difference is each call's cost, and
here that is the VM: a microbenchmark puts a 32-bit int $0x80 at 12.49 us against 0.09 us for a
64-bit syscall - 140 times, where real hardware has two or three. So fsys 3's 32-bit penalty measured
on this VM is mostly the VM's; every 32-bit ratio measured here is inflated where a workload makes
system calls. tag2's cost stands - it sits in a loop that makes none.

## Iteration 354 - 2026-10-17 - Claude

**Seed 56 processed, and the after-seed-56 batch applied.** Small (hypervolume +1.3%, the fastest
4.1% behind the old front's), the fourth run of these genes. But the checks: all four machines
gathered for the first time. The Tegra's first native run, ARMv7 with 4-byte cells: Spearman 0.944 -
the laptop's ranking carries to another architecture. dream.lan's paired check put the same designs
at 64 bits (0.977) and 32 (0.833): on one machine Spearman 0.854 - the skew is the width's. Real
hardware also settled the VM's doubt: fsys 3 keeps its place at 32 bits (r 1.00). Those that lose are
the five fastest, one lineage (the C kernel primitives klookup and kinput among its marks). The batch
- two-width selection, jitimg and jitvar, the comparison at 32 bits - applied: 66 engine paths, the
gate 268 of 268 on seed 56's front. NEXT-RUN: none, for the owner's hours.

## Iteration 355 - 2026-10-17 - Claude

**Seed 57: one 12-hour run (the owner).** Asked one run of 12 hours or two runs of 12 in all: one -
each run's fixed part, from seed 56's timeline (57 min before the evolution: the tests and four remote
checks prepared; the re-measure; the comparison), is about 3 h 40 min with two widths, so two runs
would evolve about 4.6 hours against one's 8.3, at 1.86 times each design's cost. NEXT-RUN: seed 57
tag2 12h widths, the comparison with --widths 8,4. And the reserve learned --widths: the comparison's
share half again (164 minutes against 121 with seed 56's timings), its recorded time kept as one
width's so the next chain's estimate holds either way.

## Iteration 356 - 2026-10-17 - Claude

**This lab is RelF's base (the owner) - re-anchored on relf.** relf master (8ec0e75, its Iteration
718) is vendored with its sources (vendor/relf/tree: engine, Forth, shell, tools, the shell's VM
benchmarks, the CV8 documents) - tools/update-relf.sh now follows master, where relf's CV8 work is;
the copy builds here and runs relf's realistic shell script. relf's own ledger (its Iteration 716)
names what it wants from this lab: XF@ and XV@, DEFER, (+LOOP), PICK and fused pairs for CV8 - new
instructions, measured on its shell. relf already has the instrument (bench-vm.py: paired CPU time
with bootstrap intervals) and the workloads (loop, fn, str, arith, realistic, start). LICENCE.md:
GPLv2 only, as relf's and SOD32's. RELF.md: the adoption criteria and the plan.

## Iteration 357 - 2026-10-17 - Claude

**The A/B harness for relf - tools/relf-ab.sh - and this VM's noise floor.** A is the vendored relf;
B, the same with a candidate patch (its images rebuilt when the instruction map, kernel.4 or cross.4
change). B must fail nothing in relf's own make test that A passes - a regression gate, A's failures
recorded once per vendored commit; then relf's bench-vm.py on its six shell workloads. Getting there
vendored relf's tests and examples too (make test's first run here failed only for examples/ left
out); with them relf passes its whole suite on this VM. The noise floor, A against A, twelve rounds:
medians within 6 % of 1, intervals about 10 % wide either side (start, 30 %) - so this VM gates
correctness and large effects, and the ledger's candidates, 1.5-5 % of dispatches each, must be
measured on the laptop, as relf's own reports were. Next: the realistic script's instruction pairs.

## Iteration 358 - 2026-10-17 - Claude

**relf's realistic shell script, instruction by instruction and pair by pair - and the constraint
that frames relf's request.** tools/relf-pairs.py runs relf's own counting engine (its profile.py's)
and decodes the shell image, recording every instruction: 18,401,921 dispatches, agreeing with relf's
profile. VAR@ - a variable fetched in one dispatch - is 15.2 % of them; the pairs are led by VAR@ VAR@
(4.2 %) and VAR@ + (3.1 %), then 0= ?BRANCH (2.3 %) and + @ (1.8 %); the top ten about 18 %. But relf
had fused pairs and gave them up at its Iteration 536 (QUESTIONS.md A15) to bring its one-byte
opcodes to 64, the two-bit tag's prerequisite. So each candidate is a trade within that budget: its
pair's dispatches against those of the operation it pushes into the escape band.

## Iteration 359 - 2026-10-17 - Claude

**The budget for relf's fused instructions.** tools/relf-pairs.py --all counts the five shell scripts
together and sets each candidate against relf's 64 one-byte opcodes: the k-th best pair takes the k-th
coldest operation's slot, that operation then escaped. The coldest cost almost nothing (LIT64 0.03 %,
?BRANCH8 0.04 %, R@ 0.13 %), so the nets are nearly the pairs: VAR@ VAR@ 4.42 %, VAR@ + 2.81 %, 0=
?BRANCH 2.18 % - the top three about 9.4 % of all dispatches, twelve about 18. A first count had
offered DOVAR and DODOES as the coldest: they are data words' code fields, run each time a variable
is but outside any code body, so uncounted - kept, with NOOP, out of the trade.

## Iteration 360 - 2026-10-17 - Claude

**The first instruction-set patch for relf: `0= ?BRANCH` as one opcode - correct by relf's own suite,
2.1 % fewer dispatches.** Placed by relf's own rules: direct primitives are numbered by kernel.4's
PRIMITIVE order, so a new one would renumber the synthetic band; spec opcodes stand at explicit
numbers and the peephole emits them by number (PEEP-VAR's 100 and 101) - so 0=?BRANCH is spec 0x60,
b16. Four files: its row in opcodes.tab (both engines' tables generated from it), the C handler
(?BRANCH's, the test inverted), the assembly handler (jz to jnz), and kernel.4's IF-BRANCH, - IF's
branch, which rewinds a just-compiled 0= as PEEP-VAR rewinds a call. relf-ab.sh: relf's whole make
test passes (both engines and widths, images reproducing, the shell suites). relf-pairs.py on the
patched shell: 385,963 runs of the new opcode, 2.10 % fewer dispatches. Its time, about 1 %, is under
this VM's noise - the laptop's to measure.

## Iteration 361 - 2026-10-17 - Claude

**The second patch for relf: `var @ +` as one opcode - and what the dispatch count caught that the
test suite could not.** VAR@+ (spec 0x71, a slot operand): the variable added to the top of the stack;
kernel.4's peephole rewrites a just-compiled VAR@'s opcode byte in place when + follows it, nothing
between (NO-PEEP forgets the VAR@, as a branch landing there must). The first version passed relf's
whole suite, but its count came out 336,000 dispatches above the fusions' arithmetic: 167,966 more
calls and as many EXITs. kernel.4's inliner knows its slot opcodes by number (100, 101) and so had
stopped inlining every small word that now held VAR@+. Taught the new opcode, the inliner made calls
fewer than before (40,428 fewer): words shortened by the fusion now fit its limits. Both patches:
relf's whole make test passes; the realistic script 4.74 % fewer dispatches (the arithmetic exact to
48); this VM leaning faster, fn's ratio 0.933 with its interval below 1 - the laptop to confirm.

## Iteration 362 - 2026-10-17 - Claude

**The third patch for relf: `a @ b @` as one opcode - 6.41 % fewer dispatches with all three.** 2VAR@
carries two slots, a new operand format that relf's image tools (image-audit.py, superinst.py,
opcodes.py) and its inliner had to learn - the lesson of VAR@+ applied first. Its first version passed
relf's whole suite and never fired: CALL, begins with NO-PEEP, which since VAR@+ also forgot the last
VAR@, so compiling the call to b erased the first fetch before @ arrived. CALL, now keeps it; a real
call moves HERE past it, a branch target still clears it. Then: 2VAR@ about 329,000 times, VAR@+ a
little less (some `a @ b @ +` now 2VAR@ +, no loss), and calls fewer again - the realistic script
18,401,921 dispatches to 17,221,555, the arithmetic exact to 23. relf's whole make test passes; this VM
times realistic at 0.944 and arith at 0.947, both intervals below 1. Passing tests show a fusion safe;
only the count shows it happens. All three now the laptop's to time.

## Iteration 363 - 2026-10-17 - Claude

**A pause in the fusions, the genes classed for relf, and 32-bit engines as relf builds them.** On the
three-patch shell the remaining pairs are a flat field near 1 % each, no `0=` left before UNTIL's
branch - so no fourth opcode until the laptop times the three (each further one buys about 1 % and
spends a slot of relf's 64). This lab's genes classed by what relf would pay: C engine only (compiler,
regpin, d256, alignhot, sharedcall... - testable at once on relf's shell), opcode set or image format
(dear: both engines, the compilers, the tools, A15's trade), kernel words, and the JIT (not for CV8).
And this lab's 32-bit engines built -fno-pie -no-pie, as relf's are: three designs alive, plain
executables - pending after seed 57, so its own speed32 stays comparable with itself.

## Iteration 364 - 2026-10-17 - Claude

**This lab's cheap genes on relf's shell: none transfers.** The C-engine-only class, each through
relf's whole make test and timed on its shell: clang 3-5 % slower on four workloads; pinned registers
mixed (str 6 % slower, arith 4 % faster); -Os 2-5 % slower, three workloads significantly - though
clang and -Os are what every fastest design of seeds 55-56 chose. They belong to those designs' whole
combinations; relf's cv8.c is tuned with gcc -O2 by its own hundreds of iterations, and it has d256
and guard pages already. relf-ab.sh learned make variables for B alone (RELF_AB_MAKE_B, passed whole)
and to measure the shells it built: relf's make test rebuilt relf64 without the variable (an rbx count
of 98, against 434 pinned, gave it away); the shell measured had embedded the right engine, now by
construction. This lab's offer to relf is at its instructions' level, measured on its terms.

## Iteration 365 - 2026-10-17 - Claude

**The order of the work, from the owner: a generic Forth first.** This lab builds a generic Forth,
with no optimization for relf's shell. First the best generic designs, found on this lab's own
workloads; then how they fit relf and its shell; only then relf tuned for its shell - and relf too
kept as generic as possible. Recorded as a standing decision (HANDOFF) and at the head of RELF.md.
Iterations 357-364 went ahead of it: the three fusion patches were chosen from the shell's dispatch
profile - parked as phase-3 reference, their laptop timing optional. The relf profile for the search
and the port list from it are dropped; the tools stay for phases 2 and 3.

## Iteration 366 - 2026-10-17 - Claude

**An article from the findings: a goal, deprioritized** (the owner): revisited when the best designs
are found, and to be written from this log - so this log must hold, or name, everything it needs.
Audited: every iteration from 1 has its entry now (199's re-headed to 199-202, which it covered; 249
and 253 written from their commits); every file under results/ is named here or in an earlier entry,
the raw archives by their directory. From now on each iteration names the files it adds.

**Where the methods are**: lab/evolve/evolve.py's header - the genes (with each gene() definition's
comment, the iteration that made it), the operators, and the objectives: speed, the geometric mean of
end-to-end time (cycles where the hardware counters can be read, CPU time otherwise) over the
selection workloads - kernel, fib, corpus, loop, bubble, ackermann since Iteration 127 (kernel, fib,
parse, corpus until 41; loop added at 41) - each program loaded from a file (corrected at 369); size, the engine's plus the image's bytes (since
Iteration 75 - corrected at 368: this said the image's alone, as evolve.py's header did); memory (rss);
held out, never selected on: sieve and parse since 127 (loop until 41, sieve from 41); since Iteration 354 (--widths 8,4) speed at 4-byte cells a fourth. The
machines: results/amd-ryzen-8840hs.md (the laptop, every run) and results/armv7-tegra.md, dream.lan in
the cross-machine checks below, lab/evolve/REMOTES for how each is checked. The run-by-run extremes for
charts: results/progress-by-run.md (lab/evolve/progress-table.py). The stopping rule and every run's
verdict: the seed reports below, and HANDOFF.md's standing decisions.

**The aim, and the findings consolidated** (added at Iteration 368): GOALS.md - the aim, simplicity and
minimalism (Iteration 72), how success is measured, the conventions and the register of what was
rejected; the consolidated findings in the root documents: FINDINGS-CELL-WIDTH.md, FINDINGS-FOOTPRINT.md, FINDINGS-OUTER-INTERPRETER.md, FINDINGS-PERFORMANCE.md, FINDINGS-SPN.md, FORMAT-TAG2.md, JIT.md. The article's argument starts there; this log is their evidence, iteration by iteration.

**The files no entry had named** - named here, by kind, each with its own title:

**Seed reports - each run's verdict, front and facts**:
- `results/evolve-amd-ryzen-7-pro-8840hs-seed1.md` - Evolution on the Ryzen 7 PRO 8840HS - the first run
- `results/evolve-amd-ryzen-7-pro-8840hs-seed2.md` - Evolution on the Ryzen 7 PRO 8840HS - seed 2
- `results/evolve-amd-ryzen-7-pro-8840hs-seed6.md` - Seed 6 on the AMD Ryzen 7 PRO 8840HS (Iteration 36)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed7.md` - Seed 7 on the AMD Ryzen 7 PRO 8840HS (Iteration 40)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed8.md` - Seed 8 on the AMD Ryzen 7 PRO 8840HS (Iteration 42)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed9.md` - Seed 9 on the AMD Ryzen 7 PRO 8840HS (Iteration 45)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed10.md` - Seed 10 on the AMD Ryzen 7 PRO 8840HS (Iteration 47)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed11.md` - Seed 11 on the AMD Ryzen 7 PRO 8840HS (Iteration 52)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed12.md` - Seed 12 on the AMD Ryzen 7 PRO 8840HS (Iteration 53)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed13.md` - Seed 13 on the AMD Ryzen 7 PRO 8840HS (Iteration 56)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed14.md` - Seed 14 on the AMD Ryzen 7 PRO 8840HS (Iteration 62)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed15.md` - Seed 15 on the AMD Ryzen 7 PRO 8840HS (Iteration 63)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed16.md` - Seed 16 on the AMD Ryzen 7 PRO 8840HS (Iteration 72)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed17.md` - Seed 17 on the AMD Ryzen 7 PRO 8840HS (Iteration 76)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed18.md` - Seed 18 on the AMD Ryzen 7 PRO 8840HS (Iteration 77)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed19.md` - Seed 19 on the AMD Ryzen 7 PRO 8840HS (Iteration 78)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed20.md` - Seed 20 on the AMD Ryzen 7 PRO 8840HS (Iteration 79)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed21.md` - Seed 21 on the AMD Ryzen 7 PRO 8840HS (Iteration 82)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed22.md` - Seed 22 on the AMD Ryzen 7 PRO 8840HS (Iteration 83)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed23.md` - Seed 23 on the AMD Ryzen 7 PRO 8840HS (Iteration 86)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed30.md` - Seed 30 on the AMD Ryzen 7 PRO 8840HS - the first run with jitx (Iteration 109)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed36.md` - Seed 36 on the AMD Ryzen 7 PRO 8840HS - from scratch: the anchoring test (Iteration 123)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed40.md` - Seed 40 on the AMD Ryzen 7 PRO 8840HS - the batch's first run: the JIT genes, half the time of the best before (Iteratio
- `results/evolve-amd-ryzen-7-pro-8840hs-seed41.md` - Seed 41 on the AMD Ryzen 7 PRO 8840HS - small: the JIT genes spread, the gene set converging (Iteration 198)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed42.md` - Seed 42 on the AMD Ryzen 7 PRO 8840HS - not small: the knee moved (Iteration 209)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed44.md` - Seed 44 on the AMD Ryzen 7 PRO 8840HS - small, the first: fsys 5 found its place at the small end (Iteration 230)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed47.md` - Seed 47 on the AMD Ryzen 7 PRO 8840HS - small: every measure inside the rule, hypervolume +1.4% (Iteration 269)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed49.md` - Seed 49 on the AMD Ryzen 7 PRO 8840HS - not small: hypervolume +4.0% (Iteration 288)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed50.md` - Seed 50 on the AMD Ryzen 7 PRO 8840HS - small: hypervolume +0.4% (Iteration 296)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed51.md` - Seed 51 on the AMD Ryzen 7 PRO 8840HS - small, the fastest +4.9% (Iteration 300)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed52.md` - Seed 52 on the AMD Ryzen 7 PRO 8840HS - small (Iteration 310)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed53.md` - Seed 53 on the AMD Ryzen 7 PRO 8840HS - small (Iteration 320)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed54.md` - Seed 54 on the AMD Ryzen 7 PRO 8840HS - small (Iteration 333)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed55.md` - Seed 55 on the AMD Ryzen 7 PRO 8840HS - small; the first run checked at 32 bits (Iteration 334)
- `results/evolve-amd-ryzen-7-pro-8840hs-seed56.md` - Seed 56 on the AMD Ryzen 7 PRO 8840HS - small; the first run checked on four machines (Iteration 354)

**What each gene is worth - knockouts**:
- `results/evolve-knockout-amd-ryzen-7-pro-8840hs.md` - What each gene is worth - knockouts on the Ryzen 7 PRO 8840HS

**Cross-machine checks**:
- `results/xcheck-dream-seed54.md` - dream.lan's check of seed 53's front, during seed 54 (Iteration 333)
- `results/xcheck-dream-seed55.md` - dream.lan's checks of seed 54's front, during seed 55 (Iteration 334)
- `results/xcheck-seed56.md` - The checks of seed 55's front during seed 56 - four machines (Iteration 354)

**Machines and their measurements**:
- `results/amd-ryzen-7-pro-8840hs-x86_64-run1.md` - Results
- `results/amd-ryzen-7-pro-8840hs-x86_64-run2.md` - Results
- `results/amd-ryzen-8840hs.md` - AMD Ryzen 7 PRO 8840HS, 16 cores
- `results/armv7-tegra.md` - ARMv7 (NVIDIA Tegra), 4 cores, Gentoo
- `results/spn-amd-ryzen-7-pro-8840hs-x86_64.md` - SPN measurements: AMD Ryzen 7 PRO 8840HS w/ Radeon 780M Graphics

**Drafts - scripts, patches and data behind the analyses**:
- `results/drafts/callrel-draft.patch` - a patch
- `results/drafts/founder-variants-iter187.txt` - a measurement's raw output
- `results/drafts/frontmeasures.py` - a script
- `results/drafts/gp-credit.py` - a script
- `results/drafts/gp-linkage.py` - a script
- `results/drafts/hybprice-iter172.txt` - a measurement's raw output
- `results/drafts/hybprice.py` - a script: hybprice: the hybrid stack/register design priced on every executed dispatch,
- `results/drafts/hybprice3-iter173.txt` - a measurement's raw output
- `results/drafts/hybprice3.py` - a script: hybprice: the hybrid stack/register design priced on every executed dispatch,
- `results/drafts/jithelp-wip.patch` - a patch
- `results/drafts/loop-audit-chains.py` - a script
- `results/drafts/loop-audit-inventory.py` - a script
- `results/drafts/loop-audit-profile.py` - a script
- `results/drafts/opcall-repro.py` - a script
- `results/drafts/pgo-draft.patch` - a patch
- `results/drafts/regprice-iter178.txt` - a measurement's raw output
- `results/drafts/relf-gene-classes.md` - This lab's genes, by what relf would pay to adopt one (Iteration 363; RELF.md item 4)
- `results/drafts/skew-32-front.jsonl` - data, one JSON record per line
- `results/drafts/skew-32-knockouts.jsonl` - data, one JSON record per line
- `results/drafts/surrogate-additive.py` - a script
- `results/drafts/surrogate-parents.py` - a script
- `results/drafts/surrogate-replay.py` - a script
- `results/drafts/surrogate-train.py` - a script
- `results/drafts/threads-profile.py` - a script
- `results/drafts/two-width-scratch-db.jsonl` - data, one JSON record per line

**Gene studies and analyses**:
- `results/bss.md` - Scratch buffers out of the image file: the gene `bss`
- `results/dropx8.md` - The compiler's X8 copies, dropped: the gene `dropx8`
- `results/fused-keep-tests.md` - Tests that keep their value: DUP ?BRANCH and OVER ?BRANCH
- `results/jit-kernel-words.md` - Kernel words made native, priced (Iteration 103)
- `results/kfast.md` - The Forth sources: where the dispatches go, and the gene `kfast`
- `results/lean.md` - Build artifacts left out of the image: the gene `lean`
- `results/price-hotcalls-seed3-front.md` - One-byte calls through a table of hot words - priced on seed 3's front
- `results/relf-pairs-realistic.md` - relf's realistic shell script, by instruction and by adjacent pair (Iteration 358)
- `results/rtimm.md` - n + and SWAP n + in code compiled at run time: the gene `rtimm`
- `results/rtloopall.md` - rtloop for a design with all eight loop opcodes: the gene `rtloopall`

**Archives, named by directory**:
- `results/applied-after-seed39/` - the batch applied after seed 39: ORDER.md names each patch, its order and its tests (15 files)
- `results/applied-after-seed40/` - the batch applied after seed 40: ORDER.md names each patch, its order and its tests (6 files)
- `results/applied-after-seed41/` - the batch applied after seed 41: ORDER.md names each patch, its order and its tests (27 files)
- `results/applied-after-seed42/` - the batch applied after seed 42: ORDER.md names each patch, its order and its tests (9 files)
- `results/applied-after-seed43/` - the batch applied after seed 43: ORDER.md names each patch, its order and its tests (5 files)
- `results/applied-after-seed44/` - the batch applied after seed 44: ORDER.md names each patch, its order and its tests (6 files)
- `results/applied-after-seed45/` - the batch applied after seed 45: ORDER.md names each patch, its order and its tests (7 files)
- `results/applied-after-seed46/` - the batch applied after seed 46: ORDER.md names each patch, its order and its tests (5 files)
- `results/applied-after-seed47/` - the batch applied after seed 47: ORDER.md names each patch, its order and its tests (7 files)
- `results/applied-after-seed50/` - the batch applied after seed 50: ORDER.md names each patch, its order and its tests (5 files)
- `results/applied-after-seed51/` - the batch applied after seed 51: ORDER.md names each patch, its order and its tests (3 files)
- `results/applied-after-seed52/` - the batch applied after seed 52: ORDER.md names each patch, its order and its tests (3 files)
- `results/applied-after-seed54/` - the batch applied after seed 54: ORDER.md names each patch, its order and its tests (2 files)
- `results/applied-after-seed55/` - the batch applied after seed 55: ORDER.md names each patch, its order and its tests (2 files)
- `results/applied-after-seed56/` - the batch applied after seed 56: ORDER.md names each patch, its order and its tests (4 files)
- `results/drafts/chat-to-iter265/` - the earlier chat's working material to Iteration 265: logs, scripts, jobs, patches (457 files)
- `results/drafts/fsys/` - 5 files
- `results/pending/` - 2 files
- `results/relf-patches/` - 5 files

## Iteration 367 - 2026-10-17 - Claude

**The supers gene: a misnamed pool in every tag-2 design, and no slots in nearly all.** design_pairs
profiles a design and gives the supers gene its pool of hot pairs, naming each profiled code as a
plain CV8 opcode - but a tag-2 design profiles its own one-byte codes, assigned through a per-design
table (vm-tag2-one.h; t2hot orders it hot first), the identity for 5 codes of 128 in seed 56's fastest
(a0a0277bf2). So since tag2 (Iteration 66) every tag-2 design's pool was its codes misread: "OR DROP"
at 5.12 % was DUP and a specialisation; wide codes 128-191 were dropped. It cost little speed by
accident: superinstructions' slots go first to format-10 words - the fastest lists 17 pairs and builds
none - and across seeds 55-56 only 4 and 6 of 168 and 187 front designs built any (71 and 94), all
misread pairs (NEGATE NEGATE, DROP UM*, XOR C!): engine bytes for nothing. Really there, among fusable
primitives: + XOR at 3.80 % of 105,295,516 dispatches, then 0.25 % and less. The fix names the codes
through the table and keeps the wide ones: its pool for a0a0277bf2 is the hand count's, and the same
genome without the tag - named right all along - gives the same ten pairs. Pending after seed 57
(results/applied-after-seed57/tag2-pairs-after-seed57.patch, ORDER.md's second); the finding in
results/drafts/supers-tag2.md. Open for the owner: whether pairs should compete with format-10 words
for the slots by value. Found by the generic pair analysis proposed at Iteration 365 - which turned
out to exist already (price.py, design_pairs), so the work was auditing it rather than building it.

## Iteration 368 - 2026-10-17 - Claude

**The aim restated where a new chat reads first: simplicity and minimalism.** GOALS.md has made it the
project's main goal since Iteration 72 - the smallest, simplest system that does the job; small images,
a small and plain engine, few mechanisms, each easy to read and to remove; speed where it costs little,
never as a reason for complexity - and README.md opens with it. But HANDOFF's "What this is" described
the search and its objectives without it, and a summary written from there (Iteration 365's) left it
out; the owner asked that it be explicit. Now HANDOFF opens with it, RELF.md puts it above relf ("in
every phase the aim stays GOALS.md's"), and evolve.py's header says what size is: the engine's plus the
image's bytes since Iteration 75 - its "the self-hosting image" predated that, and Iteration 366's
methods note had repeated it (corrected there, and pointed to GOALS.md and the FINDINGS documents).
The supers question, left to the lab by the owner, decided by GOALS.md's own rule: no new slot
mechanism (it would tie each genome to its profile, for one pair at 3.8 % of dispatches); the fixed
pool lets the search weigh a pair against a format-10 word in one mutation; after seed 58, if
superinstructions still buy nothing, the gene comes out of tag-2 designs, as rtlit did.

## Iteration 369 - 2026-10-17 - Claude

**Dormant list genes are by design; the methods' workloads corrected; the open items rewritten.** After
the supers finding, every list gene audited for entries that never take effect. Format-10 words: about
half are listed past their slots - seed 55, 5,110 listed and 2,492 built; seed 56, 5,714 and 2,858 -
mostly compare-and-branch fusions (>?BRANCH, U<?BRANCH8, ?NBRANCH...) left in the tail by selection.
Not a fault: a mutation inserts a word at a random place (the search can promote any), and express()
keeps only what is built - a design's identity, and what seed-facts.py counts (its expressed ops10 equal
ops10_in on all 187 of seed 56's front) - so past adoption claims stand; dormant entries are a neutral
reservoir. I had suspected the reports; checked before changing anything, the suspicion was unfounded.
The supers naming (367) stays the one real fault. Two documents had the selection workloads wrong:
evolve.py's header and Iteration 366's methods note said kernel, fib, parse and corpus with loop held
out - that was the start; loop was selected from Iteration 41 (sieve held out), and since 127 selection
is kernel, fib, corpus, loop, bubble, ackermann, with sieve and parse held out (git: 467dc55, 7814967).
Both corrected. HANDOFF's open items rewritten to the state now - the old list still called the runner,
the 32-bit follow-ups and the two-width batch to-dos, and seed 52 next.

## Iteration 370 - 2026-10-17 - Claude

**The footprint workload's generator** (lab/evolve/footprint-gen.py; results/generalization.md,
section 3 and its Iteration 370 note): selection measures small programs whose hot code fits, so a
held-out program whose code footprint grows - N words in levels, each calling one of the level below
(chains of at most 8, any N), a table of their tokens run round-robin, a checksum; --defs-only for the
compile phase. Its first version had two faults the validation caught: `7 AND +` takes two cells (now
`DUP 7 AND +`, every operation one cell in, one out), and the table was only in the full variant, so
the subtraction measured N dictionary lookups, not the run - read from timings that did not fit (N =
100 and 10,000 making the same 200,000 calls 35 times apart). And my first comparison matched the
interpreter's closing OK, not the checksum. Fixed: s6 and seed 56's fastest, its JIT on, agree at N =
100, 1,000, 10,000 and 30,000 (55,288, 4,166, 24,548, 6,157). Rough single runs here: compile time
quadratic on s6 (10,000 words 3.4 s, 30,000 41 s), superlinear on the hashed fastest (0.31 s, 3.0
s); the run phase slowing with N on both (s6 0.03 to 0.14 s for 200,000 calls from N = 100 to 10,000)
- the footprint effect, to be measured on the laptop with --calls scaled to N.

## Iteration 371 - 2026-10-17 - Claude

**The footprint experiment** (lab/evolve/footprint.py; results/generalization.md): the chain's
`experiment footprint.py` - a sample of the newest run's front timed on footprint-gen.py's programs of
N words, full and definitions-only, in rounds with hand-made s6 (once per round, size and variant: at
30,000 words it costs most of a round), its order alternating; medians; checksums checked against s6's;
each design's run and compile phases against s6's, and at each N the rank agreement of the selection's
speed with the run phase's. Two faults found in trying it: the unit - METRIC is CPU time unless
EVOLVE_METRIC=cycles, so a match is not cycles - and the re-measure lookup, which for a file not named
db*.jsonl derived the file's own name and read markdown as JSON (compare-fronts.py's loader assumes the
chain's names; this one checks). End to end on 2 designs, N = 100 and 1,000, 2 rounds: s6's run phase
157.5 ns a call at N = 100, 274.9 at 1,000 - the footprint effect, seen even here; the sampled fastest
0.280 and 0.234 of s6. Proposed for the chain after seed 57: `then experiment footprint.py`.

## Iteration 372 - 2026-10-17 - Claude

**Housekeeping: the tests green, and every document's citations checked.** run-tests.sh: PASS, no
regressions, after Iterations 361-371's changes. Then every path cited in the 222 tracked documents
(not the vendored relf, not the chat-to-iter265 archive): 1,618 citations, 120 distinct ones naming no
file. 62 were patches cited at results/pending/ after the routine had moved them to their
applied-after-seedN/ directory - the move never carried the citations along; rewritten (16 of them
had a copy in the chat-to-iter265 archive too - the applied one taken), and HANDOFF's step 7 now
carries them with one command. Of the rest, all explained, none in a current document wrong: prompts
cited by number (prompts/01 for prompts/01-problem-framing.md - the convention), names wrapped across
a line, placeholders (seedN, spn-HOST), prose (corpus/parse/kernel), relf's own paths in RELF.md
(engine/cv8.c, bench/langs/bench.4 - vendor/relf/tree), and a plan's never-made directory
(FORMAT-TAG2.md's forth/tag2/, "the plan was"). I had first called the prompts missing - they are
tracked; checked before changing anything. Eleven files cited here were deleted when superseded;
each is in git, before the commit that deleted it (git show COMMIT^:PATH):

| deleted | by | where it went |
|---|---|---|
| results/drafts/bfind-wip.patch | dabaa3b (Iteration 317) | the after-seed-52 batch, patch 2 |
| results/drafts/cell64-wip.patch | ec9eb72 (326) | the 32-bit checks at native 4-byte cells |
| results/drafts/cell32-wip.patch | 450e77a (332) | the 32-bit checks, pending, then applied after seed 55 |
| results/drafts/two-width-wip.patch | dca350b (338) | selection at both widths, applied after seed 56 |
| results/drafts/jitimg-wip.patch | 507a86c (342) | jitimg and jitvar, then the jit-genes patch |
| results/drafts/jit-genes-wip.patch | f7f1c8d (343) | the after-seed-56 batch, patch 2 |
| results/drafts/jit-genes-fixed.patch | 0f781e9 (345) | patch 2 corrected - applied-after-seed56/ |
| results/drafts/coreext-after-seed40-draft.patch, recurse-noname.md | 5b30490 (171) | the standard's words, ready |
| results/pending/skipscan-after-seed39.patch | 6e5afed (145) | tab-free parsing, its replacement |
| tools/sysc-xform.py, tools/test-sysc-shell.sh | 23e66f3 (169) | the after-seed-39 batch applied; run-tests.sh's shell suite |

Then two more checks, the same iteration. **The consolidated findings documents predate the search**:
FINDINGS-CELL-WIDTH (2026-09-13), -PERFORMANCE (09-29) and -FOOTPRINT (09-30) are the hand-made VM's,
before Iteration 1; -OUTER-INTERPRETER stops at Iteration 4, -SPN at 31, JIT.md at 108 (missing
jitloop, jitinl, jittail, jitk, jitimg, jitvar and the parked drafts); only FORMAT-TAG2.md is recent
(333). Neither the superinstruction finding (367) nor the workloads' correction (369) touches them.
So the search's own findings, Iterations 1-372, are consolidated nowhere yet - this log, the seed
reports and the drafts hold them: for the article, that consolidation is part of the work. And **what
the search chose** (results/drafts/gene-usage-53-56.md): every gene over seeds 53-56's 722 front
designs - msc, scale and tail never on; eight genes under 10% of every front; twelve on in every
design; the JIT on 445, clang on 181. My first count read only the values present - a gene at its
default is absent from an expression - and called compiler=1 universal (GCC is 541 of the 722);
caught by a contradiction with express()'s own rule, before anything was written. The evidence for
a simplicity review after seed 57, whose two widths may bring an off side back.


## Iteration 373 - 2026-10-17 - Claude

**Is the search stuck in a local optimum? (the owner's question) - and a correction.** Iteration
372's audit listed tag2 and bytehdr as on in all 722 front designs, as the search's choice. They are
imposed: every run since Iteration 71 is `seed N tag2`, evolve.py's --require tag2, which sets both
on every CV8 design - the plain CV8 encoding has not been searched with today's genes since then.
Corrected in results/drafts/gene-usage-53-56.md and HANDOFF before the simplicity review could rely
on it. The question has three answers here: a true local optimum is possible - four small runs in a
row, ten genes fixed by choice, the fastest from one lineage, every run carrying the last fronts, and
the screen skipping children predicted worse (a valley's first steps) - against the attic (lost gene
values kept and fed back), borrowing (whole blocks across a valley), dormant genes, and seed 36's
from-scratch run (Iteration 123), which reached the carried runs' region and not past it, with the
genes of then; a constraint - tag2 required, at 32 bits a 36% cost; and blind spots - the
superinstructions misnamed for 300 iterations (367). Proposed for the owner's hours after seed 57
(HANDOFF 4c): the anchoring test again (nocarry or fromzero) and a run without the tag2 requirement;
the simplicity review's freezing after them - a frozen gene would make an anchoring permanent.

## Iteration 374 - 2026-10-17 - Claude

**Seed 58 set as the anchoring and constraint test (the owner's go).** `seed 58 12h widths nocarry then
experiment compare-fronts.py --rounds 6 --widths 8,4 --frontier --cpus 2,8`: from scratch (the
hand-made designs and founders, no earlier front) and without the tag2 requirement every run since
Iteration 71 has had, at both widths - back in the carried region with tag2 chosen by the search
itself, and neither concern holds; elsewhere, a follow-up separates anchoring from the constraint.
So that seed 58 can start when seed 57's chain ends, the after-seed-57 batch is applied now, before
seed 57's processing (its one condition - seed 57 run on the code before it - holds): non-PIE 32-bit
engines and superinstruction pairs named right; run-tests.sh PASS; moved to
results/applied-after-seed57/, its citations carried by step 7's command (its first use). Two checks
for the path no run has taken since Iteration 71: seed 56's front made plain CV8 (tag2 off) - 10 of
10 built and alive, JIT and not; a miniature run in seed 58's configuration (8 a generation, 1
generation, both widths) - 24 of 24 alive, speed32 on all, 18 plain and 6 tag-2 (one turned on by
mutation), four encodings. This bundle goes to ~/Downloads only after seed 57's chain has finished.

## Iteration 375 - 2026-10-17 - Claude

**Ready for the first two-width run's processing.** The stopping rule judged runs at 64 bits only -
its five measures, the hypervolume three-dimensional - so seed 57, the first run selected for speed at
32 bits, could be judged small while its gain there went uncounted: what Iteration 188's rule was made
against ("a small size increase for a big speed gain is a gain - do not lock such out"). Proposed,
for the owner to confirm (GOALS.md): a run selected at both widths is small only if its fastest at 32
bits moved under 5% too; the 3-D hypervolume kept, comparable with every earlier run.
compare-fronts.py's 32-bit section now prints the verdict at both widths, for the run being judged
only, as its 64-bit table does. Tested end to end on two three-design runs from seeds 55 and 56, the
first try not judging at all: two databases outside the archive both labelled "this clone: db.jsonl",
so each run's "others" were empty - the test's layout, not the patch; laid out as an archived run and
the current one, the current judged not small at both widths (its 32-bit fastest +24.5%), the archived
"(an earlier run)" in both tables. Seed 57's own comparison runs on its commit, before this: its
verdict at both widths by hand from its "At 32 bits" table. And lab/evolve/gene-usage.py - Iteration
372's audit as a tool, an absent gene counted as off; one group, or two by their difference: it
reproduces the audit exactly, and finds consecutive carried runs (55, 56) differing by up to 17 points
a gene - the scale for reading seed 58 against the carried line.

## Iteration 376 - 2026-10-17 - Claude

**The verdict at both widths confirmed (the owner); weighing results across machines - a proposal.**
GOALS.md now records the rule as the owner's. Then his question: what if a design does very well on the
Tegra and badly on the laptop? Seed 55's four-machine check (results/xcheck-seed56.md): at one width
the machines agree on the order (Spearman 0.944 with the Tegra, 0.917 with dream at 64 bits, 0.977 for
the paired designs) and differ in how much the fast designs win (the fastest ~1.45x slower on the Tegra
than on the laptop, slow ones ~1.2x); the width reorders more (0.833). But the scenario cannot be seen
as things are: xcheck.py samples the laptop's front, so a design the laptop rejects is never measured
elsewhere. Proposed (results/drafts/cross-machine-weighing.md): selection stays on the laptop, the
other machines its generalization test; a disagreement diagnosed before weighed - measured again, the
width separated from the architecture, knockouts on both; the final generic choice by the geometric
mean over machine classes, each class once, with a veto; an architecture-specific mechanism a build
choice only if large and simple; and the blind spot tested - rejected designs measured elsewhere.

## Iteration 377 - 2026-10-17 - Claude

**Three classes of machine, equal (the owner) - and the blind spot's test built.** GOALS.md now says how
the best generic designs are chosen across machines: x86-64, x86 at 32 bits and ARMv7, equal - the
geometric mean of their speeds over the classes, each once, with a veto (none more than a margin behind
its class's best; 25% proposed) - selection staying on the laptop at both widths, the other machines
its test. Since xcheck.py sampled only the laptop's front, a design good elsewhere and rejected here
could never be seen; now `--sample ... --rejected K` takes K of the n from the run's db.jsonl beside
its report: living designs off the front, within its speed span, spread by speed, under the same
filters (no JIT, GCC only, built and alive at 4-byte cells for a 32-bit host); the flag is carried
through the host's records (it had built each record afresh) and through --ids (dream's paired
64-bit check takes the 32-bit check's designs - from the front only, before); the report marks them
and says how many ran faster there than the front's median and fastest. Tested on a fake archive from
seed 56 (half its front as the front, all 187 in the database): 5 front and 3 rejected sampled, all 8
through --ids, and a fake host result with one rejected design the fastest there - reported by name.
REMOTES: the Tegra 16 designs, 4 rejected, 120 minutes; dream at 32 bits 30, 6 rejected, 40 minutes,
its paired 64-bit check the same 30. They run in seed 58's chain, on what seed 57 rejected.

## Iteration 378 - 2026-10-18 - Claude

**Seed 57 processed - small at 64 bits, not small at both widths: the first run selected for speed at
32 bits.** Its chain (`seed 57 tag2 12h widths ...`, commit d1d1a44e6) ran 11 h 52 min: the evolution
8 h 22 min, 32,567 designs over 128 generations, 24,104 alive, 23,480 of them with a 32-bit speed (the
chain's recorded line lacks `widths` - next-run.sh consumes the word; the database shows the selection
ran). By the five 64-bit measures: fastest +3.9%, smallest +0.00%, memory +0 KB, hypervolume +2.0%,
best Q +1.2% - small; its fastest at 32 bits 0.337 of s6 (1a3cfe3e03), +20.3% against every earlier
run's (seed 56's 0.405) - **not small** by the owner's two-width rule (Iteration 376), applied by hand,
the comparison predating it: by the old rule the fifth small run in a row. The front: 200 designs, the
two speeds' Spearman over it 0.717 - 32-bit specialists kept now (the 32-bit fastest is 0.332 at 64
bits) - while its genes moved no further from seeds 53-56's than consecutive runs do (gene-usage.py:
the largest difference dskew, 17 points). The Q-best of all runs: its 9d47925af2 (Q 0.213). jitvar on
none of the 200, jitimg on 5. Held out: sieve 0.946. The checks of seed 56's front: dream 0.980, at 32
bits 0.713 and the same designs at 64 bits 0.949 (the width again), the Tegra 0.881. Gates on master
(the after-seed-57 batch applied at 374): tests PASS, 7 of 7 IDENTICAL, the jail PASS, the gate 274 of
274 (the run's front 200, the joint front 124), ans-check 0 of 51 differ (its negative control caught);
the laptop's stash on master but for the c-baseline-x86-64.md hunk, left out as since seed 49. No
predictions had been written for seeds 56 and 57 - step 4 skipped twice; seed 58's written now, before
it starts. Files: results/evolve-amd-ryzen-7-pro-8840hs-seed57.md, results/xcheck-seed57.md; session 51
appended to results/compare-fronts-amd-ryzen-7-pro-8840hs.md; results/progress-by-run.md regenerated;
results/predictions.md. Seed 58 next, as set at Iteration 374.

## Iteration 379 - 2026-10-18 - Claude

**The run no longer waits for the network (the owner's observation).** Seed 58's monitor showed dream
busy and the laptop idle. The chain called remote-checks.sh start synchronously before the evolution,
and start sampled, copied and started each host's check in turn - "never costs the run", but it did:
in seed 57's chain the checks started at 14:51 and the run at 15:43. Its files' times: the sampling
done by 15:05:52 (14 minutes, the laptop's CPUs); dream's three copies 2 min 50 s, 3 min 06 s, 2 min
58 s; the Tegra's 37 min 44 s - for a 7 MB repository bundle, three SSH connections a check: slow
connection setup more likely than bandwidth (the owner's to check: `time ssh rage.lan true`). Now the
sampling alone comes before the run - it builds designs on the laptop, and the run's timings need its
CPUs - and the copying and starting go to remote/launch.sh in the background, its notes to the chain
log, each laptop-side deadline from the check's own start, one SSH connection a host (ControlMaster,
ControlPath /tmp/fve-ssh-%C); a "launched" marker keeps a resumed chain from launching twice
(next-run.sh); REMOTES_FILE names a hosts' file for tests. Tested with two fake hosts and ssh/scp
stand-ins sleeping 4 s a call: start returned after its 50 s of sampling (the second host's with
--rejected 2, scanning seed 57's 32,567 records), the copies done 30 s later in the background, both
checks noted started. About 40-50 minutes more evolution a 12-hour chain, from seed 59's; seed 58
started on the old path.

## Iteration 380 - 2026-10-18 - Claude

**The Tegra's 38 minutes were not the SSH connection.** The owner timed `ssh rage.lan true`: 0.24 s - so
Iteration 379's guess, slow connection setup (sshd's reverse DNS or GSSAPI), is wrong. The copy's
throughput is what remains: seed 57's 7 MB bundle took about 38 minutes to the Tegra (~3 KB/s) and
dream's copies about 3 minutes each - a network matter on the owner's side, testable with `time scp`
of a few MB to each host. The fix of 379 stands as it is: the run no longer waits for the copying,
whatever its cause. Seed 58 runs on (its evolution after the old path's copies); this bundle goes to
~/Downloads only after seed 58's chain has finished.

## Iteration 381 - 2026-10-18 - Claude

**Probes for the remote checks (the owner's suggestion).** Iteration 379's diagnosis was a guess for
want of numbers; now remote-checks.sh records them. probe: each host's connection timed ("answers in
203 ms"; remote/connect). The background launcher: each check's three steps timed and its bytes counted -
"copied 8.1 MB in 0m 01s (8150 KB/s); mkdir 206 ms, start 205 ms" in its started line and
remote/HOST-HOW/transfer.txt. run.sh on the host: at its start the CPUs, the load average and the five
busiest processes (load-start.txt), then the load average every 30 s until the check ends (load.log), in
its process group so stop and gather end it too. gather: both brought back and summed up at the end of
the host's report - the copy, the connection, and the load while the check ran (mean, peak, CPUs, the
busiest at its start): a remote measurement's noise readable beside it. Tested end to end with stand-ins
- an ssh taking 0.2 s and running the command in a fake host's directory, an scp copying there for real
- the generated run.sh run on the "host" for 70 s (cloning the bundle, building its stages: 4 samples,
0.00 to 0.83), then gather with a fabricated out.json: the report ended with both lines. From seed 59.

## Iteration 382 - 2026-10-18 - Claude

**The new-chat prompt checked against this VM, before a switch.** HANDOFF-PROMPT.md's setup installs
gcc-multilib, clang and clang-19; this VM has gcc-13-multilib (gcc-multilib itself not installed) and an
asm/ header link made by hand, and the ARM cross tools and qemu-user besides. run-tests.sh and
build-stages.sh need neither the ARM tools nor the link - the prompt suffices for the routine - but a
guarded line now makes the link where it is missing, and the ARM tools are named as optional (for
tools/arm-qemu-check.sh). The handoff check passes; seed 58 runs; the next chat starts with seed 58's
archive and this bundle.

## Iteration 383 - 2026-10-18 - Claude

**This chat closes; seed 58's archive goes to the next.** Seed 58's chain (the anchoring and constraint
test, at c49de1703) ran 03:12 to about 14:45 UTC; the owner takes its archive to a new chat. NEXT-RUN is
`none` (next-run.sh: pulled, and stopping) - seed 59's run is chosen when seed 58 is processed, its
outcome deciding it. /tmp cleared of everything this work wrote: unpacked packs and chain archives
(results in results/), logs, relf's test temporaries, compiler temporaries, and scratch files each
identical to a repository file (hotwords.py, hotwords-v1.json, factor.patch) or recorded in PROGRESS.md
with a repository tool to reproduce it (jitleft.py's table, kernel 54.6%) - except price.py's table for
seed 53's ccf55ad2f5 (a scratch look at Iteration 310), never recorded: reproducible with
lab/evolve/price.py from the genome in results/evolve-amd-ryzen-7-pro-8840hs-seed53.md. Left: three
tool caches not of this work, listed in /tmp/handoff-disposable.txt.

## Iteration 384 - 2026-10-18 - Claude

**Seed 58 processed - from scratch and free of the tag-2 requirement, it passed every carried run at the
small end, at 32 bits and in hypervolume; seed 59 (the owner: 12 hours) separates anchoring from the
constraint.** A new chat, set up by HANDOFF-PROMPT.md: build, run-tests PASS, validate 7 of 7 IDENTICAL,
test-jail PASS on this VM. The archive (chain-20261018-031219, at c49de1703): both packs and four remote
reports, status done; the pack's tests PASS, validate 7 IDENTICAL, jail PASS. Its
results-measured-here.patch is two old stashes of the laptop's benchmark files (Oct 4 and Oct 14) that apply
neither way to master - the laptop's local re-measurements, not seed 58's; left out.

The verdict (Session 52): at 64 bits fastest -3.4%, smallest +10.51%, memory +4 KB, hypervolume +11.1%, best
Q -5.3%; at 32 bits +21.5% - not small at either width, by its gains. A positive figure is the run ahead: its
smallest, 09de03f091, is 14,146 bytes against every other run's 15,633 (the per-run minimum in the session's
table). This chat's first reading, in its summary to the owner, took the sign the other way; the per-run
minimum caught it before anything was committed, and HANDOFF's lessons now say so. The front of 171: the small
third 57 of 57 plain CV8, the middle 36 plain and 21 tag-2, the fast third 53 of 57 tag-2; the fastest at 64
bits tag-2 (1b5ac698ce), the fastest at 32 bits (d55f05136f) and the smallest plain. The search tried 18,153
plain designs and 16,021 tag-2. So the constraint concern holds - the requirement kept the carried runs out
of the small end and the 32-bit end - and anchoring is not separated by this run. gene-usage.py against seeds
53-57: the structure the same, the tuning different (dskew -30, opcall -28, rtiplus +23, d256 +22, regpin -21,
bfind -21, opt +20, lto -19, abortif +19). seed-facts: speed against 32-bit speed over the front, Spearman
0.573. heldout.py: sieve 0.883 (seeds 53-57: 0.946-0.963). Item 1's first half: with the pool named right, 73
of the front's 74 tag-2 designs build superinstruction pairs (before: inert in ~97%).

Predictions 4 of 5 as written: 2 missed (tag-2 on 43% of the front, not 60%); 4 met only as written (0.310
against seed 57's recorded 0.337, but 21.5% ahead of its 0.377 in the same session). The remote checks, of
seed 57's front and first its rejected designs (xcheck --rejected, item 4d): the Tegra 0.973, dream 0.959,
dream at 32 bits 0.875; no rejected design faster on any host than the front's fastest. The old remote path
held seed 58's evolution back 55 minutes (the checks 03:17:26, the run 04:12:39). Two faults (open item 0d):
2 designs did not compile, `L_t2call4` used but not defined - both tag-2 with opcall `>R`, made by a mutation
to bytehdr=0, which require() never allowed (it sets tag2 and bytehdr together); and on the Tegra three of
seed 57's designs did not link, two of them front designs with regpin=1 and lto=1, xcheck keeping only ld's
last line.

The gates at this commit: gate.py alive 264 of 264 (the run's front 171, the joint front 129, 36 in both);
ans-check on 44 designs (every fourth of the front by size, and its extremes) - 0 differ, its negative control
caught (failed 0 -> 1).

Seed 59 (NEXT-RUN), the owner asking for 12 hours and a run that answers his concerns: `seed 59 tag2 12h widths
nocarry then experiment compare-fronts.py --rounds 6 --widths 8,4 --frontier --cpus 2,8` - the anchoring test
as first specified at Iteration 373 (from scratch with tag2): against seed 58 the constraint alone, against
seeds 53-57 anchoring alone. And the first chain on Iteration 379's remote path with 381's probes: lab/evolve
unchanged since 381's end-to-end test but for NEXT-RUN, both scripts pass dash -n; so the copying no longer
holds the evolution back, and every host's report ends with the copy's KB/s, the connection and the load - the
first real numbers for the Tegra's slow copy. Its checks measure seed 58's front, the first with plain-CV8
designs. next-run.sh's reserve covers the re-measure and the comparison only, so the footprint experiment
(item 2) stays out of a 12-hour chain. Its predictions are written (results/predictions.md).

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed58.md and results/xcheck-seed58.md (new);
results/predictions.md (seed 58 scored, seed 59 predicted), results/compare-fronts-amd-ryzen-7-pro-8840hs.md
(Session 52), results/progress-by-run.md, results/README.md (its per-seed line, stale at "seeds 1-47", now
1-58), lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 385 - 2026-10-18 - Claude

**While seed 59 runs: the superinstructions question answered - they buy something, the gene stays - and
seed 58's two faults fixed, the after-seed-59 batch.** The owner asked what could be done while seed 59
runs; three items needed only this VM.

Item 1 (results/drafts/supers-tag2.md; the rule decided at 368). lab/evolve/supers-knockout.py, new: a
front's designs that build pairs, each built as it is and with its supers gene emptied - the profiler's
dispatches over the six selection workloads (deterministic, so this VM's noise does not enter) and binary +
image - with a control and every as-built size checked against its record (all equal). Over 19 of seed 58's
73 tag-2 designs with pairs (every fourth by size, and the extremes): dispatch ratio median 0.9907 (0.9748 to
1.0000), the most at the small end (the 642ec43577 family, 2.4%); bytes -1,024 to +719 (median +216), the
design smaller with its pairs in 6. The control, d1e2c6b7de, unchanged. So not "buy nothing": the gene
stays. Under 1% of time, inside selection's 2% speed tie; 2 of the 19 (14ec7cd739, d79a57826d) carry pairs
that never execute, +216 and +112 bytes, each dominated by its own knockout. results/supers-knockout-seed58.md.

Open item 0d (a): opcall_on() asked for tag2 but not bytehdr - unlike jit_on() and t2wide_on(), and the
build, which makes the tag only with byte headers - so tag2=1 with bytehdr=0 built OPCALL into an engine
without the tag, its CALLNEXT() jumping to L_t2call4. Reproduced with seed 58's 8259be4f90 at bytehdr=0: it
died with clang's "3 errors generated." - seed 58's third compile death, the same fault; fixed, it builds and
runs fib; the design as recorded builds to its record's bytes before and after; all 1,093 front genomes of
seeds 53-58 express the same. (b): why() kept the last error line - for a link failure always ld's generic
one, all the Tegra's three said - and cut 120 characters, mostly path. Now the first error, the linker's own
line where only the generic ones say error, paths cut to file names, 160 characters; its test over synthetic
compile, link, LTO and Python failures caught the first draft giving a traceback's source line (assert ok)
for its exception - fixed, a Python traceback keeps its exception. The ARM link failure itself waits for its
own words from the next Tegra check.

Both in results/pending/ (ORDER.md: opcall-bytehdr-after-seed59.patch, why-after-seed59.patch), tested in a
scratch clone: run-tests PASS, validate 7 of 7 IDENTICAL, test-jail PASS; on a fresh clone they apply in
order and reproduce the tested evolve.py byte for byte. Applied after seed 59's processing.

NEXT-RUN none: seed 59 runs from the Iteration 384 bundle, and this one goes to ~/Downloads only after its
chain has finished. (next-run.sh pulls only at an invocation's start and refuses while a chain is alive, but
holding the bundle costs nothing.)

Files: lab/evolve/supers-knockout.py, results/supers-knockout-seed58.md, results/applied-after-seed59/ORDER.md,
results/applied-after-seed59/opcall-bytehdr-after-seed59.patch, results/applied-after-seed59/why-after-seed59.patch (new);
HANDOFF.md, lab/evolve/NEXT-RUN, lab/evolve/README.md, results/README.md.

## Iteration 386 - 2026-10-18 - Claude

**A review of the methodology, workflows and logic - the owner's request; results/review-methodology-386.md.**
Each suspicion checked against the code or the data before it was written down; every figure reproduced by
lab/evolve/review-checks.py (new: pedigree, curse, cpus, screen).

The finding that bears on the running seed 59: `nocarry` is not from scratch. Every run but fromzero puts two
evolved designs in generation 0 (evolve.py, Iterations 155 and 178): seed 37's fastest, starting seed 58 at
speed 0.174, and seed 40's knee. By expected pedigree share (every listed parent weighted equally), seed 37's
fastest is 55.0% of seed 58's fastest third and 48.7-49.4% of the rest, seed 40's knee 11.3-17.0%: one design in
140 half the front's ancestry. So seed 58's "within 3.4% of the carried fast end" is largely inherited, and
seed 59, with the same founders, cannot answer the anchoring question; the constraint finding stands (both
founders are tag-2, the plain encoding came from the hand-made and random side). fromzero, tested here in
miniature (--pop 8 --gens 1 --fromzero --require tag2 --widths 8,4), runs - exit 0, both widths, no hand-made
design or founder in generation 0 - but only 2 of its 16 designs were tag-2: require() tags only designs
already CV8, and random genomes mostly draw other encodings, at 1.2-2.0 times s6 - too far down for a fair 12
hours. The clean test needs an opt-in switch leaving out the evolved founders (what seed 36 was), not built.

Measurement: the fast end's in-run speeds are optimistic - re-measured / in-run, the fastest tenth 1.112 (all
17 between 1.073 and 1.142), the fastest third 1.081, the middle 1.032, the slowest third 0.991: selection on
noise, the 2% speed tie inside ~10%. Session 52's verdict measures from each CPU alone: "fastest" moves up to
5.4 points between the CPUs, "best Q" up to 6.2, seed 57's best Q +3.5% on cpu 2 and -0.4% on cpu 8 - the 2%
bars inside the noise. The front of all runs from the two CPUs: 80-100% of members in common while fronts held
under 20 designs, 46-65% in the last ten sessions. Held out, seed 58: Spearman 0.883 over the front, 0.866 over
its fastest third, 0.529 over its fastest tenth. 1a3cfe3e03 at 32 bits: 0.337 in session 51, 0.400 in session
52, built and measured both times - the non-PIE rebuild between them: 32-bit numbers do not compare across
sessions. Logic: "converged" was said of the tag-2 subspace; one run per configuration; the anchoring test
asymmetric (seed 59's prediction 1 reworded); the supers gain under selection's resolution. Workflow: the
verdict's sign unlabelled (read backwards at 384); one reader for code, outputs and predictions; HANDOFF's
stale "Seed 52 is the laptop's next run" (removed); --frontier keeping the 64-bit bests, not the 32-bit one
(latent). Cleared: the surrogate screen - 0 of 968 audited screened children on the final front, 6.9 expected
at the measured rate of 0.71%; tag-2 share 48.0% screened, 46.7% not.

Files: results/review-methodology-386.md, lab/evolve/review-checks.py (new); HANDOFF.md (the review, item 0's
decision, item 0e the proposals, a lesson, the stale bullet out), results/predictions.md (seed 59's prediction
1 reworded), lab/evolve/README.md, results/README.md.

## Iteration 387 - 2026-10-18 - Claude

**While seed 59 runs: the review's switch built - `noevolved`, the clean anchoring test - and two of its fixes;
the after-seed-59 batch now four patches.** The owner asked what else could be done while waiting.

`noevolved` (next-run.sh) and `--noevolved` (evolve.py), pending patch 3: nocarry, and no founder drawn from an
earlier run's record - seed 37's fastest and seed 40's knee, two thirds of seed 58's ancestry (Iteration 386) -
left out; the hand-made designs and the founders built from them kept: the anchoring test as seed 36 ran it.
Opt-in. Tested: next-run.sh's keyword block run alone - the keyword in either place gives NOEVOLVED=1 and
NOCARRY=1, nocarry and fromzero unchanged, the detached chain's environment path set, the resume key "seed 60 tag2
noevolved nocarry at ..." so it never resumes a nocarry run; evolve.py --pop 8 --gens 0 --rounds 1 --noevolved
--require tag2: both founders reported left out, generation 0 the 7 hand-made designs and 8 founders built from
them, the best start the s6 + JIT founder at 0.81 against seed 37's 0.174 under nocarry; exit 0. Proposed for seed
60 (the owner's hours), after the batch is applied at seed 59's processing: `seed 60 tag2 12h widths noevolved
then experiment compare-fronts.py --rounds 6 --widths 8,4 --frontier --cpus 2,8`.

compare-fronts.py, pending patch 4: the verdict's sign labelled in both sections (a positive figure is the run
ahead - review 4a); --frontier keeps each run's 32-bit fastest beside its 64-bit bests (review 4d). Tested: the
thinning block of the old file and the new on three designs - the 64-bit fastest, the smallest, a 32-bit
specialist dominated at 64 bits: the old kept two, the new all three.

The batch, all four applied in a scratch clone: run-tests PASS - no regressions; validate 7 of 7 IDENTICAL; test-jail PASS; on a
fresh clone the four apply in order and reproduce the three tested files byte for byte. Five files this work
had written as root (seed 58's records, the knockout's tool and record, ORDER.md) handed back to claude - git
keeps no owner, so no bundle carried it; it blocked edits only.

Files: results/applied-after-seed59/noevolved-after-seed59.patch, results/applied-after-seed59/compare-fronts-after-seed59.patch (new);
results/applied-after-seed59/ORDER.md, HANDOFF.md, lab/evolve/NEXT-RUN (still none).

## Iteration 388 - 2026-10-18 - Claude

**While seed 59 runs, the owner leaving the choice to this lab: the verdicts audited for noise, and the
superinstruction knockout repeated with the JIT off.**

The verdicts (results/verdict-audit-388.md; `review-checks.py verdicts`, new): every session since the
five-measure rule - 16 - rebuilt from its own tables with compare-fronts' hypervolume copied verbatim, then
computed from cpu 2 alone and cpu 8 alone. 15 printed verdicts rebuilt exactly; the 16th, session 45 (seed 51),
printed "fastest +4.9%" against the 5% bar and rebuilt +5.1% from three-decimal speeds - a knife edge. The CPUs
agree in 14: session 44 (seed 50) small on cpu 2, not on cpu 8 (best Q +0.2% / +2.1%); session 45 small by 0.1
points of cpu 2's fastest, cpu 8 +0.7%. Both were followed at once by new genes, so no decision turned on
them; the rule's recent end (seeds 53-55) holds on both CPUs. Found on the way: the verdict reads cpu 2 alone -
compare-fronts takes the session's speed from the first CPU (`c0 = cpus[0]`), cpu 8's half of every session
feeding only the agreement section. The review's 2b tempered accordingly; proposed (the owner's): the speed
from both CPUs, the per-CPU verdicts beside it; until then step 2 of the processing routine runs the check.

Superinstructions with the JIT off (supers-knockout.py --set=jit=0, the option new; 10 of seed 58's tag-2
designs and the control): the interpreter, as at 32 bits - dispatch ratio median 0.9973 (at best 0.9913),
against 0.9907 with the JIT on; and a byte cost in every design, +24 to +735 (median +240), where the JIT build
had shown savings to -1,024 - exactly 1 KB, its layout's. Control unchanged; d79a57826d's pairs never run.
Below selection's 2% tie either way: by GOALS.md the gene comes out of tag-2 designs unless the owner counts
this as something (HANDOFF item 1, rewritten).

Files: results/verdict-audit-388.md (new); lab/evolve/review-checks.py (verdicts), lab/evolve/supers-knockout.py
(--set), results/supers-knockout-seed58.md (the JIT-off section), results/review-methodology-386.md (2b, 3d, the
second proposal), HANDOFF.md (routine step 2, items 0e and 1), results/README.md, lab/evolve/README.md.

## Iteration 389 - 2026-10-18 - Claude

**The owner's three decisions: superinstructions kept for now; the verdict from both CPUs; seed 60, 12 hours.**

The verdict from both CPUs: compare-fronts.py takes the session's speed - and so the verdict, the fronts, the
Q-best and the gate's joint front - as each design's geometric mean over the CPUs measured, where it had read the
first CPU alone (results/verdict-audit-388.md). Each workload's ratio is combined likewise; one CPU is unchanged;
the per-CPU numbers stay in the section comparing the two, and the 32-bit section is measured on one CPU as
before. Tested on per-CPU ratios: two CPUs give the geometric mean (0.435588 of 0.447214 and 0.424264), the
workloads' ratios agree with it, one CPU is unchanged. GOALS.md's judging paragraph says so. review-checks.py
verdicts gained the rule's own line: the 16 sessions since Iteration 188 by it - 15 give the printed verdict;
session 44 (seed 50) turns not small (best Q +2.7% from both, against +0.2% and +2.1% alone - a minimum over
designs need not lie between its per-CPU values), on which no decision turned; seed 58's fastest, from both
CPUs, is 0.4% behind the others, not 3.4%. Seed 59's comparison runs the older code: its verdict by the new rule
is that line, at processing.

The after-seed-59 batch - five patches with this one (results/applied-after-seed59/ORDER.md) - applied ahead of
seed 59's processing, as at Iteration 374: seed 59's chain pulled its code at its start, so it runs on the code
before the batch. On master with all five: run-tests PASS - no regressions, validate 7 of 7 IDENTICAL, test-jail PASS; the three
changed files byte for byte those tested in the scratch clones. results/pending moved, its citations followed.

Seed 60 (NEXT-RUN, the owner's 12 hours): `seed 60 tag2 12h widths noevolved then experiment compare-fronts.py
--rounds 6 --widths 8,4 --frontier --cpus 2,8` - the clean anchoring test, the first comparison judged from both
CPUs; to start when seed 59's chain has finished. Its predictions written (results/predictions.md), read by the
review's 3c. Superinstructions: kept for now (the owner), HANDOFF item 1 records why it was asked.

Files: results/applied-after-seed59/ (moved from results/pending; both-cpus-after-seed59.patch new);
lab/evolve/compare-fronts.py, evolve.py, next-run.sh (the batch); lab/evolve/review-checks.py (the both-CPU line);
results/verdict-audit-388.md (the rule's section), results/predictions.md (seed 60), GOALS.md, HANDOFF.md,
lab/evolve/NEXT-RUN, results/README.md (the pending line out).

## Iteration 390 - 2026-10-18 - Claude

**While seed 59 runs: two of the review's findings turned into tools, and the Tegra's link failure narrowed.**

heldout.py (the review, 2d): beside the whole front's Spearman, the fastest third's and tenth's, and the regret -
how much slower held out the selection's fastest is than the held-out fastest. Seed 58: 0.883 / 0.866 / 0.529, the
figures of review-checks.py; regret +4.5% (d79a57826d against 1b5ac698ce). Seed 57: 0.946 over the front but
-0.141 over its fastest tenth - no agreement at all at the top - and a regret of only +3.0%: the top designs are
near-tied, noise shuffling equals. 2d weighed accordingly in the review; step 3 of the routine reads the new lines.

tools/handoff-check.py, rule 11 (the review, 4c): a "**Seed N is the laptop's next run**" or "**Seed N is set**"
for another N than NEXT-RUN's line, or more than one seed running, fails the check. Made to fail first: "Seed 52
is the laptop's next run" injected into a scratch copy - rule 11 named it against NEXT-RUN's seed 60; master's
own HANDOFF raises nothing.

The Tegra's link failure (open item 0d): not regpin - its engine code is x86-64 only, inert on ARM - and not lto:
of seed 57's designs measured there, lto=1 built three times and lto=1 with regpin=1 once (dfd14a3b70). A cross
build here (arm-linux-gnueabihf-gcc 13, installed on this VM; EVOLVE_CC) stops earlier, at the x86 runtime -
Iteration 330's qemu harness is not tracked - but showed the new why() at work: "rt-linux-x86_64.c:59:5: error:
unknown register name 'rcx' in 'asm'", the first error with its file's name. Seed 60's chain checks seed 59's
front on the Tegra with that why(): a recurrence will name its cause.

Files: lab/evolve/heldout.py, tools/handoff-check.py (rule 11), HANDOFF.md (routine step 3, item 0d),
results/review-methodology-386.md (2d weighed), lab/evolve/README.md.

## Iteration 391 - 2026-10-18 - Claude

**The fast gate - designs re-measured before they enter the fast end (the owner) - built and tested, pending
after seed 60; and the ARM cross-compiler found to break the 32-bit build.**

The owner judged re-measuring a good idea; it waits for seed 60's processing so the anchoring test runs on the
evolver of seeds 53-59. evolve.py: a child whose speed is under the gate - 1.05 x the 20th fastest design alive
so far - is measured again with the same rounds on the engine as built, and its speed is the geometric mean of
the two (speed1 and speed2 kept; memory and size the first measurement's); `--fastgate N` sets the 20, 0 turns
it off. Why: a 3% noise and thousands of candidates make the best-looking ~11% optimistic (seed 58's fastest
tenth, re-measured / in-run 1.112). Cost, seed 58 replayed through the gate generation by generation: 1,121 of
24,885 measured children (4.5%) under it, their evaluations 4.4% of the time - an upper bound, the second
measurement with no build and no 32-bit pass. Tested: fast_gate() over 30 designs 1.05 x the 20th fastest, None
with fewer and with 0; a miniature run (--pop 6 --gens 2 --rounds 1 --fastgate 3) measured 3 of 28 designs
twice - 524fef96b3 0.2264 then 0.2547, 12.5% apart - each speed exactly the geometric mean of its two and of its
workloads' figures, memory the first's, generation 0 once; run-tests PASS - no regressions, validate 7 of 7 IDENTICAL, test-jail
PASS; on a fresh clone the patch reproduces the tested file. The 32-bit fast end not gated, a later step if the
first run with this shows it worth it - seed 61, read by `review-checks.py curse`.

The first build for it failed: "asm/errno.h: No such file or directory". Installing gcc-arm-linux-gnueabihf at
Iteration 390 had removed gcc-multilib (apt's history: "Remove: gcc-multilib:amd64"), and /usr/include/asm with
it. Nothing committed was touched - the full checks ran at 389, and nothing was built natively between. Put
back with apt-get install gcc-multilib (which took the ARM compiler out: the two cannot both be installed);
HANDOFF-PROMPT's optional ARM tools now say so, and HANDOFF's lessons.

Files: results/applied-after-seed62/ORDER.md, results/applied-after-seed62/fastgate-after-seed62.patch (new); HANDOFF.md, HANDOFF-PROMPT.md.

## Iteration 392 - 2026-10-18 - Claude

**The owner's worry of a local minimum (Iteration 373, asked again): mapped to its sources, and seed 58 seen
from inside - no collapse.** results/convergence-seed58.md.

Five sources, five tests: a constraint fencing off a region (seed 58: real - the plain-CV8 small and 32-bit
ends); the carry anchoring (seed 60, noevolved); every run starting from the same human designs (not ruled out
by seed 60; seeds 58, 59 and 60 start three ways; replicates proposed); the search collapsing inside a run
(measured here); the gene set's edge (no search setting passes it - new mechanisms do).

review-checks.py progress (new): by generation, the best speed and the smallest binary + image so far, the
best 32-bit, diversity - the mean share of built genes (express()) two designs differ in, overall and in each
encoding family - and the encodings alive. Seed 58: diversity holds and rises, 0.47-0.56 overall, the tag-2
family 0.35-0.47 rising to the end, the plain family 0.46-0.53; both encodings to the last generation. The raw
genome's diversity (0.09 at generation 0) was first read and set aside - unbuilt genes drift freely, so what is
built is the measure. Gains: the smallest (exact) in 21 generations, the last at 130 of 133 (40 bytes in the
last third); the 32-bit best to 120; speed's large steps at generations 5 and 15 (22.9%, 3.6%), then under 2%
each to 100. Diminishing returns, not a stall. Step 3 of the processing routine now runs the check on every
returned seed.

Proposed (the owner's): after seed 60, the check and gene-usage.py on seeds 58-60; replicates if the hours allow
(two shorter noevolved runs, different seeds); escape mechanisms only if those show runs stuck.

Files: results/convergence-seed58.md (new); lab/evolve/review-checks.py (progress), HANDOFF.md (item 4c, the
routine), results/README.md, lab/evolve/README.md.

## Iteration 393 - 2026-10-18 - Claude

**The replicates queued (the owner: yes) - seeds 61 and 62, seed 60's start, 6 hours each - and the tool to read
them; the fast gate moved to after seed 62.**

Seeds 61 and 62: `tag2 6h widths noevolved`, other seeds, each its own command when the one before has finished
(NEXT-RUN's comment; HANDOFF item 0). Not one chain: a chain of two seeds has never run - next-run.sh carries a
chain's steps in one directory, and both seed steps would write the remote checks' same per-host directories; a
night is a lot to bet on a path never taken. No comparison in them either: a comparison anywhere later in a chain
reserves its time in every seed step before it, which would cut each replicate's evolution. They are read instead
from their databases at one generation, which is fairer anyway - runs never end at one generation.

review-checks.py spread (new): databases cut at one generation, each front's fastest, smallest, least memory, best
Q and hypervolume (log space, one reference for all), and the fronts' gene usage apart in points. Tested on seed 58
cut at generations 40, 80 and 133: every measure better at each later cut, as it must be (fastest 0.1258, 0.1220,
0.1179; smallest 14,368, 14,202, 14,146; hypervolume 0.563, 0.598, 0.611), and gene usage drifting 5-6 points
between neighbours - the scale against which two replicates are read.

The after-seed-60 batch (the fast gate) renamed after-seed-62 - its file and its citations: seeds 60-62 must run one
evolver, or a change of evolver would read as run-to-run spread. Predictions for 61 and 62 written.

Files: results/applied-after-seed62/fastgate-after-seed62.patch (renamed), results/applied-after-seed62/ORDER.md, lab/evolve/review-checks.py
(spread), lab/evolve/NEXT-RUN (comment), results/predictions.md, HANDOFF.md, results/README.md, lab/evolve/README.md.

## Iteration 394 - 2026-10-18 - Claude

**Context economy (the owner: can a chat last longer?).** What tools print stays in the chat; this one spent most
on full reports and logs, on the pending-batch cycle (five times, about eight calls each) and on long replies.
tools/batch-check.sh (new): the pending batch tested as it will be applied - a fresh clone, ORDER.md's patches,
the build, run-tests, validate, jail - logs under /tmp/batch-check, one line out; the patched clone removed on
success (a scratch tree the handoff check flags). Run on the after-seed-62 batch: 1 patch applied, run-tests
PASS, validate 7 of 7 IDENTICAL, jail PASS - in three calls. HANDOFF's lessons hold the practices.

Files: tools/batch-check.sh (new), HANDOFF.md.

## Iteration 395 - 2026-10-18 - Claude

**The tools audited (the owner: does shorter output break anything?) - nothing downstream broken, batch-check.sh
fixed; and process-seed.sh for the chat that processes seeds 59-62.** results/tools-audit-394.md.

Every code change since Iteration 383, each changed output traced to what reads it: none breaks. batch-check.sh
did - it exited 0 on a failed test and removed the patched clone after a failure; now PASS only if every check
says so in its own words and by its exit status, else FAIL, exit 1, the clone kept - five cases tested with stub
tools, and the real batch PASS. compare-fronts.py run end to end here (--cpus 0,0, --widths, --frontier): exit 0,
its new text, the 32-bit specialist kept. lab/evolve/process-seed.sh (new): the routine's reading steps on a
chain archive, about a screen of summary - on seed 58's archive it reproduced Iteration 384's findings; HANDOFF's
routine starts with it. Two traps of this VM noted: git as root in claude's tree, pkill -f matching its caller.

Files: results/tools-audit-394.md, lab/evolve/process-seed.sh (new); tools/batch-check.sh, HANDOFF.md,
lab/evolve/README.md, results/README.md.

## Iteration 396 - 2026-10-18 - Claude

**Housekeeping: the documents made orthogonal (the owner).** Each document one role - HANDOFF the state, the
routine, open items and lessons; PROGRESS the history; GOALS the aims and rules; NEXT-RUN the next run and why;
results/ the evidence and its index - and each fact in one of them.

HANDOFF.md 478 lines to 332: the state section from sixteen bullets, nine of them history (seeds 47-57, old
batches - in PROGRESS already), to five current ones; "a generic Forth first" was there and in the standing
decisions - now only there; the routine rebuilt around process-seed.sh (its steps 1-3 had described by hand what
the script does), pointing to GOALS.md for the rule it restated, its stale step - reverse-applying the laptop's
measured-here patch, which Iteration 384 found cannot apply - gone, the citations' sed kept word for word; open
items 0, 0d, 0e, 1, 4b-4d condensed to status and pointers (0e's proposals all done or queued; superinstructions,
the owner's decision, moved to the standing decisions). NEXT-RUN 409 lines to 36: 93 iterations' comments, history,
out (git log keeps them) - and its grammar, which only those comments and next-run.sh's code had (nocarry,
fromzero, noevolved, widths), stated once in its header. GOALS.md stated the verdict rule twice - the second copy
stray, in "Rejected or deferred" - and Iteration 389 had put the owner's both-CPU decision into that copy, not the
rule: now one statement, in Success, with it. No file is listed twice in an index; every listed tool exists.

Files: HANDOFF.md, lab/evolve/NEXT-RUN, GOALS.md.

## Iteration 397 - 2026-10-18 - Claude

**The owner's three decisions: footprint.py after seed 62; jithelp and jitre tried; the new mechanism (item 4) in
the next chat.** The footprint experiment (item 2) ends seed 62's command in NEXT-RUN's comment - an experiment
step takes no reserve, so the replicates stay alike. jithelp and jitre (Iterations 344 and 346's drafts) join the
after-seed-62 batch unchanged: they apply after the fast gate on a fresh clone; seed 58's 1b5ac698ce built with
them expresses both and lives, 40,565 bytes against its recorded 36,021. What they buy, by jitleft.py's
deterministic counts: little - the kernel's dispatches left to the interpreter 989,120 to 987,090 (53.7% to 53.6%),
bubble's 151,968 to 129,788, the rest unchanged or nearly; a 1-round timing here (0.2369 to 0.2044) sits in this
VM's noise. Kept as the owner chose, the evidence in ORDER.md; seed 63's front decides. batch-check.sh's first run
on the batch tested 1 patch of 3: it clones what is committed, and the two were not - its line said so (the
commit, the count), its header says so now; committed, all three PASS (run-tests, validate 7 of 7, jail).
Predictions for the footprint step and the two genes written.

Files: results/applied-after-seed62/jithelp-after-seed62.patch, results/applied-after-seed62/jitre-after-seed62.patch (new);
results/applied-after-seed62/ORDER.md, lab/evolve/NEXT-RUN (comment), results/predictions.md, HANDOFF.md, tools/batch-check.sh.

## Iteration 398 - 2026-10-19 - Claude

**Seed 59 processed - small at both widths, the tag-2 requirement's cost replicated; the probes answer the network
question; a fifth of its front dies on the corpus at 32 bits.** By process-seed.sh first (its summary: 79 lines).

Seed 59 - seed 58's start with the requirement the designed difference - from both CPUs: fastest +1.2%, smallest
-11.12%, memory -4 KB, hypervolume +0.4%, best Q -4.1%, small on each CPU alone too; at 32 bits -9.2%. Against seed
58 the small end +12.5% (15,915 bytes), 32 bits +11% (0.344), the 64-bit fast end alike: the requirement costs those
two ends and only them. From inside: diversity holds (0.516), but the gains stopped at generation 88 of 143 (seed
58, free, to 130). Held out 0.909, its fastest tenth 0.123, the regret +8.7%. Predictions: 3 met, 1 met but for a
clause, 1 missed (32 bits 11% behind seed 58, not 15%).

The new remote path's first chain: the evolution six minutes after the checks (seed 58: 55; 8 h 55 min of
evolution against 8 h 01). The probes: every copy 8.2-8.6 MB in 0-1 s (the Tegra 7,219 KB/s); the Tegra's long wait
is its own start, about 36 minutes - its build - which Iteration 380 had put on the copy. The checks of seed 58's
front: dream 0.959 / 0.963, at 32 bits 0.651, the Tegra 0.709 - against the laptop's 64-bit speeds, which rank a
two-encoding front poorly at 32 bits (open item 0g); no rejected design faster than the front's fastest anywhere.

The fault (open item 0f): 34 of the front's 171 "died: corpus" as 32-bit engines - all jit=1, scale=0, tos=0; 2,057
in the database, and 326 that did not compile at 32 bits. Their 64-bit engines are sound, and a missing 32-bit
speed counts as the worst (Iteration 336), so they hold the front by their 64-bit objectives. Seed 58's front had
none. The fault for the next chat; whether a design wrong on one machine class is dead, the owner's.

Gates at this commit: gate.py alive 289 of 289 (the run's front 171, the joint front 122, 4 in both); ans-check on
44 - 0 differ, its negative control caught.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed59.md, results/xcheck-seed59.md (new); results/predictions.md,
results/compare-fronts-amd-ryzen-7-pro-8840hs.md (Session 53), results/progress-by-run.md, results/README.md,
HANDOFF.md.

## Iteration 399 - 2026-10-19 - Claude

**Open item 0f found: bfind's walk compared three characters at 4-byte cells; the fix, and a check that fails
without it, wait in the after-seed-62 batch.** Seed 60 started (the owner, from Iteration 398's bundle, 12 h). The
setup here: run-tests PASS, validate 7 of 7 IDENTICAL.

The separator on seed 59's front: the 34 dead at 32 bits all express bfind without tos; of the 44 alive with jit=1,
scale=0, tos=0, 43 have bfind 0 and the other does not express it. The cause: bf_walk's signature, its mask and
bf_ld64's result were UNS64 - the cell, uint32_t at 4-byte cells - so the count and three characters were compared,
and a name of 4 to 7 characters matched the newest of its length and first three (one thread, by the hash). The
corpus case: line 254, `{ 1 2 2DUP -> 1 2 1 2 }` - the tester's CELLS answered by another of CELL+ CELL- CELL,; a
single result round-trips at the same wrong place, and 2DUP's is the corpus's first test with more than one.
Rebuilt here as eval32 builds them, 708757c03f and 686ae7cd5f died so on master's engine and live with the three
declarations uint64_t (no 64-bit engine changes: UNS64 is uint64_t there).

The check that missed it: engines-check's four bfind variants sat on s6, a TOS design, whose THREAD-FIND and (FIND)
are gen-tos.py's own bodies - no bf_walk at either width (all four alive at 4-byte cells on the faulty engine). In
the patch they set tos 0 and run at 4-byte cells too: on the faulty engine all four die at 2DUP's test; with the fix
they live - batch-check, the four patches: PASS - 4 patches on a fresh clone of 0165837: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS. Found with it: bfind is inert in every TOS design - 42 of seed 59's
front carry it unbuilt (item 4b).

NEXT-RUN: seed 61 (6 h), for when seed 60's chain has finished, as the owner queued at 393. Predictions: the remote
checks of seed 59's front will see the same deaths at 32 bits; seed 63 none.

Files: results/bfind32-fault-399.md, results/drafts/bfind32-repro-399.py, results/applied-after-seed62/bfind32-after-seed62.patch
(new); results/applied-after-seed62/ORDER.md, results/predictions.md, results/README.md, lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 400 - 2026-10-19 - Claude

**Every 32-bit failure of seed 58 classified: 745 bugs (fixes pending, patches 4 and 5), 74 the designs' own.** The
archive sent as seed 59's is seed 58's chain (commit c49de17, Iteration 378's bundle); seed 59's is chain-31b591c59.
The owner, on dead or slowest: understand why each design fails - inapplicable there, or a bug that can be fixed.

Seed 58's database: 24,831 evaluated at 32 bits, 819 failed. "died: corpus", 418 - every one bfind expressed without
tos, none of the 24,012 measured: Iteration 399's fault. "engine did not compile", 401 - every one tail, none of the
measured: build_tail preprocessed with cc and compiled with gcc -m32, so the engine was the x86-64 one, 8-byte cells
and __int128; behind it the i386/ARM SYSCALL's local label sysc_done, which gen-tail.py rewrote as a call to a handler
that does not exist; behind that, tail_offenders read only x86-64's call forms, so clang's undetected calls grew the
C stack (died on the corpus). Patch 5: preprocessing by CCV(g); the branches without the label; i386's call forms read
(x86-64's as before - no 64-bit change); each tail failure with its tool's first error; engines-check's tail variants
at 4-byte cells. With it seed 58's three sampled tail designs and the GCC and preserve_none variants live at 32 bits;
clang's tail engine without musttail fails as "tail calls not jumps" - clang makes no i386 dispatch a jump without
it. Of the 401: GCC 227 and clang with preserve_none 100 live (by these samples), clang without it 74, the designs'
own. batch-check, the five patches: PASS - 5 patches on a fresh clone of 0092bee: run-tests PASS (engines-check 78 paths), validate 7 of 7 IDENTICAL, jail PASS.

Proposed (results/fail32-400.md): no design dead for a machine class - a failure there is a bug to fix, or a
mechanism that cannot exist there, left out of that class's build as the JIT is (336); until classified, the slowest
there. The 74: the slowest at 32 bits, or a 32-bit build with musttail for clang - the owner's. The Tegra's three link
failures in this archive keep only collect2's last line: seed 60's chain records the first error. Item 4b: tail's
absence from fronts since seed 57 is partly this fault.

Files: results/fail32-400.md, results/drafts/fail32-classify-400.py, results/drafts/fail32-tail-400.py,
results/drafts/fail32-tailerr-400.py, results/applied-after-seed62/tail32-after-seed62.patch (new); results/applied-after-seed62/ORDER.md,
results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 401 - 2026-10-19 - Claude

**Seed 59's 32-bit failures: Iteration 400's classes, as predicted; and musttail on every clang tail engine (pending,
patch 6).** Seed 59's archive (chain-31b591c59): 2,057 "died: corpus" at 32 bits, all bfind without tos; 326 "engine
did not compile", all tail - GCC 168, clang with preserve_none 72, clang without 86 (results/drafts/
fail32-tailsplit-401.py). None of the 24,802 measured has either.

The owner asked for a view on the 160 clang tail designs without musttail (seeds 58-59). Decided: musttail on every
clang tail engine at both widths (gen-tail.py --musttail) - the guarantee a tail engine needs, not a trade-off; the
trade-off in tailpn is preserve_none, which stays a gene; musttail exists on i386, so the 32-bit engine need not differ
from the 64-bit one; GCC's left to its optimizer, which makes the jumps at both widths. With patches 1-6, seed 59's
a973c305bc and 0136e7294a (clang, no tailpn) and f510231b27 (GCC) live at 4-byte cells (fail32-tail-400.py with the
label seed59), and engines-check's clang tail variant lives at both widths. batch-check, the six: PASS - 6 patches on a fresh clone of de0b64f: run-tests PASS (engines-check 79 paths), validate 7 of 7 IDENTICAL, jail PASS.

No 32-bit failure of seeds 58-59 was a design that cannot exist there: bugs, and one missing guarantee.

Files: results/drafts/fail32-tailsplit-401.py, results/applied-after-seed62/musttail-after-seed62.patch (new); results/fail32-400.md,
results/applied-after-seed62/ORDER.md, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 402 - 2026-10-19 - Claude

**The open items while seed 60's chain compares: bfind built in TOS designs (pending, patch 7); xcheck against the
laptop's 32-bit speeds (item 0g); seed 59's 64-bit deaths classified; a lead on the Tegra's link failures.** The
owner's log: seed 60's evolution done at 13:12 (generation 138, 34,522 designs), its chain in compare-fronts.

bfind in TOS designs: a name's walk is one macro, NAME_WALK - bf_walk's in a bfind design, else the plain loop - taken
by THREAD-FIND, (FIND) and gen-tos.py's TOS bodies of them. On master s6 with THREAD-FIND builds the same engine with
bfind as without; with the patch they differ at both widths, for THREAD-FIND on CV8 and (FIND) on the two-bit tag, all
alive, and a design built twice without bfind is identical (results/drafts/bfindtos-402.py). engines-check: two bfind
variants on s6 itself, checked built - the engine not the same without bfind. batch-check, the seven: PASS - 7 patches on a fresh clone of befd1b6: run-tests PASS (engines-check 83 paths), validate 7 of 7 IDENTICAL, jail PASS.

Item 0g: xcheck.py --report --laptop32 FILE compares a 4-byte host with the laptop's own 32-bit speeds too; nothing
changes without it. Seed 59's checks of seed 58's front: the Tegra 0.709 to 0.857, dream at 32 bits 0.651 to 0.650 -
for dream the machine, not the width (results/xcheck32-402.md).

At 64 bits seed 59's only deaths are the reach limit's 188 - CV8 at scale 0 without both varcall and doesfar, calls
that cannot span the image, not run: the designs' own (results/fail32-400.md, results/drafts/fail64-reach-402.py).
The Tegra: all eight link failures of seeds 58-59's chains have fsys on, 5 of the 24 measured - a lead for item 0d
(results/drafts/xcheck-fails-402.py); seed 60's chain records the linker's first error.

Files: results/xcheck32-402.md, results/drafts/bfindtos-402.py, results/drafts/fail64-reach-402.py,
results/drafts/xcheck-fails-402.py, results/applied-after-seed62/bfindtos-after-seed62.patch (new); lab/evolve/xcheck.py,
results/bfind32-fault-399.md, results/fail32-400.md, results/applied-after-seed62/ORDER.md, results/README.md, HANDOFF.md.

## Iteration 403 - 2026-10-19 - Claude

**The other open items, while seed 60's chain compares: processing compares 4-byte hosts at 32 bits by itself;
footprint.py runs end to end; seed 59 read for items 4b and 4c; item 4's return candidate sized.**

Item 0g, closed: process-seed.sh re-reports every 4-byte host with xcheck --laptop32 against the checked run's
results file - on seed 59's archive its summary gives dream at 32 bits 0.650 and the Tegra 0.857 beside the old lines.

Item 2: footprint.py, scheduled after seed 62, run here on seed 59's database (2 designs, N = 100 and 1,000, one round):
built, timed against s6, its tables written, exit 0 - the chain step will run.

Item 4b: seed 59's front has msc, scale and tail at 0%, as seeds 53-58 (results/drafts/gene-usage-53-59.md). Item 4c:
seed 59 does not collapse - the tag-2 family's diversity 0.45-0.52 to the last generation - but it stopped gaining:
the smallest last improved at generation 88 of 143, the best speed's last 2% gain at 81 (review-checks.py progress);
seed 58 was still gaining when it stopped. Its front against seeds 53-58's: rtloopall +56 points, escape +54, supers
+53, guard +48, compiler +35, tos -39 - a run without the carry ends elsewhere; seed 60 (no evolved founders) is the
clean test.

Item 4, the return candidate sized: the JIT's EXIT is a copy-and-patch stencil that ends at its first ret (jit.c reads
0xC3); "EXIT as pop and jmp" would be a second EXIT stencil and a gene choosing it - x86-64 only, worth it only where
calls nest deeper than the return predictor (the JIT's ackermann). Not built: the owner's call.

Waiting on data: 0d (seed 60's chain names the Tegra's link error), 4b and 4c (seed 60's anchoring answer, seeds
61-62), 3 and the batch (seed 63). Deferred by standing decisions: 5, 6, 7.

Files: results/drafts/gene-usage-53-59.md (new); lab/evolve/process-seed.sh, HANDOFF.md.

## Iteration 404 - 2026-10-19 - Claude

**The gene jitret, pending as patch 8: the JIT's EXIT as a pop and an indirect jump, not ret** (the owner: try it).
A ret is predicted by the return predictor, the last 32 or so calls, and the JIT's ackermann nests past 250. With
jitret, EXIT's stencil (mov, mov, ret) is copied with its ret made pop %rcx; jmp *%rcx - rcx free at a return, the
state in rax and rdx; the same address and stack pointer as ret (engine/jit.c, at the stencils' scan). evolve.py: the
gene (needs the JIT) and -DJITRET=1; engines-check: the JIT with jitret.

Measured here (an Intel Xeon, one CPU - rough; the laptop's Zen 4 predicts otherwise), engines-check's JIT design with
and without it against s6, 7 rounds: ackermann 0.464 to 0.343 (-26%), fib 0.329 to 0.329, bubble 0.947 to 1.032 (+9%),
loop 1.149 to 1.213 (+6%), corpus 1.272 to 1.232, kernel 1.049 to 1.077 - the six about 3% faster
(results/jitret-404.md, results/drafts/jitret-404.py). A trade-off, so a gene: seed 63's fronts decide, on the
laptop's predictors. batch-check, the eight: PASS - 8 patches on a fresh clone of c397f25: run-tests PASS (engines-check 84 paths), validate 7 of 7 IDENTICAL, jail PASS.

Files: results/jitret-404.md, results/drafts/jitret-404.py, results/applied-after-seed62/jitret-after-seed62.patch (new);
results/applied-after-seed62/ORDER.md, results/README.md, HANDOFF.md.

## Iteration 405 - 2026-10-19 - Claude

**The after-seed-62 batch rehearsed: every new mechanism alive on real designs and in a short run; one new 32-bit
failure, GCC's t2call tail call on the two-bit tag, fixed as patch 9** (results/rehearsal-405.md). The owner: yes.

The batch's eight patches in a scratch clone, built. Targeted - 13 of seed 59's front designs, evaluated as a run does
at both widths: 4 JIT designs with jithelp, jitre and jitret alive; 3 tos designs with bfind (now built) alive; seed
59's 3 that died at 32 bits (bfind, no tos) alive there, 0.44-0.49; clang tail engines with and without preserve_none
alive; a GCC tail engine on the two-bit tag alive at 64 bits, at 32 "tail calls not jumps (t2call)". A short run (pop
16, one round, tag2, both widths, noevolved), stopped with the session at generation 21: 330 designs, 322 alive at both
widths, 8 refused by the reach limit, no 32-bit failure; jitret in 51, jithelp in 4, GCC tail in 4, clang tail in 6,
all alive.

The failure: t2call, the two-bit tag's shared call path, a static function reached only by jumps - GCC at i386 gave it
a local convention, arguments in registers, so its incoming stack could not hold the five arguments of the next
dispatch: call *%eax in H_t2call. The same pattern keeping the declared convention is a jmp with the design's own flags
(results/drafts/sibcall-i386-405.c). Patch 9: every handler noipa on 32-bit GCC (TC_NOIPA in gen-tail.py, empty
elsewhere); engines-check builds tail calls on the two-bit tag at both widths. With it seed 59's three with a GCC tail
engine on the tag live at both widths, 32-bit 0.813, 0.821, 0.874. batch-check, the nine: PASS - 9 patches on a fresh clone of 789364b: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

Files: results/rehearsal-405.md, results/drafts/rehearsal-targeted-405.py, results/drafts/rehearsal-db-405.py,
results/drafts/tailipa-405.py, results/drafts/t2call-build-405.py, results/drafts/sibcall-i386-405.c,
results/applied-after-seed62/tailipa-after-seed62.patch (new); results/applied-after-seed62/ORDER.md, results/README.md, HANDOFF.md.

## Iteration 406 - 2026-10-19 - Claude

**Seed 60 processed - the anchoring test, clean: small at both widths, so no evidence of anchoring at 12 hours; the
Tegra's build failures named; seed 61 next at 11 hours** (the owner). From the hand-made designs and the founders built
from them alone, with the tag-2 requirement, at both widths: 34,598 designs in 8 h 50 min of evolution, generations
0-138. The verdict from both CPUs: fastest +3.6%, smallest -11.20%, memory -4 KB, hypervolume +0.4%, best Q -5.3% -
small; on each CPU alone too (cpu 2 +2.4%, cpu 8 +3.3%); at 32 bits its fastest 0.325, 3.5% behind - small at both
widths. It reached the carried runs' fast end and passed it under the bar; it stayed 11% above seed 58's plain small
end, the requirement's cost (results/evolve-amd-ryzen-7-pro-8840hs-seed60.md; results/compare-fronts-amd-ryzen-7-pro-
8840hs.md, Session 54). heldout: sieve 0.958, the pick's regret +1.5%. Diversity 0.48 to the end, the smallest still
gaining at generation 136. Predictions: 2 met, 1 met but for a clause (lean on 165 of 167), 2 missed - both better than
predicted (its fastest ahead, not 5-15% behind; at 32 bits 4.8% behind seed 58, not 15%). At 32 bits its deaths are the
two classes the pending batch fixes, no other: 1,042 bfind without tos, 484 tail.

The remote checks of seed 59's front (results/xcheck-seed60.md): dream 0.941 and 0.721, at 32 bits 0.370; the Tegra
built 4 of 10. Its six failures named by the why() of 389: the assembler's `bad immediate value for offset (5224)`, every
one with alignhot 64; across seeds 58-60's chains all 14 failures have alignhot 32 or 64, all 28 that built 0 or 1 -
most likely GCC's ARM literal pools placed without alignment's padding (item 0d; leaving alignhot out of an ARM build
proposed, the owner's).

Gates at this commit: build; run-tests PASS; validate 7 of 7 IDENTICAL; the jail PASS; gate.py: alive: 279 of 279 (the run's front 167, the joint front 120, 8 in both); ans-check: 0 of 43 designs differ from s6 somewhere. (its negative control caught).

NEXT-RUN: `seed 61 tag2 11h widths noevolved` - 11 hours, the owner's, without a comparison step: about 10.5 hours of
evolution, past seed 60's 138 generations, so the replicates read at one generation lose nothing of seed 60's.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed60.md, results/xcheck-seed60.md (new); results/compare-fronts-amd-
ryzen-7-pro-8840hs.md, results/predictions.md, results/progress-by-run.md, results/README.md, lab/evolve/NEXT-RUN,
HANDOFF.md.

## Iteration 407 - 2026-10-19 - Claude

**The Tegra's builds fixed in master: alignhot left out of a 32-bit ARM build; the genes not yet built, listed; the
latest results' action items.** Seed 61 started (the owner, 16:26, from Iteration 406's bundle at ed674ec - 11 hours).

The fix (the owner: yes): evolve.py's ccflags adds alignhot's -falign-jumps, -labels and -functions only off 32-bit ARM
(ARM32: the host's machine armv*) - all 14 of seeds 58-60's Tegra failures, the assembler's bad immediate offset, had
alignhot 32 or 64. Checked here: with alignhot 64 the x86 flags keep it and an ARM32 build's lose it, the rest the
same; run-tests PASS and validate 7 of 7 IDENTICAL at this commit. In master, not the pending batch: it changes no
x86 build, so seeds 60-62 still evolve with one evolver; seed 62's chain is the first to try it on the Tegra (the
prediction in results/predictions.md).

The inventory (the owner: are all the genes in?): not yet - a register machine (the largest prize priced), translation
to direct threading at load, the interpreter's return prediction, and the search's own escape (islands, immigrants) -
HANDOFF item 4e. Action items from seed 60: the simplicity review (4b) is now the owner's to call - the anchoring answer
is in; the tag-2 requirement's cost (11% above the small end, seeds 59 and 60) for seed 63's command; dream's 32-bit
ranking (0.370, and -0.257 against the laptop's own 32-bit speeds, over 6) wants a larger sample before it is read.

NEXT-RUN: none until the owner gives seed 62's hours - so this bundle, pulled, cannot start seed 61 again.

Files: lab/evolve/evolve.py, lab/evolve/NEXT-RUN, results/predictions.md, HANDOFF.md.

## Iteration 408 - 2026-10-19 - Claude

**Seed 62 at 11 hours queued; dream's 32-bit sample made real; the simplicity review proposed; the tag-2 question for
seed 63 put.** The owner: 11 hours for seed 62 too, and proceed with the open items.

NEXT-RUN: `seed 62 tag2 11h widths noevolved then experiment footprint.py`, for when seed 61's chain has finished.

dream's 32-bit check measured 10 designs, 4 of them rejected ones: a 4-byte sample took GCC's designs without the JIT
only, and seed 59's front is half JIT and two-thirds clang - 6 eligible of 171. A prebuilt sample is built on the
laptop, where clang builds 32-bit engines (Iteration 336): xcheck --sample now keeps GCC-only for a host that builds the
designs itself (the Tegra) alone. On seed 60's front here: 109 eligible, 10 sampled for --n 12 - 7 clang, 3 GCC - and
their binaries built (REMOTES asks dream for 30).

The simplicity review (item 4b, the owner's to call now that seed 60 found no anchoring): over seeds 53-60's fronts,
1,431 designs, bytehdr, doesfar, thinhdr and varcall are on in every design, bss and lean in all but one and two; msc,
scale and tail in none, tail for a fault. Proposed: freeze the six, remove msc and scale, judge tail after seed 63
(results/drafts/simplicity-proposal-408.md, results/drafts/gene-usage-53-60.md). And seed 63's command: with the tag-2
requirement or free - seeds 59-60 ended 11-12% above seed 58's free small end.

Files: results/drafts/simplicity-proposal-408.md, results/drafts/gene-usage-53-60.md (new); lab/evolve/xcheck.py,
lab/evolve/REMOTES, lab/evolve/NEXT-RUN, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 409 - 2026-10-19 - Claude

**The simplicity review built, pending as patch 10; seed 63 to run free of the tag-2 requirement** (the owner: yes to
both). evolve.py's FROZEN holds bytehdr, doesfar, thinhdr, varcall, bss and lean on and msc and scale at 0 in every
design the search makes - require() at get(), now always, not only under a requirement - and mutation no longer picks
them; hand-made designs keep their own, so s6 and the stages are unchanged. GENES.md says so above its rows.

Rehearsed: a short free run here with patches 1-10 (pop 16, one round, both widths, noevolved, no tag-2 requirement), to generation 13: 222 designs, 7 hand-made; status {'ok': 222}; 32-bit failures none; designs the search made off a frozen value: 0 - no reach-limit death (seed 60: 247), varcall and doesfar being on. batch-check, the ten: PASS - 10 patches on a fresh clone of 50942b8: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

Seed 63's command waits for seed 62's processing (NEXT-RUN's comment): free of the requirement - its hours and start
asked then. Predictions for it and the freeze: results/predictions.md.

Files: results/drafts/frozen-check-409.py, results/applied-after-seed62/frozen-after-seed62.patch (new); results/drafts/simplicity-
proposal-408.md, results/applied-after-seed62/ORDER.md, results/predictions.md, lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 410 - 2026-10-19 - Claude

**Two levers for the interpreted designs priced on seed 60's front: handler replication not worth building, the
register machine's prize shrunk to 0-39% a workload, and a cheaper lead found** (results/drafts/price-410.md). The owner:
proceed with the remaining items - my pick, the interpreter's return prediction, priced before building.

Handler replication (copies of EXIT and the call handlers, each its own indirect jump): from the laptop's counters,
compute work mispredicts at most 0.54 a thousand instructions; kernel and corpus lose 6.8-23.6% of their cycles to misses,
calls and returns 15-25% of those. Removing every one: the six workloads' geometric mean 0.4-1.6% at most - and no
dispatch removed, where the front end waits on the jump itself (Iteration 301). Not built.

The register machine (stackops.py - its profile parse fixed: the profiler's T and O lines are not pairs): of seed 60's
three fastest interpreted designs' dispatches, moves and lone literals are kernel 11-13%, fib 7-14%, corpus 12-15%,
loop 20%, bubble 39%, ackermann 0.1% - seed 5's were 38-50%. Its first stage (regprice.py) saves 3.8-8.1% of the image's
code on kernel, corpus and parse, and nothing of fib, loop and bubble, whose code is compiled at run time. The lead: R>
in those run-time-compiled loops, 20-26% of loop's and bubble's dispatches - a run-time fusion's target, cheaper than a
register machine; priced next.

Files: results/drafts/price-410.md (new); lab/evolve/stackops.py, results/README.md, HANDOFF.md.

## Iteration 411 - 2026-10-19 - Claude

**Iteration 410's register-machine table corrected, its "R> lead" a mislabel of I; and rtiplus, I + fused at run time,
found inert on the two-bit tag** (results/drafts/price-410.md, "Corrected"). The owner: proceed with the remaining
items - the lead's pricing.

Pricing it, the loop's dispatches named by the converter's own map (CALLMAP) disagreed with stackops.py's: on
4ac602c8bd - escape 2, the two-bit tag - the opcode named R> is I, < is DUP, NEGATE SWAP, LSHIFT XOR, DROP LIT8.
stackops.py now names by the converter's map first. The bound again, seed 60's three fastest interpreted designs:
kernel 20-22%, fib 7-14%, corpus 24%, loop 40%, bubble 46%, ackermann 19% - larger than 410's, and its largest single
mover is I: 20% of loop's dispatches, 26% of bubble's.

I + has a fusion already, rtiplus (Iteration 60). On 4ac602c8bd with it on, I+ takes its opcode slot and the kernel
variant k64-bt-...-loopall-iplus loads the overlay - and the loop's dispatches are unchanged: 20,032,046 against
20,031,683, I still 4,000,038. On the two-bit tag the fusion never fires: expressed, not built, as bfind was under tos.
A timing of the two on this VM said -5.5% on the six workloads' mean, with -19% on ackermann, which nothing changed:
noise and layout - the dispatch count is the measure here. The lead: make I+ fire on the tag (cv8-fuse-iplus.4 was
written for cv8-fuse.4; a tag-2 kernel loads cv8t-fuse.4), or rtiplus needing a design off it.

Files: results/drafts/opnames-411.py, results/drafts/rtiplus-count-411.py, results/drafts/rtiplus-time-411.py (new);
lab/evolve/stackops.py, results/drafts/price-410.md, results/README.md, HANDOFF.md.

## Iteration 412 - 2026-10-19 - Claude

**rtiplus fires on the two-bit tag: I+ pinned to a one-byte code (pending, patch 11) - the loop's dispatches -20%.** The
owner: proceed - fix I+ on the tag.

The cause, in tools/layout.py: on the tag the run-time fuser's SUPER-TABLE holds one-byte codes, and an entry with an
escaped opcode is dropped. I+ is never used by the image's own code, ranks low, and was escaped - so the (I, +) -> I+
entry went, and cv8-fuse-iplus.4's hook found nothing to fuse. Pinned where the table carries it, as Iteration 176
pinned IMM-OPS's keeping forms. On seed 60's 4ac602c8bd with rtiplus on and the batch to patch 11: the loop's
dispatches 20,031,683 to 16,032,016, I's 4,000,036 to 37; bubble unchanged (its I is not before a +); built and alive
both ways. batch-check, the eleven: PASS - 11 patches on a fresh clone of ba83322: run-tests PASS (engines-check 86 paths), validate 7 of 7 IDENTICAL, jail PASS.

Next: on the tag a run-time pair whose fused opcode is escaped is dropped the same way - how many survive for a front
design (results/drafts/price-410.md, "Fixed").

Files: results/drafts/iplustag-alive-412.py, results/applied-after-seed62/iplustag-after-seed62.patch (new); results/drafts/
price-410.md, results/applied-after-seed62/ORDER.md, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 413 - 2026-10-19 - Claude

**The tag drops no other run-time pair: I+ was the only one.** The owner: proceed - the follow-up of 412. The converter
instrumented in a scratch clone to report its run-time pair table on the tag, kept and dropped (results/drafts/
t2pairs-instrument-413.patch); 24 of seed 60's front built with the after-seed-62 batch, every seventh by speed
(results/drafts/t2pairs-413.py). 21 build no run-time pair table - rtfuse off, or no overlay to carry one; the 3 with
rtfuse carry 4, 1 and 3 entries, all kept. I+'s entry was the only casualty: the one opcode the image's own code never
uses. Run-time fusion is rare on the front and its tables small - nothing further to fix (results/drafts/price-410.md).

What remains waits for the runs: seed 61's archive (the replicates' second, the Tegra still failing as predicted), seed
62's (the Tegra fix's first test, dream's larger 32-bit sample, the replicates read together, the eleven-patch batch
applied), then seed 63, free of the tag-2 requirement.

Files: results/drafts/t2pairs-413.py, results/drafts/t2pairs-instrument-413.patch (new); results/drafts/price-410.md,
HANDOFF.md.

## Iteration 414 - 2026-10-19 - Claude

**The project reviewed for what can be done while seeds 61-62 run: the processing steps to come, tried first.** The
owner: review the project. What remains is the runs' (seeds 61-63) or the owner's; the tools those steps use were not
all tried, so each ran here on what is in hand (results/drafts/preflight-414.md).

review-checks.py spread, on seeds 58-60's databases: it works - 466 s for three, so in the background. At generation
133: fastest 0.118, 0.117, 0.111; smallest 14,146, 15,915, 15,938; seeds 59 and 60, both on the tag, 13.6 points of
gene usage apart on average - many settings, one performance. review-checks.py curse on seed 60: the fast end's
optimism 1.066, already below seed 58's 1.112 without the fast gate - seed 63 is read against both. The batch's
application, dry-run in a scratch clone: the eleven apply, the move and the citations' sed work, and handoff-check named
the one thing the routine missed - results/README.md's pending/ORDER.md line; step 6 says so now. And seed 63's command,
proposed for the owner: seed 60's shape without the requirement, with the comparison - its hours his.

Files: results/drafts/preflight-414.md (new); results/README.md, HANDOFF.md.

## Iteration 415 - 2026-10-19 - Claude

**The handoff made self-sufficient for the processing ahead.** The owner: the previous chat is still open if a file is
needed from it - none is: its last bundle (Iteration 398) passed the handoff check, nothing outside the repository, and
every archive since came from the laptop. And make sure the next handoff misses nothing.

One gap: seed 62's processing compares the replicates (review-checks.py spread) over seeds 60-62's databases, and those
live on the laptop, not in the repository - a new chat would have needed seed 60's and 61's archives again. Seed 62's
chain now runs the comparison itself, on the laptop over seeds 58-62 (NEXT-RUN: `... then experiment footprint.py then
experiment review-checks.py spread` - an experiment step gets this run's database and the newest four archived), so its
archive carries it. HANDOFF.md's state names the files a new chat needs - the unprocessed chain archives, seed 61's by
its commit - and HANDOFF-PROMPT.md asks for them.

Files: lab/evolve/NEXT-RUN, results/predictions.md, HANDOFF-PROMPT.md, HANDOFF.md.

## Iteration 416 - 2026-10-19 - Claude

**Programs past 4 MB on every design: plain CV8's three reaches extended (pending, patch 12).** The owner: yes, make
sure programs larger than 4 MB are supported. Two test programs - calls across 4.9 MB of dictionary with a DOES> child
far out (big1, 209), and a DOES> word past 4 MB (big2, 5). On master the two-bit tag ran both; plain CV8 refused both:
at byte headers its call reached 2 MB (21 bits - not the 4 MB I had said), its header link 4 MB, its DOES> call 2 MB.

The fix: a call past reach as the body's address and EXECUTE (cv8.4's FAR,, CALL1, the forms in reach); a fourth link
form, 0xE0-0xFF and 29 bits, with every shorter link as before (cv8b.4, the engine's PREVNFA and bf_prev, the
converter); the far DOES> call in cells - 32 MB at 8-byte cells, 16 at 4 (cv8.4, the engine's and SPN's DODOES, the
converter). Two tries failed on the way: NIP, which this kernel lacks - the overlay did not compile, and build-stages.sh
built on (open, HANDOFF 0h) - and EXECUTE compiled as a primitive, which here is a colon word. Now big1 209 and big2 5 on
s6, seed 58's 09de03f091, seed 60's 4ac602c8bd and 5ee5c38165, and s6 at 4-byte cells; engines-check runs both on s6, the
tag and 4-byte cells. Cost: +184 bytes a plain-CV8 image (s6 9,161 to 9,345). batch-check, the twelve: PASS - 12 patches on a fresh clone of 911e26a: run-tests PASS (engines-check 89 paths, the programs past 4 MB among them), validate 7 of 7 IDENTICAL, jail PASS.

Files: results/bigprog-416.md, results/drafts/bigprog-gen-416.py, results/drafts/bigprog-416.py, results/pending/
bigprog-after-seed62.patch (new); results/applied-after-seed62/ORDER.md, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 417 - 2026-10-19 - Claude

**The final batch rehearsed on plain CV8; patch 12 leaner; patch 13, the stage build stops on an overlay that does not
load** (results/rehearsal-417.md). The owner: proceed - all three.

Patch 12's far call is now (FAR) - the target's address to the return stack, EXIT goes there - in place of EXECUTE looked
up by name: the callee sees its caller's return address, and a plain-CV8 image costs 104 bytes, not 184 (s6 9,161 to
9,265). Patch 13: tools/build-stages.sh checks each dump's load messages for evolve.py's DUMP_ERRORS - a clean build
passes, and cv8b.4 given `: ZZX 1 NIP ;` stops it: "an overlay did not load: Undefined word NIP".

Rehearsed with all thirteen: the far-call tests and the programs past 4 MB right on s6 at both widths; seed 58's front,
all plain CV8, sampled - 8 of 8 alive at both widths; a short free run to generation 7: designs 127 | by encoding {'cell': 1, 'sod16': 1, 'cpt16': 4, 'cv8': 112, 'tag2': 9} | status {'ok': 127} | 32-bit failures none | off a frozen value 0.
batch-check, the thirteen: PASS - 13 patches on a fresh clone of 1a37de3: run-tests PASS (engines-check 89 paths), validate 7 of 7 IDENTICAL, jail PASS.

Files: results/rehearsal-417.md, results/drafts/rehearsal-417.py, results/drafts/rehearsal-db-417.py, results/drafts/
farcall-tests-417.py, results/applied-after-seed62/dumpcheck-after-seed62.patch (new); results/applied-after-seed62/bigprog-after-seed62.patch,
results/applied-after-seed62/ORDER.md, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 418 - 2026-10-20 - Claude

**The register machine begun, kept apart: results/wip-regmachine/ - its first pricing, on code as it runs.** The owner:
work on it independently, so that unfinished it costs the next seed runs nothing. A directory on master, not a git
branch (the bundle carries master alone); nothing there runs, and its patches will reach a run only through the gates
and the owner's approval.

price-418.py: designs built with the profiler and the converter's opcode names; from the profiler's pairs and triples,
the dispatches a register stage could take in as operands - a move or literal straight before the operation that
consumes it, and the one before that. On the tag (seed 60's two fastest interpreted): loop 40%, corpus 13%, kernel
6-10%, sieve 10%, fib, bubble and ackermann nothing - 86% of it loop's `I +`, which rtiplus fuses since patch 11;
control (calls, EXIT, branches) 20-67%. On plain CV8 (seed 58's smallest and a larger one): kernel 21-23%, fib 36%,
corpus 23-26%, loop 25-40%, bubble 11-23%, sieve 17-18%, spread over many patterns (`LIT8 <`, `DUP LIT8 <`, `LIT32 +`,
`DUP @`, `R@ =`...). As an upper estimate - time following dispatches, operands free - the six workloads' mean about 11%
faster on the tag (most of it now I+'s) and 23% on plain CV8. So: on the tag little beyond the fusions in place; on
plain CV8 real room, best met by a general operand form behind a gene - its bytes weighed by the search, plain CV8
holding the small end. Next there: which descriptor set covers how much, then one form prototyped as a patch.

Files: results/wip-regmachine/README.md, results/wip-regmachine/price-418.py, results/wip-regmachine/price-418.out
(new); results/README.md, HANDOFF.md.

## Iteration 419 - 2026-10-20 - Claude

**The register machine's pricing carried on, in results/wip-regmachine/: what few forms would cover - and how much of it
the project's own fusions already do.** The owner: proceed.

coverage-419.py, eight plain-CV8 designs of seed 58's front: the taken-in share by the operand sources it needs - a
literal, the top kept, the return stack, the loop index, OVER and SWAP. fib's 20-36% is nearly all literals and a kept
top; loop's is the loop index; kernel's 11-25% and corpus's 15-27% are spread. Two operations take most in: `+` 42%,
`<` 21%. existing-419.py: those forms largely exist - rtimm's immediates, the loop compiler, I+. On the smallest design,
which uses none, the run-time loop compiler alone takes loop's dispatches down 79% and bubble's 62% for 465 bytes; the
larger designs already carry it. A first try, which pushed format-10 words out of their slots, is kept beside it.

So a general register stage would add less than its first pricing: loop and bubble are the loop compiler's, fib's is
rtimm's immediates (coupled to the run-time fuser, which needs built pairs), kernel's and corpus's spread share is left.
Next there: rtimm without that coupling, measured on fib - before any new engine form.

Files: results/wip-regmachine/coverage-419.py, coverage-419.out, existing-419.py, existing-419.out,
existing-419-first.out (new); results/wip-regmachine/README.md, HANDOFF.md.

## Iteration 420 - 2026-10-20 - Claude

**The immediates measured as they already exist: the gains are there gene by gene; what keeps the small end from them is
their bytes** (results/wip-regmachine/README.md). The owner: proceed - rtimm freed from built pairs, measured on fib.
Correction first: 419 said rtimm waited on built pairs; Iteration 175 freed it already - rtimm=2, the immediates with no
pairs. So this measures it.

existing-420.py, seed 58's smallest design: rtimm=2 - fib -13.6% (`-1 +` and `SWAP -2 +` fused), +608 bytes; DUP<I built
in CMOVE's place adds nothing to fib and costs kernel 9.4% and corpus 6.5% (a format-10 slot is dear); the loop compiler,
-79% loop and -62% bubble for 465 bytes, with the immediates +1,119. The forms a register stage was priced for are there;
their bytes (3-4% of the smallest design each) are why the small end goes without, and a register stage would cost bytes
the same way. Next in the work directory: where those bytes go, then a lean immediates-only overlay and a lean loop
compiler, measured against these rows.

Files: results/wip-regmachine/existing-420.py, existing-420.out (new); results/wip-regmachine/README.md, HANDOFF.md.

## Iteration 421 - 2026-10-20 - Claude

**Where the run-time compilers' bytes go** (results/wip-regmachine/bytes-421.py, its output bytes-421.out). The owner:
proceed. On seed 58's smallest design, from the converter's map of the image's words: the engine grows by nothing in
either case. **rtimm=2, +608**: nine overlay words (IMM+ 89, SUPER-TABLE 88, SMALL-LIT? 85, SUPER-OP 52, FOLD-TABLE 32,
?BRANCH, 26, IMM-OPS 16, LIT-PREV 16, FOLD-DEFAULTS 15), headers about 106, COMPILE, and LITERAL +59 - and the pair
lookup, 140 bytes, serves no pairs: rtimm=2 has none. **rtloop=1, +465**: twelve words (X10-OP 55, X10-XTS 48,
COMPILE,8 32...), headers about 125; its cheaper form exists - rtloop=2, internal words headerless (Iteration 190): +361
here. Across the image, names and links are about 2,679 bytes (32%); hiding internal names in general was priced and
deferred by the owner (222-223, 227) - an overlay's own internal words may go, as rtloop=2 does.

Next in the work directory: a cheaper rtimm=2 - no pair lookup without pairs, internal words headerless - 608 toward
380 bytes, prototyped as a patch and measured.

Files: results/wip-regmachine/bytes-421.py, bytes-421.out (new); results/wip-regmachine/README.md, HANDOFF.md.

## Iteration 422 - 2026-10-20 - Claude

**A cheaper rtimm=2, built as a patch in the work directory: the same forms for 240 bytes instead of 608**
(results/wip-regmachine/rtimm-lean-422.patch; README.md there). The owner: proceed.

forth/cv8-imm.4 carries rtimm=2's forms (`n +` as ADDI n, `SWAP n +` as SWAP+I n) over the kernel's own compiler, without
cv8-fuse.4's pair lookup and its copy of the fold table; BEGIN clears LAST-OP as the fuser's does; its internal words
are headerless. evolve.py builds it, as a kernel variant `-lit`, for rtimm=2 in a plain-CV8 design with no pairs and no
fused tests; tag-2 designs keep the full overlay. On seed 58's smallest design: +240 bytes, fib -13.6% as before; with
rtloop=2, +599 for fib, loop -79% and bubble -62%, where the two at their old cost were 1,119.

Checked: the corpus at both widths; run-time compiles - a literal before BEGIN, `n +`, `SWAP n +`, a loop, a branch -
the same numbers with and without, at both widths; the seed 58 and 60 front designs with rtimm=2 rebuilt, one lean
(-392 bytes), five unchanged and byte-identical to their records; run-tests PASS; validate IDENTICAL. Master's code is
unchanged: the patch was taken with git diff and the tree restored; it applies to master as of this iteration.

Files: results/wip-regmachine/rtimm-lean-422.patch, rtimm-lean-422.out, rtimm-lean-422-measure.py,
rtimm-lean-422-checks.py, rtimm-lean-422-front.py (new); results/wip-regmachine/README.md, HANDOFF.md.

## Iteration 423 - 2026-10-20 - Claude

**A fix to the cheaper rtimm=2, and a leaner loop table - both patches in the work directory, checked at both widths for
real** (results/wip-regmachine/README.md). The owner: continue.

Fix: rtimm=2 passes --rtfuse, so the full overlay fuses a design's built pairs and tests rtfuse or not; 422's rtimm_lean
asked only about rtfuse, and would have taken that fusion from a plain design with pairs and rtfuse off. It now asks for
no pairs and no tests at all; the designs measured had neither, so 422's numbers stand. The five front designs it left
alone are tag-2 designs with fused tests - no tag-2 lean version would apply; not built.

rtloop-lean-423.patch: the loop compiler's X10-XTS as three 16-bit offsets, no range check (forth/cv8-fuse-loop.4,
tools/layout.py). -56 bytes on seed 58's smallest (rtloop=2 +361 -> +305), dispatches unchanged; 301 front designs with
the loop compiler rebuilt, all alive, median -48 bytes; run-time compiles of I, J, UNLOOP EXIT, ?DO, LEAVE, +LOOP right;
run-tests PASS, validate 7 of 7 IDENTICAL.

Correction: 422's "cell 4" checks built 64-bit again - the width is EVOLVE_CELL's, not the genome's. Both patches applied
together and checked at 64 and, with EVOLVE_CELL=4 and gcc -m32, at 32 bits: the corpus and fifteen run-time compiles
right in every variant; both on the smallest design +543 bytes at 64 bits (+511 at 32), where the two cost 1,119. The
patches apply to master alone and together; master's code is unchanged.

Files: results/wip-regmachine/rtloop-lean-423.patch, rtloop-lean-423.out, rtloop-lean-423-checks.py, both-423.out,
both-423-checks.py (new); results/wip-regmachine/rtimm-lean-422.patch (the condition), README.md, HANDOFF.md.

## Iteration 424 - 2026-10-20 - Claude

**The two cheaper run-time compilers queued as the after-seed-63 batch, rehearsed with the after-seed-62 batch**
(results/applied-after-seed63/ORDER.md). The owner: queue both for the after-seed-63 batch.

On a clone of master with the thirteen after-seed-62 patches applied, rtloop-lean applied as made; rtimm-lean did not:
one hunk - its headerless line - met the batch's changes there, and was placed by hand, the patch's changed lines the
same. Then the rehearsal: the stages built, run-tests PASS, validate 7 of 7 IDENTICAL, test-jail PASS; seed 58's
smallest at 64 and 32 bits in five variants, the corpus right and fifteen run-time compiles the same in every one (both
on: +551 bytes at 64 bits, +511 at 32); 36 front designs with rtimm=2 or the loop compiler built and alive, one lean
(rehearsal-424.out). They wait one run - seed 63 judges the after-seed-62 batch - and the processing routine (step 6)
now says how a queued batch becomes results/pending/ once the one before it is applied.

Files: results/applied-after-seed63/ORDER.md, rtimm-lean-after-seed63.patch, rtloop-lean-after-seed63.patch,
rehearsal-424.out (new); results/README.md, results/wip-regmachine/README.md, HANDOFF.md.

## Iteration 425 - 2026-10-20 - Claude

**Seed 61 processed: seed 60's first replicate landed at seed 60's ends** (results/evolve-amd-ryzen-7-pro-8840hs-seed61.md).
`seed 61 tag2 11h widths noevolved` at ed674ec37: 37,813 designs in 10 h 17 min of evolution, generations 0-151. No
verdict - no comparison step. By each run's own measures: fastest 3cee75bc70 0.110 (seed 60: 0.111), smallest
37d5da9011 15,907 bytes (15,930); at 32 bits 0.344 (0.325). Its Q-best 2a2b350006 reads Q 0.188 of s6's, under seed 57's
0.209, but s6's figures move with the code; by the raw numbers it equals seed 57's e6b5f1749e within 0.4%. Front 154,
all tag-2; tos 125, the JIT 72. heldout 0.951, the pick's regret +3.0%; fast-end optimism 1.095 at the fastest tenth;
diversity 0.486; the smallest still gaining at generation 142, the speed's last 2% at 75. At 32 bits 1,780 corpus
deaths, all bfind without tos, and 368 compile failures, all tail - the classes the after-seed-62 batch fixes.

The pack's checks PASS; on master: tests PASS, validate 7 of 7 IDENTICAL, jail PASS, the gate 154 of 154 alive (with no
comparison pack, `/dev/null` in its place - written into the routine), ans-check 0 of 40 differ, its negative control
caught. Its chain's remote checks of seed 60's front (results/xcheck-seed61.md): dream 0.863/0.910/0.929, the Tegra
0.991 - all 16 built; none of seed 60's front carries alignhot above 1, so the Tegra fix stays untested by chains (seed
61's front: alignhot 0 everywhere). Predictions scored - the length and the 32-bit classes right, the Tegra's consistent
with its failure half untested; seed 62's ends predicted from the two replicates. results/progress-by-run.md
regenerated. No compare-fronts session: no comparison step.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed61.md, results/xcheck-seed61.md (new); results/predictions.md,
results/progress-by-run.md, results/README.md, HANDOFF.md.

## Iteration 426 - 2026-10-20 - Claude

**Seed 63 planned at 11 hours** (the owner): `seed 63 11h widths noevolved then experiment compare-fronts.py --rounds 6
--widths 8,4 --frontier --cpus 2,8`, written into NEXT-RUN at seed 62's processing (HANDOFF.md, item 0). Its comparison
is reserved from the 11 hours, so about 7 3/4 hours of evolution - seed 60 at 12 hours with the same step evolved 8 h 50.
Seed 62's line stays as it is, 11 hours. A summary of the runs for the owner, no new files.

Files: HANDOFF.md.

## Iteration 427 - 2026-10-20 - Claude

**The processing tools do what seed 61's processing did by hand.** The owner: proceed with the open action items' two
tool fixes. review-checks.py fail32 DB: a run's 32-bit failures by cause - died on the corpus with bfind and no tos, no
engine from the tail engine (by compiler), the causes the after-seed-62 batch fixes, anything else by its message as
"not a known cause"; on seed 61's database it gives Iteration 425's hand count exactly (2,148 of 2,148 known: 1,780,
181, 172, 15). process-seed.sh's summary now carries review-checks.py curse (the fast end's optimism) and fail32 -
checked on seed 61's archive. gate.py RESULTS [COMPARE]: with no comparison pack it gates the run's front alone (seed
61's: 154 of 154 alive), in place of 425's /dev/null. From seed 63 on, a known cause in fail32 is a regression.

HANDOFF.md: the routine's steps 1 and 5 name them; item 4e rewritten - the register machine parked, with what 418-424
found, in place of the old "largest prize" and the work's running notes; item 4b carries the rtimm=2/rtfuse overlap
(423) as the owner's call beside tail after seed 63; item 0d says the chains cannot test the Tegra fix while the fronts
carry alignhot 0 (425) - moot, or one directed check: the owner's call.

Files: lab/evolve/review-checks.py, lab/evolve/process-seed.sh, lab/evolve/gate.py, HANDOFF.md.

## Iteration 428 - 2026-10-20 - Claude

**The Tegra's rebuild test, part of seed 62's chain** (the owner: do it as part of the next run). xcheck.py --sample
learned --also ID,ID...: designs asked for by id, their genomes from the results files beside the checked one, sampled
after the regular sample, passed through the same filters (itself on that host; at 4-byte cells built and alive here
first), marked 'asked'; the host carries the mark; the report lists them apart - "Asked for by id: N of M built and
measured here" - and keeps them out of the agreement, which is about the checked front; process-seed.sh's summary greps
the line. REMOTES' rage line asks for four of the 14 failures: ce937eca6d and 5405c5b1d9 (alignhot 32, the linker's
error in seeds 58-59's chains), 3a5638f18d and cd9d470f51 (alignhot 64, the assembler's in seed 60's) - every one of
the 14 is alignhot 32 or 64, and the two failure messages split with the alignment and the chain; 40 minutes more
(160). Three of the 14 have no genome in the repository (369ef14956, ade7c2acb9, fb73c9be4a: rejected designs, in the
laptop's databases only).

Tested here: the sample at 4-byte cells with the four asked for (4 of 4 taken, after 12 of seed 61's front); a host run
of two of the sample and the four at 4-byte cells on this x86 machine - all six built and measured, the report's
"Asked for by id" section 4 of 4, the agreement left to the other two. The Tegra itself is the test: seed 62 must start
from this bundle or a later one. Predicted: all four build there.

Files: lab/evolve/xcheck.py, lab/evolve/process-seed.sh, lab/evolve/REMOTES, results/predictions.md, HANDOFF.md.

## Iteration 429 - 2026-10-20 - Claude

**The Tegra in parallel with everything, never slowing a run; and a fix to 428's rebuild test.** The owner: no
cross-compiling on the laptop; the Tegra compiles with its own GCC; it is slow, so its builds and runs in parallel with
all the rest, never slowing them. As it stood, the Tegra's check already ran beside the evolution (started in the
background, Iteration 379), and gather waited on a host only until its own deadline - 2-2 1/2 hours into a 10 1/2-hour
run, long past by then. Now a guarantee rather than a margin: next-run.sh hands remote-checks.sh the evolution's
deadline (RUN_UNTIL); no check's deadline lies past it less 5 minutes, a check with under 15 minutes left is skipped,
and REMOTES' minutes "run" means all the time the evolution leaves - the Tegra's line takes it, so it never cuts itself
short and the chain never waits. Its one cost to the laptop is its sample, made before the evolution so as not to
disturb the run's timings: 137 s here for its exact line (12 of the front, 4 rejected, 4 asked for), each built and
alive at 32 bits - about 2 minutes of the 11 hours.

The test with stand-in hosts (SSH and SCP stand-ins, a chain-like archived front with its database) found a bug in
428: --also looked for the asked designs' genomes beside the sampled report - in a chain the archived run's report.md,
where no results file lies - so seed 62's chain would have left all four out, saying so only in a sample log. It reads
the repository's results now: the stand-in chain took 2 of 2 asked, 1 rejected, and its deadlines came out right -
"run" 54 minutes with an hour left, 600 capped to 52. Seed 62 must start from this bundle or later. The owner's
decisions recorded: the Tegra compiles for itself; no cross-compiling on the laptop; no phone host (428).

Files: lab/evolve/remote-checks.sh, lab/evolve/next-run.sh, lab/evolve/xcheck.py, lab/evolve/REMOTES, HANDOFF.md.

## Iteration 430 - 2026-10-20 - Claude

**The best design across the machine classes set to be measured head to head in seed 62's chain; seed 63's decision
rules written before its results** (the owner: proceed with both).

Head to head: bf439eb307 (seed 60, rejected by its selection; its record now in results/candidates-generic.md),
11e5884401 and ad56a8e0fd (seed 58's front) asked for by id on dream's 32-bit check, its 64-bit pair and the Tegra
(REMOTES). xcheck.py: --also reads results/candidates-*.md too, and a paired check (--from) carries its pair's asked
designs (it carried only rejected ones). review-checks.py generic REMOTE_DIR ranks every design measured on x86-64,
32-bit x86 and ARMv7 by the geometric mean of its speeds, vetoing one more than 25% behind a class's best (GOALS.md);
process-seed.sh's summary carries it. On seed 61's chain: 14 designs on all three, bf439eb307 first at 0.455, every
front design vetoed (0.780 and slower). A stand-in chain start (SSH and SCP stand-ins, seed 61's archived front):
dream's 32-bit sample took 3 of 3 asked, its 64-bit pair the same four designs with binaries built, the Tegra's 2
asked with a rejected one - its minutes "run" 170 with three hours left.

Rules: results/seed63-rules.md - eleven, each with its measure, threshold and consequence: the JIT genes and tail kept
if "used" (10% of the front, or one of its fastest tenth), else proposed out; the fast gate by the fastest tenth's
optimism (at most 1.05 works); the freeze, 32-bit failures and programs past 4 MB as correctness; the small end at most
14,535 bytes; I+ above 10%; the rtimm/rtfuse overlap by its count on the front. Prediction for the head to head
written.

Files: results/seed63-rules.md, results/candidates-generic.md (new); lab/evolve/xcheck.py, lab/evolve/review-checks.py,
lab/evolve/process-seed.sh, lab/evolve/REMOTES, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 431 - 2026-10-20 - Claude

**Seed 63's rules checked against losing good designs - one would have; revised, and adopted** (results/seed63-rules.md).
The owner: double-check the rules lose no potentially good designs; if not, use them.

The gene rule as written at 430 judged one run ("used": 10% of the front, or one of its fastest tenth). Seeds 58-61's
fronts show a run's shares swing too much: it would have marked jitimg out after seed 61, jitvar after 59 and 61, jitos
after 58, 60 and 61, rtimm after 58 and 61, opcall after 59 and 60 - each among the fastest designs in another run; the
replicates 60 and 61 alone differ by 12% against 6% (jitvar) and 2% against 30% (opcall). Revised: a gene is proposed
out only if, over its first three runs (seeds 63-65), it is never on 10% of the front nor in a fastest or smallest
tenth, and a dependence test - every front design carrying it rebuilt without it - shows nothing lost (under 2% a
workload, under 1% in bytes); then frozen off for a run, the code kept, and removed only if that run's comparison
shows no loss. The fast gate's rule gained a lower bound (under 0.98: too harsh).

The others checked: the freeze - four of seeds 56-61's 1,050 front designs broke it, none in a smallest tenth; rebuilt
with the frozen value all four live and are smaller (-120 to -2,370 bytes), the largest speed effect seed 60's
4ac602c8bd with lean, kernel +1.25% in dispatches, the rest within 0.31%. The rtimm/rtfuse proposal removes no
behaviour (rtfuse on gives the same). The rest only measure. Adopted.

Files: results/seed63-rules.md, results/README.md, HANDOFF.md.

## Iteration 432 - 2026-10-20 - Claude

**Genes by votes, not by rule** (the owner: rules should vote for removal, a gene going only on several votes).
results/seed63-rules.md's gene rule becomes "The gene votes": per gene and run, four weak removal votes - under 10% of
the front, none in its fastest tenth, its smallest, its best-Q tenth; strong keep votes, any one blocking - in such a
tenth in any of the last three runs, a dependence test showing loss, the owner's word; a candidate at 11 of 12 over
three runs with no keep vote, then the dependence test, then a reversible proposal; and votes the other way, to
unfreeze. review-checks.py votes RESULTS.md [--seed N] [--ledger FILE [--append]] counts them and keeps the ledger,
results/gene-votes.md - empty until seed 63's processing appends the first run (HANDOFF step 6); process-seed.sh's
summary shows the run's votes and the tally, without writing.

A dry run over seeds 59-61 (not in the ledger): candidates skippad, scale, fold, sharedcall, tail, msc, hotcalls,
tailpn, alignhot - scale and msc frozen at 0 by patch 10 already; jitimg, jitvar, jitos and opcall kept, each in a
fastest tenth in one of the three.

Files: results/gene-votes.md (new); lab/evolve/review-checks.py, lab/evolve/process-seed.sh, results/seed63-rules.md,
results/README.md, HANDOFF.md.

## Iteration 433 - 2026-10-20 - Claude

**Seed 62 processed: seed 60's second replicate - its small end where theirs is, its fast end 5% behind; the replicates
and the footprint answered; the after-seed-62 batch applied** (results/evolve-amd-ryzen-7-pro-8840hs-seed62.md).
`seed 62 tag2 11h widths noevolved then experiment footprint.py then experiment review-checks.py spread` at 017b7ca97 -
Iteration 425's bundle, so without 428-432's Tegra rebuild test and head to head, which move to seed 63's chain
(REMOTES' comments say so). 38,837 designs in 10 h 20 min, generations 0-155; no verdict, no comparison step.

Its ends by its own measures: fastest 0.116 (seeds 60, 61: 0.111, 0.110), smallest 15,897 bytes (15,930, 15,907), at
32 bits 0.315 (the best of the three). Front 192, all tag-2; heldout 0.973 (the best yet), regret +1.6%; fast-end
optimism 1.066; Q-best f30818656b, Q 0.204 of s6's. At 32 bits 1,966 failures, all known causes. Remote checks of seed
61's front (results/xcheck-seed62.md): dream 0.943, 0.958, 0.945; the Tegra 0.847, all 16 built; two rejected designs
faster than the front's fastest there.

**The replicates** (review-checks.py spread over seeds 58-62 at generation 133): seeds 60-62 within 0.06% at the small
end and 0.7% in hypervolume, 5.05% at the fastest - one basin at the small end, about 5% of chance at the fast end:
Iteration 393's prediction 4's condition, the case for an escape mechanism - the owner's call (HANDOFF item 4c).
**footprint.py** (12 of the front, 100-30,000 words): the order holds, weakening (Spearman 0.951 to 0.783), but the fast
designs' lead over s6 shrinks from about 4x to 1.1-1.5x at 10,000 words - the small selection programs flatter the
fast end; a footprint workload or a held-out check - the owner's call (item 2). The freeze against seed 62's front: 8
fast designs with bss off and one with thinhdr off; with bss on each is 1,056 bytes smaller and alive.

**The after-seed-62 batch applied**: batch-check PASS on a8cf8a1 (13 patches; tests, validate 7 of 7, jail); applied,
git mv to results/applied-after-seed62/ with its citations; the after-seed-63 batch moved into results/pending/ (its
paths followed; one routine sentence the path substitution had garbled rewritten). On the new master: the build, run-
tests PASS, validate 7 of 7 IDENTICAL, jail PASS, the gate 192 of 192 alive with the frozen values, ans-check 0 of 49
differ (its negative control caught) - the first background chain stopped silently after the jail, its last three
steps run again - and the queued batch's batch-check PASS on 3b12b75. Predictions scored (9 right, 4 wrong, 2 not run);
NEXT-RUN: seed 63's line; results/progress-by-run.md regenerated.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed62.md, results/xcheck-seed62.md (new); results/applied-after-seed62/
(the batch); results/pending/ (the after-seed-63 batch); the 13 patches' files; lab/evolve/NEXT-RUN, lab/evolve/REMOTES,
results/predictions.md, results/progress-by-run.md, results/README.md, HANDOFF.md.

## Iteration 434 - 2026-10-20 - Claude

**Seed 63 at 10 hours** (the owner): NEXT-RUN `seed 63 10h widths noevolved then experiment compare-fronts.py --rounds 6
--widths 8,4 --frontier --cpus 2,8`. The comparison is reserved from the hours, so about 6 3/4 hours of evolution -
some 100 generations at seed 62's pace (155 in 10 h 20). results/seed63-rules.md's rule 6 (the small end at most 14,535
bytes) gains a first step for a shorter run: if above, read at a common generation with seed 58 (review-checks.py
spread), which had 14,146 by its 133rd, before the frozen genes' bytes are examined.

Files: lab/evolve/NEXT-RUN, results/seed63-rules.md, HANDOFF.md.

## Iteration 435 - 2026-10-20 - Claude

**The two decisions seed 62 left, prepared** (the owner: both). A pre-flight first, nothing changed by it: seed 63's
chain start on the new master with stand-in hosts, REMOTES' own lines (smaller samples) and seed 62's archived front -
dream's 32-bit check took the 3 candidates, its 64-bit pair the same designs with binaries, the Tegra all 7 asked for
(the rebuild test's 4 and the 3), its deadline the run's remaining time.

**The escape mechanism** (results/drafts/escape-mechanism-435.md): the fast end stalls early - the best speed's last 2%
gain at generations 104, 75 and 45 in seeds 60-62 - and the evolver's diversity (the attic, borrowing, crowding, the
families' and Q's keepers) keeps gene values, not rival fast lineages. Islands, age-layered immigrants, restart on
stagnation and replicates compared; islands recommended - an evolver option off by default, built apart, tried in one
run against seeds 63-64 at their common generation.

**The footprint gate** (results/drafts/footprint-gate-435.md): in seed 62's database 1,266 children (4.1%) fell in the
fast gate's window; a reading at 10,000 words costs about 1-2.5 s (footprint.py here, results/drafts/
footprint-gate-435.out). A held-out check after each run about 10 minutes; a gate 1-2% of a run, but its reading does
not mix with the selection's speed without a new rule; a footprint workload for every design some 30% of the
generations. Recommended: the held-out check first, a gate or workload only if the top reorders at 10,000 words.

Files: results/drafts/escape-mechanism-435.md, results/drafts/footprint-gate-435.md, results/drafts/footprint-gate-435.out
(new); results/README.md, HANDOFF.md.

## Iteration 436 - 2026-10-20 - Claude

**The islands built, as patch 3 of the pending batch; the held-out footprint check put in seed 63's chain** (the owner:
implement both for the next run). Islands go with the batch, not into seed 63 - its batch and its pre-registered rules
are judged without a second change - so the first run that can say "islands" is seed 64.

Islands (results/applied-after-seed63/islands-after-seed63.patch): evolve.py --islands K - the population in K islands, each ranked
and bred alone, a share of the Q keepers each, a ring of migrants every 10 generations (each island's two fastest and
its best by Q); the run's front every island's together. The generation loop's breeding and survival became two
helpers, unchanged for one island. next-run.sh: the word "islands" - --islands 4. Tested here: 16 designs, 4 generations,
four islands migrating every 2 - migrants at 2 and 4, the attic fed from every island, the fast gate as usual, the
report written; and one island, two generations, as before (results/drafts/islands-smoke-436*.log).

The footprint check: footprint.py --fastest (the K fastest of the front, not K spread over it); NEXT-RUN's seed 63 line
ends `then experiment footprint.py --fastest --sample 16 --sizes 100,10000 --rounds 3` - about 15 minutes past the
10 hours. Predicted: within the 16 fastest, Spearman under 0.6 at 10,000 words.

Files: results/applied-after-seed63/islands-after-seed63.patch, results/drafts/islands-smoke-436.log, islands-smoke-436-one.log (new);
lab/evolve/footprint.py, lab/evolve/NEXT-RUN, results/applied-after-seed63/ORDER.md, results/predictions.md, HANDOFF.md.

## Iteration 437 - 2026-10-20 - Claude

**Islands and the footprint check, checked and aligned with what the owner approved.** The owner: proceed with both
(435's offer: islands built kept apart; the footprint check in the chain from seed 64 on). Iteration 436's work was
already in the repository - an earlier pass at this request whose reply never reached the conversation: islands as
patch 3 of the pending batch (off by default - the word "islands" in a seed line - so the first run that can use them
is seed 64), footprint.py --fastest, and the held-out check put after seed 63's comparison, 15 minutes past its 10
hours. Checked: the smoke runs' logs (four islands ranked and bred alone, migrants at generations 2 and 4; one island
as before); the pending batch's three patches batch-checked together on a fresh clone of 28a0066 - run-tests PASS,
validate 7 of 7 IDENTICAL, jail PASS. Aligned: the footprint check from seed 64's line on, as approved - out of seed
63's line, which stays at the owner's 10 hours; seed 63's processing writes it into seed 64's (HANDOFF item 2); its
prediction moved with it.

Files: lab/evolve/NEXT-RUN, results/applied-after-seed63/ORDER.md, results/predictions.md, HANDOFF.md.

## Iteration 438 - 2026-10-20 - Claude

**Seed 63's rules measure themselves** (the owner: proceed). review-checks.py rules RESULTS.md [--db DB] [--ledger
FILE] [--seed N]: results/seed63-rules.md's ten rules, one line each - what was measured, the rule, and PASS,
ATTENTION (the rule's "then" applies), PROPOSE, NOTED or SEE (another step reads it): the JIT genes' and tail's votes
with the ledger's three-run tally, the fast gate's optimism, the freeze (front designs off a frozen value, and the
reach limit's refusals from the database), 32-bit failures by known cause, the small end, I+'s share, the
rtimm/rtfuse overlap's count. process-seed.sh's summary carries it.

A dry run on seed 62 (before the batch, the tag-2 requirement on) - in the rules file: the fast gate 1.066, the freeze
broken by 9 front designs with 219 refusals at the reach limit, 1,966 32-bit failures of known causes, the small end
15,897 bytes - each an ATTENTION the batch or the free setup answers; I+ 0% noted; the JIT genes and tail not
candidates (one run); and three of seed 62's front designs rely on the rtimm=2/rtfuse overlap - so rule 9, had it
applied there, would change nothing.

Files: lab/evolve/review-checks.py, lab/evolve/process-seed.sh, results/seed63-rules.md, HANDOFF.md.

## Iteration 439 - 2026-10-20 - Claude

**A deep audit: are good genes or promising designs being rejected?** (the owner; results/audit-genes-designs-439.md).
Every place the pipeline turns designs away, checked against seed 62's database (38,210 CV8 designs) and seeds 58-62's
fronts, on today's master: survival is guarded (the attic, the families' and Q's keepers); the surrogate screen works
- 1 of 880 audited screened children reached the front against 5.3 expected - at a cost of about 9 front-quality
designs a run; the reach limit goes with the freeze; the 32-bit tail failures are fixed - a design of each failing kind
(tail GCC, tail clang, tailpn) built and lived at 32 bits here; the freeze, the rules and the tag-2 requirement as
checked before; selection on the laptop alone a known blind spot, measured by seed 63's head to head.

The genes (results/drafts/audit-genes-439.out, every CV8 gene set / expressed / on the fronts): **one real rejection -
rtloopall**, blocked by its prerequisite, all eight loop words in the format-10 list: of 5,819 genomes setting it in
seed 62, 92 could express it (J missing in 4,044, UNLOOP 3,380, (LEAVE) 3,250); its front share 28-65% in seeds 58-61,
1% in 62 - chance - and rtiplus behind it (1 expressed). Proposed: a repair mutation, the missing loop words first in
the list, a patch after seed 63. The rest: jithelp, jitre, jitret new (no founders; mutation reaches them); hotcalls and
sharedcall dead under the tag by design, back in the free seed 63; tail and tailpn unblocked; the rare genes used.
Mechanisms not yet genes: direct threading at load the one never priced - its pricing proposed.

Files: results/audit-genes-designs-439.md, results/drafts/audit-genes-439.out (new); results/README.md, HANDOFF.md.

## Iteration 440 - 2026-10-20 - Claude

**The audit's two follow-ups: the rtloopall repair built as patch 4 of the pending batch; direct threading at load
priced - not worth building** (the owner: proceed with 1 and 2).

The repair (results/applied-after-seed63/loopall-repair-after-seed63.patch): evolve.py's mutation, when it turns rtloopall on - or,
one child in four (EVOLVE_LOOP_REPAIR), when a child carries it blocked - puts the missing loop words first in the
format-10 list and turns the run-time loop compiler on. Tried on seed 62's blocked genomes first, it unblocked two in
three: the rest were tag-2 designs without escape, 2-4 format-10 slots, too few for eight - so the repair turns escape on
there too (escape and rtloopall are linked already). Then 4,370 of the 4,462 measured genomes carrying rtloopall blocked
express it; four repaired ones built and lived with it on; a short evolution with the repair always on (16 designs, 3
generations) - 64 of 64 alive, the repaired child among them. The four pending patches batch-checked together on
3922f6d: run-tests PASS, validate 7 of 7, jail PASS. Seed 64 is the first run with it; predicted.

Direct threading at load (results/drafts/price-dthread-440.md): the dispatch lab's own comparison - fib -5.5%, loop
+8.9%, sieve -12.4%, about 3% on the geometric mean - one table load saved, the jump's misprediction the same; the
image expanded to addresses about +58 KB on seed 62's front, a third of the memory objective; and a new engine path
the size of the tail engines. Not built; GENES.md's "Not yet" carries the price.

Files: results/applied-after-seed63/loopall-repair-after-seed63.patch, results/drafts/price-dthread-440.md (new);
results/applied-after-seed63/ORDER.md, lab/evolve/GENES.md, results/predictions.md, results/README.md, HANDOFF.md.

## Iteration 441 - 2026-10-21 - Claude

**Seed 63 processed: the batch's first run, free - the small end and 32 bits the best yet, the fast end lost because
the JIT never assembled; the after-seed-63 batch applied** (results/evolve-amd-ryzen-7-pro-8840hs-seed63.md).
`seed 63 10h widths noevolved then experiment compare-fronts.py ...` at 863f35005 (Iteration 434): 23,151 designs in 6 h
37 min, generations 0-90. **Verdict: not small** - against seeds 59-62, both CPUs agreeing: fastest -55.1%, smallest
+10.80% (14,348 bytes), hypervolume +15.1%, best Q -20.7%; at 32 bits its fastest +13.1%, the best yet.

**Why the fast end fell**: the JIT needs the two-bit tag, and the hand-made founder carrying it had tag2 off - its JIT
never expressed; seeds 59-62 required the tag, seed 58 had evolved founders; seed 63 had neither. The tag stayed at
3-6% of its designs, the JIT at 1-4% (315 of 18,624), its fastest JIT design 0.269. Not the batch: seed 62's fastest JIT
designs measured the same on seed 62's code and today's (0.163, 0.153 against 0.153, 0.155 here). A second fault: three
designs did not compile - jitre calls jit_ends, defined only with jitx. Both fixed in one patch, tested.

The rules (review-checks.py rules): the freeze PASS (no reach-limit refusal, the frozen values held), 32-bit PASS (no
failure at all), the small end PASS; the fast gate 1.051 - partly; I+ 0, behind rtloopall (its repair in the batch now
applied); jithelp, jitre, jitret, tail not candidates - the JIT's genes not voted this run (unavailable), the ledger
says why; the rtimm/rtfuse overlap: 14 front designs rely on it - no change. Remote checks of seed 62's front
(results/xcheck-seed63.md): **the Tegra built all 7 asked for - item 0d closed**; the head to head: seed 62's 5f512a3017
first across the machine classes (mean 0.419), then 83716d5eaf (0.437), bf439eb307 (0.467). Predictions: 7 right, 2
wrong (I+; the candidates above the checked front), one uninformative.

The after-seed-63 batch: batch-check PASS on 68f360b, applied (results/applied-after-seed63/). On the new master: the
build, run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS, the gate 161 of 161 alive (the run's 104 and the joint
front's 107), ans-check 0 of 27 differ (the first chain stopped after the jail again; its last two steps run again).
Session 55 appended; the gene votes' first run in the ledger; REMOTES' --also lists out; NEXT-RUN seed 64, 10 hours,
the footprint check after it; results/progress-by-run.md regenerated.

## Iteration 442 - 2026-10-21 - Claude

**The JIT fix applied before seed 64** (the owner: Continue, after the recommendation to apply it now). batch-check of
the one patch on 072d26e: run-tests PASS, validate 7 of 7 IDENTICAL, jail PASS; applied as the after-seed-63 batch's
patch 5. Seed 64 starts with a founder whose JIT works; predicted.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed63.md, results/xcheck-seed63.md (new); results/applied-after-seed63/
(the batch and patch 5); engine/jit.c, lab/evolve/evolve.py and the batch's files; lab/evolve/NEXT-RUN,
lab/evolve/REMOTES, results/gene-votes.md, results/compare-fronts-amd-ryzen-7-pro-8840hs.md, results/predictions.md,
results/progress-by-run.md, results/README.md, HANDOFF.md.

## Iteration 443 - 2026-10-21 - Claude

**Seed 64 processed: the JIT back, the smallest design of any run, not one design died; the rtloopall repair and the
footprint question answered** (results/evolve-amd-ryzen-7-pro-8840hs-seed64.md). `seed 64 10h widths noevolved then
experiment footprint.py --fastest ...` at c094ab788 (Iteration 442): 37,499 designs in 9 h 25 min, generations 0-146;
no compile failure, no reach-limit refusal, no 32-bit failure. No verdict (no comparison step).

By its own measures: fastest 0.125 (seed 62: 0.116; seed 63: 0.263), smallest 14,047 bytes (seed 58's 14,146 the
smallest before), at 32 bits 0.333. The JIT on 81 of 167 front designs, jitx and jitloop on all of them (seed 63: 10) -
the founder's fix. rtloopall expressed in 78% of the genomes that set it (seed 62: 1.6%), on 155 of the front; rtiplus on
55. heldout 0.978, the fastest tenth 0.888, regret +0.0% - the best yet; fast-end optimism 1.085 (the fast gate's rule:
revisit). The footprint check: the 16 fastest keep their order at 10,000 words (Spearman 0.888; 0.797 at 100), their lead
over s6 about 4x to 2x - no footprint gate or workload needed; the check stays. Rules: freeze, 32-bit, small end, I+ PASS;
rule 9 proposes rtfuse to govern (no front design relies on the overlap). Gene votes: none a candidate after two runs;
skippad, fold, sharedcall, tail, kstack, opcall, tailpn at 8 of 8. Remote checks of seed 63's front
(results/xcheck-seed64.md): cf524f4c20, rejected by seed 63's selection, first across the machine classes (0.409).
Predictions: 8 right, 1 wrong (the footprint top's reordering), 1 past its bound the good way (the small end).

On master: the build, run-tests PASS, validate 7 of 7 IDENTICAL, the gate 167 of 167 alive, ans-check 0 of 43 (its
negative control caught), the jail PASS - this time the whole chain finished: the jail run last and in its own session
(it had ended the chain after it twice); the routine now says so. NEXT-RUN: seed 65 as seed 64 until the owner decides
on islands; results/progress-by-run.md regenerated.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed64.md, results/xcheck-seed64.md (new); results/gene-votes.md,
results/predictions.md, results/progress-by-run.md, results/README.md, lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 444 - 2026-10-21 - Claude

**Seed 65 set: islands, 12 hours** (the owner). NEXT-RUN: `seed 65 12h widths noevolved islands then experiment
footprint.py --fastest --sample 16 --sizes 100,10000 --rounds 3 then experiment review-checks.py spread` - the islands
trial the escape note planned (435): four islands of 64, migrants every 10 generations; no comparison step, so about
11.5 hours of evolution. Its reading: at processing against seed 64 at generation 146, seed 64's database kept in this
container (build/evolve/keep/, untracked - if it is gone, seed 64's chain archive is wanted); and the chain's spread step
over every run's database at their common generation (seed 63's 90). Predicted; 443's prediction for seed 65 withdrawn.

Files: lab/evolve/NEXT-RUN, results/predictions.md, HANDOFF.md.

## Iteration 445 - 2026-10-21 - Claude

**The fast gate reviewed while seed 65 runs** (results/drafts/fastgate-review-445.md; rule 3 said revisit). Seed 64's
database: 1,174 children measured twice under the gate, second / first median 1.000 (51% slower the second time) - no
regression between the two in-run readings; but the front's fastest tenth, re-measured after the run, about 1.10 of
both. The optimism is shared luck, not single-reading noise: the gate measures again at once, back to back, in the same
moment - co-runners, clock, caches - so a design that met a kind moment meets it twice. Proposed: the second reading
deferred to the next generation's batch, the speed their geometric mean then - the same cost, no new threshold; a
patch after seed 65, the owner's call.

Files: results/drafts/fastgate-review-445.md (new); results/README.md, HANDOFF.md.

## Iteration 446 - 2026-10-21 - Claude

**The after-seed-65 batch: the fast gate's second reading deferred; the rtfuse simplification not prepared - it would
have hidden a fault** (the owner: prepare both). evolve.py: a child under the gate is marked, not measured again at
once; the next generation's batch measures it again among other co-runners, its 64-bit speed then the geometric mean of
the two readings (its 32-bit reading the first), the record saved again. Tested in a clone (its stages built): a short
evolution with the gate on the 4th fastest - 12 deferred readings applied, the run to its end
(results/drafts/fastgate-defer-446.log). batch-checked below.

The rtfuse simplification (rule 9: rtimm=2 to pass --rtfuse only with rtfuse on), checked before building: --rtfuse
also writes I+'s entry in the fuser's table, and I+ fuses only where the fuser is built. On seed 64's front, profiled:
a plain design with the fuser, loop's dispatches -20.0% with rtiplus; a plain design without, +0.0% - rtiplus expressed
and inert. 37 of the front's 55 designs with rtiplus have no fuser (30 tag-2 JIT designs, where loops are translated
anyway; 7 plain). Rule 7's 33% counts expression, not effect. Not prepared; proposed instead: rtiplus to bring the fuser
with it - the owner's call.

Files: results/applied-after-seed65/ORDER.md, results/applied-after-seed65/fastgate-defer-after-seed65.patch, results/drafts/fastgate-defer-446.log
(new); results/README.md, HANDOFF.md.

## Iteration 447 - 2026-10-21 - Claude

**I+ brings the run-time fuser - patch 2 of the after-seed-65 batch** (the owner: Continue, to preparing it). I+ is
found by the fuser's lookup in its table (forth/cv8-fuse.4's SUPER-OP, the converter writing its entry under --rtfuse):
rtiplus without the fuser was expressed and inert - 37 of seed 64's 55 front designs with it. evolve.py: overlay() and
the --rtfuse switch follow rtiplus_on() too; rtimm_lean() no longer takes an I+ design (cv8-imm.4 has no table). Tested
in a clone (its stages built): seed 64's 72a4f14f1a, plain - loop's dispatches 16,034,434 against 20,033,944 (-20.0%),
+616 bytes, alive; 46b699252e, tag-2 with the JIT - +336 bytes, alive. Like rtimm=2 today, a design with rtiplus now
fuses its built pairs and tests at run time too. The two patches batch-checked together on 42d4323: run-tests PASS,
validate 7 of 7 IDENTICAL, jail PASS. Seed 66 predicted.

Files: results/applied-after-seed65/iplus-fuser-after-seed65.patch (new); results/applied-after-seed65/ORDER.md, results/predictions.md,
results/README.md, HANDOFF.md.

## Iteration 448 - 2026-10-21 - Claude

**Rule 7 counts I+ that works** (while seed 65 runs). review-checks.py rules: the I+ line now counts the designs with
rtiplus and, of them, those built with the run-time fuser I+ needs (overlay(), as the build decides) - the share of the
front working. Seed 64, again: 55 with rtiplus, 18 working - 11% of the front, not the 33% reported at 443. The check
runs at a seed's processing before its batch is applied, so seed 65's reading is its own code's.

Files: lab/evolve/review-checks.py, HANDOFF.md.

## Iteration 449 - 2026-10-22 - Claude

**Seed 65 processed: the islands trial worth keeping by its measure; the smallest design of any run; the after-seed-65
batch applied** (results/evolve-amd-ryzen-7-pro-8840hs-seed65.md). `seed 65 12h widths noevolved islands then experiment
footprint.py ... then experiment review-checks.py spread` at e81eec6ff (Iteration 444): 50,281 designs in 11 h 16 min,
generations 0-196, none died. Against seed 64 (no islands) at generation 146, seed 64's database kept here: fastest
0.1168 against 0.1253 (6.8% ahead), smallest 14,005 against 14,047, hypervolume +1.6%, best Q -4.2%; 32 bits 8.0% behind.
At generation 90, by the chain's spread over seeds 61-65: level with seed 64 at the fast end, the best hypervolume of
the five. The fast end kept gaining to generation 124 (seed 64: 36). By its end: fastest 0.115, smallest 13,959 bytes.
Predictions 444: 3 right - by the escape note's measure islands are worth keeping; one run against one, so seed 66 runs
them again.

Its front: 179, the JIT on 93; heldout 0.985, regret +1.5%; fast-end optimism 1.115; no 32-bit failure; rule 7 - I+ working
on 6% (27 with rtiplus, 10 with the fuser). The footprint check: the 16 fastest's order 0.531 at 100 words, 0.550 at
10,000 - no worse on large programs. The Tegra measured 7 - only 3 of seed 64's front are GCC without the JIT. The gene
votes' first candidates over seeds 63-65: skippad, fold, sharedcall, tail, kstack, tailpn. The after-seed-65 batch
(the deferred gate reading, I+ with its fuser): batch-check PASS on 82ff3fe, applied. NEXT-RUN: seed 66, islands again,
12 hours.

## Iteration 450 - 2026-10-22 - Claude

**The gene votes' first freeze** (the owner: prepare that freeze and continue). sharedcall, tail, kstack and tailpn
frozen off (FROZEN) for seed 66 - reversible, the code kept; review-checks.py votes now counts only the front's own
encoding's genes: skippad and fold, the other two candidates, belong to sod16 and cpt16 and were voted on CV8 fronts they
cannot reach. batch-check on a763d7f PASS; applied as the after-seed-65 batch's patch 3. Predicted for seed 66: no loss
against seed 65 by the chain's spread.

On the new master: the build, run-tests PASS, validate 7 of 7 IDENTICAL, the gate 179 of 179 alive, ans-check 0 of 46
differ (its negative control caught), the jail PASS - run alone: the first chain stopped after validate when the
freeze's batch-check ran its own jail test beside it - the jail test here takes the user's other processes with it, so
the routine now says it runs last and alone.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed65.md, results/xcheck-seed65.md (new); results/applied-after-seed65/
(two patches and the freeze); lab/evolve/evolve.py, lab/evolve/review-checks.py and the batch's files; lab/evolve/NEXT-RUN,
results/gene-votes.md, results/predictions.md, results/progress-by-run.md, results/README.md, HANDOFF.md.

## Iteration 451 - 2026-10-22 - Claude

**The inert-gene scan** (the owner: proceed; results/drafts/inert-scan-451.md, results/drafts/inert-scan-451.py), while
seed 66 runs. Four of seed 65's front designs - the fastest, the fastest without the JIT, the best by Q, the smallest -
each expressed gene turned off in turn: binary + image bytes, and the profiler's dispatch counts on kernel, loop, fib.
**jitloop is inert in both JIT designs**: not a byte, not a dispatch; -DJITLOOP is read nowhere in the engine now, and
its converter stencils changed nothing in these images. It rides on all 93 JIT designs of the front, so the gene votes
- which count presence - could never make it a candidate: the scan sees what they cannot. Inert in one design or two:
tfind, swapi, dskew, alignfn, gotodup, opinline, noinls, fbuf. tos inert in the plain fastest (ab16f60a0c), unexpected -
tos picks the cached engine's source - to be looked at. Proposed: jitloop confirmed on more JIT designs then frozen off;
tos looked into; the scan run beside the votes at each processing - the owner's calls.

Files: results/drafts/inert-scan-451.md, results/drafts/inert-scan-451.py (new); results/README.md, HANDOFF.md.

## Iteration 452 - 2026-10-22 - Claude

**The scan's two findings checked - both false; the scan corrected and run again** (the owner: confirm jitloop, look at
tos). tos in the plain fastest: two different engines with it on and off (their hashes differ), 22,600 bytes each - equal
sizes, not an unchanged build; TOS caching changes how each operation runs, not how many. jitloop in the fastest JIT
design: bubble's dispatches 137,056 with it, 7,911,665 without (corpus -1.0%) - it gives the JIT (+LOOP) and (?DO), which
kernel, loop and fib, the first pass's three workloads, do not use; -DJITLOOP itself is read by no code, the converter's
stencils are the gene. The scan now profiles all seven workloads and calls a gene inert only when the build is the same,
engine and image hashed: on the same four designs **no gene is inert across designs** - alignfn (two designs), gotodup
and fbuf (one each) build the same with it off; the rest work, or build differently with no dispatch effect (compiler
flags, data layout, the JIT's native code - timing's to judge). The jitloop freeze withdrawn; the corrected scan proposed
beside the votes at each processing.

Files: results/drafts/inert-scan-451.md, results/drafts/inert-scan-451.py; results/README.md, HANDOFF.md.

## Iteration 453 - 2026-10-22 - Claude

**Seed 67 at 10 hours** (the owner: the next run, 10 hours - seed 66 already running at 12). Recorded in HANDOFF and as a
comment in NEXT-RUN, whose active line stays seed 66's; seed 67's line is written at seed 66's processing, with islands
if seed 66 confirms them. At 10 hours with no comparison step, about 9.5 hours of evolution - past generation 146, so the
islands reading against seed 64 still holds.

Files: lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 454 - 2026-10-22 - Claude

**Seed 66 processed: islands confirmed - the default from seed 67; the first freeze showed no loss**
(results/evolve-amd-ryzen-7-pro-8840hs-seed66.md). `seed 66 12h widths noevolved islands then experiment ...` at 94e6742bb
(Iteration 450): 45,676 designs in 11 h 16 min, generations 0-178, none died. Against seed 64 at generation 146: fastest
0.1208 against 0.1253 (3.6% ahead; seed 65: 6.8%), smallest 14,045 against 14,047, hypervolume +1.8%, 32 bits level - both
islands runs met the trial's conditions. The freeze against seed 65 at generation 90 (the chain's spread over seeds 62-66):
fastest 0.1286 against 0.1288, smallest +0.1% - no loss. By its end: fastest 0.121, smallest 14,037. heldout 0.985, regret
+1.4%; I+ with its fuser on all 39 front designs carrying it, 38 of the 85 plain ones. The fast end's optimism 1.110 - the
deferred gate reading did not lower it. The footprint check: the 16 fastest's order 0.524 at 100 words, 0.206 at 10,000.
The gene votes' next candidates over seeds 64-66: alignhot, jithelp, jitre. Predictions: 5 right, 1 wrong (the optimism).
On master: the build, run-tests PASS, validate 7 of 7 IDENTICAL, the gate 149 of 149, ans-check 0 of 38 (its negative
control caught), the jail PASS, alone. NEXT-RUN: seed 67, 10 hours (the owner), islands.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed66.md, results/xcheck-seed66.md (new); results/gene-votes.md,
results/predictions.md, results/progress-by-run.md, results/README.md, lab/evolve/NEXT-RUN, HANDOFF.md.

## Iteration 455 - 2026-10-22 - Claude

**The owner's three answers: the frozen four's code to go; the second freeze; the load tested.**

(a) The code removal: sharedcall's path cannot go - CV8's base genome sets sharedcall, so the hand-made s5 and s6 use the
shared call path, and s6 is the reference every speed is measured against; only its gene goes. tail's and tailpn's
engines (gen-tail.py, build_tail and the rest) and kstack's go - prepared as the after-seed-67 batch, so seed 67 is not
mixed with it. (b) alignhot, jithelp and jitre frozen off (12 of 12 over seeds 64-66): batch-check on cb2e94d PASS -
run-tests, validate 7 of 7 IDENTICAL, the jail - applied before seed 67 (results/applied-after-seed66/). (c) The load:
lab/evolve/loadtest.py - the newest database's front, its K fastest and K slowest, each measured against s6 with
evolve.py's own measure() idle and with N other physical cores running s6 on the kernel workload, idle, loaded, idle,
loaded; per design loaded / idle, per group the median. This machine has one core, so its smoke run (the load forced onto
the same core) checked only the path - the front read, builds, measures, the load started and stopped; the test runs in
seed 67's chain on the laptop, after the footprint check. Predicted.

Files: lab/evolve/loadtest.py, results/applied-after-seed66/ (new); lab/evolve/evolve.py, lab/evolve/NEXT-RUN,
results/predictions.md, HANDOFF.md.

## Iteration 456 - 2026-10-22 - Claude

**tail, tailpn and kstack retired - the after-seed-67 batch** (the owner: remove the frozen four's code; while seed 67
runs). Removed: tools/gen-tail.py, build_tail() and tail_offenders(), the preserve_none compiler choice, the engine's
tail branch in build() (its other branch one level up), engines-check's tail paths (89 to 69), forth/kstack.4 and its
dump variants. Kept: the genes, in the genome and frozen off - canon(), express() and every design's identity read them -
and lab/evolve/GENES.md marks them retired. sharedcall's path stays: CV8's base genome sets it, so the hand-made s5 and
s6 use it, and s6 is the reference. Tested in a clone of e1285e3, its stages built: run-tests PASS (69 engine paths,
each built and its corpus right), validate 7 of 7 IDENTICAL, a short evolution 78 of 78 alive; batch-check on c69752e PASS
(run-tests, validate 7 of 7 IDENTICAL, the jail).

Files: results/applied-after-seed67/ORDER.md, results/applied-after-seed67/retire-after-seed67.patch (new); results/README.md, HANDOFF.md.

## Iteration 457 - 2026-10-22 - Claude

**Fern designed - a small scripting language compiled into Forth words** (results/drafts/fern-design-457.md). The owner
asked, while seed 67 runs, for a minimal user-friendly scripting language on this Forth at little cost against bare
Forth, and chose to build it in a chat of its own; this note is that chat's starting point: Ruby-style syntax closed by
keywords, cells as the one type, a compiler in Forth emitting colon definitions as it parses, locals in a return-stack
frame (FRAME, L@ k, L! k, UNFRAME - plain Forth first, VM primitives and genes later), no runtime type checks, no GC
(a per-script arena), no floating point; expected within 0-20% of hand-written Forth; a four-step plan, the core first.

Files: results/drafts/fern-design-457.md (new); results/README.md, HANDOFF.md.

## Iteration 458 - 2026-10-23 - Claude

**Seed 67 processed: islands ahead a third time; the load explains half the fast end's optimism; the retirement
applied** (results/evolve-amd-ryzen-7-pro-8840hs-seed67.md). `seed 67 10h widths noevolved islands then experiment
footprint.py ... then experiment loadtest.py ... then experiment review-checks.py spread` at e1285e3b1 (Iteration 455):
35,703 designs in 9 h 15 min, generations 0-139, none died. Against seed 64 at 139 (seed 67's last): fastest 0.1197
against 0.1253 (4.5% ahead), smallest 14,103 against 14,051 (+0.37%), 32 bits 2.1% ahead - islands ahead in all three of
their runs (6.8%, 3.6%, 4.5%). The second freeze against seed 66 at generation 90: fastest 0.1235 against 0.1286,
smallest +0.4% - no loss. **The load test** (loadtest.py, the owner's question): the 8 fastest 0.947 loaded / idle, the 4
slowest 0.994 - under three busy cores the fast designs measure about 5% faster against s6; about half the fast tenth's
optimism (1.083), the rest selection's luck. heldout 0.971, regret +3.0%; I+ on 25 front designs, all with the fuser; the
footprint check's 16 fastest too close to rank (0.212, -0.026). The gene votes' next candidate: jitret (12 of 12 over seeds
65-67). Predictions: 5 right, 1 wrong (the load's size).

The after-seed-67 batch - tail, tailpn and kstack retired - batch-check on d1909bb PASS, applied (results/applied-after-
seed67/). On the new master: the build, run-tests PASS (69 engine paths), validate 7 of 7 IDENTICAL, the gate 152 of 152,
ans-check 0 of 39 (its negative control caught), the jail PASS (alone). NEXT-RUN: seed 68, 8 hours (the owner), islands,
the footprint check and the spread; the load test out of the line. Open for the owner: jitret's freeze; the load's offset
- the re-measure after a run under the run's own load, or the offset written down as calibration.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed67.md, results/xcheck-seed67.md (new); results/applied-after-seed67/
(the retirement); lab/evolve/evolve.py, lab/evolve/engines-check.py, lab/evolve/GENES.md (tools/gen-tail.py and
forth/kstack.4 removed); lab/evolve/NEXT-RUN, results/gene-votes.md, results/predictions.md, results/progress-by-run.md,
results/README.md, HANDOFF.md.

## Iteration 459 - 2026-10-23 - Claude

**c4 and its family, captured** (the owner: a deep dive into EarlGray/c4 and AoiKuiyuyou/AoikC4x86Study, derived and
similar projects, and what applies; results/drafts/c4-family-459.md). The family: rswier/c4 (~500 lines, self-hosting,
a stack VM), EarlGray's i386 JIT in 86 lines, the commented study copy, write-a-C-interpreter, jserv's AMaCC (ARMv7 JIT
and ELF on c4's infrastructure), HPCguy's Squint (AMaCC's follow-on with a peephole optimiser near gcc -O1), and,
similar, jserv's shecc (ARMv7 and RV32, BSD-2). Checked against engine/jit.c: its lessons are already ours - jitk's
register cache, immediate forms, a fused compare-and-branch. The gap they point at: the JIT is x86-64 only, and the
32-bit fastest (about 0.33) sit where the 64-bit fastest without the JIT do (0.304) - about 2.6x behind the JIT's. Proposed:
the stencil JIT ported to i386 first, ARMv7 after; a JIT-redundancy probe (a JITDUMP hook and objdump) before any peephole
pass; an interpreter-in-Forth workload; for Fern, c4's frames (ENT, LEA, LEV) and structure, and its -s listing. Licences
noted: c4's line is GPL-2.0 - ideas only.

Files: results/drafts/c4-family-459.md (new); results/README.md, HANDOFF.md.

## Iteration 460 - 2026-10-23 - Claude

**The JIT at 32-bit x86: feasible, and a prototype works** (the owner: proceed with the i386 port's study;
results/drafts/jit-i386-460.md, results/drafts/jit-i386-460.patch). A JIT design's 32-bit speed has been its
interpreted speed - eval32() builds it with the JIT off, since spn-abi.h knew only x86-64 and 32-bit ARM. The
copy-and-patch method carries over: i386 takes ARM's convention - the state one 64-bit value, regparm(2) bringing it in
eax and edx and a 64-bit return leaving it there - with SPN_CC on the stencils, markers and the native call; holes a
mov $imm32 each, found and filled a cell wide (JIT_HOLEW); endbr32 skipped. A real bug on the way: a variable called from
translated code became align8(body + 5), 4 bytes off at 4-byte cells (the corpus's FILL/MOVE test, and VARIABLE V
reading garbage) - now CELL_BYTES-aligned, the same at 64 bits. s6 with the JIT's genes at 32 bits: built (19,436
bytes), the corpus to its end, its output the same as without the JIT; speed against the 32-bit s6 (one core here,
indicative) 0.956 without, 0.767 with (fib 0.772 to 0.330, ackermann 0.924 to 0.592). Proposed: eval32 keeping the JIT,
jitk off at 32 bits, engines-check and dream's 32-bit build covering it - the after-seed-68 batch, the owner's call.

Files: results/drafts/jit-i386-460.md, results/drafts/jit-i386-460.patch (new); results/README.md, HANDOFF.md.

## Iteration 461 - 2026-10-23 - Claude

**The JIT at 32-bit x86 made real - the after-seed-68 batch** (the owner: proceed with steps 1-4). Patch 1, the engine:
Iteration 460's prototype as is. Patch 2, the lab: eval32() builds the design as it is - its JIT kept, where since
Iteration 336 it was switched off - and the build drops jitk at 32 bits (w32(): gen-jitk.py's stencils name x86-64's
registers); xcheck.py's prebuilt 32-bit sample (dream) takes JIT designs, while a host building itself at 4-byte cells
(the Tegra) still takes none; engines-check builds the JIT's variants at 32 bits (69 paths to 81). Tested in a clone with
both: run-tests PASS, validate 7 of 7 IDENTICAL; seed 67's front - its three fastest JIT designs and two from its middle
- at 32 bits with their JIT 0.35 to 0.52 of their JIT-off times (1.9 to 2.9 times faster; jitk not yet ported). One
thing this machine could not show: eval32()'s harness says "died: corpus" here for evolved 32-bit designs, with master's
code too, while the same build runs the corpus to its end directly - this machine's, to watch at seed 69 (fail32).
batch-check on e6044c3 PASS (run-tests, validate 7 of 7 IDENTICAL, the jail). Predicted for seed 69. A break in the 32-bit
column from seed 69, noted in the batch.

Files: results/applied-after-seed68/ORDER.md, results/applied-after-seed68/jit-i386-engine-after-seed68.patch,
results/applied-after-seed68/jit-i386-lab-after-seed68.patch (new); results/README.md, results/predictions.md, HANDOFF.md.

## Iteration 462 - 2026-10-23 - Claude

**c4's circle, the second pass** (the owner: a deeper search for pages, posts and projects referencing c4, c4x86 and
the rest; results/drafts/c4-family-459.md, its new sections). More of the circle: the 2014 Hacker News thread, srhuang's
HackMD trace, rswier's own c5 (c4 with a syntax tree, one commit), comzyh's commented branch, minizig, Kray-G/kcs. The
find that matters is the literature our JIT belongs to: Ertl and Paysan's "Code-Copying Compilation in Production"
(EuroForth 2025) - Gforth copying GCC's snippets since 2003, its hurdles and fixes; their IP-update paper (ECOOP 2024);
Ertl and Gregg's PACT 2004 copy-and-patch prototype; Xu and Kjolstad's copy-and-patch (OOPSLA 2021), CPython's JIT
(PEP 744) and Deegen. Checked against our code: the JIT, jitk, tailnext, nocet and align1 are already theirs; no
-fno-tree-vectorize gene; jitinl one operation only; jit_rp in memory. Six ideas proposed - a stencil relocatability
check, stencils from relocations (for ARM), jitrp, wider jitinl, a no-vectorise gene, the Forth application benchmarks
as held-out workloads - the owner's calls.

Files: results/drafts/c4-family-459.md; results/README.md, HANDOFF.md.

## Iteration 463 - 2026-10-23 - Claude

**The stencils checked safe to copy - patch 3 of the after-seed-68 batch** (the owner: proceed with the second pass's
first idea, Gforth's relocatability rule). lab/evolve/stencil-check.py compiles engine/spn-stencils.c alone and reads it
with objdump: in the part the JIT copies (to the last jump to NEXT or JUMP; EXIT's to its ret), any relocation to
anything but a marker, or any branch past the copied part, fails it. Its first form read relocations only - and passed
-fstack-protector-all's stencils on the wrong ground (their __stack_chk_fail calls sit past the copied part); the real
hazard is the jne inside the copied part to that cold block, which the exact form now reports. Today's flags: 43
stencils, every one safe, at 64 and at 32 bits; -fstack-protector-all: all 43 unsafe (a jne past the copied part);
-pg: all 43 (mcount). Instructive: the JIT built with the stack protector still ran the corpus and ran fast (fib 0.341
against 0.324) - the jump out was latent, never taken while no canary failed. engines-check runs stencil-check at 64 and
32 bits; engine/jit.c also refuses at run time a stencil whose 32-bit call or jump leaves it for the engine image (E8,
E9, 0F 8x; FF 15 / FF 25 on x86-64) - slower, never wrong; a short jump it cannot see, which is why the tests run the
exact check. Tested in a clone with patches 1 and 2: run-tests PASS, validate 7 of 7 IDENTICAL; the three patches
batch-checked together on 687a0e2: run-tests PASS, validate 7 of 7 IDENTICAL, the jail PASS.

Files: lab/evolve/stencil-check.py (new, in the patch); results/applied-after-seed68/stencil-check-after-seed68.patch,
results/applied-after-seed68/ORDER.md; results/README.md, HANDOFF.md.

## Iteration 464 - 2026-10-23 - Claude

**Seed 68 processed - and islands never ran, in it or in seeds 65-67** (results/evolve-amd-ryzen-7-pro-8840hs-seed68.md).
`seed 68 8h widths noevolved islands ...` at b75372ada (Iteration 458): 28,007 designs in 7 h 23 min, generations
0-109, none died. Its evolve.log holds 109 "generation N:" lines and no ", island " line - and so do seeds 65-67's (196,
178, 139), read from their chain archives. next-run.sh parsed "islands", then detached, re-running itself with the
parsed words in the environment - NEXT_RUN_NOEVOLVED, NEXT_RUN_WIDTHS - and no NEXT_RUN_ISLANDS: the detached chain
called evolve.py without --islands. Fixed: ISLANDS=${NEXT_RUN_ISLANDS:-} and the carrier on both re-runs; the chain's
run line and its "the run" step now name islands; seed-facts.py reports "islands: on/off" from the log. The islands
"trial" voided - its predictions and HANDOFF's "islands the default" withdrawn: seeds 64-68 are five plain replicates
(the chain's spread at generation 109: fastest 0.1197-0.1298, smallest 14,039-14,207), seed 64, the trial's yardstick,
at their slow end. Seed 68 itself: fastest 0.130, smallest 14,207; heldout 0.967, regret +5.9%; optimism 1.075; no
32-bit failure; I+ 26% working; the votes' new candidates rtfuse and jitos. Seed 69 (12 hours, the owner): the real
islands trial; the after-seed-68 batch deferred to its processing (one change at a time). The usual checks on master
were not rerun: since b75372ada the engine and the evolver are unchanged (only notes, next-run.sh and seed-facts.py) -
the seed pack's own (tests, validate, jail) stand.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed68.md, results/xcheck-seed68.md (new); lab/evolve/next-run.sh,
lab/evolve/seed-facts.py, lab/evolve/NEXT-RUN, results/gene-votes.md, results/predictions.md, results/applied-after-seed68/ORDER.md,
results/progress-by-run.md, results/README.md, HANDOFF.md.

## Iteration 465 - 2026-10-23 - Claude

**jitrp, the JIT's return-stack pointer in a register - a prototype** (the owner: proceed; results/drafts/jitrp-465.md,
results/drafts/jitrp-465.patch). While native code runs the pointer lived in jit_rp, in memory, reached through the
IMM_RP hole; with JITRP it lives in r15 - a global register variable in the stencils' file and in the engine's (declared
before every function), the eleven return-stack stencils using it, the native call handing it over in it,
gen-jitk.py's I variant through RP_VALUE(). Each of those stencils three instructions shorter (st_loop 14 to 11, st_i 10
to 7). This machine's timing swung 10-20% - valgrind installed, and cachegrind's exact instruction counts used instead:
s6 with the JIT -0.2% to -0.4% (its return-stack stencils seldom native); seed 68's fastest GCC JIT design, 6c0c4e6886,
loop -19.9%, bubble -4.5%, ackermann +2.1% (most likely the interpreter's lost register). Clang refuses the register
variable - GCC only; regpin 3 takes r15 - another register there. Both builds pass the corpus. Five steps to a gene
proposed, after the 32-bit JIT batch's run.

Files: results/drafts/jitrp-465.md, results/drafts/jitrp-465.patch (new); results/README.md, HANDOFF.md.

## Iteration 466 - 2026-10-23 - Claude

**Real Forth applications as held-out workloads - what exists, what runs** (the owner: proceed;
results/drafts/appbench-466.md). The suite is Appbench (Ertl and Paysan: benchgc, brainless, fcp, cd16sim, CoreMark,
lexex); a 2026 paper that ran it beside 18 Shootout kernels (RPyForth, arXiv 2609.23759) counted why it matters -
stack depth at the 95th percentile 14.5 cells against 4, 22.7 calls per 1,000 primitives against 0.004 - and saw the
systems rank differently on the two suites. Appbench (complang.tuwien.ac.at) and the Shootout's Forth programs are not
reachable from this machine; Gforth's own benchmarks are (its GPL-3 repository on GitHub). On s6, siev.fs, bubble.fs and
matrix.fs run to their ends with the source upper-cased (our words are upper case) and a three-line prelude - our kernel
has no NIP and no .( (CORE EXT); fib.fs needs [IF] and floats. No copy of anyone's program put in the repository.
Proposed: the owner downloads Appbench on the laptop; a held-out tier of applications in heldout.py, each with an output
check; NIP, .( and [IF] by prelude or in the kernel.

Files: results/drafts/appbench-466.md (new); results/README.md, HANDOFF.md.

## Iteration 467 - 2026-10-23 - Claude

**Appbench on our Forth - three applications run, checked** (the owner: the zip uploaded, continue;
results/drafts/appbench-467.md, results/drafts/appbench/). Terms: brainless public domain; benchgc, lexex, brew GPL;
fcp and cd16sim no notice - so no program is copied into the repository; run.py reads the zip in place. s6 lacks 61 of
140 commonly used standard words - and our own extend.4 and coreext.4 define nearly all of them (prelude.fth loads them,
then a few stubs); its lookup is case-sensitive, so fold.py upper-cases the programs' source, keeping strings,
comments, file and character names. On s6: fcp 6.8 s (120,287 nodes), brainless 4.1 s (110,023 nodes, 163,278
evaluations), cd16sim 6.5 s (its own "should be" line equal) - all three checks PASS. lexex and benchgc stop on names
built or read at run time in lower case, which no folding of the source reaches; brew not tried. Proposed: a held-out
tier of fcp, brainless and cd16sim; a case-insensitive FIND; coreext's words in the default image.

Files: results/drafts/appbench-467.md, results/drafts/appbench/fold.py, prelude.fth, run.py (new); results/README.md,
HANDOFF.md.

## Iteration 468 - 2026-10-23 - Claude

**Applications held out - the tool, and the evolved lead does not travel** (the owner: 1. run more applications, 2. a
case-insensitive gene, with concerns, 3. would coreext's words in the image grow the size?;
results/drafts/appbench-468.md). lab/evolve/appbench.py: N designs across the newest front built and run on fcp,
brainless and cd16sim against s6 (the owner's zip read in place; the folding and prelude moved to lab/evolve/appbench/),
each output checked, the child's CPU time, Spearman against the in-run speed. Tried on three of seed 68's front, one
round: all outputs right, the order kept - and the lead gone: b9c5b4ae74, 0.140 on the selection's workloads, runs the
applications at 1.028 of s6 (fcp 0.887, brainless 1.041, cd16sim 1.176); 76bfbf6558 (0.364) at 1.145; 57a20bf148
(1.605) at 1.743. Loading is not it: the prelude and the program's compilation take 0.01-0.06 s of 4-7 s runs (fcp alone:
s6 6.71 s, b9c5b4ae74 5.87 s; brainless alone: 3.84 s and 4.45 s). Proposed: appbench.py in the chain; why the JIT's lead
vanishes (JITLOG's refusals); applications in the selection - the owner's decision. The case-insensitive gene: planned,
not built - it touches every lookup path (FIND, HEADER, and the C-assisted kfast, klookup, tfind). coreext in the image:
not proposed - the measured size stays the base image's; applications load it themselves.

Files: lab/evolve/appbench.py, lab/evolve/appbench/fold.py, lab/evolve/appbench/prelude.fth,
results/drafts/appbench-468.md (new); lab/evolve/README.md, results/README.md, HANDOFF.md.

## Iteration 469 - 2026-10-23 - Claude

**Our own application, written from scratch - sim16; and the zip's place** (the owner: appbench.zip in ~/Downloads; for
the code that cannot be copied, borrow the idea and write anew). Ideas are free to use, a program's text is not, so each
is written independently as a program of the same kind; brainless is public domain and needs none of this.
lab/evolve/apps/sim16.fth: a 16-bit stack CPU simulated in Forth (operation and ALU tables of execution tokens), its own
structured assembler, and two programs in its machine code - a sieve on 2000 flags, a recursive fib(20). Core words,
upper case - no prelude, no folding; `60 BENCH` checks itself (SIEVE 303, FIB 6765, 21,936,820 steps), 3.3 s on s6.
appbench.py runs it by default, without the zip; on three of seed 68's front its outputs right and the fast design at
0.680 of s6 (fcp 0.856). Seed 70's line will add the appbench step with ~/Downloads/appbench.zip (noted in NEXT-RUN).

Files: lab/evolve/apps/sim16.fth (new); lab/evolve/appbench.py, lab/evolve/NEXT-RUN, results/drafts/appbench-468.md,
HANDOFF.md.

## Iteration 470 - 2026-10-23 - Claude

**Three more applications of our own, from scratch - gc16, scan, evo** (the owner: add all three;
results/drafts/appbench-468.md, its Iteration 470 section). gc16.fth: 20,000 cons cells, mark and sweep, tagged roots
and a collector-visible stack so nothing live is lost mid-build, a mutator replacing random roots with random lists and
trees (GCS 618, FREED 7,454,729, CHECK 2636; 2.8 s on s6). scan.fth: 14 token patterns as postfix regular expressions,
Thompson's NFA, the subset construction over byte-array sets, a longest-match scanner over 20 KB of generated program
text (NFA 44, DFA 17, IDENT 1723, NUMBER 908, SPACE 5407, no errors, CHECK 20235; 2.9 s) - its scanner word renamed off
the kernel's SCAN. evo.fth: 64 genomes of 64 bytes toward a hidden target - popcount fitness, tournaments, one-point
crossover, mutation, elitism (BEST 445 AT 200, CHECK 24466; 2.7 s) - one bug on the way: I read inside a DO loop with an
address pushed on the return stack above the loop's own. Each checks its own result; checksums under 65,521, a 31-bit
LCG, so 32-bit builds agree. appbench.py's default: the four of ours and Appbench's three. On three of seed 68's
front: every output right; the fast design at 0.566 of s6 on ours (sim16 0.595, gc16 0.461, scan 0.627, evo 0.596).

Files: lab/evolve/apps/gc16.fth, lab/evolve/apps/scan.fth, lab/evolve/apps/evo.fth (new); lab/evolve/appbench.py,
results/drafts/appbench-468.md, HANDOFF.md.

## Iteration 471 - 2026-10-23 - Claude

**What the JIT leaves on the applications, and why** (the owner: the coverage study; results/drafts/jitapps-471.md,
lab/evolve/jitapps.py). jitapps.py: the design profiled with the JIT off and on (-DJITLOG=1) over the seven
applications - dispatches left, the words they sit in (the image's by the call map, the application's by the JIT's log
of every word it decided), each refusal followed to its root. The analysis-only log (engine/jit.c, JITLOG builds only)
now tells "too long" apart (why 6) and gives the operation without stencils as jit_ops[]'s index; jitleft.py reads either
form. On seed 68's b9c5b4ae74 (0.140 on the selection's workloads) the JIT leaves 49% of sim16's dispatches, 37% of
gc16's, 93% of scan's, 83% of evo's, 72% of fcp's, 94% of brainless's, 87% of cd16sim's. Roots: operations without
stencils - by a probe, the double-cell multiply and divide under *, MOD, /, /MOD, */ and CELLS (ops 27, 28), and op 70
not yet named - and EXECUTE's dispatch (the return stack's order: sim16's STEP, cd16sim's deferred words, VALUE's
words); one missing stencil keeps a whole word and its callers interpreted. Proposed: those stencils, EXECUTE native,
op 70 named, JIT_MAXOPS - the owner's calls. The stages rebuilt for the changed JIT source; production builds unchanged.

Files: lab/evolve/jitapps.py, results/drafts/jitapps-471.md (new); engine/jit.c (JITLOG only), lab/evolve/jitleft.py,
lab/evolve/README.md, results/README.md, HANDOFF.md.

## Iteration 472 - 2026-10-23 - Claude

**The operations named; jitmul built, tested and staged frozen off** (the owner: genes for the multiply and divide and for EXECUTE; name and cover the rest; measure). layout.py lists the operations without stencils in vm-jit-ops.h: on seed 68's fast design op 27 UM*, 28 UM/MOD, 32 SP@, 70 DODOES, 118 COUNT, 119 ALIGNED. jitmul: UM* a stencil of its own, COUNT from stencils there are; UM/MOD written (one divide) but unmapped - the interpreter answers a zero divisor with -10 THROW, which a stencil cannot do yet. On the way: a bit-by-bit UM/MOD ran past the JIT's 160-byte scan window (SIGILL in the corpus); a comment holding */ closed early. s6 with the JIT and jitmul passes the corpus and matches the interpreter on an arithmetic test. engines-check has the variant; jitapps.py takes --set. jitmul in FROZEN: the owner's to unfreeze. Next: a throw path for UM/MOD, jitdoes (DODOES), jitexec (EXECUTE), then measure.

## Iteration 473 - 2026-10-23 - Claude

**jitdoes built and staged; the first measure of the new genes** (the owner: proceed; results/drafts/jitapps-471.md,
its Iteration 473 section). The 472 records completed first (the coverage note's section, HANDOFF's paragraph).
jitdoes: in jit_body, a DOES> child's first operation, DODOES, becomes a literal of its PFA and the decoding continues in
its DOES> code after the leading R>, to its EXIT - the return stack never touched; layout.py gives the JIT DODOES's and
R>'s one-byte codes; evolve.py the gene (with jitx), its flag, frozen off with jitmul; engines-check the variant. s6 with
the JIT and jitdoes (and with jitmul too) passes the corpus and matches the interpreter on a DOES> test. jitapps.py on
seed 68's b9c5b4ae74 with both: the dispatches the JIT leaves - scan 92.8% to 3.8% (UM* native frees CELLS), gc16 36.7%
to 32.6%, evo 82.6% to 68.3%, sim16, fcp, brainless and cd16sim unchanged. jitdoes reaches nothing there yet: those
programs' DOES> children are reached as callees, without the JIT header a word has. Next: a DOES> child at its call,
UM/MOD's throw path, EXECUTE.

Files: engine/jit.c, tools/layout.py, lab/evolve/evolve.py, lab/evolve/engines-check.py,
results/drafts/jitapps-471.md, HANDOFF.md.

**Later in 473**: a DOES> child is reached as a headerless callee (translated once by jit_kslot, its decode starting at
the child), so jitdoes takes it there too: on b9c5b4ae74 with both genes the JIT leaves fcp 53.9% (was 71.9%), brainless
57.2% (93.8%), cd16sim 65.9% (86.5%). appbench.py takes --ids and --set; on b9c5b4ae74 with both genes our four
applications are right and scan runs at 0.150 of s6 (0.687 before) - but fcp, brainless and cd16sim give wrong results;
with jitmul alone all three are right (fcp 0.805, brainless 0.965, cd16sim 1.190). So jitmul is checked on all seven,
and jitdoes has a fault the corpus and the small DOES> test miss: frozen, not to be unfrozen until found - suspects in
results/drafts/jitapps-471.md.

## Iteration 474 - 2026-10-23 - Claude

**jitdoes's fault found and fixed; jitmul enabled; with both, the applications at twice s6's speed** (the owner: enable
jitmul, proceed with the open items; results/drafts/jitapps-471.md, its Iteration 474 section). A bisection over the
children translated (a temporary knob, environ read by hand - no C library in an engine) put the fault at the first:
jit_body's return-stack check read jit_ops[] at the code of jitdoes's PFA literal (0xFFFD), the first literal at that
stage - an out-of-bounds read, garbage on s6, a crash on seed 68's fast design. Fixed: the check skips 0xFFFD and above.
On b9c5b4ae74 with jitmul and jitdoes every output right: sim16 0.611, gc16 0.501, scan 0.189, evo 0.511, fcp 0.632,
brainless 0.636, cd16sim 0.729 of s6 - geometric mean 0.508 (0.747 before). run-tests PASS (71 paths), validate 7 of 7,
the jail PASS (alone); the pending 32-bit JIT batch still applies. jitmul out of FROZEN (the owner) - seed 70 carries it
with that batch; jitdoes frozen until the owner says. UM/MOD's throw path designed (a setjmp helper at native entry, a
function-address hole in the stencil) and jitexec outlined - next. Predicted for seed 70.

Files: engine/jit.c, lab/evolve/evolve.py, results/drafts/jitapps-471.md, results/predictions.md, HANDOFF.md.

## Iteration 475 - 2026-10-23 - Claude

**jitdoes enabled; UM/MOD native through a throw path; the applications at 2.4 times s6** (the owner: enable jitdoes,
proceed with the open items; results/drafts/jitapps-471.md, its Iteration 475 section). The interpreter enters native
code through jit_call (__builtin_setjmp, as jit_interp); UM/MOD's stencil at a zero divisor calls jit_throw0 through a
new hole (SPN_TH_VALUE), which longjmps back; the interpreter does as L_umdiv - -10, THROW. A call, so a jump to NEXT
follows it and it is copied. Without the hole (32-bit x86 for now) the stencil is a trap with no exit: never used.
UM/MOD mapped under jitmul. Tests: both signs, star-slash, an overflowing UM/MOD, division by zero caught and uncaught -
s6 with the JIT and both genes as the interpreter, line for line; the fast design with them as without. On b9c5b4ae74 with
jitmul and jitdoes, every output right: evo 0.287 of s6 (0.511 at 474), fcp 0.509, gc16 0.408 - geometric mean 0.416
(0.747 before the genes). jitdoes out of FROZEN. run-tests PASS (71 paths), validate 7 of 7, the jail PASS (alone). The
pending 32-bit batch did not apply on top any more (two conflicts in jit.c, the holes' width and the new hole): rebased
in order, the conflicts resolved, all three applying to cc7a93e. jitexec designed, next. Predicted for seed 70.

Files: engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py, lab/evolve/evolve.py,
results/pending/ (the three patches rebased, ORDER.md), results/drafts/jitapps-471.md, results/predictions.md, HANDOFF.md.

## Iteration 476 - 2026-10-23 - Claude

**jitexec - EXECUTE through a helper; staged frozen** (the owner: proceed; results/drafts/jitapps-471.md, its Iteration
476 section). The kernel's EXECUTE is `: EXECUTE >R ;`, which native code cannot follow. A call of a word whose body is
>R then EXIT becomes a row of its own (layout.py --jitexec, JIT_L_EXECUTE), whose stencil calls jit_exec through a new
hole (SPN_EX_VALUE): native when the token's word is, translated now when it can be, else interpreted through jitre's
sentinel and longjmp (built for jitexec too; jit_interp restores the throw path's return point after). Tests - EXECUTE
of native words, a DOES> child, primitives, through tables and loops, of EXECUTE itself, a THROW through it caught by
CATCH - as the interpreter on s6 (corpus passed) and on the fast design. run-tests PASS, validate 7 of 7, the jail PASS;
engines-check's variant added. On b9c5b4ae74 with all three genes: sim16 0.195 of s6 (0.531), brainless 0.359 (0.603),
geometric mean 0.347 (0.416) - but fcp 0.675 (0.509): an untranslatable token now costs a trip through the interpreter.
Frozen until the owner says. The pending batch rebased again (a clean three-way merge).

Files: engine/jit.c, engine/spn-stencils.c, engine/vm-lab.c, tools/layout.py, lab/evolve/evolve.py,
lab/evolve/engines-check.py, results/pending/ (rebased), results/drafts/jitapps-471.md, HANDOFF.md.

## Iteration 477 - 2026-10-23 - Claude

**jitexec enabled** (the owner) - out of FROZEN; seed 70's search has jitmul, jitdoes and jitexec, with the 32-bit JIT
batch applied at seed 69's processing and the appbench step in its chain. The caveat recorded: the selection's
workloads never EXECUTE, so the search cannot weigh it; fcp runs a third slower with it on the fast design (an
untranslatable token's trip through the interpreter). Predicted for seed 70.

Files: lab/evolve/evolve.py, results/drafts/jitapps-471.md, results/predictions.md, HANDOFF.md.

## Iteration 478 - 2026-10-23 - Claude

**Another model's list of projects, verified and weighed** (results/drafts/more-projects-478.md). All nine repositories
exist; their READMEs read here. Most of what they hold CV8, SPN and the JIT already have (variable-length literals and
calls, frequency-assigned operations, hot calls, native code at definition time). New to us: nibbleforth's
whole-program factoring of repeated sequences into words and inlining of single-use words - two size genes proposed -
and astil_forth's register allocation and native code saved with the image, for later. The list did not weigh the
applications finding: the largest open lever is still speed on real programs.

Files: results/drafts/more-projects-478.md (new); results/README.md, HANDOFF.md.

## Iteration 479 - 2026-10-23 - Claude

**A prompt for other models, to find more projects and ideas** (the owner; results/drafts/scout-prompt-479.md): the
project and its constraints, the applications finding that prompts the search, seven areas wanted, everything already
reviewed (so it is not suggested again), and an answer format - each item with its URL, the idea, the area, the fit to
our constraints, the expected gain and cost, its licence, and the answerer's confidence that the source exists.

Files: results/drafts/scout-prompt-479.md (new); results/README.md, HANDOFF.md.

## Iteration 480 - 2026-10-23 - Claude

**Five answers to the scouting prompt, checked, merged, weighed** (the owner; results/drafts/scout-answers-480.md). The
repositories checked on GitHub, the papers by search: most exist as described (copapy, MIT, with ARM32 among its
architectures and our very method; Mason's dual threaded and native execution - and a 2026 copy-and-patch JIT for
threaded interpreters on his profile, newer than the answers; Gregg's code-copying JIT; the R copy-and-patch JIT); four
claims do not hold (Shannon and Bailey's is stack allocation for stack machines, not a JIT's registers; no OSR in
Wasmtime; no EuroForth benchmark corpus; the MOEA Framework's author). Found on the way: Prokopski and Verbrugge's
compiler-guaranteed code-copying safety. The order proposed: an inline cache for EXECUTE (fcp's third back), native
regions with exits to the interpreter (one missing stencil costs a boundary, long words split), coverage and feature
kernels in what the selection sees (ccforth's MIT benchmarks among them). The prompt's reviewed list extended.

Files: results/drafts/scout-answers-480.md (new); results/drafts/scout-prompt-479.md, results/README.md, HANDOFF.md.

## Iterations 481-483 - 2026-10-23 - Claude

**EXECUTE's inline cache; fcp's real cause and jitcfa; jitcfa enabled** (the owner: proceed with the cache, then enable
jitcfa; results/drafts/jitapps-471.md, its 481-483 section). The cache (481): per EXECUTE site three cells in the
stencil's literal hole - the token, its native code, the four bytes after the token - a hit calls the native code
directly, a miss takes jit_exec, which fills it; right on every test; worth 0.9% of sim16's instructions (cachegrind)
and about 5% of its time. fcp's cause (482): the analysis build counting jit_exec's interpreted targets - at least five
million trips, almost all to evalLP and evalDP, refused because the JIT's return-stack check read the operations down
the page and an EXIT's arm left the depth wrong for the arm after it. jitcfa (482): the check along the paths - depths
per branch target, code after an unconditional jump or EXIT resumed from its target's depth, loops checked against
their head. Right on those shapes, on the corpus and on all seven applications; run-tests PASS (73 paths), validate 7
of 7, the jail PASS. On b9c5b4ae74 with all four genes: fcp 0.392 of s6 (0.646 without jitcfa), brainless 0.400,
cd16sim 0.577, geometric mean 0.344. The owner enabled jitcfa (483). The pending batch rebased a third time, clean.
Predicted for seed 70.

Files: engine/jit.c, engine/spn-stencils.c, tools/layout.py, lab/evolve/evolve.py, lab/evolve/engines-check.py,
results/pending/ (rebased, ORDER.md), results/drafts/jitapps-471.md, results/predictions.md, HANDOFF.md.

## Iteration 484 - 2026-10-23/24 - Claude

**Measured before partial translation; three cheap fixes first** (the owner: start partial translation;
results/drafts/jitapps-471.md, its 484 section). jitapps.py on b9c5b4ae74 with all four genes, now naming the operations
without stencils: the remainder's causes SP@ (PICK is a colon word on it - evo's, scan's, brainless's largest), ALIGNED
(fcp's), DOES> code whose R> is fused, then return-address words, words over 256 operations, a nested JIT opcode. SP@
and ALIGNED got stencils under jitmul (SP@ in the interpreter's layout, three instructions); jitdoes takes fused DOES>
code by pushing the PFA to the return stack and decoding the code whole. Right on PICK, DEPTH, SP@, ALIGNED and DOES>
children against the interpreter; run-tests PASS (73 paths), validate 7 of 7, the jail PASS. The fast design on the
applications: evo 0.234 of s6 (0.320), fcp 0.305 (0.392), brainless 0.325 (0.400) - geometric mean 0.301, 3.3 times s6.
Open: gc16 refused at DODOES with no DOES> in it. The pending batch rebased a fourth time, clean.

Files: engine/jit.c, engine/spn-stencils.c, tools/layout.py, lab/evolve/jitapps.py, results/pending/ (rebased,
ORDER.md), results/drafts/jitapps-471.md, HANDOFF.md.

## Iterations 485-486 - 2026-10-24 - Claude

**gc16's puzzle solved; inline strings and cold calls in the JIT; the applications at 3.7 times s6; a broken rebase
repaired** (the owner: continue; results/drafts/jitapps-471.md, its 485-486 section). Partial translation weighed with
the frozen jitre (an untranslatable callee called through the interpreter): the JIT's leftover fell, but the hot trips
made gc16 and cd16sim slower - transitions too dear. The refusal log (analysis builds) now shows bytes: gc16's GC was
refused at the count byte of `." HEAP FULL"` decoded as an opcode (9, DODOES). In jitexec: (S") and (.") decoded as
their string's address and length (and TYPE through the helper), the decoding resumed after the string; and calls of
cold words (output, input, ABORT, THROW - the converter's list) made through the helper instead of refusing the
caller. Right on the tests, the corpus and every application; gc16 now wholly native - 0.219 of s6 (0.434), geometric
mean 0.272. run-tests PASS, validate 7 of 7, the jail PASS. **My error, found while rebasing**: the pending engine patch
had carried an unresolved conflict in engine/vm-lab.c since the 475 rebase - the checks applied the patch (markers
apply) and looked for markers in jit.c only. Rebuilt from the original: the native call site resolved with SPN_CC,
jit.c's native calls given SPN_CC; master plus the batch passes engines-check at 64 and 32 bits.

Files: engine/jit.c, engine/spn-stencils.c, tools/layout.py, results/pending/ (repaired, ORDER.md),
results/drafts/jitapps-471.md, HANDOFF.md.

## Iteration 487 - 2026-10-24 - Claude

**Seed 69 processed - islands not kept; the after-seed-68 batch applied; seed 70 at 11 hours** (the owner: proceed;
the next run 11 hours; results/evolve-amd-ryzen-7-pro-8840hs-seed69.md). The pack's checks PASS; 44,876 designs,
generations 0-175, islands on (700 island lines - the 464 fix working). Against the five plain replicates at generation
109 (the chain's spread): fastest 0.1274 against 0.1197-0.1298, smallest 14,199 against 14,039-14,207, hypervolume
0.6041 against 0.6027-0.6202 - inside the spread; its end 0.1125 and 14,043. The prediction failed on speed: islands not
kept. Held out 0.968; the fast end's optimism 1.096; 32-bit failures 0; dream 0.963, the Tegra 0.965; footprint's order
negative (-0.171, -0.329). **The gene votes fixed**: review-checks.py votes now counts only the genes in the run's own
code (its commit's evolve.py, from the results file's "asked at" or --at) - seed 69 would otherwise have cast four
removal votes each against jitmul, jitdoes, jitexec and jitcfa, which did not exist in it; jitos a candidate (12 of 12).
The after-seed-68 batch: batch-check PASS (3 patches on e5c6239), applied, moved to results/applied-after-seed68/; the
routine's chain on master after it: build, run-tests PASS, validate 7 of 7, the jail PASS, the gate 147 of 147 alive,
ans-check 0 of 38 differ (rerun - the first stopped short when the chat's turn ended). NEXT-RUN: seed 70, 11 hours, without islands, footprint, spread and the
applications after it. The compare-fronts record and the progress table updated; predictions scored.

Files: results/evolve-amd-ryzen-7-pro-8840hs-seed69.md, results/xcheck-seed69.md (new); results/applied-after-seed68/
(moved), engine/, lab/evolve/ (the batch), lab/evolve/review-checks.py, lab/evolve/NEXT-RUN, results/gene-votes.md,
results/compare-fronts-amd-ryzen-7-pro-8840hs.md, results/progress-by-run.md, results/predictions.md, results/README.md,
HANDOFF.md.

## Iteration 488 - 2026-10-24 - Claude

**The after-seed-70 batch: native (ABORT"), JIT_MAXOPS 1024** (the owner: proceed with what is left; results/pending/
ORDER.md). Seed 70's bundle made first (iter487: the routine's chain all PASS - build, run-tests, validate 7 of 7, the
jail, the gate 147 of 147, ans-check 0 of 38 differ, its negative control caught). Then, outside master: JIT_MAXOPS at
1024 moved nothing alone - the refusal log's bytes showed why: the long words, and fcp's STR>MV, ?PROMOTEMV and
cd16sim's LINE:, hold (ABORT")'s inline messages ("Malformed...", "Illegal..."), decoded as code. Native (ABORT"): one
operation, its message skipped; a false flag dropped, a true one handed back to the interpreter at the call itself
through a resume helper (longjmp to jit_call's return point) - it never returns. Right against the interpreter (a false
flag in a hot loop, CATCH giving -2, one uncaught), the corpus; brainless's leftover 5.8% to 4.3%, cd16sim's 18.1% to
17.7%, fcp's unchanged - its rest is return-address words, DOES> code run by interpreted callers, nested JIT headers.
Saved as the after-seed-70 batch; master's working tree back to the bundle's.

Files: results/pending/ (new: the patch, ORDER.md); results/README.md, HANDOFF.md.
