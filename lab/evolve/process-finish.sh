#!/bin/sh
# lab/evolve/process-finish.sh N ITERATION [--dry] - a returned seed's processing finished, once process-run.sh is DONE
# and the chat has judged (Iteration 560). It stops at the first thing wrong, saying what:
#   1. every check passed - /tmp/process-checks/status: build, run-tests, validate (7 of 7), the gate (every design
#      alive), ans-check (0 differ, the negative control caught), deaths-check, the jail; each step's exit 0;
#   2. the results file's two [process-finish: ...] lines filled - the chain on master, deaths-check's table (and the
#      control's line when process-run.sh made one);
#   3. nothing left to judge: no TODO in the results file, its xcheck, the comparison's newest session;
#   4. process-records.sh N ITERATION (NEXT_METHOD= passed on) - the batch moved, the progress table, the ledgers;
#   5. the chat's records there: predictions.md scores seed N, NEXT-RUN names seed N+1 (or none), HANDOFF.md says
#      "master: Iteration ITERATION", PROGRESS.md has its entry;
#   6. --dry stops here; else everything committed and tools/make-bundle.sh /mnt/user-data/outputs - then present it.
# OPEN='why' (563): deaths-check's open deaths recorded as an open correctness issue, not waived - the chain line says
# so; no other check can be. Safe to run again after fixing what it named. As the build user.
set -u
N=${1:?N}; I=${2:?ITERATION}; DRY=${3:-}
cd "$(dirname "$0")/../.." || exit 1
S=/tmp/process-checks/status; R=$(ls results/evolve-*-seed"$N".md 2>/dev/null | head -1)
say() { echo "process-finish: $*"; }; die() { say "STOP - $*"; exit 1; }
[ -n "$R" ] || die "no results/evolve-*-seed$N.md"
[ -f "$S" ] || die "no $S"
# 563: only this chain's lines - from the last "START from build" on (a resumed step appends after it); the status file
# keeps an earlier chain's lines, and their passes are not this seed's
K=/tmp/process-finish.status; awk '/^START from build/{b=""} {b=b $0 "\n"} END{printf "%s", b}' "$S" > "$K"; S=$K
grep -q '^START from build' "$S" || die "no full chain in /tmp/process-checks/status - process-checks.sh from build"
grep -q '^DONE' "$S" || die "process-checks.sh not DONE (/tmp/process-checks/status)"
H0=$(sed -n 's/^START from build at \([0-9a-f]*\).*/\1/p' "$S")
git diff --quiet "$H0" HEAD -- engine forth lab/evolve/evolve.py || die "the checks ran at $H0 and the engine, kernel or evolver changed since - run them again"
for k in build run-tests validate gate ans-check deaths jail; do                      # 1.
    l=$(grep "^$k=" "$S" | tail -n 1); [ -n "$l" ] || die "no $k line in $S"
    case $l in "$k=0"*) ;; "deaths="*) [ -n "${OPEN:-}" ] || die "$l - an open correctness issue: fix it, or OPEN='why' records it";;
        *) die "$l" ;; esac
done
grep -q '^validate=0 7 of 7 IDENTICAL' "$S" || die "$(grep '^validate=' "$S")"
G=$(sed -n 's/^gate=0 alive: \([0-9]*\) of \([0-9]*\).*/\1 \2/p' "$S"); set -- $G
[ $# -eq 2 ] && [ "$1" = "$2" ] || die "$(grep '^gate=' "$S")"; GA="$1 of $2"
A=$(sed -n 's/^ans-check=0 \([0-9]* of [0-9]*\) designs differ.*/\1/p' "$S")
case $A in "0 of "*) ;; *) die "$(grep '^ans-check=' "$S")" ;; esac
grep '^ans-check=' "$S" | grep -q 'negative control caught' || die "ans-check's negative control not caught"
H=$H0
D=/tmp/process-checks/deaths.log; DL=$(tail -n 1 "$D" | sed 's/^deaths-check: //')
CL=$(grep -h '^control at' /tmp/process-run/status 2>/dev/null | sed 's/ [0-9:]*$//')
[ -z "${OPEN:-}" ] || DL="$DL - OPEN, a correctness issue: $OPEN"
CHAIN="process-checks.sh at $H: build 0, run-tests PASS, validate 7 of 7 IDENTICAL, the gate alive $GA, ans-check $A differ (its negative control caught), deaths-check: $DL, the jail PASS."
python3 - "$R" "$CHAIN" "$D" "$CL" << 'PY' || die "the results file's [process-finish: ...] lines"
import re, sys
r, chain, d, cl = sys.argv[1:]; s = open(r).read()
rows = [l.strip() for l in open(d) if re.match(r'\| [0-9a-f]{10} \|', l)]
dead = 'deaths-check.py rebuilt them here (design, generation, in the run, genes, here): %s.' % ('; '.join(
    ' - '.join(c.strip() for c in l.strip('|').split('|')) for l in rows) or 'none to rebuild') + (' The %s.' % cl if cl else '')
s = s.replace('[process-finish: the chain]', chain).replace('[process-finish: deaths-check]', dead)
open(r, 'w').write(s)
PY
say "1-2. every check passed; the chain line and the deaths filled"
T=$(grep -l 'TODO\|\[process-finish' "$R" "results/xcheck-seed$N.md" 2>/dev/null | tr '\n' ' ')                   # 3.
C=$(ls results/compare-fronts-*.md 2>/dev/null | head -1)
[ -z "$C" ] || ! awk '/^## Session /{s=""} {s=s $0 "\n"} END{printf "%s", s}' "$C" | grep -q TODO || T="$T $C (its newest session)"
[ -z "$T" ] || die "TODO left in: $T"
sh lab/evolve/process-records.sh "$N" "$I" || die "process-records.sh"                                               # 4.
M=""                                                                                                                  # 5.
grep -q "Scored at seed $N " results/predictions.md || M="$M results/predictions.md (\"Scored at seed $N\");"
L=$(grep -v '^#' lab/evolve/NEXT-RUN | grep -v '^ *$' | head -n 1)
case $L in "seed $((N + 1)) "*|none*) ;; *) M="$M lab/evolve/NEXT-RUN (its line: $L);" ;; esac
grep -q "^- master: Iteration $I\.\$" HANDOFF.md || M="$M HANDOFF.md (\"- master: Iteration $I.\");"
grep -q "^## Iteration $I " PROGRESS.md || M="$M PROGRESS.md (\"## Iteration $I\");"
[ -z "$M" ] || die "the chat's records missing:$M"
say "3-5. nothing left to judge; the records written"
[ "$DRY" = --dry ] && { say "--dry: nothing committed"; exit 0; }
P=$(sed -n '1s/^# Seed [0-9]* on the .* - \(.*\) (Iteration [0-9]*)$/\1/p' "$R")
git add -A && git commit -q -m "Iteration $I: seed $N processed - ${P:-see its results file}" || die "the commit"
say "committed $(git log --oneline -1 | cut -c1-100)"
sh tools/make-bundle.sh /mnt/user-data/outputs 2>&1 | tail -n 3
