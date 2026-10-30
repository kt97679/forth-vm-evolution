#!/bin/sh
# tools/disposable.sh PATH REASON ... - a line in /tmp/handoff-disposable.txt, the format handoff-check.py reads (Iteration
# 568; results/drafts/automation-audit-567.md, candidate 8 - typed by hand until then, once in a format it refused):
# "PATH REASON", one per path - a PATH listed again has its reason replaced. DISPOSABLE=FILE another list.
set -u
P=${1:?PATH}; shift; R=${*:?REASON - why it can go}
F=${DISPOSABLE:-/tmp/handoff-disposable.txt}
case $P in /*) ;; *) P=$(pwd)/$P ;; esac
touch "$F" && grep -v -F -x -e "$P" "$F" | awk -v p="$P" 'index($0, p " ") != 1' > "$F.new"; mv "$F.new" "$F"
echo "$P $R" >> "$F" && chmod a+r "$F" && echo "disposable: $P - $R ($(wc -l < "$F") in $F)"
