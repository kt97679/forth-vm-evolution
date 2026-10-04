#!/bin/sh
# make-bundle.sh [OUT] - the handoff (prompts/07-git-handoff): a bundle
# with HEAD and master - HEAD is what lets `git pull OUT master` and
# `git clone OUT` work - then the check that it can be received: clone it
# and compare HEAD. OUT defaults to forth-vm-evolution.bundle, the name
# handoffs of this project have used.
set -e
cd "$(dirname "$0")/.."
OUT=${1:-forth-vm-evolution.bundle}
git bundle create "$OUT" HEAD master 2>/dev/null
git bundle list-heads "$OUT"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
git clone -q "$OUT" "$T/check"
if [ "$(git rev-parse HEAD)" = "$(git -C "$T/check" rev-parse HEAD)" ]; then
    echo "PASS - $OUT clones; HEAD $(git rev-parse --short HEAD)"
else
    echo "FAIL - the clone's HEAD is not this HEAD"; exit 1
fi
