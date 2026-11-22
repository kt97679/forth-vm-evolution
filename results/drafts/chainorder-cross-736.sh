#!/bin/sh
# results/drafts/chainorder-cross-736.sh - chainorder (and numfirst and hashk with it) in the self-hosting compiler checked
# (Iteration 736). Designs, each a record of its own (evolve.py's gid): ROLE:GENES, the genes switched on - default
# smallest, portable-fastest and small-jit with chainorder (the Forth walk, NEXT-NFA88 as NEXT-NFA8; klookup's C walk, the
# engine's PREVNFA; the tag - cv8t-chainorder.4 - and the JIT's bf_prev), and smallest and small-jit with chainorder,
# numfirst and hashk together. Exported by lab/evolve/export-designs.py into /tmp/cox/designs, then tools/selfhost-ship.sh
# STRICT=1 (export-genes.py's genes.4 - the chainorder file before cv8b.4, G-CO-HOT, G-TRIM8, G-ONCE - the fixed point at
# 8- and 4-byte cells, the evolver's gate, shipped, `make selfhost selfhost32`); then probe programs (a word defined and
# used, a hot name redefined at run time, numbers) on each self-built image against the translator's, at both widths,
# and the held-out parse workload's instructions (cachegrind) on the self-built image against the shipped self-built
# design without the genes. As the build user, from the top of a built tree with the patch.
set -u
SPEC=${*:-smallest:chainorder portable-fastest:chainorder small-jit:chainorder smallest:chainorder,numfirst,hashk small-jit:chainorder,numfirst,hashk}
O=${COX:-/tmp/cox}; rm -rf "$O"; mkdir -p "$O"
python3 -I - "$O/records.jsonl" $SPEC > "$O/pairs" <<'EOF' || exit 1
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'lab', 'evolve')); out = sys.argv[1]; spec = sys.argv[2:]; sys.argv = ['x']
import evolve as E
pairs = []
with open(out, 'w') as f:
    for s in spec:
        n, gs = s.split(':'); r = json.load(open(os.path.join('designs', n, 'record.json')))
        g = E.canon(dict(r['genome'], **{k: 1 for k in gs.split(',')})); i = E.gid(g)
        assert all(E.express(g).get(k) for k in gs.split(',')), (s, 'a gene not expressed')
        f.write(json.dumps(dict(r, id=i, genome=g)) + '\n'); pairs.append('%s-%s=%s' % (n, gs.replace(',', '-'), i))
print(','.join(pairs))
EOF
P=$(cat "$O/pairs"); echo "records: $P"
# export-designs names each design by the pair's left side; the roles' records.json name them as their roles
python3 lab/evolve/export-designs.py "$O/designs" "$O/records.jsonl" "$P" > "$O/export.log" 2>&1
echo "export-designs=$? $(tail -n 1 "$O/export.log" | cut -c1-120)"
NAMES=$(printf '%s' "$P" | tr ',' '\n' | cut -d= -f1 | tr '\n' ' ')
for n in $NAMES; do for w in "" 32; do cp "$O/designs/$n/image$w.img" "$O/$n-translator$w.img"; done; done
STRICT=1 sh tools/selfhost-ship.sh "$O/designs" $NAMES > "$O/ship.log" 2>&1
echo "selfhost-ship=$? $(tail -n 1 "$O/ship.log" | cut -c1-140)"
grep -h "selfhost: .* ok - rebuilt\|FAIL" "$O/ship.log" | cut -c1-150
for n in $NAMES; do
    printf '%s genes.4: ' "$n"; grep -h "G-CHAINORDER\|chainorder.4\|G-TRIM8" "$O/designs/$n/genes.4" | tr '\n' ' ' | cut -c1-160; echo
    for w in "" 32; do
        e=$O/designs/$n/forth$w; same=same
        for p in ': FOO 42 ; FOO . 7 DUP + . CR' ': DUP 99 ; 1 DUP . CR' 'VARIABLE V 5 V ! V @ V @ * . CR' '77 . -5 . HEX 1A . DECIMAL CR' ': 123 456 ; 123 . 8 . CR'; do
            a=$(printf '%s\n' "$p" | (cd "$O/designs/$n" && "$e" "$O/designs/$n/image$w.img") 2>&1 | tr -d '\r' | grep -v '^Welcome' | tr '\n' '|')
            b=$(printf '%s\n' "$p" | (cd "$O/designs/$n" && "$e" "$O/$n-translator$w.img") 2>&1 | tr -d '\r' | grep -v '^Welcome' | tr '\n' '|')
            [ "$a" = "$b" ] || same="DIFFER on '$p': self-built '$a', translator '$b'"
        done
        echo "  $n${w:+ ($w-bit)}: self-built $(wc -c < "$O/designs/$n/image$w.img") B (the translator's $(wc -c < "$O/$n-translator$w.img") B); the probes $same"
    done
done
python3 -I - "$O" $NAMES <<'EOF'
import os, re, subprocess, sys
O, names = sys.argv[1], sys.argv[2:]
sys.path.insert(0, os.path.join(os.getcwd(), 'lab', 'evolve')); sys.argv = ['x']
import evolve as E
prog = E.program('parse')
def ir(eng, img, cwd):
    p = subprocess.run(['valgrind', '--tool=cachegrind', '--cache-sim=no', '--cachegrind-out-file=/dev/null', eng, img], input=prog, cwd=cwd,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3600)
    n = re.findall(rb'I\s+refs:\s+([\d,]+)', p.stderr); return (int(n[-1].replace(b',', b'')) if n else 0), p.stdout
for n in names:
    role = n.split('-chainorder')[0]; d = os.path.join(O, 'designs', n); s = os.path.join('designs', role)
    a, oa = ir(os.path.join(d, 'forth'), os.path.join(d, 'image.img'), d)
    b, ob = ir(os.path.join(d, 'forth'), os.path.join(O, n + '-translator.img'), d)
    c, oc = ir(os.path.join(s, 'forth'), os.path.join(s, 'image.img'), s) if os.path.exists(os.path.join(s, 'forth')) else (0, b'')
    print('  %s: parse instructions - self-built %d, the translator\'s %d (%.3f), the shipped self-built %s without (%s); outputs %s' % (
        n, a, b, a / b if b else 0, role, '%.3f' % (a / c) if c else '-', 'same' if oa == ob == (oc or oa) else 'DIFFER'))
EOF
