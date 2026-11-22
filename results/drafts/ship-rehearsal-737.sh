#!/bin/sh
# results/drafts/ship-rehearsal-737.sh [TREE] - the final shipping path rehearsed on the tree as it is (Iteration 737; the
# owner, seed 97 running: "start with 1"): results/drafts/roles-build-718.sh's two phases on the ten roles as designs/
# has them (results/relf-designs-718.md's records), in a scratch clone (/tmp/fzr, its export /tmp/fz), in the order the
# packages allow - then relf-handoff-726.py. AS ROOT (the packages; every build as claude). Nothing is sent or committed.
#   1. CROSS=1's packages (tools/setup-sandbox.sh: lld, qemu-user, libc6-dev-armhf-cross, libgcc-13-dev-armhf-cross) -
#      without them export-arm.py's clang builds find no ARM libgcc; gcc-multilib stays (export-arm builds its 4-byte
#      reference with gcc -m32);
#   2. phase 1 (the stages, validate, export-designs.py, export-arm.py's clang designs);
#   3. the cross GCC in, gcc-multilib out: export-arm.py --gcc (the GCC designs' forth-arm, run by qemu-arm); then
#      gcc-multilib back (the cross GCC out);
#   4. phase 2 with TRANSLATOR= the gate's verdicts (725's, designs/TRANSLATOR-BUILT - a file, as their text has quotes):
#      the self-built ship, the designs' make, test, selfhost, 32 and libc, pack-designs.py;
#   5. every image against designs/'s, and relf-handoff-726.py against results/handoff-relf-726.md.
set -u
T=${1:-/home/claude/forth-vm-evolution}; U="runuser -u claude --"
apt-get install -y gcc-multilib lld qemu-user libc6-dev-armhf-cross libgcc-13-dev-armhf-cross > /tmp/ship-apt1.log 2>&1 || exit 1
N=$(cd "$T" && for d in designs/*/record.json; do printf '%s=%s,' "$(basename "$(dirname "$d")")" "$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['id'])" "$d")"; done | sed 's/,$//')
rm -rf /tmp/fzr /tmp/fz && $U git clone -q "$T" /tmp/fzr || exit 1
cd /tmp/fzr && $U sh results/drafts/roles-build-718.sh 1 /tmp/fzr results/relf-designs-718.md "$N" > /tmp/ship-p1.log 2>&1
apt-get install -y gcc-arm-linux-gnueabihf > /tmp/ship-apt2.log 2>&1 || exit 1
$U python3 lab/evolve/export-arm.py /tmp/fz/designs results/relf-designs-718.md "$N" --gcc arm-linux-gnueabihf-gcc > /tmp/fz/export-arm-gcc.log 2>&1
echo "export-arm --gcc=$? $(tail -n 1 /tmp/fz/export-arm-gcc.log | cut -c1-100)" >> /tmp/fz/status
apt-get install -y gcc-multilib > /tmp/ship-apt3.log 2>&1 || exit 1
grep -v '^#' "$T/designs/TRANSLATOR-BUILT" | sed 's/ /:/' | paste -sd'|' > /tmp/fz/translator; chown claude:claude /tmp/fz/translator
$U sh -c 'cd /tmp/fzr && TRANSLATOR="$(cat /tmp/fz/translator)" sh results/drafts/roles-build-718.sh 2 /tmp/fzr results/relf-designs-718.md "$1"' x "$N" > /tmp/ship-p2.log 2>&1
cat /tmp/fz/status
s=0 d=; for n in $(echo "$N" | tr ',' '\n' | sed 's/=.*//'); do for w in "" 32; do cmp -s "$T/designs/$n/image$w.img" "/tmp/fzr/designs/$n/image$w.img" && s=$((s + 1)) || d="$d $n$w"; done; done
echo "images: $s of 20 the same as designs/'s${d:+ - differ:$d}"
$U python3 results/drafts/relf-handoff-726.py > /tmp/fz/handoff.md 2> /tmp/fz/handoff.err && cmp -s /tmp/fz/handoff.md results/handoff-relf-726.md && echo "relf-handoff-726.py: the same as results/handoff-relf-726.md" || echo "relf-handoff-726.py: DIFFERS or failed ($(tail -n 1 /tmp/fz/handoff.err))"
