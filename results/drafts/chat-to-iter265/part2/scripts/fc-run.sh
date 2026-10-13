#!/bin/sh
# /tmp/fc-run.sh OUT ID... - the counting harness over kernel and corpus, fsys 4 and 5
out=$1; shift
cd /tmp/batch43
runuser -u claude -- env TREE=/tmp/batch43 python3 /tmp/fsys-count.py "$@" --db results/evolve-amd-ryzen-7-pro-8840hs-seed42.md --db results/evolve-amd-ryzen-7-pro-8840hs-seed40.md --levels 4,5 --works kernel,corpus --words 30 > "$out" 2>&1
echo "exit $?" >> "$out.done"
