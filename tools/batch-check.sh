#!/bin/sh
# tools/batch-check.sh [OUT] - the pending batch tested as it will be applied, quietly (Iteration 394).
#
# A chat's context is spent on what tools print; this cycle ran five times in Iterations 385-391 at about
# eight calls and screens of output each. Here: a fresh clone of master, results/pending's patches applied
# in ORDER.md's order (its "git apply results/pending/X.patch" lines), the stages built, then run-tests,
# validate and the jail test. Every log under OUT (default /tmp/batch-check); one line on stdout and in
# OUT/summary. Testing the applied fresh clone itself is also the check that the patches apply in order and
# reproduce what was tested. It tests what is COMMITTED - the clone sees nothing uncommitted: commit the batch
# first, and check the line's commit and patch count (Iteration 397: a run before the commit tested 1 patch of 3).
# Run it as the user that builds (not root), detached if it must outlive a call:
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
    # Iteration 501: a patch that adds conflict markers applies cleanly - the after-seed-68 engine patch carried one from
    # its 475 rebase to 486 (results/applied-after-seed68/ORDER.md) - so markers are refused before applying.
    if grep -n '^+\(<<<<<<< \|=======$\|>>>>>>> \)' "$p" > "$OUT/markers.log"; then say "$p adds conflict markers ($OUT/markers.log)"; exit 1; fi
    git apply "$p" 2> "$OUT/apply.log" || { say "$p does not apply ($OUT/apply.log)"; exit 1; }
    n=$((n + 1))
done
[ "$n" -gt 0 ] || { say "ORDER.md names no patch to apply"; exit 1; }
LAYOUTS=1 bash tools/build-stages.sh > "$OUT/build.log" 2>&1 || { say "the build failed ($OUT/build.log)"; exit 1; }
bash tools/run-tests.sh > "$OUT/tests.log" 2>&1; rt=$?; t=$(tail -1 "$OUT/tests.log")
python3 lab/evolve/evolve.py --validate > "$OUT/validate.log" 2>&1; rv=$?
vi=$(grep -c ' image IDENTICAL' "$OUT/validate.log"); va=$(grep -c ' image ' "$OUT/validate.log")
python3 lab/evolve/test-jail.py > "$OUT/jail.log" 2>&1; rj=$?; j=$(tail -1 "$OUT/jail.log")
# Iteration 394's audit: PASS only if every check says so in its own words AND by its exit status - a summary
# line must not hide a failure; on any FAIL the patched clone stays, and the script exits 1.
if [ "$rt" -eq 0 ] && [ "$t" = "PASS - no regressions" ] && [ "$rv" -eq 0 ] && [ "$va" -gt 0 ] && [ "$vi" -eq "$va" ] \
   && [ "$rj" -eq 0 ] && [ "$j" = "PASS" ]; then verdict=PASS; else verdict=FAIL; fi
say "$verdict - $n patch(es) applied to a fresh clone of $(git -C "$REPO" log --oneline -1 | cut -c1-50); run-tests: $t (exit $rt); validate: $vi of $va IDENTICAL (exit $rv); jail: $j (exit $rj); logs in $OUT"
[ "$verdict" = PASS ] || { echo "batch-check: the patched clone kept, to look at: $T" >> "$OUT/summary"; exit 1; }
cd "$OUT" && rm -rf "$T"   # the patched clone is a scratch tree the handoff check would flag
