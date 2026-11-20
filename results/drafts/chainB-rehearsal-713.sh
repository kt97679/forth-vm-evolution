#!/bin/sh
# results/drafts/chainB-rehearsal-713.sh [CHAIN_A_TGZ] - chain B's processing rehearsed before its archive comes (Iteration
# 713; the owner: "ensure we are not losing good designs"): chainB-rehearsal-713.py makes a stand-in archive from chain A's,
# then process-followup.sh 96-roles-b runs on it in a scratch clone (/tmp/chainB-rehearsal), and the checks: every one of
# the list's designs re-measured in the pick (dream all, both widths) and in the laptop's readings; the memory the median of five for the lean end and one read
# for the rest; pool-sizes.py's made-up design in the summary. PASS or FAIL. As the build user, from the repository's top.
set -u
A=${1:-$(ls -t /mnt/user-data/uploads/*forth-vm-evolution-chain-517d6310-*[_.]tar.gz 2>/dev/null | head -n 1)}
[ -f "$A" ] || { echo "chainB-rehearsal: no chain A archive"; exit 1; }
R=/tmp/chainB-rehearsal; rm -rf "$R"; mkdir -p "$R"
git clone -q . "$R/tree" && ln -s "$PWD/build" "$R/tree/build" || exit 1
cp lab/evolve/process-followup.sh lab/evolve/ids-records.py lab/evolve/pool-sizes.py "$R/tree/lab/evolve/"   # the tree as it is
python3 results/drafts/chainB-rehearsal-713.py "$A" results/followup-seed96-roles-b.md results/followup-seed96-roles-b-lean.md \
    "$R/work" "$R/forth-vm-evolution-chain-rehearse_tar.gz" || exit 1
ROLES=fastest=782f3ad7ff,arm=3eb59b271d,knee=11a56ff9e4,smallarm=ae99617f06,memory=fb0d57c8a2,smallest=d180351903,fast64=c7c35f9c97,fast32=ee34931cd7,allround=06b188f45b,smalljit=c6f1c1331b
(cd "$R/tree" && OUT=$R/out sh lab/evolve/process-followup.sh 96-roles-b 713 "$ROLES" "$R/forth-vm-evolution-chain-rehearse_tar.gz") > "$R/process.log" 2>&1
echo "process-followup: $(tail -n 1 "$R/process.log" | cut -c1-120)"
python3 - "$R" <<'EOF'
import json, os, re, sys
R = sys.argv[1]; T = os.path.join(R, 'tree'); f = []
L = [json.loads(l) for l in open(os.path.join(T, 'results/followup-seed96-roles-b.md')) if l.startswith('{"')]
lean = {json.loads(l)['id'] for l in open(os.path.join(T, 'results/followup-seed96-roles-b-lean.md')) if l.startswith('{"')}
S = open(os.path.join(R, 'out', 'summary.md')).read()
pick = open(os.path.join(T, 'results/followup-pick-seed96-roles-b.md')).read()
lt = open(os.path.join(T, 'results/chain-followup96-roles-b/s1/loadtest.md')).read()
for r in L:
    if not str(r.get('src', '')).startswith('measure-ids.py'): f.append('%s: record not from the packs (%s)' % (r['id'], r.get('src')))
    want = 5 if r['id'] in lean else 1
    if len(r.get('rss_reads', [0])) != want: f.append('%s: %d reads, %d wanted' % (r['id'], len(r.get('rss_reads', [0])), want))
    if r['id'] not in lt: f.append('%s: not in s1/loadtest.md' % r['id'])
for i in sorted(lean):
    r = [x for x in L if x['id'] == i][0]; reads = r['rss_reads']
    if r['rss'] != sorted(reads)[2] or r['rss'] != reads[0]: f.append('%s: memory %s, reads %s - not the median' % (i, r['rss'], reads))
n = len(L)
if '%d candidates, %d re-measured at both widths' % (n, n) not in pick: f.append('the pick: not all %d re-measured' % n)
if pick.count('%d candidates measured' % n) < 2: f.append('dream: not all %d measured at both widths' % n)
if '0000000000' not in S or 'pool-sizes.py: 1 below its threshold' not in S: f.append('pool-sizes.py\'s design not in the summary')
if 'measure-ids pack(s)' not in S: f.append('the measure-ids line not in the summary')
if '219878ec89' not in S: f.append('219878ec89 (the smallest after the batch) not in the summary\'s roles')
print('chainB-rehearsal: %d designs, %d lean - %s' % (len(L), len(lean), 'PASS' if not f else 'FAIL'))
for x in f[:20]: print('  ' + x)
EOF
