#!/bin/sh
# lab/evolve/process-followup.sh N ITERATION ROLES [ARCHIVE] - a returned follow-up chain's processing, its mechanical
# part, in one command (Iteration 615: 611's steps by hand, results/followup-pick-seed87.md's and
# results/followup-roles-seed87.md's). In order:
#   1. the archive unpacked as process-seed.sh unpacks it (OUT/chain-*, each pack in OUT/<pack>);
#   2. the chain's own lines - its NEXT-RUN line and head, the laptop's steps done and skipped, each remote line's
#      sessions - and each loadtest pack's step;
#   3. the readings laid out by session: chain-sessions.py OUT DEST/chain-followupN (kept, as results/chain-followup87);
#   4. the pooled pick: final-pick.py over every session -> DEST/followup-pick-seedN.md (its title and command, as 611's)
#      and OUT/pick.json;
#   5. each role against its holder: lab/evolve/followup-roles.py -> OUT/roles.txt (PRED= the iteration whose predictions
#      it prints, HANDOFF= the handoff file, default results/handoff-relf-611.md).
# OUT/summary.md, printed at the end, is the screen to judge from. N: the portable run's seed (results/followup-seedN.md
# the list); ROLES: the handoff's portable roles, role=id,... (followup-roles.py); ARCHIVE: default the newest
# forth-vm-evolution-chain-*_tar.gz in /mnt/user-data/uploads. OUT=/tmp/followup, DEST=results - the rehearsal's another
# (results/drafts/followup-rehearsal-615.sh: 611's readings made into an archive, every output against 611's). About a
# minute, as the build user. The judgment stays in the chat: the roles (the owner's trades - 611),
# results/followup-roles-seedN.md, the package and designs/ when a role changes (pack-designs.py, export-designs.py).
set -u
N=${1:?N}; I=${2:?ITERATION}; ROLES=${3:?ROLES}
A=${4:-$(ls -t /mnt/user-data/uploads/forth-vm-evolution-chain-*_tar.gz 2>/dev/null | head -n 1)}
cd "$(dirname "$0")/../.." || exit 1
O=${OUT:-/tmp/followup}; D=${DEST:-results}; C=results/followup-seed$N.md; K=$D/chain-followup$N; F=$D/followup-pick-seed$N.md
die() { echo "process-followup: STOP - $*"; exit 1; }
[ -f "$A" ] || die "no chain archive (ARCHIVE, or forth-vm-evolution-chain-*_tar.gz in /mnt/user-data/uploads)"
[ -f "$C" ] || die "no $C"
[ ! -e "$K" ] || die "$K there already - remove it to lay the readings out again"
case $A in /*) ;; *) A=$PWD/$A ;; esac
rm -rf "$O"; mkdir -p "$O"; S=$O/summary.md
(cd "$O" && tar xzf "$A") 2> "$O/unpack.log" || die "cannot unpack $A ($O/unpack.log)"     # 1.
H=$(ls -d "$O"/chain-* 2>/dev/null | head -n 1); [ -n "$H" ] || die "no chain-* in $A"
for t in "$H"/packs/*.tar.gz; do [ -f "$t" ] || continue; p=$O/$(basename "$t" .tar.gz); mkdir -p "$p"; tar xzf "$t" -C "$p" || die "cannot unpack $t"; done
{                                                                                              # 2.
echo "# Seed $N's follow-up chain - $(basename "$A") (lab/evolve/process-followup.sh, Iteration $I)"
echo
echo "the chain at $(cat "$H/head" 2>/dev/null): $(grep -o 'experiment loadtest.py --ids [^ ]*' "$H/line" | sort | uniq -c | sed 's/^ *//') listed"
echo "the laptop: $(grep -c 'this step DONE' "$H/chain.log") steps done, $(ls "$O"/*-loadtest-*/pack/loadtest.md 2>/dev/null | wc -l) loadtest packs"
grep -h -E 'skipp|deadline|not started|FAIL|STOP|crash|Traceback' "$H/chain.log" | sed 's/^next-run: /  /' | cut -c1-200 | head -n 8
grep -h 'sessions measured' "$H/chain.log" | sed 's/^next-run: /  /'
echo
} > "$S"
python3 lab/evolve/chain-sessions.py "$O" "$K" > "$O/sessions.log" 2>&1 || die "chain-sessions.py ($O/sessions.log)"   # 3.
head -n 1 "$O/sessions.log" >> "$S"
ss=$(ls -d "$K"/s[0-9]* 2>/dev/null | sed 's/.*\/s//' | sort -n)                                # 4.
[ -n "$ss" ] || die "one session only - $K is flat; final-pick.py on it by hand"
also=$(for k in $ss; do [ "$k" = 1 ] || printf -- '--also-session %s/s%s ' "$K" "$k"; done)
python3 lab/evolve/final-pick.py "$C" "$K"/s1/loadtest.md "$K"/s1/*.out.json $also --json "$O/pick.json" > "$O/pick.out" 2>&1 \
    || die "final-pick.py ($O/pick.out)"
n() { ls "$K"/s[0-9]*/"$1" 2>/dev/null | wc -l; }
last=$(echo "$ss" | tail -n 1)
{ echo "# Seed $N's best beside the portable designs found before, re-measured on three machines, every session pooled (Iteration $I)"
  echo
  echo "\`python3 lab/evolve/final-pick.py $C $K/s1/loadtest.md $K/s1/*.out.json --also-session $K/s2 ... s$last\` - the laptop $(n loadtest.md) sessions (10 rounds), dream $(n dream.lan-prebuilt64.out.json) at 8-byte cells and $(n dream.lan-prebuilt32.out.json) at 4-byte, the Tegra $(n rage.lan-prebuiltarm.out.json) (lab/evolve/process-followup.sh). The roles against ${HANDOFF:-results/handoff-relf-611.md}: results/followup-roles-seed$N.md."
  echo
  cat "$O/pick.out"; } > "$F"
python3 lab/evolve/followup-roles.py "$C" "$K" --roles "$ROLES" --handoff "${HANDOFF:-results/handoff-relf-611.md}" \
    ${PRED:+--predictions "$PRED"} > "$O/roles.txt" 2>&1 || die "followup-roles.py ($O/roles.txt)"   # 5.
{ echo; echo "the pick: $F (OUT/pick.json); its set:"; grep '^| [0-9]' "$O/pick.out" | cut -c1-160 | head -n 16
  echo; cat "$O/roles.txt"; } >> "$S"
cat "$S"
echo "process-followup: DONE - $S; the readings $K, the pick $F; judge the roles, then results/followup-roles-seed$N.md"
