#!/bin/sh
# results/drafts/jitdead-cross-723.sh - the gene jitdead in the cross compiler (Iteration 723, on the queued genes'
# branch: results/queued-genes applied). Four JIT records from designs/ with jitdead on: jd-small (small-jit 15eda54ebd:
# jitimg, jitx), jd-bar (best-all-round df097ba2e2), jd-lm (least-memory fb0d57c8a2: no jitimg, no jitx - jit_wends
# the headed words alone, none), jd-small-nx (small-jit with jitx off: the headed words' rows, their pads off the
# ends) - each through results/drafts/selfhost-ids-714.sh at both widths (the export by the translator, the genes,
# selfhost-check: A = B, the gate; the run-time compiler's tables and the five programs' code the translator's). Then
# A's layout lines against the translator's (the design's src/vm-jit-ops.h): JIT_NWENDS, jit_wends, JITN_CODE.
# The last line says PASS or FAIL. From the top, as the build user.
set -u
B=build/jitdead-cross; rm -rf "$B"; mkdir -p "$B"
python3 -I - "$B/list.jsonl" <<'EOF'
import json, sys
out = open(sys.argv[1], 'w')
for i, n, extra in (('a723100001', 'small-jit', {}), ('a723100002', 'best-all-round', {}),
                    ('a723100003', 'least-memory', {}), ('a723100004', 'small-jit', {'jitx': 0})):
    r = json.load(open('designs/%s/record.json' % n)); r['id'] = i
    r['genome']['jitdead'] = 1; r['genome'].update(extra)
    out.write(json.dumps(r) + '\n')
EOF
N="jd-small=a723100001 jd-bar=a723100002 jd-lm=a723100003 jd-small-nx=a723100004"
fail=0
for w in "" --32; do
    sh results/drafts/selfhost-ids-714.sh $w "$B/list.jsonl" $N > "$B/ids$w.log" 2>&1 || fail=1
    grep "^selfhost-ids:" "$B/ids$w.log" | cut -c1-230
    s=src; [ -n "$w" ] && s=src32
    for p in $N; do
        n=${p%%=*}; d=build/selfhost/check-$n; [ -n "$w" ] && d=$d-32
        grep -q jit_wends "build/selfhost-ids/out/$n/$s/vm-jit-ops.h" 2>/dev/null || { echo "  $n$w: no JIT layout in the design (no jitimg, no jitx)"; continue; }
        [ -f "$d/A.img.jit.h" ] || { echo "  $n$w: no A.img.jit.h"; fail=1; continue; }
        python3 -I - "build/selfhost-ids/out/$n/$s/vm-jit-ops.h" "$d/A.img.jit.h" "$n$w" <<'EOF' || fail=1
import sys
key = lambda l: 'jit_wends' if 'jit_wends[][2]' in l else ' '.join(l.split()[:2])
t = {key(l): l for l in open(sys.argv[1]).read().splitlines() if l}
a = {key(l): l for l in open(sys.argv[2]).read().splitlines() if l}
ks = ['#define JIT_NWENDS', 'jit_wends', '#define JITN_CODE']
d = [k for k in ks if t.get(k) != a.get(k)]
print('  %-16s JIT_NWENDS T %s A %s; JITN_CODE T %s A %s; jit_wends %s' % (sys.argv[3],
      t.get(ks[0], '-').split()[-1], a.get(ks[0], '-').split()[-1], t.get(ks[2], '-').split()[-1], a.get(ks[2], '-').split()[-1],
      'the same' if t.get(ks[1]) == a.get(ks[1]) else 'differ (the layouts differ: A is the cross compiler\'s)'))
sys.exit(0 if t.get(ks[2]) == a.get(ks[2]) and t.get(ks[0]) is not None and a.get(ks[0]) is not None else 1)
EOF
    done
done
[ $fail = 0 ] && echo "jitdead-cross: PASS - the four self-host at both widths with jitdead" || { echo "jitdead-cross: FAIL"; exit 1; }
