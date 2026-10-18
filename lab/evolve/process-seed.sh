#!/bin/sh
# lab/evolve/process-seed.sh ARCHIVE [OUT] - a returned chain archive, its mechanical part done (Iteration 395).
#
# HANDOFF's "Processing a returned seed", steps 1-3, the parts that only read and run: unpack the archive and its
# packs; the seed pack's own checks; the verdict as printed and from both CPUs (review-checks.py verdicts);
# seed-facts.py, heldout.py, review-checks.py progress; the remote checks' agreement lines. Every output in a file
# under OUT (default /tmp/process); a summary of about a screen in OUT/summary.md - read that, and the files only
# where it points. Interpreting, the predictions, the records and the gates stay the chat's.
# Run it as the user that builds (it imports the evolver, which refuses root).
set -u
[ $# -ge 1 ] || { sed -n '2,9p' "$0"; exit 2; }
REPO=$(cd "$(dirname "$0")/../.." && pwd); EV=$REPO/lab/evolve
A=$(readlink -f "$1"); OUT=${2:-/tmp/process}
rm -rf "$OUT"; mkdir -p "$OUT"; cd "$OUT" || exit 1
tar xzf "$A" 2> unpack.log || { echo "process-seed: cannot unpack $A (unpack.log)"; exit 1; }
C=$(ls -d "$OUT"/chain-* 2>/dev/null | head -1); [ -n "$C" ] || { echo "process-seed: no chain-* in $A"; exit 1; }
for t in "$C"/packs/*.tar.gz; do [ -f "$t" ] || continue; d=$OUT/$(basename "$t" .tar.gz); mkdir -p "$d"; tar xzf "$t" -C "$d"; done
SP=$(ls -d "$OUT"/*-seed[0-9]*/pack 2>/dev/null | head -1); CP=$(ls -d "$OUT"/*-compare-fronts-*/pack 2>/dev/null | head -1)
S=$OUT/summary.md; : > "$S"; p() { printf '%s\n' "$*" >> "$S"; }
p "# $(cat "$C/line" 2>/dev/null) - status $(cat "$C/status" 2>/dev/null), at $(cat "$C/head" 2>/dev/null)"
p "packs: $(ls "$C"/packs 2>/dev/null | tr '\n' ' ')"
if [ -n "$SP" ]; then
    p ""; p "## The seed pack - its own checks"
    p "- tests: $(tail -1 "$SP/tests.log" 2>/dev/null); validate: $(grep -c IDENTICAL "$SP/validate.log" 2>/dev/null) IDENTICAL; jail: $(tail -1 "$SP/jail.log" 2>/dev/null)"
    p "- $(grep -m1 -E 'carried in' "$SP/next-run.log" 2>/dev/null)"
    [ -f "$SP/results-measured-here.patch" ] && p "- results-measured-here.patch: $(grep -c '^diff --git' "$SP/results-measured-here.patch") file diffs (the laptop's own re-measures - HANDOFF step 1)"
    python3 "$EV/seed-facts.py" "$SP/db.jsonl" "$SP/report.md" > seed-facts.txt 2>&1
    p ""; p "## seed-facts.py (seed-facts.txt: $(wc -l < seed-facts.txt) lines; its first 25)"; p '```'; head -25 seed-facts.txt >> "$S"; p '```'
    python3 "$EV/heldout.py" "$SP/report.md" > heldout.txt 2>&1
    p ""; p "## heldout.py (heldout.txt)"; p '```'; head -4 heldout.txt >> "$S"; p '```'
    python3 "$EV/review-checks.py" progress "$SP/db.jsonl" > progress.txt 2>&1
    p ""; p "## review-checks.py progress (progress.txt) - the last generation and the gains"; p '```'; tail -4 progress.txt >> "$S"; p '```'
fi
if [ -n "$CP" ]; then
    F=$CP/compare-fronts.md
    p ""; p "## The comparison - the verdict (\"+\" is the run ahead)"; p '```'
    grep -E '^\| this clone[^|]*\| [-+][0-9.]+% \|' "$F" >> "$S"           # Judging the runs: the run's row
    grep -E '^\| this clone[^|]*\| [0-9.]+ \([0-9a-f]{10}\) \|' "$F" >> "$S"   # at 32 bits: the run's row
    grep -E '^(The Q-best design of all runs|\*\*Calibration)' "$F" | cut -c1-200 >> "$S"; p '```'
    { echo "## Session 0 - Iteration 0: this archive's"; cat "$F"; } > session.md
    python3 "$EV/review-checks.py" verdicts session.md > verdicts.txt 2>&1
    p ""; p "## The verdict by the owner's rule of Iteration 389 (verdicts.txt)"; p '```'; grep -E '^  (printed|cpu 2 alone|cpu 8 alone|both CPUs)' verdicts.txt >> "$S"; p '```'
fi
if ls "$C"/remote/*.md > /dev/null 2>&1; then
    p ""; p "## The remote checks (their reports in $C/remote)"; p '```'
    grep -HiE 'spearman|rejected by' "$C"/remote/*.md | sed "s|$C/remote/||" | cut -c1-200 >> "$S"; p '```'
fi
echo "process-seed: $(wc -l < "$S") lines in $S; the rest in $OUT"
