#!/bin/sh
cd /tmp/base45 && runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/j33-build.log 2>&1
echo "base build: $(tail -1 /tmp/j33-build.log)" > /tmp/j33.log
runuser -u claude -- python3 /tmp/eng-id.py /tmp/base45 /tmp/engH add5ec8937 d3149e10c6 cc6d168e0a dde890d478 2>&1 | grep -v pinned | sed 's/^/before: /' >> /tmp/j33.log
runuser -u claude -- python3 /tmp/eng-id.py /tmp/b45 /tmp/engI add5ec8937 d3149e10c6 cc6d168e0a dde890d478 2>&1 | grep -v pinned | sed 's/^/after:  /' >> /tmp/j33.log
touch /tmp/job33.done
