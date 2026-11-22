#!/bin/sh
# results/drafts/selfhost-variants-723.sh - the cross compiler's fused branches on designs that use them all
# (Iteration 723). portable-fastest d727605472 has =I?BRANCH and DUP?NBRANCH, but not ?NBRANCH, so its DUP?NBRANCH never
# fires (sod16.py's keepbranch needs the fused 0= ?BRANCH), and neither short form. Three variants of its record:
#   pfv-nq    + ?NBRANCH                          (DUP?NBRANCH fires)
#   pfv-short + ?NBRANCH DUP?NBRANCH8 =I?BRANCH8  (and the short forms)
#   pfv-nodn  + ?NBRANCH - DUP?NBRANCH            (the control: no DUP?NBRANCH)
# each through results/drafts/selfhost-ids-714.sh at both widths (export, genes, selfhost-check, the run-time tables),
# then the sizes: the translator's T and the cross compiler's A. pfv-nodn - pfv-nq is one byte a DUP?NBRANCH site (the
# DUP gone) in each, so A's and T's differences should agree; pfv-nq - pfv-short is a byte a short site (A's RELAX is
# exact where shorten() estimates, so A's may be the larger). The last line says PASS or FAIL.
set -u
B=build/selfhost-variants; rm -rf "$B"; mkdir -p "$B"
python3 -I - designs/portable-fastest/record.json "$B/list.jsonl" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1])); out = open(sys.argv[2], 'w')
for i, add, drop in (('a723000001', ['?NBRANCH'], []), ('a723000002', ['?NBRANCH', 'DUP?NBRANCH8', '=I?BRANCH8'], []),
                     ('a723000003', ['?NBRANCH'], ['DUP?NBRANCH'])):
    v = json.loads(json.dumps(r)); v['id'] = i
    v['genome']['ops10'] = [o for o in v['genome']['ops10'] if o not in drop] + add
    out.write(json.dumps(v) + '\n')
EOF
fail=0
for w in "" --32; do
    sh results/drafts/selfhost-ids-714.sh $w "$B/list.jsonl" pfv-nq=a723000001 pfv-short=a723000002 pfv-nodn=a723000003 \
        > "$B/ids$w.log" 2>&1 || fail=1
    grep "^selfhost-ids:" "$B/ids$w.log"
    i=; c=8; [ -n "$w" ] && { i=32; c=4; }
    for n in pfv-nq pfv-short pfv-nodn; do
        d=build/selfhost/check-$n; [ -n "$w" ] && d=$d-32
        echo "$c $n T $(wc -c < build/selfhost-ids/out/$n/image$i.img) A $(wc -c < $d/A.img)" >> "$B/sizes.txt"
    done
done
python3 -I - "$B/sizes.txt" <<'EOF'
import sys
s = {}
for l in open(sys.argv[1]):
    c, n, _, t, _, a = l.split(); s[c, n] = (int(t), int(a))
for c in ('8', '4'):
    nq, sh, nd = s[c, 'pfv-nq'], s[c, 'pfv-short'], s[c, 'pfv-nodn']
    print('%s-byte cells: T / A  pfv-nq %d / %d  pfv-short %d / %d  pfv-nodn %d / %d' % (c, nq[0], nq[1], sh[0], sh[1], nd[0], nd[1]))
    print('  DUP?NBRANCH sites (nodn - nq): translator %d, cross %d' % (nd[0] - nq[0], nd[1] - nq[1]))
    print('  short-form bytes (nq - short): translator %d, cross %d' % (nq[0] - sh[0], nq[1] - sh[1]))
EOF
[ $fail = 0 ] && echo "selfhost-variants: PASS - the three self-host at both widths" || { echo "selfhost-variants: FAIL"; exit 1; }
