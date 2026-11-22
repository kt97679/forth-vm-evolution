#!/bin/sh
# results/drafts/numfirst-cross-736.sh [NAME ...] - numfirst in the self-hosting compiler checked (Iteration 736): each role
# (default smallest - the Forth form, cv8-numfirst.4's INTERPRET8 and HEADER8 by the X8 rule; portable-fastest - the C
# form, the engine's (FIND) and HEADER8; small-jit - the C form under the tag, cv8t-numfirst.4, the JIT) with numfirst on,
# a record of its own (evolve.py's gid), exported by lab/evolve/export-designs.py into /tmp/nfx/designs, then
# tools/selfhost-ship.sh STRICT=1 on it: export-genes.py's genes.4 (the file last in G-OVERLAYS, DIGITS? and NF-FLAG in
# G-HEADERLESS, G-SKIP: the marker, and INTERPRET8 in the C form), tools/selfhost-check.sh at 8- and 4-byte cells (A = B,
# the evolver's gate), the self-built images shipped, each design's own `make selfhost selfhost32`. Then numfirst's
# probe programs (results/drafts/numfirst-probe-733.py's) on every self-built image at both widths, against the outputs
# off and on gave there. As the build user, from the top of a built tree with the patch.
set -u
NAMES=${*:-smallest portable-fastest small-jit}
O=/tmp/nfx; rm -rf "$O"; mkdir -p "$O"
python3 -I - "$O/records.jsonl" $NAMES > "$O/pairs" <<'EOF' || exit 1
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'lab', 'evolve')); out = sys.argv[1]; names = sys.argv[2:]; sys.argv = ['x']
import evolve as E
pairs = []
with open(out, 'w') as f:
    for n in names:
        r = json.load(open(os.path.join('designs', n, 'record.json')))
        g = E.canon(dict(r['genome'], numfirst=1)); i = E.gid(g)
        f.write(json.dumps(dict(r, id=i, genome=g)) + '\n'); pairs.append('%s=%s' % (n, i))
print(','.join(pairs))
EOF
echo "records: $(cat "$O/pairs")"
python3 lab/evolve/export-designs.py "$O/designs" "$O/records.jsonl" "$(cat "$O/pairs")" > "$O/export.log" 2>&1
echo "export-designs=$? $(tail -n 1 "$O/export.log" | cut -c1-120)"
for n in $NAMES; do for w in "" 32; do cp "$O/designs/$n/image$w.img" "$O/$n-translator$w.img"; done; done
STRICT=1 sh tools/selfhost-ship.sh "$O/designs" $NAMES > "$O/ship.log" 2>&1
echo "selfhost-ship=$? $(tail -n 1 "$O/ship.log" | cut -c1-140)"
grep -h "selfhost: .* ok - rebuilt\|FAIL" "$O/ship.log" | cut -c1-150
for n in $NAMES; do
    printf '%s genes.4: ' "$n"; grep -h "numfirst\|G-SKIP\|NUMFIRST-MARK\|DIGITS" "$O/designs/$n/genes.4" | tr '\n' ' ' | cut -c1-200; echo
    for w in "" 32; do
        e=$O/designs/$n/forth$w; i=$O/designs/$n/image$w.img; bad=0; out=
        for p in '77 . -5 . 0 . -0 . HEX 10 . 1A . DECIMAL 2 BASE ! 101 . DECIMAL 3 1+ . CR' ': 123 456 ; 123 . -7 . 8 . CR' ': -9 1 ; -9 . 9 . CR' '2 BASE ! 12 . CR'; do
            o=$(printf '%s\n' "$p" | (cd "$O/designs/$n" && "$e" "$i") 2>&1 | tr -d '\r' | grep -v '^Welcome\|^OK$' | tr '\n' '|')
            out="$out$o"
        done
        want='77 -5 0 0 10 1A 101 4 |456 -7 8 |1 9 |Undefined word 12|'
        [ "$out" = "$want" ] && r=same || r="DIFFER: $out"
        echo "  $n${w:+ ($w-bit)}: self-built $(wc -c < "$i") B (the translator's $(wc -c < "$O/$n-translator$w.img") B); the probe $r"
    done
done
