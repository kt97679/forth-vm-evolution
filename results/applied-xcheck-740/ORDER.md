# xcheck.py's --also finds the roles' holders (Iteration 740) - applied at 740

Found by results/drafts/guard-challengers-740.sh (the guard challengers' path through a follow-up chain, rehearsed):
dream's and the Tegra's lines take the genomes of the ids a chain asks for (`--also @LIST`) only from results/evolve-*-seed*.md,
results/candidates-*.md and the laptop's database - and two of today's holders, fastest-x86-64's 9b15ba26f7 and
fastest-x86-32's 11f956db93, are in none of the files (chains A-C found them in seed 96's database, which the laptop no
longer has once the series runs). The roles' follow-up after the series would have measured neither on dream, and
followup-roles.py would have refused ("holders without a reading in every class"). The patch adds
results/relf-designs-*.md, the roles' records, to the lookup. Seed runs ask for no ids (REMOTES is empty), so seed 98
is unchanged. Check, then apply, from the repository's top:

    env RECORD=1 sh tools/batch-check.sh
    git apply results/applied-xcheck-740/xcheck-holders-740.patch

batch-check (740, on Iteration 739 with this batch committed - 1 patch): PASS - run-tests PASS (the generators: 118
paths), validate 7 of 7 IDENTICAL, the jail PASS. Applied at 740 (git apply, here; results/drafts/guard-
challengers-740.sh then measured all six on dream's stand-in).

