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
