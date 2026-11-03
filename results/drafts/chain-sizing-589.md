# Sizing a chain to the three machines (Iteration 589; the owner: "plan runs so that we fully use fury, dream and rage")

**What the owner saw.** Chain C's rage line still running, the laptop idle. A chain gives each machine its own line and
ends when the last is gathered (lab/evolve/remote-checks.sh: gather waits for a host until its deadline). Chain C's lines
at chain B's rates: rage about 2.6 hours (its stages 16 minutes, then 48 designs at 10 rounds - chain B: 35 s a design
at 2 rounds); dream about 20-25 minutes for both widths (chain B: 44 designs at 3 rounds in about 3.5 minutes a width,
load.log); the laptop its four passes of the 40 (alone and loaded, both widths). The ARM line cannot move to x86, so the
laptop and dream wait for rage. Chain C's own line lengths (each host's load.log, the chain's steps) replace these
estimates at its processing.

**Two kinds of idle.** Idle cores while a host measures are deliberate: each host times one design at a time - designs
measured together share cache, memory bandwidth and boost clocks (the laptop's loaded class measures that effect), so
filling those cores changes the readings. Idle machines while the slowest line runs are the fillable kind.

**The filler, when one is wanted: more sessions, not more rounds.** The final pick's weak point is one session against
another (the laptop's 64-bit fast band 0.889 against itself; chain A's laptop order -0.357 against dream), not the
rounds within a session. In chain C's shape dream had room for about five more sessions, the laptop two or three.

**The rule, at chain C's processing.** No machine work is planned after chain C - consolidation, the figures and the
article are the sandbox's. If predictions 3 and 4 hold (rage's and dream's two sessions agree, Spearman 0.8 or more:
results/predictions.md, chain C), the final set rests on two agreeing sessions and no further run is made. If either
fails, a chain D sized to fill the slowest line: the x86 lines repeat whole sessions until rage's expected end, each kept
as its own session for final-pick.py --also-session. That needs a repeat count per line in the chain (next-run.sh's
experiment step on the laptop, REMOTES on the hosts) - built and tested in that processing chat, not before it is needed.

**Considered, not taken.** The gene-retirement tests (deterministic - build-hash at both widths, run-tests, validate,
batch-check; an hour each on the sandbox's one CPU) on dream's idle cores: four patches left, and the setup and the round
trip through the owner cost more than they save.

**591: run before chain C's processing** (the owner: "we can start 12 hours run now, please add whatever makes sense"):
chain D as above - NEXT-RUN's step repeated while lab/evolve/repeat-fits.sh says another session ends by the remote lines'
last deadline; REMOTES' --sessions K in each line (one build, then sessions while one as long as the last fits). Chains C
and D processed together.
