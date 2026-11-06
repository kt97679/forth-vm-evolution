#!/bin/sh
# results/drafts/followup-rehearsal-615.sh - lab/evolve/process-followup.sh rehearsed (Iteration 615): seed 87's
# follow-up readings (results/chain-followup87, laid out at 611 by chain-sessions.py) made back into a chain archive of
# that shape - a loadtest pack a laptop step, each remote line's out.json and out-sK.json with their reports - and the
# command run on it with 611's roles; PASS when every reading it lays out is 611's byte for byte, the pooled pick is
# results/followup-pick-seed87.md's (its sessions' paths aside) and the roles are results/drafts/followup-roles-611.py's. From the repository's root,
# as the build user; R=/tmp/followup-rehearsal.
set -u
R=${R:-/tmp/followup-rehearsal}; K=results/chain-followup87; rm -rf "$R"; CH=$R/build/chain-rehearsal
mkdir -p "$CH/packs" "$CH/remote" "$R/pk"; echo b74b8486cb > "$CH/head"; : > "$CH/chain.log"
echo "experiment loadtest.py --ids results/followup-seed87.md --rounds 10 (the rehearsal)" > "$CH/line"
for d in $(ls -d $K/s[0-9]* | sed 's/.*\/s//' | sort -n); do
    s=$K/s$d
    if [ -f "$s/loadtest.md" ]; then
        p=forth-vm-evolution-loadtest-rehearsal-fury-$(printf '%03d' "$d"); mkdir -p "$R/pk/$p/pack"; cp "$s/loadtest.md" "$R/pk/$p/pack/"
        (cd "$R/pk/$p" && tar czf "$CH/packs/$p.tar.gz" pack); echo "next-run: this step DONE - $p.tar.gz, in the chain's archive" >> "$CH/chain.log"
    fi
    for f in "$s"/*.out.json; do
        [ -f "$f" ] || continue; h=$(basename "$f" .out.json); mkdir -p "$CH/remote/$h"
        if [ "$d" = 1 ]; then cp "$f" "$CH/remote/$h/out.json"; [ ! -f "$s/$h.md" ] || cp "$s/$h.md" "$CH/remote/$h.md"
        else cp "$f" "$CH/remote/$h/out-s$d.json"; [ ! -f "$s/$h.md" ] || cp "$s/$h.md" "$CH/remote/$h-s$d.md"; fi
    done
done
for h in "$CH"/remote/*/; do echo "next-run: remote $(basename "$h"): $(ls "$h" | wc -l) sessions measured" >> "$CH/chain.log"; done
(cd "$R/build" && tar czf "$R/forth-vm-evolution-chain-rehearsal-fury-0_tar.gz" chain-rehearsal)
OUT=$R/out DEST=$R/results HANDOFF=results/handoff-relf-601.md PRED=610 sh lab/evolve/process-followup.sh 87 615 \
    fastest=690981ca5b,arm=690981ca5b,knee=c2ef9488ff,smallarm=22420b3b61,memory=fb0d57c8a2,smallest=cea114f47e \
    "$R/forth-vm-evolution-chain-rehearsal-fury-0_tar.gz" > "$R/run.log" 2>&1 || { echo "rehearsal: FAIL - the command (run.log):"; tail -n 3 "$R/run.log"; exit 1; }
nf=0; nd=0
for f in $(cd $K && find . -type f ! -name README.md | sort); do nf=$((nf + 1)); cmp -s "$K/$f" "$R/results/chain-followup87/$f" || nd=$((nd + 1)); done
nl=$(cd "$R/results/chain-followup87" && find . -type f | wc -l)
sed -n '/^# The final set/,$p' results/followup-pick-seed87.md > "$R/pick.611"; sed -n '/^# The final set/,$p' "$R/results/followup-pick-seed87.md" | sed "s|$R/results/|results/|g" > "$R/pick.here"   # the sessions' paths named as 611's
python3 results/drafts/followup-roles-611.py > "$R/roles.611" 2>&1
p1=$([ "$nd" = 0 ] && [ "$nf" = "$nl" ] && echo PASS || echo FAIL); p2=$(cmp -s "$R/pick.611" "$R/pick.here" && echo PASS || echo FAIL)
p3=$(cmp -s "$R/roles.611" "$R/out/roles.txt" && echo PASS || echo FAIL)
# 616: the rule after the follow-up on 611's readings - seed 87's gain confirmed, as 611 found it (the mean -4.2% against
# 8cc7f60d6b, results/followup-roles-seed87.md; binary + image 0.98%, short of 1%)
p5=$(cmp -s results/followup-pick-seed87.json "$R/results/followup-pick-seed87.json" && echo PASS || echo FAIL)   # 617: the pick's JSON, 614's
p4=$(grep -q '^verdict: a gain confirmed' "$R/out/gain.txt" && grep -q 'the mean of the three: .*-4.20%' "$R/out/gain.txt" \
     && grep -q 'binary + image: .*-0.98% - no' "$R/out/gain.txt" && echo PASS || echo FAIL)
echo "rehearsal: the readings $p1 ($nf of 611's files, $nd differ, $nl laid out); the pick $p2; the roles $p3 ($(wc -l < "$R/out/roles.txt") lines); the rule $p4; the pick's JSON $p5"
[ "$p1$p2$p3$p4$p5" = PASSPASSPASSPASSPASS ] && echo "rehearsal: PASS" || { echo "rehearsal: FAIL"; exit 1; }
