#!/bin/sh
# clean-runs.sh [--dry-run] [--held] - tidy the runs directory (RUNS,
# default runs/ in the clone - Iteration 84). Iteration 63; since Iteration 83
# lab/evolve/next-run.sh runs it before every run (the owner asked).
#
# Removed:
#  - archived-* directories past the newest KEEP (default 4, and never
#    fewer than CARRY_LAST or COMPARE_LAST - the next run's carry and the
#    comparison read the newest; with either 0, "all", none is removed);
#    their databases travelled in the runs' pack tarballs;
#  - run directories, NAME-<commit> (7 or more hex digits), whose pack
#    tarball is here: it holds their logs;
#  - run directories whose pack tarball is in a finished chain's packs/ (Iteration 541; finished - 549);
#  - chain tarballs (forth-vm-evolution-chain-*) past the newest KEEP_CHAINS
#    (default 2): each copies its chain directory, which stays (Iteration 541);
#  - other pack tarballs past the newest KEEP_PACKS (default 8, by the time
#    in their names): sent back, and recorded in the repository's results/;
#  - in every finished chain (its status not running or stopping): the
#    copies sent to the remotes - remote/repo.bundle, a copy of the
#    repository, and remote/*/bins.tar.gz, binaries a build remakes
#    (Iteration 541).
# Never removed: a seed pack (forth-vm-evolution-seedN-*.tar.gz), wherever it
# is, or anything holding one - the runs' records, which the article's
# figures are recomputed from (GOALS.md); a listed one is kept and reported
# as a bug. Kept: the lock, and anything else it does not recognise.
# --dry-run: say what it would remove, each with its size. --held: the caller
# holds the lock.
set -eu
RUNS=${RUNS:-$(cd "$(dirname "$0")/.." && pwd)/runs}
KEEP=${KEEP:-4}; KEEP_PACKS=${KEEP_PACKS:-8}; KEEP_CHAINS=${KEEP_CHAINS:-2}; DRY=0; HELD=0
for a in "$@"; do
    case $a in
        --dry-run) DRY=1 ;; --held) HELD=1 ;;
        *) echo "usage: sh tools/clean-runs.sh [--dry-run] [--held]" >&2; exit 2 ;;
    esac
done
[ -d "$RUNS" ] || exit 0
if [ $HELD = 0 ]; then
    exec 9> "$RUNS/.lock"
    flock -n 9 || { echo "a run holds $RUNS/.lock - not now" >&2; exit 1; }
fi
cd "$RUNS"
LIST=$(mktemp); trap 'rm -f "$LIST"' EXIT
C=${CARRY_LAST:-4}; P=${COMPARE_LAST:-4}
if [ "$C" != 0 ] && [ "$P" != 0 ]; then
    [ "$C" -gt "$KEEP" ] && KEEP=$C
    [ "$P" -gt "$KEEP" ] && KEEP=$P
    n=$(ls -d archived-* 2>/dev/null | wc -l)
    ls -d archived-* 2>/dev/null | sort | head -n $(( n > KEEP ? n - KEEP : 0 )) >> "$LIST"
fi
in_finished_chain() {   # Iteration 549: a running chain's later steps copy its first step's logs from that step's
    for p in chain-*/packs/forth-vm-evolution-"$1"-*.tar.gz; do    # directory - seed 74's experiments failed so
        [ -f "$p" ] || continue
        case $(head -n 1 "${p%%/packs/*}/status" 2>/dev/null || true) in running|stopping|'') continue ;; esac
        return 0
    done
    return 1
}
for d in */; do
    d=${d%/}; h=${d##*-}
    case $d in archived-*|*[!A-Za-z0-9-]*) continue ;; esac
    case $h in ''|*[!0-9a-f]*) continue ;; esac
    [ ${#h} -ge 7 ] || continue
    { ls forth-vm-evolution-"$d"-*.tar.gz > /dev/null 2>&1 || in_finished_chain "$d"; } \
        && echo "$d" >> "$LIST"
done
newest_past() {    # the tarballs on stdin, oldest first, all but the newest $1 (by the time in their names)
    sed -n 's/^\(.*-\([0-9]\{8\}-[0-9]\{6\}\)\.tar\.gz\)$/\2 \1/p' | sort \
        | awk -v k="$1" '{ a[NR] = $2 } END { for (i = 1; i <= NR - k; i++) print a[i] }'
}
ls forth-vm-evolution-chain-*.tar.gz 2>/dev/null | newest_past "$KEEP_CHAINS" >> "$LIST"
ls forth-vm-evolution-*.tar.gz 2>/dev/null | grep -v -e '^forth-vm-evolution-chain-' -e '^forth-vm-evolution-seed[0-9]' \
    | newest_past "$KEEP_PACKS" >> "$LIST" || true
for c in chain-*/; do
    [ -d "$c" ] || continue; c=${c%/}
    st=$(head -n 1 "$c/status" 2>/dev/null || true)
    case $st in running|stopping|'') continue ;; esac
    ls -d "$c"/remote/repo.bundle "$c"/remote/*/bins.tar.gz 2>/dev/null >> "$LIST" || true
done
G=$(mktemp)
while read -r x; do
    case $x in *forth-vm-evolution-seed[0-9]*.tar.gz)
        echo "clean-runs: BUG - a seed pack was listed, kept: $x" >&2; continue ;; esac
    if [ -d "$x" ] && find "$x" -name 'forth-vm-evolution-seed[0-9]*.tar.gz' | grep -q .; then
        echo "clean-runs: BUG - $x holds a seed pack, kept" >&2; continue; fi
    echo "$x"
done < "$LIST" > "$G"
mv "$G" "$LIST"
[ -s "$LIST" ] || exit 0
before=$(du -sk . | cut -f1)
na=$(grep -c '^archived-' "$LIST" || true); nb=$(grep -c '/remote/' "$LIST" || true)
nt=$(grep -v '/' "$LIST" | grep -c '\.tar\.gz$' || true); nd=$(( $(wc -l < "$LIST") - na - nb - nt ))
what="$na archives, $nd run directories, $nt pack tarballs, $nb copies in finished chains"
if [ $DRY = 1 ]; then
    echo "clean-runs: would remove $what:"
    while read -r x; do printf '  %9s KB  %s\n' "$(du -sk -- "$x" | cut -f1)" "$x"; done < "$LIST"
    echo "  $(tr '\n' '\0' < "$LIST" | xargs -0 du -skc -- | tail -1 | cut -f1) KB in all"; exit 0
fi
while read -r x; do rm -rf -- "$x"; done < "$LIST"
echo "clean-runs: removed $what - $(( (before - $(du -sk . | cut -f1)) / 1024 )) MB freed"
