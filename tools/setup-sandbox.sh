#!/bin/sh
# tools/setup-sandbox.sh [BUNDLE] - a new chat's sandbox in one command, as root (Iteration 560; HANDOFF-PROMPT.md's
# steps 0-1, a few calls each chat until then, and a stumble or two: a directory claude cannot write, git refusing root).
# The compilers (gcc-multilib for the 4-byte cells, clang, clang-19 for preserve_none) and the 32-bit asm/ headers, when
# missing; the clone, as the user claude, in /home/claude/forth-vm-evolution (DEST=), with the owner's identity. BUNDLE:
# default the newest forth-vm-evolution-claude-*.bundle in /mnt/user-data/uploads not ending in -checkpoint. CHECK=1
# also starts the build, run-tests and validate detached (/tmp/setup-check/status) - not for a returned seed:
# lab/evolve/process-run.sh builds and checks. Run from any clone of the bundle:
#   git clone -q /mnt/user-data/uploads/<bundle> /tmp/s && sh /tmp/s/tools/setup-sandbox.sh && rm -rf /tmp/s
set -u
[ "$(id -u)" = 0 ] || { echo "setup-sandbox: as root"; exit 1; }
B=${1:-$(ls -t /mnt/user-data/uploads/forth-vm-evolution-claude-*.bundle 2>/dev/null | grep -v -- '-checkpoint' | head -n 1)}
D=${DEST:-/home/claude/forth-vm-evolution}
[ -f "$B" ] || { echo "setup-sandbox: no bundle (BUNDLE, or one in /mnt/user-data/uploads)"; exit 1; }
if ! dpkg -s gcc-multilib clang clang-19 > /dev/null 2>&1; then
    apt-get update -qq > /tmp/setup-apt.log 2>&1
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq gcc-multilib clang clang-19 >> /tmp/setup-apt.log 2>&1 ||
        echo "setup-sandbox: apt-get failed - /tmp/setup-apt.log"
fi
[ -e /usr/include/asm ] || ln -s x86_64-linux-gnu/asm /usr/include/asm
if [ -d "$D/.git" ]; then echo "setup-sandbox: $D exists - left as it is"
else mkdir -p "$D" && chown claude:claude "$D" && runuser -u claude -- git clone -q "$B" "$D" || { echo "setup-sandbox: the clone failed"; exit 1; }; fi
runuser -u claude -- git -C "$D" config user.name "Kirill Timofeev" && runuser -u claude -- git -C "$D" config user.email kt97679@gmail.com
echo "setup-sandbox: $(basename "$B") -> $D at $(runuser -u claude -- git -C "$D" log --oneline -1 | cut -c1-70)"
echo "setup-sandbox: $(dpkg -s gcc-multilib clang-19 2>/dev/null | grep -c '^Status: install ok') of 2 packages in; asm/ $([ -e /usr/include/asm ] && echo there)"
if [ "${CHECK:-0}" = 1 ]; then
    rm -rf /tmp/setup-check; mkdir /tmp/setup-check; chown claude:claude /tmp/setup-check
    runuser -u claude -- setsid nohup sh -c "cd $D && S=/tmp/setup-check/status
        env LAYOUTS=1 bash tools/build-stages.sh > /tmp/setup-check/build.log 2>&1; echo build=\$? >> \$S
        bash tools/run-tests.sh > /tmp/setup-check/tests.log 2>&1; echo \"run-tests=\$? \$(tail -n 1 /tmp/setup-check/tests.log)\" >> \$S
        python3 lab/evolve/evolve.py --validate > /tmp/setup-check/validate.log 2>&1; echo \"validate=\$? \$(grep -c IDENTICAL /tmp/setup-check/validate.log) of 7 IDENTICAL\" >> \$S
        echo DONE >> \$S" > /dev/null 2>&1 &
    echo "setup-sandbox: the build, run-tests and validate started - sh tools/wait-for.sh /tmp/setup-check/status DONE"
fi
