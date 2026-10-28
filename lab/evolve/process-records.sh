#!/bin/sh
# lab/evolve/process-records.sh N ITERATION - HANDOFF.md's "Processing a returned seed" step 6, its mechanical part, for
# seed N (Iteration 560; done by hand until seed 77 - at 372 a batch's citations were left behind). In order:
#   1. the batch: results/pending/ moved to results/applied-after-seedN/ - only when every patch its ORDER.md applies
#      is applied (git apply -R --check), else it stops - its citations followed in every .md, README.md's line renamed;
#   2. results/progress-by-run.md (progress-table.py);
#   3. the gene votes appended to results/gene-votes.md, the stopping line to results/stopping-series.md - each skipped
#      when the ledger already has seed N, so a second run adds nothing;
#   4. NEXT_METHOD='why' set: the next series' method line (from seed N+1, the extremes from every alive design) - a
#      method change (GOALS.md: the hours among it) restarts the count.
# DB= the seed pack's db.jsonl (default process-seed.sh's under /tmp/process). Commits nothing: prints what it did and
# what stays the chat's - the predictions, NEXT-RUN, HANDOFF.md, the PROGRESS entry. As the build user.
set -u
[ $# -ge 2 ] || { sed -n '2,12p' "$0"; exit 2; }
N=$1; I=$2; cd "$(dirname "$0")/../.." || exit 1
DB=${DB:-$(ls /tmp/process/*-seed"$N"-*/pack/db.jsonl 2>/dev/null | head -1)}
RES=$(ls results/evolve-*-seed"$N".md 2>/dev/null | head -1)
[ -n "$RES" ] || { echo "process-records: no results/evolve-*-seed$N.md - draft-results.py first"; exit 1; }
[ -f "$DB" ] || { echo "process-records: no db.jsonl (DB=, or process-seed.sh first)"; exit 1; }
say() { echo "process-records: $*"; }

if [ -d results/pending ]; then                                              # 1. the batch
    P=$(sed -n 's|^ *git apply \(results/pending/[^ ]*\.patch\).*|\1|p' results/pending/ORDER.md)
    [ -n "$P" ] || { say "results/pending/ORDER.md names no patch - left as it is"; exit 1; }
    # applied: each patch reverses cleanly, or - a later commit touched its lines - a commit says so (the convention:
    # "Iteration I: the after-seed-N batch applied")
    C=$(git log --format=%h -1 --grep="the after-seed-$N batch applied")
    for p in $P; do git apply -R --check "$p" 2> /dev/null || [ -n "$C" ] || { say "$p is not applied - apply the batch first"; exit 1; }; done
    [ -z "$C" ] || say "the batch applied at $C"
    [ ! -e "results/applied-after-seed$N" ] || { say "results/applied-after-seed$N exists already - pending left as it is"; exit 1; }
    git mv results/pending "results/applied-after-seed$N" || exit 1
    git grep -lz 'results/pending/' -- '*.md' | xargs -0 -r sed -i \
        "s|results/pending/\([A-Za-z0-9._-]*-after-seed$N\.patch\)|results/applied-after-seed$N/\1|g; s|results/pending/ORDER\.md|results/applied-after-seed$N/ORDER.md|g"
    sed -i "s|^- \`pending/ORDER\.md\` - [^:]*:|- \`applied-after-seed$N/\` - the after-seed-$N batch, applied at seed $N's processing (Iteration $I):|" results/README.md
    say "the batch ($(echo $P | wc -w) patches) moved to results/applied-after-seed$N/, citations followed; README: $(grep -c "applied-after-seed$N/\`" results/README.md) line"
    L=$(git grep -lE 'results/pending/[A-Za-z0-9._-]+-after-seed[0-9]+\.patch' -- '*.md' | grep -vE '^(PROGRESS\.md|results/applied-after-seed[0-9]+/)' | tr '\n' ' ')
    [ -z "$L" ] || say "still citing results/pending/ (a batch queued behind? check): $L"
else
    say "no results/pending/ - no batch to move"
fi

python3 lab/evolve/progress-table.py > results/progress-by-run.md && say "results/progress-by-run.md written"   # 2.

if grep -q "^| $N | " results/gene-votes.md; then say "gene-votes.md has seed $N already - not appended"      # 3.
else python3 lab/evolve/review-checks.py votes "$RES" --seed "$N" --db "$DB" --ledger results/gene-votes.md --append > /dev/null &&
    say "gene votes appended: $(grep -c "^| $N | " results/gene-votes.md) genes"; fi
if grep -q "\"seed\": $N," results/stopping-series.md; then say "stopping-series.md has seed $N already - not appended"
else python3 lab/evolve/stopping.py "$DB" --seed "$N" --ledger results/stopping-series.md $([ -f /tmp/process/curve.json ] && echo --curve /tmp/process/curve.json) --append | grep -E '^verdict' |
    sed 's/^/process-records: stopping: /'; fi

if [ -n "${NEXT_METHOD:-}" ]; then                                           # 4.
    M=$((N + 1))
    if grep -q "\"method\": \"from seed $M\"" results/stopping-series.md; then say "the method line from seed $M is there already"
    else python3 -c 'import json, sys; print(json.dumps(dict(method="from seed " + sys.argv[1], why=sys.argv[2], extremes="alive"), ensure_ascii=False))' \
        "$M" "$NEXT_METHOD" >> results/stopping-series.md && say "a new series from seed $M - its method line appended"; fi
fi
say "the chat's: the predictions scored and written, NEXT-RUN, HANDOFF.md, the PROGRESS entry, then make-bundle.sh"
