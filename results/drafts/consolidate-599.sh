#!/bin/sh
# results/drafts/consolidate-599.sh - Iteration 599: consolidation's batch - checked, applied, and the final set's 21 hashed before and after (alone, in order)
set -u
cd /home/claude/forth-vm-evolution || exit 1
O=/tmp/consol; S=$O/status; : > $S
st() { echo "$* $(date +%T)" >> $S; }
die() { st "STOP - $*"; exit 1; }
IDS=$(python3 -c "import json; print(','.join(json.loads(l)['id'] for l in open('results/final-set-chainsBCD-seed86.md') if l.startswith('{')))")
st "START at $(git rev-parse --short HEAD), $(echo $IDS | tr ',' '\n' | wc -l) designs"
env LAYOUTS=1 bash tools/build-stages.sh > $O/build-pre.log 2>&1 || die "build before (build-pre.log)"
python3 lab/evolve/evolve.py --validate > $O/validate-pre.log 2>&1; st "validate before - $(grep -c IDENTICAL $O/validate-pre.log) IDENTICAL"
rm -f $O/bh-pre-8.jsonl $O/bh-pre-4.jsonl
python3 results/drafts/build-hash-584.py $O/bh-pre-8.jsonl --only $IDS > $O/bh-pre-8.log 2>&1
python3 results/drafts/build-hash-584.py $O/bh-pre-4.jsonl --cell4 --only $IDS > $O/bh-pre-4.log 2>&1
st "hashed before - $(grep -c . $O/bh-pre-8.jsonl) at 8, $(grep -c . $O/bh-pre-4.jsonl) at 4"
RECORD=1 sh tools/batch-check.sh > $O/batch-check.log 2>&1; L=$(cat /tmp/batch-check/summary 2>/dev/null)
st "batch-check - $(echo "$L" | cut -c1-160)"
case $L in "batch-check: PASS"*) ;; *) die "batch-check did not pass - /tmp/batch-check" ;; esac
[ -z "$(git status --porcelain)" ] || die "the tree has changes after batch-check"
P=$(sed -n 's|^ *git apply \(results/pending/[^ ]*\.patch\).*|\1|p' results/pending/ORDER.md)
for p in $P; do
    git apply --index "$p" || die "$p does not apply to master"
    ! git diff --cached --name-only | grep -qx forth/kernel.4 || die "$p changes forth/kernel.4 - reseed by hand"
done
git commit -q -m "Iteration 599: the after-seed-86 batch applied - $(echo $P | wc -w) patches ($(for p in $P; do basename "$p" -after-seed86.patch; done | tr '\n' ' ' | sed 's/ $//; s/ /, /g')), batch-check PASS" || die "the batch's commit"
st "applied - $(git log --oneline -1 | cut -c1-120)"
env LAYOUTS=1 bash tools/build-stages.sh > $O/build-post.log 2>&1 || die "build after (build-post.log)"
st "built after"
bash tools/run-tests.sh > $O/tests.log 2>&1; st "run-tests - $(tail -n 1 $O/tests.log | cut -c1-100)"
python3 lab/evolve/evolve.py --validate > $O/validate.log 2>&1; st "validate - $(grep -c IDENTICAL $O/validate.log) IDENTICAL"
rm -f $O/bh-post-8.jsonl $O/bh-post-4.jsonl
python3 results/drafts/build-hash-584.py $O/bh-post-8.jsonl --only $IDS > $O/bh-post-8.log 2>&1
python3 results/drafts/build-hash-584.py $O/bh-post-4.jsonl --cell4 --only $IDS > $O/bh-post-4.log 2>&1
st "hashed after - $(grep -c . $O/bh-post-8.jsonl) at 8, $(grep -c . $O/bh-post-4.jsonl) at 4"
st "jail - alone"
python3 lab/evolve/test-jail.py > $O/jail.log 2>&1; st "jail - $(tail -n 1 $O/jail.log | cut -c1-100)"
st DONE
# Then, by hand (Iteration 599): each width's bh-pre and bh-post compared by id - 21 of 21 the same engine and image bytes
# at both widths, none died; bh-pre the same as results/drafts/build-hash-584-8.jsonl and -4.jsonl, 21 of 21.

