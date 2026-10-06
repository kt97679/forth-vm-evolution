#!/bin/sh
# clean-runs.sh [--yes] [--keep N] - tidy the runs directory
# (RUNS, default ~/forth-vm-evolution-runs; Iteration 63, the owner asked).
#
# Kept as they are: every pack tarball at the top (forth-vm-evolution-*.tar.gz
# - each run's database, report and logs, what was sent back), the newest N
# archived-* directories (default 4: the comparison and the next run's carry
# read them), the newest run directory, records/, and anything it does not
# recognise. Packed: the older archived-* directories and the older run
# directories (seedN-<commit>, <experiment>-<commit>), each into
# records/NAME.tar.gz, then removed - nothing lost, only made small.
# Without --yes it only says what it would do. It takes the runs' lock, so
# it never runs beside a run.
set -eu
RUNS=${RUNS:-$HOME/forth-vm-evolution-runs}
KEEP=4; YES=0
while [ $# -gt 0 ]; do
    case $1 in
        --yes) YES=1 ;;
        --keep) shift; KEEP=${1:?--keep needs a number} ;;
        *) echo "usage: sh tools/clean-runs.sh [--yes] [--keep N]" >&2; exit 2 ;;
    esac
    shift
done
[ -d "$RUNS" ] || { echo "nothing to do: no $RUNS"; exit 0; }
exec 9> "$RUNS/.lock"
flock -n 9 || { echo "a run holds $RUNS/.lock - not now" >&2; exit 1; }
cd "$RUNS"

LIST=$(mktemp); trap 'rm -f "$LIST"' EXIT
n=$(ls -d archived-* 2>/dev/null | wc -l)
ls -d archived-* 2>/dev/null | sort | head -n $(( n > KEEP ? n - KEEP : 0 )) >> "$LIST"
# run directories end in the 8 hex digits of their commit; the newest stays
ls -dt -- *-[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f] 2>/dev/null \
    | while read -r d; do [ -d "$d" ] && echo "$d"; done | tail -n +2 >> "$LIST"

if [ ! -s "$LIST" ]; then echo "nothing to pack: $(du -sh . | cut -f1) in $RUNS"; exit 0; fi
echo "in $RUNS ($(du -sh . | cut -f1), $(find . -type f | wc -l) files):"
while read -r d; do printf '   %-44s %6s %6s files\n' "$d" "$(du -sh "$d" | cut -f1)" "$(find "$d" -type f | wc -l)"; done < "$LIST"
if [ "$YES" -ne 1 ]; then
    echo "would pack these $(wc -l < "$LIST") into records/NAME.tar.gz and remove them - again with --yes to do it"
    exit 0
fi
mkdir -p records
while read -r d; do
    t=records/$d.tar.gz; [ ! -e "$t" ] || t=records/$d-$(date -u +%Y%m%d-%H%M%S).tar.gz
    tar -czf "$t" "$d" && tar -tzf "$t" > /dev/null && rm -rf "$d"
done < "$LIST"
echo "packed $(wc -l < "$LIST") into records/: now $(du -sh . | cut -f1), $(find . -type f | wc -l) files"
