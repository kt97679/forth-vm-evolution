#!/bin/sh
cd /tmp/b45
{ echo "== reseed"; runuser -u claude -- sh tools/reseed.sh > /tmp/j39-reseed.log 2>&1; echo "exit $?: $(tail -2 /tmp/j39-reseed.log | head -1)"; } > /tmp/j39.log 2>&1
{ echo "== build"; runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j39-build.log 2>&1; echo "exit $?: $(tail -1 /tmp/j39-build.log)"; } >> /tmp/j39.log 2>&1
{ echo "== sizes"; rm -rf /tmp/engK; mkdir -p /tmp/engK; chown claude:claude /tmp/engK; runuser -u claude -- python3 /tmp/eng-id.py /tmp/b45 /tmp/engK add5ec8937 d3149e10c6 cc6d168e0a 2>&1 | grep -v pinned; } >> /tmp/j39.log 2>&1
touch /tmp/job39.done
