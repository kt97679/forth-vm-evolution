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

## Remote checks - the front on two other machines (Iteration 306)

The owner's machines, both reached from the laptop by ssh without a password, both
slower than the laptop: **dream.lan**, an Intel Core i7-6700 (Skylake, 4 cores and 8
threads, x86-64) - a different microarchitecture, the check against tuning to Zen 4;
and **rage.lan**, an NVIDIA Tegra (ARMv7, 32-bit, 4 cores, Gentoo, GCC 16.2;
results/armv7-tegra.md) - a different instruction set. On a 32-bit host a design builds
with 4-byte cells and the C library, and the JIT does not express (jit_on: x86-64 only):
there only the designs without the JIT are themselves. Both are idle during runs, and
have GCC but neither clang nor perf (the owner, Iteration 307): a design built with clang
(compiler, tailpn) is not itself on them, so the sample keeps to GCC-built designs.

The owner's suggestion (Iteration 308) - the laptop's binaries to dream, and builds for
the Tegra made on the laptop - taken for dream: no build uses -march or -mtune (the x86-64
baseline, the JIT's stencils too), and the engines are static with raw system calls, so
the laptop's engines and images run on dream unchanged. xcheck.py --sample --bundle builds
the sampled designs and s6 on the laptop into one tarball (four designs and s6: 70 KB);
dream measures those very binaries (--prebuilt) - a ranking that moves there moved for
the microarchitecture alone, clang-built and JIT designs included, and dream builds
nothing. For rage, native builds first (GCC 16, no JIT, 4-byte cells): they work now,
and the first run times them. Cross-building on the laptop - a second target in the
evolver's build (4-byte cells, the C library, a cross compiler, no JIT) and the laptop's
cross toolchain (gcc-arm-linux-gnueabihf; tools/arm-qemu-check.sh did it for SPN) - if
the Tegra's own builds prove too slow.

- **When:** in every chain, right after the checks, alongside the seed run - on the
  front that just finished, as the measurements are. The remote machines do the work;
  the laptop only copies, polls by ssh and fetches - nothing that moves its timings.
  So they add no hours to a chain.
- **What:** on dream, a sample of 24 designs of the joint front - the 6 fastest, 6
  about the best Q, the 6 smallest, 6 between - and s6, as the laptop built them; the six selection workloads and
  sieve; 3 rounds. On rage, 12 designs without the JIT, and s6; 2 rounds. Each design's
  speed against s6 there; the Spearman correlation with the laptop's speeds for the same
  designs, as heldout.py gives it for workloads; where the laptop's fastest rank there;
  the designs that move most, with their genes.
- **Time:** estimated, to be replaced by the first run's own times - dream 20-30
  minutes (the stages built once a commit, 24 designs built, the measurements), rage
  1-1.5 hours (the image translation is pure Python, "minutes on a slow machine"). Both
  well inside a 6-hour seed run. Each has a hard limit - when the laptop's evolution
  stops; what is finished by then is packed, the rest named as not measured.
- **First contact, automatic:** each host's environment into the archive (uname, cc,
  clang and python3 versions, /bin/sh, the locale, free disk, cores, the CPU governor)
  and a feasibility check - s6 built there and the corpus right. A host that fails is
  reported unusable, with why, and skipped: a remote never stops or fails the chain.
- **How:** the laptop copies the chain's bundle to each host, which fetches it into
  ~/fve-xcheck at the chain's commit and runs lab/evolve/xcheck.py (written, Iteration 307) under
  setsid, with its own log and progress lines; the laptop polls, and at the chain's end
  fetches results and logs into the archive. Each check pins to its host's least busy
  core and records the load - the hosts are to be left idle during a run.
- **Stop and recovery:** `next-run.sh stop` stops the remote checks too (ssh, their
  process group); a start's recovery clears what a crashed chain left on them; status
  and monitor show their progress.
- **Results:** results/xcheck-<host>.md, a section a run - over runs, which genes'
  worth differs by machine.

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
- The remote checks with a stand-in ssh and scp that run a second clone here, as a host
  would - including a host unreachable and a host whose build fails: the chain goes on,
  the archive says so.
- After each: no root-owned file under the clone.

## Built so far (Iteration 313)

lab/evolve/chainctl.py and next-run.sh's chain layer - each step's own logic unchanged:

- **One chain, one session**: the first step makes RUNS/chain-TIME/ (line, head, sid, status,
  steps, chain.log, packs/) and detaches under setsid; every later step detaches inside it.
- **status / monitor / stop**: `sh lab/evolve/next-run.sh status|monitor|stop`. stop TERMs the
  session, KILLs after 60 s, and packs; a stopped step is recorded STOPPED.
- **One archive**: RUNS/forth-vm-evolution-chain-HEAD-HOST-TIME[-STATUS].tar.gz, written as
  .partial and renamed - every step's pack, every failed step's logs, the chain's log. STATUS:
  none (done), done-some-failed, failed, stopped, interrupted.
- **A failed step does not cost the rest**: after a failed measurement the chain goes on;
  after a failed seed run the comparison is skipped (recorded) and the chain packed.
- **Checks once a chain**: the tests, validation and jail in the first step; a later step builds
  and keeps the first one's logs.
- **Progress**: a line every 5 minutes during the evolution (chainctl.py ticker).
- **Recovery at start**: a chain that ended without finishing archived as interrupted; stale
  .partial files removed; root-owned files in the clone listed and given back with sudo, in the
  foreground, before anything starts.

Tested on the VM, a scratch clone with its own bundle and two stand-in tools: a chain whose first
step failed went on, its second step's pack and the first one's logs - its tool's own error among
them - in one archive, done-some-failed; the second step built only, the tests not run again;
status during and after; monitor on a finished chain; stop in the middle of the build - five
processes, none after, stopped, archived; a crash - every process killed -9, the status left
"running" - archived as interrupted by the next start, which then ran.

**Not yet tested**: the seed step's chain changes (the ticker, a fresh seed's rebuild after the
first step's checks) - a miniature seed chain before seed 53; the root-owned files path.
**Not yet built**: perf-hold holding for every measurement of a chain and chowning what it makes;
the remote checks (dream.lan, rage.lan) started and gathered by the chain.

