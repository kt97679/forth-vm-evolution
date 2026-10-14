#!/bin/sh
# perf-hold-start.sh START DONE LOG - next-run.sh calls this in the foreground,
# before its chain goes to the background, when counters.py is in the chain
# (Iteration 282). counters.py needs perf's user-space counters, which Ubuntu's
# kernel.perf_event_paranoid (4) refuses, and in the background sudo cannot ask.
# So sudo asks here, once, and lab/evolve/perf-hold.py is left running as root:
# it sets 2 only while counters.py measures, and puts the old value back after.
# perf itself first, while someone is here to fix it (Iteration 283): Ubuntu's perf is a
# wrapper that exits 2 when the tools for the running kernel are not installed - the
# second laptop try stopped so, in the background, perf's own message lost
if ! out=$("${PERF:-perf}" --version 2>&1); then      # PERF: what next-run.sh found (counters.py --find-perf)
    echo "next-run: perf does not run here:" >&2; echo "$out" | sed -n '1,6s/^/    /p' >&2
    echo "next-run: on Ubuntu: sudo apt install linux-tools-\$(uname -r) - for the kernel running now; nothing started" >&2
    exit 1
fi
p=$(cat /proc/sys/kernel/perf_event_paranoid)
[ "$p" -le 2 ] && exit 0                         # counters allowed already: no sudo
if ! [ -t 0 ] && ! [ -t 1 ]; then
    echo "next-run: counters.py needs kernel.perf_event_paranoid at 2 (it is $p), and sudo a terminal to ask on - start next-run.sh from one" >&2
    exit 1
fi
echo "next-run: counters.py needs perf's counters - kernel.perf_event_paranoid is $p. sudo asks once, now;"
echo "next-run: it is set to 2 only while counters.py measures, and put back after (lab/evolve/perf-hold.py)."
sudo -v || { echo "next-run: sudo refused - nothing started" >&2; exit 1; }
# HUP ignored from the fork on (an ignored signal stays ignored across exec), then a session of
# its own: a terminal closing as this returns - a race on a busy machine - cannot end the hold
sudo -n -b sh -c 'trap "" HUP; exec setsid python3 "$0" "$@" < /dev/null > /dev/null 2>&1' "$(cd "$(dirname "$0")" && pwd)/perf-hold.py" "$1" "$2" "$3" || { echo "next-run: perf-hold.py did not start - nothing started" >&2; exit 1; }
