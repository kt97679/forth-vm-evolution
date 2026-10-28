#!/bin/sh
# lab/evolve/process-run.sh ITERATION [ARCHIVE] - a returned seed's processing, its mechanical part, as one detached job
# (Iteration 560; HANDOFF.md, "Processing a returned seed"). In order, each step's line in /tmp/process-run/status:
#   1. process-seed.sh ARCHIVE (default: the one chain archive in /mnt/user-data/uploads) - /tmp/process/summary.md;
#   2. draft-results.py --iteration ITERATION - the results file, xcheck, the spread's session; TODO: the verdict and
#      the predictions only;
#   3. a batch in results/pending/: tools/batch-check.sh, then - PASS only - its patches applied in ORDER.md's order
#      with git apply --index (the patches' own files, nothing else) and committed; a patch that changes
#      forth/kernel.4 stops it (reseed by hand: tools/reseed.sh);
#   3b. the run's curve for the stopping rule (stopping.py --curve, minutes - after the batch, whose stopping.py may
#      bring it);
#   4. process-checks.sh on master (build, run-tests, validate, the gate, ans-check, deaths-check, the jail - alone);
#   5. a batch applied and a death that computes right on master: the control - deaths-check on the commit before the
#      batch, in its own clone - so "the batch fixed it" is measured, not assumed (Iteration 560: seed 77's 0b17df4e1c).
# Start it detached and poll:   setsid nohup sh lab/evolve/process-run.sh 561 > /dev/null 2>&1 &
#   then: sh tools/wait-for.sh /tmp/process-run/status 'summary|DONE|STOP'   (summary.md is ready at "summary")
# Judge while it runs (summary.md; the results file's header - never run anything as this user once the status says
# "jail - alone"); at DONE: sh lab/evolve/process-finish.sh N ITERATION. As the build user, never root.
# A detached job dies when the chat's turn ends - the sandbox suspends, /tmp stays (Iteration 561: a test cut off at
# its run-tests). Start it early in a turn and see it to DONE; cut off: FROM=checks resumes at step 4 - /tmp/process and
# the drafts kept, the chat's edits to them too - and with the batch already applied.
set -u
I=${1:?ITERATION}; A=${2:-$(ls /mnt/user-data/uploads/forth-vm-evolution-chain-*_tar.gz 2>/dev/null | tail -1)}
cd "$(dirname "$0")/../.." || exit 1
O=/tmp/process-run; mkdir -p "$O"; S=$O/status; : > "$S"
st() { echo "$* $(date +%T)" >> "$S"; }
die() { st "STOP - $*"; exit 1; }
if [ "${FROM:-}" = checks ]; then                                 # 561: a cut-off run resumed at the checks
    ls /tmp/process/*-seed[0-9]*-*/pack/db.jsonl > /dev/null 2>&1 || die "FROM=checks: no /tmp/process - run it whole"
    [ ! -d results/pending ] || [ -n "$(git log --format=%h -1 --grep='batch applied')" ] || die "FROM=checks: a batch waits unapplied"
    st "START again from the checks at $(git rev-parse --short HEAD)"
else
[ -f "$A" ] || die "no chain archive (ARCHIVE, or forth-vm-evolution-chain-*_tar.gz in /mnt/user-data/uploads)"
[ -z "$(git status --porcelain -- engine forth tools lab results)" ] || die "the tree has changes - commit or stash them first (cut off after its drafts: FROM=checks)"
st "START $(basename "$A") at $(git rev-parse --short HEAD)"
sh lab/evolve/process-seed.sh "$A" > "$O/process-seed.log" 2>&1 || die "process-seed.sh (process-seed.log)"
st "summary - /tmp/process/summary.md: $(tail -n 1 "$O/process-seed.log")"
python3 lab/evolve/draft-results.py --iteration "$I" > "$O/draft.log" 2>&1 || die "draft-results.py (draft.log)"
st "drafted - $(grep -c '' "$O/draft.log") files: $(grep -o 'results/[^ ]*' "$O/draft.log" | tr '\n' ' ')"
PRE=; N=$(ls -d /tmp/process/*-seed[0-9]*-* | sed -n 's/.*-seed\([0-9]*\)-.*/\1/p' | head -n 1)
T=; [ -d results/pending ] && for p in $(sed -n 's|^ *git apply \(results/pending/[^ ]*\.patch\).*|\1|p' results/pending/ORDER.md); do
    git apply -R --check "$p" 2> /dev/null || T="$T $p"; done          # applied already (by hand, once): skipped
if [ -d results/pending ] && [ -z "$T" ]; then
    C=$(git log --format=%h -1 --grep="the after-seed-$N batch applied"); PRE=$(git rev-parse --short "$C^" 2> /dev/null)
    st "the batch applied already, at ${C:-?} - not again"
elif [ -d results/pending ]; then
    PRE=$(git rev-parse --short HEAD)
    sh tools/batch-check.sh > "$O/batch-check.log" 2>&1; L=$(cat /tmp/batch-check/summary 2>/dev/null)
    st "batch-check - $(echo "$L" | cut -c1-160)"
    case $L in "batch-check: PASS"*) ;; *) die "batch-check did not pass - /tmp/batch-check" ;; esac
    P=$(sed -n 's|^ *git apply \(results/pending/[^ ]*\.patch\).*|\1|p' results/pending/ORDER.md)
    for p in $P; do
        git apply --index "$p" || die "$p does not apply to master"
        ! git diff --cached --name-only | grep -qx forth/kernel.4 || die "$p changes forth/kernel.4 - reseed by hand (tools/reseed.sh), commit, then process-checks.sh"
    done
    git commit -q -m "Iteration $I: the after-seed-$N batch applied - $(echo $P | wc -w) patches ($(for p in $P; do basename "$p" -after-seed$N.patch; done | tr '\n' ' ' | sed 's/ $//; s/ /, /g')), batch-check PASS" || die "the batch's commit"
    st "applied - $(git log --oneline -1 | cut -c1-120)"
fi
fi                                                                # the FROM=checks branch's end
N=$(ls -d /tmp/process/*-seed[0-9]*-* | sed -n 's/.*-seed\([0-9]*\)-.*/\1/p' | head -n 1)
[ -n "${PRE:-}" ] || { C=$(git log --format=%h -1 --grep="the after-seed-$N batch applied"); [ -z "$C" ] || PRE=$(git rev-parse --short "$C^"); }
D=$(ls /tmp/process/*-seed[0-9]*-*/pack/db.jsonl | head -n 1)     # 562: the run's curve for the stopping rule, detached
if grep -q "opt('--curve')" lab/evolve/stopping.py && ! grep -q "\"seed\": $N," /tmp/process/curve.json 2> /dev/null; then
    python3 lab/evolve/stopping.py "$D" --seed "$N" --curve /tmp/process/curve.json > "$O/curve.log" 2>&1; st "curve - $(tail -n 1 "$O/curve.log")"
fi
R=$(grep -o 'results/evolve-[^ ]*-seed[0-9]*\.md' "$O/draft.log" | head -1)
st "checks - process-checks.sh $R (its status /tmp/process-checks/status)"
sh lab/evolve/process-checks.sh "$R" > /dev/null 2>&1
st "checks done - $(grep -c '=0' /tmp/process-checks/status) steps 0, $(grep -cE '=[1-9]' /tmp/process-checks/status) not"
if [ -n "$PRE" ] && grep -q 'right - as s6' /tmp/process-checks/deaths.log 2>/dev/null; then
    C=$O/control; rm -rf "$C"; git clone -q . "$C" && git -C "$C" checkout -q "$PRE" && cp lab/evolve/deaths-check.py "$C/lab/evolve/"
    ( cd "$C" && env LAYOUTS=1 bash tools/build-stages.sh > "$O/control-build.log" 2>&1 &&
      python3 lab/evolve/deaths-check.py "$(ls /tmp/process/*-seed[0-9]*-*/pack/db.jsonl | head -1)" > "$O/control.log" 2>&1 )
    st "control at $PRE (before the batch) - $(tail -n 1 "$O/control.log" 2>/dev/null)"; rm -rf "$C"
fi
st DONE
