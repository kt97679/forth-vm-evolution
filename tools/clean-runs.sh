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
#  - pack tarballs past the newest KEEP_PACKS (default 8, by the time in
#    their names): sent back, and recorded in the repository's results/.
# Kept: the lock, and anything else it does not recognise.
# --dry-run: say what it would remove. --held: the caller holds the lock.
set -eu
RUNS=${RUNS:-$(cd "$(dirname "$0")/.." && pwd)/runs}
KEEP=${KEEP:-4}; KEEP_PACKS=${KEEP_PACKS:-8}; DRY=0; HELD=0
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
for d in */; do
    d=${d%/}; h=${d##*-}
    case $d in archived-*|*[!A-Za-z0-9-]*) continue ;; esac
    case $h in ''|*[!0-9a-f]*) continue ;; esac
    [ ${#h} -ge 7 ] || continue
    ls forth-vm-evolution-"$d"-*.tar.gz > /dev/null 2>&1 && echo "$d" >> "$LIST"
done
ls forth-vm-evolution-*.tar.gz 2>/dev/null \
    | sed -n 's/^\(.*-\([0-9]\{8\}-[0-9]\{6\}\)\.tar\.gz\)$/\2 \1/p' | sort \
    | awk -v k="$KEEP_PACKS" '{ a[NR] = $2 } END { for (i = 1; i <= NR - k; i++) print a[i] }' >> "$LIST"
[ -s "$LIST" ] || exit 0
before=$(du -sk . | cut -f1)
na=$(grep -c '^archived-' "$LIST" || true); nt=$(grep -c '\.tar\.gz$' "$LIST" || true); nd=$(( $(wc -l < "$LIST") - na - nt ))
if [ $DRY = 1 ]; then
    echo "clean-runs: would remove $na archives, $nd run directories, $nt pack tarballs:"; sed 's/^/  /' "$LIST"; exit 0
fi
while read -r x; do rm -rf -- "$x"; done < "$LIST"
echo "clean-runs: removed $na archives, $nd run directories, $nt pack tarballs - $(( (before - $(du -sk . | cut -f1)) / 1024 )) MB freed"
