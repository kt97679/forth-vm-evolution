#!/bin/sh
# tools/wait-for.sh FILE PATTERN [SECONDS] - wait until FILE has a line matching the extended regex PATTERN, at most
# SECONDS (default 280: a tool call ends near 300 s), then print FILE's last lines (Iteration 560 - the polling loop
# every processing typed again). Exit 0 when matched, 1 when the time ran out: call it again.
F=$1; P=$2; T=${3:-280}; i=0
while [ "$i" -lt "$T" ]; do grep -qE "$P" "$F" 2>/dev/null && { tail -n 4 "$F" | cut -c1-220; exit 0; }; sleep 5; i=$((i + 5)); done
tail -n 2 "$F" 2>/dev/null | cut -c1-220; echo "wait-for: no '$P' in $F after ${T}s - call again"; exit 1
