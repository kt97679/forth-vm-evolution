#!/bin/sh
# results/drafts/chainC-rehearsal-714.sh [CHAIN_B_TGZ] - chain C's processing rehearsed before its archive comes (Iteration
# 714, while chain C runs): chainC-rehearsal-714.py makes a stand-in archive from chain B's, then process-followup.sh
# 96-roles-c runs on it in a scratch clone (/tmp/chainC-rehearsal), and the checks: every one of the list's designs
# re-measured in the pick (dream all, both widths) and in the laptop's readings, its record from the measure-ids pack;
# the Tegra's readings the -arm list's; pool-sizes.py's made-up JIT design in the summary; the roles and holders in
# roles.txt. PASS or FAIL. As the build user, from the repository's top.
set -u
B=${1:-$(ls -t /mnt/user-data/uploads/*forth-vm-evolution-chain-eccab9505-*[_.]tar.gz 2>/dev/null | head -n 1)}
[ -f "$B" ] || { echo "chainC-rehearsal: no chain B archive"; exit 1; }
R=/tmp/chainC-rehearsal; rm -rf "$R"; mkdir -p "$R"
git clone -q . "$R/tree" && ln -s "$PWD/build" "$R/tree/build" || exit 1
cp lab/evolve/followup-roles.py lab/evolve/process-followup.sh "$R/tree/lab/evolve/"   # the tree as it is
python3 results/drafts/chainC-rehearsal-714.py "$B" results/followup-seed96-roles-c.md results/followup-seed96-roles-c-arm.md \
    results/followup-seed96-roles-b.md "$R/work" "$R/forth-vm-evolution-chain-rehearse_tar.gz" || exit 1
# The roles chain C can judge, held by chain B's leaders: the Tegra measures only the JIT-free designs a size or ARMv7
# question needs, so the settled roles (arm, knee, memory, allround) and the handoff's holders lack a class here - 714:
# followup-roles.py judges only the roles --roles names.
ROLES=fastest=d727605472,smallarm=ae99617f06,smallest=219878ec89,fast64=9b15ba26f7,fast32=ea782c6094,smalljit=c6f1c1331b
(cd "$R/tree" && OUT=$R/out HANDOFF=results/handoff-relf-657.md PRED=714 sh lab/evolve/process-followup.sh 96-roles-c 715 "$ROLES" \
    "$R/forth-vm-evolution-chain-rehearse_tar.gz") > "$R/process.log" 2>&1
echo "process-followup: exit $? - $(tail -n 1 "$R/process.log" | cut -c1-120)"
python3 - "$R" <<'EOF'
import json, os, sys
R = sys.argv[1]; T = os.path.join(R, 'tree'); f = []
L = [json.loads(l) for l in open(os.path.join(T, 'results/followup-seed96-roles-c.md')) if l.startswith('{"')]
ARM = {json.loads(l)['id'] for l in open(os.path.join(T, 'results/followup-seed96-roles-c-arm.md')) if l.startswith('{"')}
S = open(os.path.join(R, 'out', 'summary.md')).read()
pick = open(os.path.join(T, 'results/followup-pick-seed96-roles-c.md')).read()
lt = open(os.path.join(T, 'results/chain-followup96-roles-c/s1/loadtest.md')).read()
ra = json.load(open(os.path.join(T, 'results/chain-followup96-roles-c/s1/rage.lan-prebuiltarm.out.json')))
rt = open(os.path.join(R, 'out', 'roles.txt')).read()
for r in L:
    if not str(r.get('src', '')).startswith('measure-ids.py'): f.append('%s: record not from the pack (%s)' % (r['id'], r.get('src')))
    if r['id'] not in lt: f.append('%s: not in s1/loadtest.md' % r['id'])
got = {x['id'] for x in ra['designs'] if not x.get('rejected')}
if got != ARM: f.append('the Tegra: %d designs, the -arm list %d (%d off)' % (len(got), len(ARM), len(got ^ ARM)))
n = len(L)
if '%d candidates, %d re-measured at both widths' % (n, n) not in pick: f.append('the pick: not all %d re-measured' % n)
if '0000000000' not in S or 'pool-sizes.py: 1 below its threshold' not in S: f.append('pool-sizes.py\'s JIT design not in the summary')
if 'measure-ids pack(s)' not in S: f.append('the measure-ids line not in the summary')
for h in ('d727605472', '219878ec89', '9b15ba26f7', 'ea782c6094', 'c6f1c1331b', 'ae99617f06'):
    if h not in rt: f.append('%s not in roles.txt' % h)
print('chainC-rehearsal: %d designs, the Tegra %d - %s' % (n, len(ARM), 'PASS' if not f else 'FAIL'))
for x in f[:20]: print('  ' + x)
EOF
