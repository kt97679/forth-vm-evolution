# The runner's protocol - one command, one archive, a clean stop (Iterations 302-303)

The owner's requirements (Iteration 302): one command on the laptop, one archive back
with every step's results and every log; made even when a step failed, a failed step
not costing the others; privileges asked at the start, anything needing them later
done by a root helper forked at the start that polls for its condition and chowns what
it creates; the code pulled once; the checks once per chain; the measurements first.
And (Iteration 303): a clear way to stop a run; cleanup on every exit, so an
interrupted run leaves nothing half done; and at every start, a cleanup of what an
earlier run left when the machine crashed or the run was killed. And (Iteration 304):
status and stop, and a monitor that follows the run's progress.

This is the specification lab/evolve/next-run.sh is rebuilt to (HANDOFF.md, open item 0).

## What the current runner does, and lacks (read at Iteration 303)

- Detaches with `nohup sh "$0" ... &` - no session of its own; the chain's evolver
  starts every engine and build with start_new_session=True, so a signal to the
  runner's process group would miss them. No stop command: stopping means finding
  processes by hand.
- An flock on runs/.lock - released when its holder dies, so a crash leaves no stale
  lock. A state file, build/evolve/next-run.state: the same NEXT-RUN at the same commit
  resumes an interrupted seed run - stop then start again is a pause.
- A fresh run moves, never deletes: earlier outputs to runs/archived-*, with a manifest.
- Interruption can leave: a pack's staging directory (runs/*/pack), a half-written
  tarball under its final name, perf-hold's start and done files, and - if perf-hold
  itself were killed - kernel.perf_event_paranoid at 2 until a reboot.
- perf-hold.py, running as root, creates runs/perf-hold.log if it is not there: a
  root-owned file in the owner's home, against his rule.

## Commands

- `sh lab/evolve/next-run.sh` - start NEXT-RUN's chain (or a chain given on the
  command line). Everything below happens.
- `sh lab/evolve/next-run.sh status` - whether a chain runs, its step, since when, its log.
- `sh lab/evolve/next-run.sh monitor` - follow the chain's log as it grows, from its
  start: read-only - Ctrl-C ends the watching, never the run. It ends by itself when
  the chain does, saying how (finished, failed at a step, stopped) and where the
  archive is. With no chain running, the last one's ending and archive.
- `sh lab/evolve/next-run.sh stop` - stop the running chain: SIGTERM to every process
  descending from the chain's leader (the process tree by parent links - the engines'
  and builds' own sessions included), 30 s to go, then SIGKILL; the chain's trap packs.

The start, status, monitor and stop all name the others in what they print, so the
next command is always on the screen.

## The start, in the foreground - the owner there

1. Recover what an earlier chain left (below).
2. Pull the newest bundle, once (local changes outside results/ refuse, as now).
3. If the chain measures: find perf, ask sudo once, fork the root helper.
4. Detach - setsid, so a closed terminal does not end it - and record the chain in
   runs/.chain: leader pid, start time, the chain's line, commit, log path.

## The chain, detached

- The checks once, at its start (build, tests, validate, jail). If they fail, no step
  that needs a working build runs; the archive is still made.
- The steps in order: the measurements (missmap.py; counters.py --extra with Zen 4's
  cache events) on the front that just finished; the seed run (fresh or resumed, as
  now); the comparison. A failed step is recorded and the next runs unless it needs the
  failed one's output (the comparison needs the seed run's database).
- One log for the whole chain - every step appends to it, so monitor follows one
  file - and each step's own output also in its own log, in the chain's directory.
- During the seed run, a progress line in the chain's log every five minutes: the
  generation, designs measured, the front's size, the time left before the evolution
  stops - so a monitor shows the hours of evolution, not silence.

## The end, always - a trap on EXIT, TERM, INT and HUP

- One archive, runs/forth-vm-evolution-chain-<commit>-<host>-<time>.tar.gz: each step's
  results, every log - the runner's, build, tests, validate, jail, evolve, perf-hold -
  the chain record, and STATUS: finished, failed at step X, or stopped by the owner.
  Written as .partial and renamed, so nothing half written carries the final name.
- Each step's own pack kept beside it, for the first real use.
- Staging directories removed; runs/.chain marked done.

## Before every start: recovery

- runs/.chain naming a leader that no longer runs: that chain was interrupted - a
  crash, a kill -9. Its logs and partial outputs packed into an "interrupted" archive;
  its staging directories and *.partial files removed; the perf setting restored if
  perf-hold left a record of changing it (root is asked at the start anyway; a reboot
  restores it too). Then the start goes on - a seed run resumes, as now, if NEXT-RUN is
  the same.
- runs/.chain naming a leader still running: refuse, naming `next-run.sh status` and
  `next-run.sh stop`.
- Any root-owned file under the clone: chowned back (root is there at the start), and
  named in the log.

## Root: chown everything, watch the chain

- perf-hold.py chowns every file it creates or appends to, to the owner of the runs
  directory; its records go where the recovery finds them.
- It holds for every measurement of the chain (a start and a done file each), and
  exits - restoring - when the chain's leader is gone, as well as when its own time
  runs out.

## Tested here before the laptop relies on it

- A chain in miniature - a few-minute seed run, the comparison at one round, the
  measurements against a stand-in perf that refuses a stripped binary: the archive's
  contents, every log in it.
- stop in mid-run: no process left - the engines' sessions included - the archive says
  stopped, nothing staged left, the lock free.
- kill -9 of the whole tree, a crash: the next start finds it, packs it, resumes the
  seed run.
- monitor through a whole miniature chain: it shows each step and the progress lines,
  ends by itself with the archive's path; Ctrl-C in it leaves the chain running.
- After each: no root-owned file under the clone.
