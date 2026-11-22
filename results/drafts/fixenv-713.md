# The fixed environment for engine runs - tested (Iteration 713; results/applied-genes-727/fixenv-after-seed96.patch)

The owner: "if you think it will help us find better designs - let's do it" (results/drafts/early-games-713.md: the
memory reading carries the measuring process's environment). The patch: evolve.sh() gives an engine or cputime run
the environment of evolve.run_env - PATH=/usr/bin:/bin, cputime's CPUTIME_JAIL, and EVOLVE_PAD filling the strings of
the environment and the arguments (the exec's file name counted) to 1,024 bytes of the initial stack, so the stack's
pages no longer depend on the caller's environment or the paths' lengths. EVOLVE_KEEP_ENV=1 keeps the caller's.

`python3 results/drafts/fixenv-test-713.py TREE fb0d57c8a2` (the patch applied in TREE; medians of 15, the kernel
workload of 9, [the range]; the sandbox's own environment is 17 KB):

| | the parent's environment as it is | 20 KB larger |
|---|---|---|
| fixed environment | start-up 15 [14-16], kernel 27 [26-28] | start-up 15 [14-15], kernel 27 [27-28] |
| as before (EVOLVE_KEEP_ENV=1) | start-up 19 [18-20], kernel 31 [31-32] | start-up 24 [23-26], kernel 36 [36-38] |

The outputs are alike in every run. 27 pages (108 KB) is the laptop's record for this design (chain A's measure-ids
pack), so the laptop's own environment costs about nothing today, and the sandbox now reads as the laptop does.
What run_env gives: PATH, CPUTIME_JAIL, EVOLVE_PAD of 903 bytes here. All of the search's measuring goes through sh()
(E.measure: measure-ids.py, loadtest.py, xcheck.py on the remotes); lucky.py and run-spread.py, studies of a run's
spread, launch their own. Queued with the reopened search's series (results/applied-genes-727/ORDER.md): its runs then
compare with each other, not with the earlier series' records.
