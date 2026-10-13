#!/bin/sh
cd /tmp/p13 && runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j38-build.log 2>&1
cat > /tmp/symdiff.py <<'PY'
import os, sys, shutil
tree = sys.argv[1]; out = sys.argv[2]
sys.argv = ['x']; sys.path.insert(0, tree + '/lab/evolve'); import evolve as E
E.setup()
g = E.canon(E.recorded_genome('add5ec8937')); d = os.path.join(E.EV, 'sym'); shutil.rmtree(d, ignore_errors=True)
os.environ['SYMMAP'] = out; E.PROFILING[0] = True
try: eng, img = E.build(g, d)
finally: E.PROFILING[0] = False
print(tree, os.path.getsize(img))
PY
chmod 644 /tmp/symdiff.py
runuser -u claude -- python3 /tmp/symdiff.py /tmp/p13 /tmp/sym-p13.txt > /tmp/j38.log 2>&1
runuser -u claude -- python3 /tmp/symdiff.py /tmp/b45 /tmp/sym-b45.txt >> /tmp/j38.log 2>&1
touch /tmp/job38.done
