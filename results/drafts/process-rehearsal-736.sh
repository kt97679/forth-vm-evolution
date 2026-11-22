#!/bin/sh
# results/drafts/process-rehearsal-736.sh BUNDLE - seed 97's processing rehearsed before its archive comes (Iteration 736;
# the owner: "start with 1 and 2"): a stand-in made by the laptop's own path - the bundle cloned into /tmp/sr/repo, then
# `next-run.sh seed 97 widths` with POP=8 GENS=3 JOBS=2 REMEASURE=2 (BUNDLES the bundle's folder: the pull a no-op) - and
# processed in a fresh clone of this tree (/tmp/pr, built): process-seed.sh, draft-results.py, process-checks.sh (OUT=
# /tmp/pr-checks), process-records.sh 97. Each step's status printed; the logs under /tmp/pr-*. As the build user.
set -u
B=${1:?a bundle}; R=$(pwd)
rm -rf /tmp/sr /tmp/pr /tmp/pr-process /tmp/pr-checks; mkdir -p /tmp/sr
git clone -q "$B" /tmp/sr/repo || exit 1
(cd /tmp/sr/repo && BUNDLES=$(dirname "$B") RUNS=/tmp/sr/runs POP=8 GENS=3 JOBS=2 REMEASURE=2 sh lab/evolve/next-run.sh seed 97 widths) | tail -n 2
while [ "$(cat /tmp/sr/runs/chain-*/status 2>/dev/null)" != done ]; do sleep 30; done
A=$(ls -t /tmp/sr/runs/forth-vm-evolution-chain-*.tar.gz | head -n 1); echo "stand-in: $A"
git clone -q "$R" /tmp/pr && cd /tmp/pr && env LAYOUTS=1 bash tools/build-stages.sh > /tmp/pr.build 2>&1; echo "build=$?"
sh lab/evolve/process-seed.sh "$A" /tmp/pr-process > /tmp/pr.seed 2>&1; echo "process-seed=$? $(grep -c Traceback /tmp/pr-process/*.txt | grep -v ':0' | tr '\n' ' ')"
python3 lab/evolve/draft-results.py /tmp/pr-process --iteration 0 > /tmp/pr.draft 2>&1; echo "draft-results=$? $(tail -n 1 /tmp/pr.draft)"
DB=$(ls /tmp/pr-process/forth-vm-evolution-seed97-*/pack/db.jsonl)
OUT=/tmp/pr-checks DB=$DB sh lab/evolve/process-checks.sh results/evolve-amd-ryzen-7-pro-8840hs-seed97.md > /dev/null 2>&1; cat /tmp/pr-checks/status
DB=$DB sh lab/evolve/process-records.sh 97 0 | sed 's/^/  /'
