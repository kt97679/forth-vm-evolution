#!/usr/bin/env python3
"""lab/evolve/chainctl.py - a chain of runs as one thing (Iteration 313; results/drafts/
runner-protocol.md). next-run.sh starts a chain - every step of a NEXT-RUN line, "A then B"
- as one session (setsid), with one directory:

    RUNS/chain-YYYYmmdd-HHMMSS/
        line        the chain's line, as next-run.sh read it
        head        the commit it runs
        sid         the session: every process of the chain is in it
        status      running | stopping | done | failed | stopped | interrupted
        steps       a line a step: ok, FAILED or skipped, and its pack
        chain.log   everything the chain printed - the one log
        packs/      each step's pack, and the logs of a step that failed
        archive     the path of the one archive, once made

and the owner's commands read it (next-run.sh passes them here):

    sh lab/evolve/next-run.sh status    where the chain is: its step, its progress, alive or
                                        not; when it has finished, the archive to send
    sh lab/evolve/next-run.sh monitor   the one log, followed until the chain ends - read
                                        only: Ctrl-C stops the watching, not the chain
    sh lab/evolve/next-run.sh stop      the chain's whole session ended (TERM, then KILL
                                        after 60 s) - and the archive made all the same

next-run.sh itself uses:

    chainctl.py pack CHAIN STATUS       the one archive: RUNS/forth-vm-evolution-chain-HEAD-
                                        HOST-TIME[-STATUS].tar.gz, written as .partial and
                                        renamed when whole
    chainctl.py ticker PID [UNTIL]      a progress line every 5 minutes while PID lives:
                                        the generation, designs measured, the front
    chainctl.py recover RUNS REPO       before a start: a chain that ended without finishing
                                        (a crash, the power) archived as interrupted; stale
                                        .partial files removed; root-owned files in REPO
                                        listed (exit 3), for next-run.sh to give back
"""
import os, signal, socket, subprocess, sys, tarfile, time

STEP_PREFIX = 'next-run: '


def chains(runs):
    """The chain directories, oldest first (their names are UTC times)."""
    try: names = sorted(n for n in os.listdir(runs) if n.startswith('chain-'))
    except OSError: return []
    return [os.path.join(runs, n) for n in names if os.path.isdir(os.path.join(runs, n))]


def read(chain, name, default=''):
    try:
        with open(os.path.join(chain, name)) as f: return f.read().strip()
    except OSError: return default


def write(chain, name, text):
    tmp = os.path.join(chain, name + '.new')
    with open(tmp, 'w') as f: f.write(text.rstrip('\n') + '\n')
    os.replace(tmp, os.path.join(chain, name))


def state(chain):
    return (read(chain, 'status', 'running').split('\n') or ['running'])[0].strip()


def members(chain):
    """The chain's processes: [(pid, args)] in its session - none, if it has ended."""
    sid = read(chain, 'sid')
    if not sid.isdigit(): return []
    try: out = subprocess.run(['ps', '-e', '-o', 'sid=,pid=,args='], capture_output=True, text=True).stdout
    except OSError: return []
    me = os.getpid(); procs = []
    for line in out.splitlines():
        f = line.split(None, 2)
        if len(f) >= 2 and f[0] == sid and int(f[1]) != me: procs.append((int(f[1]), f[2] if len(f) > 2 else ''))
    return procs


def alive(chain): return bool(members(chain))


def last_lines(path, n):
    try:
        with open(path, 'rb') as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - 65536))
            return f.read().decode(errors='replace').splitlines()[-n:]
    except OSError: return []


def current_step(chain):
    """The newest '== HH:MM:SS step' line of the chain log, and the newest progress line."""
    lines = last_lines(os.path.join(chain, 'chain.log'), 400)
    step = next((l for l in reversed(lines) if l.startswith('== ')), '')
    prog = next((l for l in reversed(lines) if l.startswith(STEP_PREFIX + 'progress')), '')
    return step, prog


# ---- the owner's commands

def cmd_status(runs):
    cs = chains(runs)
    if not cs: print('no chain has run here (%s)' % runs); return 0
    c = cs[-1]; st = state(c); live = alive(c)
    print('chain %s: %s' % (os.path.basename(c), read(c, 'line') or '?'))
    print('  at commit %s; status %s%s' % (read(c, 'head') or '?', st, ' - running now' if live else ''))
    steps = read(c, 'steps')
    for l in steps.splitlines(): print('  step: %s' % l)
    if live:
        step, prog = current_step(c)
        if step: print('  now: %s' % step[3:])
        if prog: print('  %s' % prog[len(STEP_PREFIX):])
        others = [a for p, a in members(c) if 'perf-hold' in a or 'xcheck' in a]
        for a in others: print('  alongside: %s' % a[:100])
        print('  follow it: sh lab/evolve/next-run.sh monitor   end it: sh lab/evolve/next-run.sh stop')
    else:
        a = read(c, 'archive')
        if st in ('running', 'stopping'):
            print('  it is not running and did not finish - the next start archives it as interrupted')
        elif a: print('  send: %s' % a)
    return 0


def cmd_monitor(runs):
    cs = chains(runs)
    if not cs: print('no chain has run here (%s)' % runs); return 1
    c = cs[-1]; log = os.path.join(c, 'chain.log')
    for l in last_lines(log, 40): print(l)
    if not alive(c):
        print('-- the chain is not running (status %s)%s' % (state(c), ('; send ' + read(c, 'archive')) if read(c, 'archive') else ''))
        return 0
    print('-- following %s (Ctrl-C stops the watching, not the chain)' % log)
    try:
        with open(log, 'rb') as f:
            f.seek(0, 2); quiet = 0
            while True:
                b = f.read()
                if b: sys.stdout.write(b.decode(errors='replace')); sys.stdout.flush()
                else:
                    time.sleep(2); quiet += 1
                    if quiet % 5 == 0 and not alive(c):
                        b = f.read()
                        if b: sys.stdout.write(b.decode(errors='replace'))
                        break
        print('-- the chain has ended: status %s%s' % (state(c), ('; send ' + read(c, 'archive')) if read(c, 'archive') else ''))
    except KeyboardInterrupt:
        print('\n-- stopped watching; the chain goes on')
    return 0


def cmd_stop(runs):
    cs = chains(runs)
    if not cs or not alive(cs[-1]):
        print('no chain is running here'); return 0
    c = cs[-1]
    write(c, 'status', 'stopping\n' + '\n'.join(read(c, 'status').splitlines()[1:]))
    print('stopping chain %s: %s' % (os.path.basename(c), read(c, 'line')))
    for sig, wait in ((signal.SIGTERM, 60), (signal.SIGKILL, 10)):
        procs = members(c)
        if not procs: break
        for pid, a in procs:
            try: os.kill(pid, sig)
            except OSError: pass
        t = time.time()
        while time.time() - t < wait and members(c): time.sleep(1)
    left = members(c)
    if left: print('  still alive after KILL: %s' % ', '.join(str(p) for p, a in left))
    if not read(c, 'archive') or state(c) == 'stopping':
        pack(c, 'stopped')
    print('  stopped; send %s' % read(c, 'archive'))
    return 0


# ---- next-run.sh's

def pack(chain, status):
    """The one archive: everything in the chain directory, whatever happened."""
    runs = os.path.dirname(chain)
    head = read(chain, 'head') or 'unknown'
    rest = read(chain, 'status').splitlines()[1:]
    write(chain, 'status', '\n'.join([status] + rest))
    name = 'forth-vm-evolution-chain-%s-%s-%s%s.tar.gz' % (head, socket.gethostname().split('.')[0],
                                                          time.strftime('%Y%m%d-%H%M%S', time.gmtime()),
                                                          '' if status == 'done' else '-' + status)
    final = os.path.join(runs, name); part = final + '.partial'
    with tarfile.open(part, 'w:gz') as t:
        for n in sorted(os.listdir(chain)):
            if n.endswith('.new'): continue
            t.add(os.path.join(chain, n), arcname=os.path.join(os.path.basename(chain), n))
    os.replace(part, final)
    write(chain, 'archive', final)
    return final


def cmd_pack(chain, status):
    print(STEP_PREFIX + 'the chain packed (%s) - send %s' % (status, pack(chain, status)))
    return 0


def evolution_progress(repo):
    # next-run.sh appends the evolution's output to evolve.log at the clone's top (Iteration 313's
    # ticker read build/evolve/'s, and said "no generation yet" through a whole run)
    lines = last_lines(os.path.join(repo, 'evolve.log'), 200) or last_lines(os.path.join(repo, 'build/evolve/evolve.log'), 200)
    gen = next((l.strip() for l in reversed(lines) if l.strip().startswith('generation ')), '')
    try:
        with open(os.path.join(repo, 'build/evolve/db.jsonl'), 'rb') as f: n = sum(1 for _ in f)
    except OSError: n = 0
    return gen, n


def cmd_ticker(pid, until, every=300):
    every = int(os.environ.get('TICK_EVERY', every))      # a test's shorter interval
    repo = os.getcwd()
    while True:
        for _ in range(every):
            time.sleep(1)
            if not os.path.exists('/proc/%d' % pid): return 0
        gen, n = evolution_progress(repo)
        left = ''
        if until > 0:
            m = max(0, int((until - time.time()) / 60))
            left = ', the evolution stops in %d h %02d min' % (m // 60, m % 60)
        print('%sprogress %s - %s, %d designs in the database%s' % (STEP_PREFIX, time.strftime('%H:%M:%S', time.gmtime()),
                                                                   gen or 'no generation yet', n, left), flush=True)


def cmd_recover(runs, repo):
    code = 0
    for c in chains(runs):
        if state(c) in ('running', 'stopping') and not alive(c):
            a = pack(c, 'interrupted')
            print('next-run: chain %s (%s) ended without finishing - a crash or the power? Its logs and packs, '
                  'archived: %s' % (os.path.basename(c), read(c, 'line'), a))
    try: names = os.listdir(runs)
    except OSError: names = []
    for n in names:
        if n.endswith('.partial'):
            os.remove(os.path.join(runs, n)); print('next-run: removed %s - an archive never finished' % n)
    try:
        out = subprocess.run(['find', repo, '-xdev', '-uid', '0'], capture_output=True, text=True).stdout.split()
    except OSError: out = []
    if out:
        print('next-run: %d files in %s belong to root - an earlier root helper left them:' % (len(out), repo))
        for p in out[:10]: print('    %s' % p)
        code = 3
    return code


def main(a):
    if len(a) >= 2 and a[0] == 'status': return cmd_status(a[1])
    if len(a) >= 2 and a[0] == 'monitor': return cmd_monitor(a[1])
    if len(a) >= 2 and a[0] == 'stop': return cmd_stop(a[1])
    if len(a) >= 3 and a[0] == 'pack': return cmd_pack(a[1], a[2])
    if len(a) >= 2 and a[0] == 'ticker': return cmd_ticker(int(a[1]), int(a[2]) if len(a) > 2 else 0)
    if len(a) >= 3 and a[0] == 'recover': return cmd_recover(a[1], a[2])
    if len(a) >= 2 and a[0] == 'alive':
        cs = chains(a[1]); return 0 if cs and alive(cs[-1]) else 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
