#!/bin/sh
# lab/evolve/repeat-fits.sh CHAIN SECONDS [NOW] - exit 0 when one more session of SECONDS, started NOW (default: now),
# ends by the chain's deadline; 1 otherwise, saying why on stdout (Iteration 591, chain D - the owner, 589: "plan runs so
# that we fully use fury, dream and rage"). next-run.sh's then_next asks it before a repeat of the same experiment
# ("A then A then A"): the laptop's sessions repeat while the remote lines run, and stop when another would end past
# them. The deadline: the latest of the remote lines' deadlines (CHAIN/remote/*/until, epoch seconds - each line's own
# stacked on its host's earlier ones); with no line started, the chain's start (CHAIN/line's time) plus REPEAT_MINUTES
# (default 690 - the owner's 12 hours less the pack), so a chain whose remotes all failed still ends in its window.
set -u
C=${1:?CHAIN}; S=${2:?SECONDS}; NOW=${3:-$(date +%s)}
D=$(cat "$C"/remote/*/until 2> /dev/null | sort -n | tail -1)
if [ -z "$D" ]; then
    T=$(stat -c %Y "$C/line" 2> /dev/null) || { echo "repeat-fits: no deadline and no $C/line - not repeated"; exit 1; }
    D=$(( T + ${REPEAT_MINUTES:-690} * 60 )); why="the chain's start + ${REPEAT_MINUTES:-690} minutes"
else why="the remote lines' last deadline"; fi
E=$(( NOW + S ))
if [ "$E" -le "$D" ]; then echo "repeat-fits: another session of $S s ends $(( (D - E) / 60 )) minutes before $why"; exit 0; fi
echo "repeat-fits: another session of $S s would end $(( (E - D) / 60 )) minutes past $why - not repeated"; exit 1
