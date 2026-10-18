#!/bin/sh
# tools/batch-check.sh [OUT] - the pending batch tested as it will be applied, quietly (Iteration 394).
#
# A chat's context is spent on what tools print; this cycle ran five times in Iterations 385-391 at about
# eight calls and screens of output each. Here: a fresh clone of master, results/pending's patches applied
# in ORDER.md's order (its "git apply results/pending/X.patch" lines), the stages built, then run-tests,
# validate and the jail test. Every log under OUT (default /tmp/batch-check); one line on stdout and in
# OUT/summary. Testing the applied fresh clone itself is also the check that the patches apply in order and
# reproduce what was tested. Run it as the user that builds (not root), detached if it must outlive a call:
#   setsid nohup sh tools/batch-check.sh > /dev/null 2>&1 &   ... then: cat /tmp/batch-check/summary
set -u
REPO=$(cd "$(dirname "$0")/.." && pwd); OUT=${1:-/tmp/batch-check}
rm -rf "$OUT"; mkdir -p "$OUT"; T=$OUT/tree
say() { echo "batch-check: $*" | tee "$OUT/summary"; }
git clone -q "$REPO" "$T" || { say "the clone failed"; exit 1; }
cd "$T" || exit 1
[ -f results/pending/ORDER.md ] || { say "no pending batch - nothing to test"; exit 0; }
n=0
for p in $(sed -n 's/^ *git apply \(results\/pending\/[^ ]*\.patch\).*/\1/p' results/pending/ORDER.md); do
    git apply "$p" 2> "$OUT/apply.log" || { say "$p does not apply ($OUT/apply.log)"; exit 1; }
    n=$((n + 1))
done
[ "$n" -gt 0 ] || { say "ORDER.md names no patch to apply"; exit 1; }
LAYOUTS=1 bash tools/build-stages.sh > "$OUT/build.log" 2>&1 || { say "the build failed ($OUT/build.log)"; exit 1; }
bash tools/run-tests.sh > "$OUT/tests.log" 2>&1; t=$(tail -1 "$OUT/tests.log")
python3 lab/evolve/evolve.py --validate > "$OUT/validate.log" 2>&1; v=$(grep -c IDENTICAL "$OUT/validate.log")
python3 lab/evolve/test-jail.py > "$OUT/jail.log" 2>&1; j=$(tail -1 "$OUT/jail.log")
say "$n patch(es) applied to a fresh clone of $(git -C "$REPO" log --oneline -1 | cut -c1-60); run-tests: $t; validate: $v of 7 IDENTICAL; jail: $j (logs in $OUT)"
cd "$OUT" && rm -rf "$T"   # the patched clone is a scratch tree the handoff check would flag; on a failure it stays, to look at
