#!/bin/sh
# tools/rage-check.sh [HOST] [RESULTS.md] - the Tegra's engines checked on the Tegra itself, from the laptop, before its
# check of a front (Iteration 571; the owner: before seed 84, the confirmation run). In this repository, as the owner:
#   sh tools/rage-check.sh                 HOST rage.lan, RESULTS the newest results/evolve-*-seedN.md
# HEAD bundled and copied to HOST:fve-ragecheck/, cloned there, its stages built (tools/build-stages.sh), then
# tools/arm-cross-check.py RESULTS run there natively: the hand-made stages and the front's GCC designs built by the
# host's cc without the C library (engine/rt-linux-armv7.c, Iteration 570) - alive, and fib and apps as the stage s6
# with the C library gives them. What qemu cannot say: the host's GCC (16 on rage) with the runtime, and the engine's
# start on a 32-bit host - the legacy-layout re-exec, which under qemu fails and is skipped. In the foreground, each
# design's line as it comes; the log kept in HOST:fve-ragecheck/check.log (the clone removed after a pass). Exit 0: every
# design passed - rage's check of the next front will build as tested. The Tegra is slow: its stages and about ten
# designs take a while (Iteration 571 could not time it). Run it while no chain's check runs there. SSH and SCP may
# name stand-ins (results/drafts/rage-check-e2e-571.sh); RAGECHECK_OPTS more arguments for arm-cross-check.py (--n K).
# RAGECHECK_CMD (Iteration 646): another command run there in its place - 'sh tools/rage-designs-check.sh', designs/' forth-arm.
set -u
HOST=${1:-rage.lan}; REPO=$(cd "$(dirname "$0")/.." && pwd)
RES=${2:-$(ls "$REPO"/results/evolve-*-seed*.md 2>/dev/null | sort -V | tail -n 1)}
[ -f "$RES" ] || { echo "rage-check: no results file (RESULTS.md)"; exit 2; }
SSH=${SSH:-ssh}; SCP=${SCP:-scp}; O="-o BatchMode=yes -o ConnectTimeout=10"; D=fve-ragecheck
B=$(mktemp /tmp/rage-check-XXXXXX.bundle) && rm -f "$B" || exit 2
git -C "$REPO" bundle create "$B" HEAD > /dev/null 2>&1 || { echo "rage-check: git bundle failed"; exit 2; }
echo "rage-check: $HOST, $(git -C "$REPO" log --oneline -1 | cut -c1-60), $(basename "$RES")"
$SSH $O "$HOST" "mkdir -p $D && rm -rf $D/repo" < /dev/null && $SCP -q $O "$B" "$HOST:$D/repo.bundle" \
    || { rm -f "$B"; echo "rage-check: $HOST not reached (ssh, no password asked)"; exit 2; }
rm -f "$B"; R=results/$(basename "$RES")
$SSH $O "$HOST" "cd $D && git -c advice.detachedHead=false clone -q repo.bundle repo && cd repo && echo 'rage-check: building the stages there' && \
    { LAYOUTS=1 bash tools/build-stages.sh > ../build.log 2>&1 || { echo 'rage-check: build-stages.sh FAILED ($D/build.log)'; exit 1; }; } && \
    { ${RAGECHECK_CMD:-python3 tools/arm-cross-check.py $R ${RAGECHECK_OPTS:-}}; echo \"rage-check: exit \$?\"; } 2>&1 | tee ../check.log; grep -qx 'rage-check: exit 0' ../check.log \
    && { cd .. && rm -rf repo repo.bundle; echo 'rage-check: PASS'; } || { echo 'rage-check: FAILED - $D/check.log, $D/repo kept'; exit 1; }" < /dev/null
