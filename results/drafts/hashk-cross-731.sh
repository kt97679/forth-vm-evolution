#!/bin/sh
# results/drafts/hashk-cross-731.sh [NAME ...] - hashk in the self-hosting compiler checked (Iteration 731): each role
# (default smallest - the Forth HASH, cv8-hashk.4's HASH8 swapped by the X8 rule; portable-fastest - HASH an engine op,
# klookup's C walk, the cached top; small-jit - the JIT) with hashk on, a record of its own (evolve.py's gid), exported
# by lab/evolve/export-designs.py into /tmp/hxd/designs, then tools/selfhost-ship.sh STRICT=1 on it: export-genes.py's
# genes.4 (G-HASHK, the overlay where HASH is no op), tools/selfhost-check.sh at 8- and 4-byte cells (A = B, the
# evolver's gate - the corpus, the kernel workload, the far tests), the self-built images shipped, each design's own
# `make selfhost selfhost32`. As the build user, from the top of a built and validated tree with the patch.
set -u
NAMES=${*:-smallest portable-fastest small-jit}
O=/tmp/hxd; rm -rf "$O"; mkdir -p "$O"
python3 -I - "$O/records.jsonl" $NAMES > "$O/pairs" <<'EOF' || exit 1
import json, os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'lab', 'evolve')); out = sys.argv[1]; names = sys.argv[2:]; sys.argv = ['x']
import evolve as E
pairs = []
with open(out, 'w') as f:
    for n in names:
        r = json.load(open(os.path.join('designs', n, 'record.json')))
        g = E.canon(dict(r['genome'], hashk=1)); i = E.gid(g)
        f.write(json.dumps(dict(r, id=i, genome=g)) + '\n'); pairs.append('%s=%s' % (n, i))
print(','.join(pairs))
EOF
echo "records: $(cat "$O/pairs")"
python3 lab/evolve/export-designs.py "$O/designs" "$O/records.jsonl" "$(cat "$O/pairs")" > "$O/export.log" 2>&1
echo "export-designs=$? $(tail -n 1 "$O/export.log" | cut -c1-120)"
STRICT=1 sh tools/selfhost-ship.sh "$O/designs" $NAMES > "$O/ship.log" 2>&1
echo "selfhost-ship=$? $(tail -n 1 "$O/ship.log" | cut -c1-140)"
grep -h "selfhost: .* ok - rebuilt\|FAIL" "$O/ship.log" | cut -c1-150
for n in $NAMES; do printf '%s genes.4: ' "$n"; grep -h "G-HASHK\|cv8-hashk" "$O/designs/$n/genes.4" | tr '\n' ' ' | cut -c1-160; echo; done
