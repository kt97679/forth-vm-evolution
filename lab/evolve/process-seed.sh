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
    VN=$(echo "$SP" | sed -n 's|.*-seed\([0-9][0-9]*\)-[^/]*/pack$|\1|p')   # 576: the seed pack's name - the line can start with another step (seed 85's: "experiment ... then seed 85")
    python3 "$EV/review-checks.py" votes "$SP/report.md" ${VN:+--seed "$VN"} --db "$SP/db.jsonl" --ledger "$REPO/results/gene-votes.md" > votes.txt 2>&1   # 532: the front from the records
    p ""; p "## review-checks.py votes (votes.txt) - the gene votes, with results/gene-votes.md (appended at step 6)"; p '```'; head -3 votes.txt | cut -c1-400 >> "$S"; p '```'
    # Iteration 573: the confirmation run (GOALS.md step 2) - no series run. next-run.sh strips a line's words (carryall,
    # widths, noevolved, random) before it writes the chain's line - seed 83's reads "seed 83 9h then ..." - so the word is
    # read where the run's WANT is kept: the pack's machine.txt and the chain's steps. The marker file tells the rest.
    W=$({ grep -h '^seed ' "$SP/machine.txt"; sed -n 's/^ok \(seed .*\)/\1/p' "$C/steps"; } 2> /dev/null | head -n 1)   # the run's WANT
    case " $W $(cat "$C/line" 2> /dev/null) " in *" carryall "*) echo carryall > "$OUT/confirmation" ;; esac
    case " $W " in *" random "*) echo random > "$OUT/random" ;; esac      # 573: the random-search baseline, GOALS.md step 4
    if [ -f "$OUT/confirmation" ]; then
        # the final set's draft first: its candidates (573) are a place confirm.py's KEEP looks
        python3 "$EV/final-set.py" $(python3 "$EV/confirm.py" --pool-files "$VN") "$SP/db.jsonl" --json finalset.json --candidates candidates-final.md > finalset.txt 2>&1
        python3 "$EV/confirm.py" "$SP/db.jsonl" --seed "$VN" --candidates candidates-final.md > confirm.txt 2>&1
        p ""; p "## confirm.py (confirm.txt) - GOALS.md step 2: against the pooled true front, the re-enabled genes' classes"; p '```'
        grep -v '^|---' confirm.txt | cut -c1-300 >> "$S"; p '```'
        p "- the restore (next-run.log): $(grep -c 'restore-archives: seed [0-9]* - archived' "$SP/next-run.log" 2>/dev/null) restored - seeds $(sed -n 's/.*restore-archives: seed \([0-9]*\) - archived.*/\1/p' "$SP/next-run.log" 2>/dev/null | tr '\n' ' ')"
        p ""; p "## final-set.py (finalset.txt, finalset.json, candidates-final.md) - GOALS.md step 3's draft from the pool and this run"; p '```'
        sed -n '3p' finalset.txt | cut -c1-400 >> "$S"; grep '^| [0-9]' finalset.txt | cut -c1-200 >> "$S"; grep '^The candidates' finalset.txt | cut -c1-300 >> "$S"; p '```'
    elif [ -f "$OUT/random" ]; then        # 573: the random-search baseline (GOALS.md step 4) - no series run; values, not a test
        python3 "$EV/baseline.py" "$SP/db.jsonl" --seed "$VN" > baseline.txt 2>&1
        p ""; p "## baseline.py (baseline.txt) - GOALS.md step 4: the random run beside the series"; p '```'; grep -v '^|---' baseline.txt | cut -c1-300 >> "$S"; p '```'
        CA=$(ls "$REPO"/results/candidates-final-seed*.md 2> /dev/null | tail -n 1); LT=$(ls "$OUT"/*-loadtest-*/pack/loadtest.md 2> /dev/null | tail -n 1)
        if [ -n "$CA" ] && [ -n "$LT" ]; then            # GOALS.md step 3: the set from the chain's re-measures
            python3 "$EV/final-pick.py" "$CA" "$LT" $(ls "$C"/remote/*/out.json 2> /dev/null) --json finalpick.json > finalpick.txt 2>&1
            p ""; p "## final-pick.py (finalpick.txt, finalpick.json) - GOALS.md step 3 from the re-measures: $(basename "$CA"), the chain's loadtest, $(ls "$C"/remote/*/out.json 2> /dev/null | wc -l) hosts"
            p '```'; grep -v '^|---' finalpick.txt | cut -c1-260 >> "$S"; p '```'
        else p ""; p "## final-pick.py - not run: the candidates ${CA:-none}, the chain's loadtest ${LT:-none}"; fi
    else
    python3 "$EV/stopping.py" "$SP/db.jsonl" ${VN:+--seed "$VN"} --ledger "$REPO/results/stopping-series.md" > stopping.txt 2>&1   # Iteration 554
    p ""; p "## stopping.py (stopping.txt) - GOALS.md's stopping rule, with results/stopping-series.md (appended at step 6)"; p '```'; cut -c1-500 stopping.txt >> "$S"; p '```'
    fi
    python3 "$EV/lifted.py" "$SP/db.jsonl" > lifted.txt 2>&1   # Iteration 557: the freezes lifted at 556, on the true front
    p ""; p "## lifted.py (lifted.txt) - the freezes lifted at 556 on the true front; prediction 556"; p '```'; grep -v '^|---' lifted.txt | cut -c1-300 >> "$S"; p '```'
    python3 "$EV/review-checks.py" rules "$SP/report.md" ${VN:+--seed "$VN"} --db "$SP/db.jsonl" --ledger "$REPO/results/gene-votes.md" > rules.txt 2>&1   # Iteration 438
    p ""; p "## review-checks.py rules (rules.txt) - results/seed63-rules.md's rules, measured"; cut -c1-300 rules.txt | grep -v '^pinned' >> "$S"
fi
# 580 (the owner, 579): the final pick in two chains, neither with a seed step. Chain A re-measures
# results/candidates-final-seedN.md on the laptop: final-pick.py narrows it to results/shortlist-seedN.md (--shortlist).
# Chain B re-measures the shortlist beside dream and the Tegra (REMOTES --also): final-pick.py with every host - the set.
LTN=$(ls "$OUT"/*-loadtest-*/pack/loadtest.md 2> /dev/null | tail -n 1); IDS=$(sed -n 's/.*loadtest\.py --ids \([^ ]*\).*/\1/p' "$C/line" 2> /dev/null | head -1)
if [ -z "$SP" ] && [ -n "$LTN" ] && [ -n "$IDS" ] && [ -f "$REPO/$IDS" ]; then
    case $(basename "$IDS") in candidates-final-seed*) SL=$REPO/results/shortlist-$(basename "$IDS" | sed 's/^candidates-final-//'); WH="chain A - the shortlist to $(basename "$SL")" ;;
                               *) SL=; WH="chain B - the final set, across machines" ;; esac
    python3 "$EV/final-pick.py" "$REPO/$IDS" "$LTN" $(ls "$C"/remote/*/out.json 2> /dev/null) --json finalpick.json ${SL:+--shortlist "$SL"} > finalpick.txt 2>&1
    p ""; p "## final-pick.py (finalpick.txt, finalpick.json) - $WH: $IDS, the chain's loadtest, $(ls "$C"/remote/*/out.json 2> /dev/null | wc -l) hosts"
    p '```'; grep -v '^|---' finalpick.txt | cut -c1-260 >> "$S"; p '```'
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
    N=$(echo "$SP" | sed -n 's|.*-seed\([0-9][0-9]*\)-[^/]*/pack$|\1|p'); L32=$(ls "$REPO"/results/evolve-*-seed$((${N:-1} - 1)).md 2>/dev/null | head -1)
    for o in "$C"/remote/*/out.json; do
        [ -f "$o" ] && [ -n "$L32" ] && grep -q '"cell": *4' "$o" || continue
        python3 "$EV/xcheck.py" --report "$o" --laptop32 "$L32" 2>/dev/null | grep -E '32-bit speeds' | sed "s|^|$(basename "$(dirname "$o")").md, --laptop32 $(basename "$L32"): |" | cut -c1-220 >> "$S"
    done; p '```'
    python3 "$EV/review-checks.py" generic "$C/remote" > generic.txt 2>&1      # Iteration 430: the three classes
    p ""; p "## review-checks.py generic (generic.txt) - the best design across the three machine classes"; p '```'; head -14 generic.txt | cut -c1-200 >> "$S"; p '```'
fi
echo "process-seed: $(wc -l < "$S") lines in $S; the rest in $OUT"
