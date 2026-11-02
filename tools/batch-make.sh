#!/bin/sh
# tools/batch-make.sh N ITERATION SCRATCH - a batch's mechanics, from a scratch tree's commits (Iteration 567;
# results/drafts/automation-audit-567.md, candidate 1 - by hand until then: about ten tool calls a batch, and a fix-up
# commit when an index line or the PASS line was missed). In the main tree, as the build user:
#   - every commit of SCRATCH (setup-sandbox.sh SCRATCH=) past its origin/master, but the "scratch: results/pending/..."
#     ones (the batch already there), becomes results/pending/NAME-after-seedN.patch - NAME the first word of its
#     subject, before any ":" ("design: ..." -> design-after-seed81.patch); a patch already there is made again, so a
#     scratch tree rebased onto a newer master regenerates the batch;
#   - results/pending/ORDER.md: made when absent (its title, process-run's line); for a new patch its "git apply" line
#     after the last one and a "**NAME-after-seedN.patch** TODO" paragraph at the end - handoff-check refuses a TODO,
#     so the chat writes what each does, why, and how it was tested;
#   - results/README.md's pending line, written from the patches;
#   - one commit. Then the chat writes the prose, commits, and runs the check, which records its PASS itself:
#       setsid nohup env RECORD=1 sh tools/batch-check.sh > /dev/null 2>&1 &
# N: the seed at whose processing process-run.sh applies the batch.
# PENDING=DIR (Iteration 588): the batch's directory, default results/pending - results/queued-consolidation for
# consolidation's queue (results/drafts/retire-stages-584.md), which process-run.sh never applies.
set -u
N=${1:?N - the seed whose processing applies the batch}; I=${2:?ITERATION}; X=${3:?SCRATCH - the scratch tree}; Q=${PENDING:-results/pending}
cd "$(dirname "$0")/.." || exit 1
say() { echo "batch-make: $*"; }
[ -d "$X/.git" ] || { say "no scratch tree at $X (setup-sandbox.sh SCRATCH=$X)"; exit 1; }
[ -z "$(git status --porcelain -- "$Q" results/README.md)" ] || { say "$Q or results/README.md has changes - commit them first"; exit 1; }
[ -z "$(git -C "$X" status --porcelain --untracked-files=no)" ] || { say "$X has changes not committed - commit them as the patches they are"; exit 1; }
O=$Q/ORDER.md; mkdir -p "$Q"
[ -f "$O" ] || printf '# The after-seed-%s batch - to apply first at seed %s'"'"'s processing (Iteration %s)\n\nprocess-run.sh checks and applies it.\n\n' "$N" "$N" "$I" > "$O"
grep -q "^# The after-seed-$N batch" "$O" || { say "$O is another seed's batch: $(head -n 1 "$O")"; exit 1; }
made=0
for c in $(git -C "$X" rev-list --reverse origin/master..HEAD); do
    s=$(git -C "$X" log -1 --format=%s "$c")
    case $s in "scratch: "*) continue ;; esac
    name=$(echo "$s" | sed 's/[: ].*//' | tr 'A-Z' 'a-z' | tr -cd 'a-z0-9-')
    [ -n "$name" ] || { say "commit $c: no name in its subject '$s'"; exit 1; }
    P=$Q/$name-after-seed$N.patch
    git -C "$X" diff --binary "$c^" "$c" > "$P"   # 588: --binary, or a binary file is "Binary files differ" and never applies
    files=$(git -C "$X" diff --name-only "$c^" "$c" | tr '\n' ' ' | sed 's/ $//; s/ /, /g')
    if grep -q "git apply $P" "$O"; then say "$P made again ($files)"
    else
        python3 - "$O" "    git apply $P" "**$name-after-seed$N.patch** ($files) - TODO: what it does, why, how it was tested." << 'PY'
import re, sys
p, line, para = sys.argv[1:]; s = open(p).read()
a = list(re.finditer(r'^ +git apply .*\n', s, re.M))
if a: s = s[:a[-1].end()] + line + '\n' + s[a[-1].end():]
else: s = s.rstrip('\n') + '\n\n' + line + '\n\n'
open(p, 'w').write(s.rstrip('\n') + '\n\n' + para + '\n')
PY
        say "$P new ($files) - its paragraph in ORDER.md is a TODO"
    fi
    made=$((made + 1))
done
[ "$made" -gt 0 ] || { say "no commit in $X past origin/master but the batch's own - nothing to make"; exit 1; }
names=$(sed -n "s|^ *git apply $Q/\\(.*\\)-after-seed[0-9]*\\.patch.*|\\1|p" "$O" | tr '\n' ' ' | sed 's/ $//; s/ /, /g')
L="- \`pending/ORDER.md\` - the batch to apply first at seed $N's processing: $names (ORDER.md says what each does)."
[ "$Q" = results/pending ] || L="- \`${Q#results/}/ORDER.md\` - the batch queued for consolidation, applied after the final pick: $names (ORDER.md says what each does)."
python3 - results/README.md "$L" << 'PY'
import sys
p, line = sys.argv[1:]; s = open(p).read().split('\n')
i = [k for k, l in enumerate(s) if l.startswith(line.split(' - ')[0])]
if i: s[i[0]] = line
else:
    j = [k for k, l in enumerate(s) if l.startswith('- `applied-after-seed')]   # 568: the batches oldest first - after the last
    s.insert(j[-1] + 1 if j else len(s), line)
open(p, 'w').write('\n'.join(s))
PY
git add "$Q" results/README.md && git commit -q -m "Iteration $I: the after-seed-$N batch - $names (batch-make.sh from $X)" &&
    say "committed: $(git log --oneline -1 | cut -c1-90)"
grep -q TODO "$O" && say "next: the TODO paragraphs in $O, a commit, then: setsid nohup env PENDING=$Q RECORD=1 sh tools/batch-check.sh > /dev/null 2>&1 &" ||
    say "next: setsid nohup env PENDING=$Q RECORD=1 sh tools/batch-check.sh > /dev/null 2>&1 &"
