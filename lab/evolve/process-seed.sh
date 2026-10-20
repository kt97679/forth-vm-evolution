#!/bin/sh
# lab/evolve/process-seed.sh ARCHIVE [OUT] - a returned chain archive, its mechanical part done (Iteration 395).
#
# HANDOFF's "Processing a returned seed", steps 1-3, the parts that only read and run: unpack the archive and its
# packs; the seed pack's own checks; the verdict as printed and from both CPUs (review-checks.py verdicts);
# seed-facts.py, heldout.py, review-checks.py progress, curse and fail32 (Iteration 427); the remote checks' agreement lines,
# and review-checks.py generic - the best design across the machine classes (Iteration 430). Every output in a file
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
    python3 "$EV/review-checks.py" curse "$SP/report.md" > curse.txt 2>&1        # Iteration 427: done by hand until seed 61
    p ""; p "## review-checks.py curse (curse.txt) - the fast end's optimism, re-measured / in-run"; p '```'; head -3 curse.txt >> "$S"; p '```'
    python3 "$EV/review-checks.py" fail32 "$SP/db.jsonl" > fail32.txt 2>&1
    p ""; p "## review-checks.py fail32 (fail32.txt) - the 32-bit failures by cause"; p '```'; head -8 fail32.txt >> "$S"; p '```'
    VN=$(awk '$1 == "seed" {print $2}' "$C/line" 2>/dev/null)        # Iteration 432: the gene votes, with the ledger - not written
    python3 "$EV/review-checks.py" votes "$SP/report.md" ${VN:+--seed "$VN"} --ledger "$REPO/results/gene-votes.md" > votes.txt 2>&1
    p ""; p "## review-checks.py votes (votes.txt) - the gene votes, with results/gene-votes.md (appended at step 6)"; p '```'; head -3 votes.txt | cut -c1-400 >> "$S"; p '```'
    python3 "$EV/review-checks.py" rules "$SP/report.md" ${VN:+--seed "$VN"} --db "$SP/db.jsonl" --ledger "$REPO/results/gene-votes.md" > rules.txt 2>&1   # Iteration 438
    p ""; p "## review-checks.py rules (rules.txt) - results/seed63-rules.md's rules, measured"; cut -c1-300 rules.txt | grep -v '^pinned' >> "$S"
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
    grep -HiE 'spearman|rejected by|asked for by id' "$C"/remote/*.md | sed "s|$C/remote/||" | cut -c1-200 >> "$S"
    # Iteration 403 (item 0g): a 4-byte host against the laptop's own 32-bit speeds too - those of the run it checked
    N=$(awk '$1 == "seed" {print $2}' "$C/line" 2>/dev/null); L32=$(ls "$REPO"/results/evolve-*-seed$((${N:-1} - 1)).md 2>/dev/null | head -1)
    for o in "$C"/remote/*/out.json; do
        [ -f "$o" ] && [ -n "$L32" ] && grep -q '"cell": *4' "$o" || continue
        python3 "$EV/xcheck.py" --report "$o" --laptop32 "$L32" 2>/dev/null | grep -E '32-bit speeds' | sed "s|^|$(basename "$(dirname "$o")").md, --laptop32 $(basename "$L32"): |" | cut -c1-220 >> "$S"
    done; p '```'
    python3 "$EV/review-checks.py" generic "$C/remote" > generic.txt 2>&1      # Iteration 430: the three classes
    p ""; p "## review-checks.py generic (generic.txt) - the best design across the three machine classes"; p '```'; head -14 generic.txt | cut -c1-200 >> "$S"; p '```'
fi
echo "process-seed: $(wc -l < "$S") lines in $S; the rest in $OUT"
