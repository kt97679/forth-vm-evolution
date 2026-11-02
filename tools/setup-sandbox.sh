#!/bin/sh
# tools/setup-sandbox.sh [BUNDLE] - a new chat's sandbox in one command, as root (Iteration 560; HANDOFF-PROMPT.md's
# steps 0-1, a few calls each chat until then, and a stumble or two: a directory claude cannot write, git refusing root).
# The compilers (gcc-multilib for the 4-byte cells, clang, clang-19 for preserve_none) and the 32-bit asm/ headers, when
# missing; the clone, as the user claude, in /home/claude/forth-vm-evolution (DEST=), with the owner's identity. BUNDLE:
# default the newest forth-vm-evolution-claude-*.bundle in /mnt/user-data/uploads not ending in -checkpoint. CHECK=1
# also starts the build, run-tests and validate detached (/tmp/setup-check/status) - not for a returned seed:
# lab/evolve/process-run.sh builds and checks. Run from any clone of the bundle:
#   git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && sh /tmp/s/tools/setup-sandbox.sh && rm -rf /tmp/s
# Iteration 567 (the owner; prompts/22-setup-is-a-script.md): THE environment - idempotent, and the one place a
# requirement lives. Run it again rather than mending by hand: each step looks before it acts and says "there" or what
# it did; a second run changes nothing. CHECK=1 does not start the checks while they run (their shell's pid in
# /tmp/setup-check/pid) or once they are DONE (rm -rf /tmp/setup-check to run them again); cut off by the turn's end,
# it starts them again. A package, link, owner, identity or tree a session needs and does not find goes in here, in
# that turn - a manual step written in a document instead is a bug in this script.
# CROSS=1 (568): the packages to build ARMv7 engines with clang and run them under qemu-arm.
# SCRATCH=DIR (567 - a scratch tree, HANDOFF.md's "for a batch in progress", made by hand until then, and git refused
# root in it): master of DEST cloned into DIR as claude, the identity, results/pending's patches applied in ORDER.md's
# order (PENDING=DIR another batch's directory, 588: results/queued-consolidation), each committed, and the stages built detached - DIR.status (build=N, DONE), DIR.log. A DIR already there is left
# as it is. Delete them before the bundle: rm -rf DIR DIR.status DIR.log
# Iteration 590: the two detached jobs start by runuser and setsid -f directly, never through asme with a redirect and &:
# dash kept the caller's stdout open (fds 10-11) in the subshell running the function, which waited on runuser, which
# waited on the job - the setup call held to the job's end, past 300 s (589's "cause not found"; reproduced with a sleep).
set -u
[ "$(id -u)" = 0 ] || { echo "setup-sandbox: as root"; exit 1; }
B=${1:-$(ls -t /mnt/user-data/uploads/forth-vm-evolution-claude-*.bundle 2>/dev/null | grep -v -- '-checkpoint' | head -n 1)}
D=${DEST:-/home/claude/forth-vm-evolution}
[ -f "$B" ] || { echo "setup-sandbox: no bundle (BUNDLE, or one in /mnt/user-data/uploads)"; exit 1; }
asme() { runuser -u claude -- "$@"; }
# Iteration 573: apt-get detached and waited for, at most WAIT seconds (default 240) - a tool call ends near 300 s, and
# the compilers' install ran past it in a fresh sandbox (the call killed, dpkg finishing by luck); killed mid-dpkg, a
# sandbox breaks. Not done in time: the clone made, nothing that needs the packages started - run this again.
apt_bg() {
    n=$1; shift; st=/tmp/setup-apt-$n.status
    if dpkg -s "$@" > /dev/null 2>&1; then echo "setup-sandbox: the $n there"; return 0; fi
    p=$(cat "/tmp/setup-apt-$n.pid" 2> /dev/null)
    if [ -z "$p" ] || ! kill -0 "$p" 2> /dev/null; then
        rm -f "$st"
        setsid nohup sh -c "echo \$\$ > /tmp/setup-apt-$n.pid; { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $*; } >> /tmp/setup-apt.log 2>&1; echo \$? > $st" > /dev/null 2>&1 &
        echo "setup-sandbox: the $n installing, detached (/tmp/setup-apt.log)"
    else echo "setup-sandbox: the $n installing already (pid $p)"; fi
    w=0; while [ ! -f "$st" ] && [ "$w" -lt "${WAIT:-240}" ]; do sleep 5; w=$((w + 5)); done
    [ -f "$st" ] || { echo "setup-sandbox: the $n still installing - run this again when it ends (/tmp/setup-apt.log)"; return 1; }
    [ "$(cat "$st")" = 0 ] && dpkg -s "$@" > /dev/null 2>&1 && { echo "setup-sandbox: the $n installed"; return 0; }
    echo "setup-sandbox: apt-get failed ($n) - /tmp/setup-apt.log"; return 1
}
PKG=ok
apt_bg compilers gcc-multilib clang clang-19 || PKG=
[ -e /usr/include/asm ] || ln -s x86_64-linux-gnu/asm /usr/include/asm
if [ "${CROSS:-0}" = 1 ] && [ -n "$PKG" ]; then    # Iteration 568: ARMv7 builds by clang here (results/drafts/tegra-cross-568.py) - never
    # gcc-arm-linux-gnueabihf: Ubuntu removes gcc-multilib for it, and the 32-bit x86 builds with it
    apt_bg arm-cross lld qemu-user libc6-dev-armhf-cross libgcc-13-dev-armhf-cross || PKG=
fi
if [ -d "$D/.git" ]; then                 # 567: left as it is, and said how it stands against the bundle
    H=$(asme git -C "$D" rev-parse HEAD); M=$(git bundle list-heads "$B" 2>/dev/null | awk '$2 == "refs/heads/master" {print $1}')
    if [ "$H" = "$M" ]; then echo "setup-sandbox: $D there, at the bundle's master - left as it is"
    elif asme git -C "$D" merge-base --is-ancestor "$M" HEAD 2> /dev/null; then echo "setup-sandbox: $D there, ahead of the bundle (this session's commits) - left as it is"
    else echo "setup-sandbox: $D there at $(echo "$H" | cut -c1-7), NOT the bundle's ${M:-?} - left as it is (DEST= another directory to start from the bundle)"; fi
else mkdir -p "$D" && chown claude:claude "$D" && asme git clone -q "$B" "$D" || { echo "setup-sandbox: the clone failed"; exit 1; }; fi
asme git -C "$D" config user.name "Kirill Timofeev" && asme git -C "$D" config user.email kt97679@gmail.com
echo "setup-sandbox: $(basename "$B") -> $D at $(asme git -C "$D" log --oneline -1 | cut -c1-70)"
echo "setup-sandbox: $(dpkg -s gcc-multilib clang-19 2>/dev/null | grep -c '^Status: install ok') of 2 packages in; asm/ $([ -e /usr/include/asm ] && echo there)"
if [ "${CHECK:-0}" = 1 ] && [ -z "$PKG" ]; then echo "setup-sandbox: the checks not started - the packages are not in yet"
elif [ "${CHECK:-0}" = 1 ]; then
    P=$(cat /tmp/setup-check/pid 2>/dev/null)
    if [ -n "$P" ] && grep -q setup-check "/proc/$P/cmdline" 2>/dev/null; then echo "setup-sandbox: the checks run already (pid $P) - not started again"
    elif grep -qx DONE /tmp/setup-check/status 2>/dev/null; then echo "setup-sandbox: the checks done already - $(grep -v DONE /tmp/setup-check/status | tr '\n' ' ')(rm -rf /tmp/setup-check to run them again)"
    else
        rm -rf /tmp/setup-check; mkdir /tmp/setup-check; chown claude:claude /tmp/setup-check
        runuser -u claude -- setsid -f nohup sh -c "echo \$\$ > /tmp/setup-check/pid; cd $D && S=/tmp/setup-check/status
            env LAYOUTS=1 bash tools/build-stages.sh > /tmp/setup-check/build.log 2>&1; echo build=\$? >> \$S
            bash tools/run-tests.sh > /tmp/setup-check/tests.log 2>&1; echo \"run-tests=\$? \$(tail -n 1 /tmp/setup-check/tests.log)\" >> \$S
            python3 lab/evolve/evolve.py --validate > /tmp/setup-check/validate.log 2>&1; echo \"validate=\$? \$(grep -c IDENTICAL /tmp/setup-check/validate.log) of 7 IDENTICAL\" >> \$S
            echo DONE >> \$S" > /dev/null 2>&1
        echo "setup-sandbox: the build, run-tests and validate started - sh tools/wait-for.sh /tmp/setup-check/status DONE"
    fi
fi
if [ -n "${SCRATCH:-}" ] && [ -z "$PKG" ]; then echo "setup-sandbox: the scratch tree not made - the packages are not in yet"
elif [ -n "${SCRATCH:-}" ]; then                                     # 567: a scratch tree, as HANDOFF.md asks
    X=$SCRATCH
    if [ -d "$X/.git" ]; then echo "setup-sandbox: scratch $X there at $(asme git -C "$X" log --oneline -1 | cut -c1-60) - left as it is"
    else
        mkdir -p "$X" && chown claude:claude "$X" && asme git clone -q "$D" "$X" || { echo "setup-sandbox: the scratch clone failed"; exit 1; }
        asme git -C "$X" config user.name "Kirill Timofeev" && asme git -C "$X" config user.email kt97679@gmail.com
        Q=${PENDING:-results/pending}
        n=0; for p in $(sed -n "s|^ *git apply \\($Q/[^ ]*\\.patch\\).*|\\1|p" "$X/$Q/ORDER.md" 2>/dev/null); do
            asme git -C "$X" apply --index "$p" && asme git -C "$X" commit -q -m "scratch: $p" || { echo "setup-sandbox: $p does not apply in $X"; exit 1; }
            n=$((n + 1)); done
        rm -f "$X.status"; touch "$X.status" "$X.log"; chown claude:claude "$X.status" "$X.log"
        runuser -u claude -- setsid -f nohup sh -c "cd $X && LAYOUTS=1 bash tools/build-stages.sh > $X.log 2>&1; echo build=\$? >> $X.status; echo DONE >> $X.status" > /dev/null 2>&1
        echo "setup-sandbox: scratch $X - master, $n pending patch(es) applied; the build started - sh tools/wait-for.sh $X.status DONE"
    fi
fi
