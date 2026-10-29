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
say "$verdict - $n patch(es) applied to a fresh clone of $(git -C "$T" log --oneline -1 | cut -c1-50); run-tests: $t (exit $rt); validate: $vi of $va IDENTICAL (exit $rv); jail: $j (exit $rj); logs in $OUT"
[ "$verdict" = PASS ] || { echo "batch-check: the patched clone kept, to look at: $T" >> "$OUT/summary"; exit 1; }
# Iteration 567 (results/drafts/automation-audit-567.md): RECORD=1 writes the PASS into ORDER.md - its "batch-check (...)"
# paragraph, made or replaced - and commits that file alone; until then a chat typed it and committed it, 11 times since
# Iteration 500. Not when ORDER.md has edits not committed (the chat's prose in progress): then the line is printed.
if [ "${RECORD:-0}" = 1 ]; then
    C=$(git -C "$T" rev-parse --short HEAD); I=$(sed -n 's/^- master: Iteration \([0-9]*\).*/\1/p' "$REPO/HANDOFF.md" | head -n 1)
    G=$(sed -n 's/.*generators *ok *\([0-9]* paths\).*/\1/p' "$OUT/tests.log" | head -n 1)
    L="batch-check ($I, on $C - $n patches): PASS - run-tests PASS (the generators: ${G:-?}), validate $vi of $va IDENTICAL, the jail PASS."
    if ! git -C "$REPO" diff --quiet HEAD -- results/pending/ORDER.md; then say "PASS - ORDER.md has edits not committed, so not recorded: $L"
    elif python3 - "$REPO/results/pending/ORDER.md" "$L" << 'PY'
import re, sys, textwrap
p, line = sys.argv[1], sys.argv[2]; s = open(p).read()
new = '\n'.join(textwrap.wrap(line, 120)) + '\n'
m = re.search(r'^batch-check \(.*?(?:\n\n|\Z)', s, re.M | re.S)
if m: s = s[:m.start()] + new + ('\n' if m.group(0).endswith('\n\n') else '') + s[m.end():]
else:
    a = [x for x in re.finditer(r'^ +git apply .*\n', s, re.M)][-1]
    s = s[:a.end()] + '\n' + new + '\n' + s[a.end():].lstrip('\n')
open(p, 'w').write(s)
PY
    then N=$(sed -n 's/^# The after-seed-\([0-9]*\) batch.*/\1/p' "$REPO/results/pending/ORDER.md")
         git -C "$REPO" commit -q -m "Iteration $I: the after-seed-$N batch checked (batch-check PASS on $C, $n patches)" -- results/pending/ORDER.md &&
             echo "batch-check: recorded in ORDER.md and committed - $(git -C "$REPO" log --oneline -1 | cut -c1-80)" >> "$OUT/summary"
    fi
fi
cd "$OUT" && rm -rf "$T"   # the patched clone is a scratch tree the handoff check would flag
