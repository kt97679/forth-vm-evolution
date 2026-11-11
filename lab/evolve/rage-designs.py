#!/usr/bin/env python3
"""lab/evolve/rage-designs.py [DB...] - designs/' forth-arm checked on the Tegra itself, as a chain's laptop step
(Iteration 647; the owner: "please include rage check into next run"). NEXT-RUN's `experiment rage-designs.py` runs it
on the laptop - next-run.sh passes every database here, unused: tools/rage-check.sh with RAGECHECK_CMD='sh
tools/rage-designs-check.sh' - HEAD bundled and copied to the Tegra, its stages built there, then lab/evolve/export-arm.py
natively: the GCC designs without the JIT (portable-arm, portable-small, least-memory) built by the Tegra's GCC as the
lab's build() builds them - the bytes it measured - and each Makefile's `make forth-arm` matching them byte for byte and
running ': SQ DUP * ; 7 SQ .' to 49. Its lines to stdout (the step's rage-designs.md, in the chain's archive); exit 0
only on PASS. Never beside a chain's check on rage (its timing): a chain without a rage line in REMOTES. RAGE_HOST:
default rage.lan; SSH and SCP may name stand-ins (results/drafts/rage-check-e2e-571.sh)."""
import os, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env = dict(os.environ, RAGECHECK_CMD='sh tools/rage-designs-check.sh')
r = subprocess.run(['sh', os.path.join(root, 'tools', 'rage-check.sh'), os.environ.get('RAGE_HOST', 'rage.lan')],
                   cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
print('# designs/\' forth-arm on the Tegra (lab/evolve/rage-designs.py, Iteration 647)\n')
print(r.stdout.rstrip())
print('\nrage-designs: %s' % ('PASS' if r.returncode == 0 else 'FAILED (rage-check.sh exit %d)' % r.returncode))
sys.exit(r.returncode)
