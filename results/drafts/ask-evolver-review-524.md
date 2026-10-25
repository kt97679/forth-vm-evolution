# A bug hunt in an evolutionary search's evaluation and selection (the code is included below)

Please read the included Python (excerpts of one file, an evolutionary search over virtual-machine designs) and find real
bugs: places where a design is measured, judged or selected differently from what the comments and the invariants below
say - a wrong result that would mislead the search, or a crash. Every bug you report will become a test, so a specific
claim with its trigger is worth far more than a general worry.

## How it works, and what must hold

- **Evaluating a design** (evaluate): build it (a C engine and an image), then alive() - correctness checks (a corpus of
  programs, far-memory code, an audit), any failure kills the design - then measure(): every workload in rounds, each run
  paired with a fixed reference design (s6) back to back, alternating which goes first; a workload's time is its median
  CPU time over the reference's median. **Every workload's output must equal the reference's** in the same rounds
  ('Redefining:' warning lines aside - a family's kernel has other words); a wrong output kills the design.
- **Objectives**: speed - the geometric mean over the selection workloads (WORK_SEL, seven; WORK_HELD are held out,
  measured but never selected on); size - engine + image bytes; memory - the most any workload but the applications
  touched (their own data would swamp it); with two widths, the 32-bit speed a fourth. Dominance has tolerances (2% in
  speed; MEM_TOL in memory).
- **The fast gate**: a child faster than 1.05 x the 20th fastest alive is measured a second time in the next
  generation's batch (other co-runners, another moment); its speed becomes the geometric mean of the two readings.
- **The screen**: an additive surrogate (one weight per gene value; log speed, log size) refitted every 10 generations
  from generation 5 on the earlier generations; a child predicted beaten by 30% in speed and 5% in size by something
  measured is recorded "screened" and not measured - one in ten of those measured anyway (an audit).
- **Selection**: NSGA-II - non-dominated rank, then crowding; no encoding family dies out by crowding.
- **Determinism**: a resumed run replays the same decisions (the screen's fit has its own seed; the audit is chosen by id).

Bugs found in this code before, to show the kind: the workloads' outputs were not compared at all (a design failing a
workload early looked fast); memory was the applications' own data; a gated design's two readings once joined per
workload in a way that compounded. Those are fixed in what follows.

## The answer I'd like

For each suspected bug: where (function and line), the mechanism, a minimal trigger (records, a genome, a sequence of
generations), the expected and the actual behaviour, and your confidence (high, medium, low). Then, separately, risky
places you believe are correct, and invariants nothing checks that should be asserted. No style comments, and no
"might be an issue" without a mechanism.

---

```python
/* ---- alive ---- */
def alive(eng, img, pw, far=True):
    """The corpus must match the cell engine's output; the kernel must match."""
    with open(CORPUS, 'rb') as f:
        r = sh([eng, img], cwd=pw, inp=f.read(), timeout=120, cpu=5)
    if r.stdout != REF_CORPUS: raise RuntimeError('died: corpus')
    # The work directory starts with a copy of the reference kernel, so
    # the workload must WRITE it: remove it first. Until this, a design
    # that died quietly before saving passed - the copy matched.
    k = os.path.join(pw, 'kernel.img')
    if os.path.exists(k): os.remove(k)
    sh([eng, img], cwd=pw, inp=KERNEL_IN, timeout=240, cpu=10)
    if not os.path.exists(k) or open(k, 'rb').read() != open(KREF, 'rb').read():
        raise RuntimeError('died: kernel workload')
    # Iteration 158 (the owner): code and data far from the image base - past
    # 64 KB, then past 8 MB more (tests/core/far.fth). Every answer right, or
    # refused out loud: a design that computes something else, crashes or
    # hangs there dies. The hand-made stages are run-tests.sh's to judge.
    if far:
        try:
            r = sh([eng, img], cwd=pw, inp=FAR_IN, timeout=60, cpu=5); out, code = r.stdout.decode(errors='replace'), r.returncode
        except Exception as e: out, code = '', 'raised: %s' % str(e)[:60]
        v = farcheck.verdict(out, code)
        if v != 'all' and not v.startswith('refused'): raise RuntimeError('died: far (%s)' % v)
        # Iteration 161: an ALLOT past the dictionary's room - refused, HERE
        # unmoved, the system going on (tests/core/full.fth).
        try: r = sh([eng, img], cwd=pw, inp=FULL_IN, timeout=60, cpu=5); out = r.stdout.decode(errors='replace')
        except Exception: out = ''
        if 'dictionary full' not in out or [l for l in out.replace('\r', '').split('\n') if re.fullmatch(r'[0-9]+ ', l)] != ['1 ', '42 ']:
            raise RuntimeError('died: dictionary full not refused')


/* ---- run_metric ---- */
def run_metric(eng, img, pw, w, single=False):
    """One timed run: the process's own CPU time (user + system, from
    getrusage of the child - tools/cputime.c), not wall time, so other
    processes on the machine do not count against it."""
    r = sh(PIN + [CPUT, eng, img], cwd=pw, inp=program(w, single), timeout=240, cpu=30)
    m = re.search(METRIC, r.stderr, re.M) or re.search(rb'^CPUNS (\d+)', r.stderr, re.M)
    # The run's memory, KB (Iteration 75): the pages it touched - cputime's
    # MINFLT, faults counted one by one - times the page size. MAXRSS only
    # from an older cputime: on Linux 6.x it reads 0 for a small static run.
    mf = re.search(rb'^MINFLT (\d+)', r.stderr, re.M)
    mr = re.search(rb'^MAXRSS (\d+)', r.stderr, re.M)
    RSS_LAST[0] = int(mf.group(1)) * PAGE_KB if mf else (int(mr.group(1)) if mr else 0)
    OUT_LAST[0] = hashlib.sha1(re.sub(rb'(?m)^Redefining:[^\n]*\n', b'', r.stdout.replace(b'\r', b''))).hexdigest()
    # Iteration 516: what it printed - measure() compares it with s6's; a family's kernel differs in its words, so
    # 'Redefining: X' differs with it (cell designs have no LIT, or CALL, for sim16 to redefine) - not the output
    return int(m.group(1))

/* ---- measure ---- */
def measure(eng, img, pw, works, rounds):
    """The MEDIAN CPU time per workload over the rounds, the design and the
    reference - hand-made s6 - run back to back in every round, alternating
    which goes first. Returns design / reference per workload, and the
    design's own medians: a ratio of runs seconds apart, so drift in
    background load or clock speed over a run of hours cancels.

    The median, not the best (Iteration 25). On the laptop a rare fib run
    is 20-38% faster - 0.4-2.3% of runs for some designs, with address
    randomisation on or off, at no stack offset in particular (Iteration
    27) - and the best of the rounds reported that luck: a different draw
    each session, so two sessions ranked the same designs up to 28% apart. The median of the same runs
    agreed within 3.6% between halves of a session and 2.1% between CPUs
    (results/run-spread-amd-ryzen-7-pro-8840hs.md)."""
    runs, ref = {}, {}
    LAST_RSS.clear(); mem = {}; outs = {}
    for r_ in range(rounds):
        for w in works:
            pair = [(eng, img, pw, runs), REF + (ref,)]
            for e, i, p, store in (pair if r_ % 2 == 0 else pair[::-1]):
                store.setdefault(w, []).append(run_metric(e, i, p, w))
                if store is runs: mem.setdefault(w, []).append(RSS_LAST[0])   # the design's, not s6's
                outs.setdefault((store is runs, w), set()).add(OUT_LAST[0])
    # Iteration 516: a workload's output must be s6's - the run, not only its time. Unchecked, the applications
    # workload (seed 71) rewarded failing it: 791 cpt16 designs stopped early in apps on undefined words and timed
    # 0.13 of s6 there, against ~1.07 elsewhere - one reached the front. Both ran the same program in the same rounds.
    for w in works:
        if outs.get((True, w)) != outs.get((False, w)): raise RuntimeError('wrong output: ' + w)
    if 'corpus' in mem and 'corpus' in LONGF:    # Iteration 100: the corpus's memory from one single run
        run_metric(eng, img, pw, 'corpus', single=True); mem['corpus'] = [RSS_LAST[0]]
    LAST_RSS.update({w: statistics.median(v) for w, v in mem.items()})     # a page or two of noise
    med = {w: statistics.median(runs[w]) for w in works}
    return {w: med[w] / statistics.median(ref[w]) for w in works}, med


/* ---- fast_gate ---- */
def fast_gate(R):
    """The speed under which a child is measured twice: 5% above the FASTGATE[0]-th fastest design alive so
    far - the fast end, and the noise band around it. The fast end's in-run speeds were ~10% optimistic
    (results/review-methodology-386.md, 2a): designs admitted on lucky draws, a 3% noise the best of
    thousands. None while fewer are alive, or with --fastgate 0."""
    n = FASTGATE[0]
    if not n: return None
    sp = sorted(r['speed'] for r in R.values() if r.get('status') == 'ok' and r.get('speed'))
    return sp[n - 1] * FASTGATE[1] if len(sp) >= n else None


/* ---- evaluate ---- */
def evaluate(g, rounds, keep=False, gate=None, again=False):
    # Build what the identity names: canon(g), as express() and gid() see it.
    # Built raw, a mutation that turned on byte headers in a design with
    # scaled calls was refused by the converter (--bytehdr wants --cpt 0) -
    # and the death recorded under the identity of the byte-granular design,
    # which converts. 34 such deaths on the Ryzen, 31 in the VM rehearsal.
    g = canon(g)
    d = os.path.join(EV, 'ind-' + gid(g)); rec = {'status': 'ok'}
    if reach_lethal(g):
        rec['status'] = 'died: reach limit at scale 0 - not run'
        return rec
    try:
        eng, img = build(g, d)
        rec['size'] = os.path.getsize(img)
        rec['bin'] = bin_size(eng); rec['total'] = rec['bin'] + rec['size']     # Iteration 75: an objective
        pw = private_work(d)
        alive(eng, img, pw, far=not hand_made(g))
        t, raw = measure(eng, img, pw, WORK_SEL + WORK_HELD, rounds)
        rec['t'] = t; rec['raw'] = raw
        rec['speed'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL))
        rec['etext'] = text_size(eng)                              # Iteration 73: tracked, not scored
        # Iteration 520: not the applications' - their data (gc16's 320 KB of cells) set every design's memory from seed 71
        # (460-500 KB, the six's 108-136): the objective measured the programs, not the machine. The rest as before.
        rec['rss'] = max([v for w_, v in LAST_RSS.items() if w_ != 'apps'] or list(LAST_RSS.values())) if LAST_RSS else None   # KB: an objective
        rec['mem'] = dict(LAST_RSS)
        rec['unit'] = UNIT
        if gate and rec['speed'] < gate:   # Iteration 391: under the fast gate, measured again; Iteration 446
            rec['gated'] = 1               # (results/drafts/fastgate-review-445.md): not at once - back to back the two
                                           # readings shared their moment's luck - but in the next generation's batch
        if TWO_WIDTHS[0] and not again: rec.update(eval32(g, rounds))       # Iteration 336: the 32-bit measurement, after the 64-bit one
    except RuntimeError as e:
        rec['status'] = str(e)
    except subprocess.TimeoutExpired:
        rec['status'] = 'died: timed out'
    if not keep: shutil.rmtree(d, ignore_errors=True)
    return rec


# ---- variation -------------------------------------------------------------

/* ---- screen (constants and functions) ---- */
SPEED_TOL = float(os.environ.get('EVOLVE_SPEED_TOL', 0.02))
# Iteration 200 (the owner: pure Python, conservative): the surrogate
# screen (results/drafts/surrogate-offline.md). A child whose predicted speed
# and binary + image are both beaten - by SCREEN_MS and SCREEN_MT - by what was
# measured before its generation is not measured: recorded "screened". The
# model is additive - one weight per gene value, log speed and log size, fitted
# by stochastic gradient descent on the earlier generations' living designs
# every SCREEN_EVERY generations (seed 40 offline: speed within 8.2%, size 1.2%;
# at 30%/5% a third of the children skipped, 1 of 163 final-front designs
# lost). One screened child in SCREEN_AUDIT is measured anyway ("screened,
# audited" in how it was made) - the screen's own check. Deterministic: the
# fit has its own seed and sees only earlier generations, the audit is chosen
# by id - a resumed run's replay decides the same. EVOLVE_SCREEN=0: off.
SCREEN = os.environ.get('EVOLVE_SCREEN', '1') != '0'
SCREEN_MS, SCREEN_MT = (float(x) for x in os.environ.get('EVOLVE_SCREEN_MARGINS', '0.30,0.05').split(','))
SCREEN_AUDIT = int(os.environ.get('EVOLVE_SCREEN_AUDIT', 10))
SCREEN_FROM = int(os.environ.get('EVOLVE_SCREEN_FROM', 5))
SCREEN_EVERY = int(os.environ.get('EVOLVE_SCREEN_EVERY', 10))
SCREEN_MIN = int(os.environ.get('EVOLVE_SCREEN_MIN', 1000))

def screen_feats(g):
    f = []
    for k, v in express(g).items():
        if isinstance(v, (list, tuple)): f += ['%s:%s' % (k, json.dumps(x, sort_keys=True)) for x in v]
        else: f.append('%s=%s' % (k, json.dumps(v, sort_keys=True)))
    return f

def screen_fit(recs, epochs=12):
    """The additive model: [(weights, bias) for log speed, for log binary + image]."""
    data = [(screen_feats(r['genome']), math.log(r['speed']), math.log(ov(r, 'total'))) for r in recs]
    model = []
    for t in (1, 2):
        w = collections.defaultdict(float); b = sum(d[t] for d in data) / len(data)
        rnd = random.Random(1); idx = list(range(len(data)))
        for ep in range(epochs):
            rnd.shuffle(idx); a = 0.02 / (1 + ep * 0.2)
            for i in idx:
                fs, y = data[i][0], data[i][t]
                e = b + sum(w[f] for f in fs) - y
                for f in fs: w[f] -= a * (e + 1e-5 * w[f])
                b -= a * e * 0.1
        model.append((dict(w), b))
    return model

def screen_predict(model, g):
    fs = screen_feats(g)
    return tuple(math.exp(b + sum(w.get(f, 0.0) for f in fs)) for w, b in model)

def screen_stair(recs):
    """What was measured, as a staircase: speeds ascending, the least size up to each."""
    sp, tt = [], []
    for s_, t_ in sorted((r['speed'], ov(r, 'total')) for r in recs):
        if tt and tt[-1] <= t_: continue
        sp.append(s_); tt.append(t_)
    return sp, tt

def screen_beaten(stair, s_, t_):
    sp, tt = stair; k = bisect.bisect_right(sp, s_ * (1 - SCREEN_MS))
    return k > 0 and tt[k - 1] <= t_ * (1 - SCREEN_MT)


/* ---- dominates and ov ---- */
def dominates(a, b):
    """Design a dominates design b: no worse in all three, better in one -
    memory by more than MEM_TOL, speed by more than SPEED_TOL. With --widths 8,4,
    speed32 a fourth, with speed's tolerance."""
    s, t, m = (ov(a, k) for k in OBJECTIVES); s2, t2, m2 = (ov(b, k) for k in OBJECTIVES)
    if not TWO_WIDTHS[0]:
        return (s <= s2 * (1 + SPEED_TOL) and t <= t2 and m <= m2 + MEM_TOL
                and (s < s2 * (1 - SPEED_TOL) or t < t2 or m < m2 - MEM_TOL))
    w, w2 = ov(a, 'speed32'), ov(b, 'speed32')
    return (s <= s2 * (1 + SPEED_TOL) and t <= t2 and m <= m2 + MEM_TOL and w <= w2 * (1 + SPEED_TOL)
            and (s < s2 * (1 - SPEED_TOL) or t < t2 or m < m2 - MEM_TOL or w < w2 * (1 - SPEED_TOL)))
def ov(r, k):
    if k == 'speed32':                  # Iteration 336: none (no 32-bit build, or not alive there) - the worst
        v = r.get('speed32'); return v if v is not None else 1e9
    if k == 'total': return r.get('total', r['size'])
    if k == 'rss': return r.get('rss') or 0
    return r[k]

def fronts(ids, R):
    # Lists, not sets: a set of ids iterates in an order that changes with
    # each process's string hashing, the fronts would come out in another
    # order, and a resumed run would pick different parents and fork.
    dom = {i: [] for i in ids}; n = {i: 0 for i in ids}
    def better(x, y):
        return dominates(R[x], R[y])
    for x in ids:
        for y in ids:
            if x != y and better(x, y): dom[x].append(y)
            elif x != y and better(y, x): n[x] += 1
    F = [[i for i in ids if n[i] == 0]]
    while F[-1]:
        nxt = []
        for x in F[-1]:
            for y in dom[x]:
                n[y] -= 1
                if n[y] == 0: nxt.append(y)
        F.append(nxt)
    F = F[:-1]
    # Iteration 197: with tolerances the relation need not be transitive - a
    # cycle would leave its designs in no front and drop them unseen; last.
    placed = set(x for f in F for x in f)
    left = [i for i in ids if i not in placed]
    return F + [left] if left else F


/* ---- first_front ---- */
def first_front(ids, R):
    """fronts(ids, R)[0] - the same designs, in the same order - without
    comparing every pair (Iteration 99: a 12-hour run makes ~90,000 designs,
    and fronts() over all of them would take hours). Sorted by speed, a
    design is dominated by one strictly faster with no more total and memory
    within MEM_TOL - so, per memory value, the least total seen among the
    faster ones decides it - or by one as fast, no worse in both and better
    in one: checked within its speed. Linear in the designs, times the few
    memory values (pages: ~10)."""
    pts = sorted(((ov(R[i], 'speed'), ov(R[i], 'total'), ov(R[i], 'rss'), i) for i in ids), key=lambda p: p[0])
    mems = sorted(set(p[2] for p in pts)); least = {m: math.inf for m in mems}; out = set(); k = 0
    while k < len(pts):
        j = k
        while j < len(pts) and pts[j][0] == pts[k][0]: j += 1
        grp = pts[k:j]
        for s, t, m, i in grp:
            dom = any(least[mv] <= t for mv in mems if mv <= m + MEM_TOL)
            dom = dom or any(i2 != i and t2 <= t and m2 <= m + MEM_TOL and (t2 < t or m2 < m - MEM_TOL) for s2, t2, m2, i2 in grp)
            if not dom: out.add(i)
        for s, t, m, i in grp: least[m] = min(least[m], t)
        k = j
    return [i for i in ids if i in out]


/* ---- crowding ---- */
def crowding(front, R):
    cd = {i: 0.0 for i in front}
    for k in OBJECTIVES + (('speed32',) if TWO_WIDTHS[0] else ()):
        s = sorted(front, key=lambda i: ov(R[i], k)); lo, hi = ov(R[s[0]], k), ov(R[s[-1]], k)
        cd[s[0]] = cd[s[-1]] = float('inf')
        for j in range(1, len(s) - 1):
            cd[s[j]] += (ov(R[s[j + 1]], k) - ov(R[s[j - 1]], k)) / ((hi - lo) or 1)
    return cd

# Iteration 188 (the owner): demote, don't delete - and keep what has
# potential. Survival keeps the best N of parents and children; what falls
# out is no longer simply gone: a demoted design carrying a gene value no
# survivor has goes to the attic (ATTIC of them, the rarest genes first), and
# leaves it once the population has that value again. One parent in ATTIC_P
# comes from the attic, and a borrowed gene may come from there: a stepping
# stone (a gene costly alone, good with a partner not yet found) keeps its
# chance to pass on, at no measuring cost - the attic is measured already.
# And the Q_KEEP best by Q - binary + image x run time x memory, the owner's
# compound quality: the front's knee - always survive, as the extremes
# (crowding) and each family's best already do.
# Iteration 197 (results/gp-deep-dive.md, seed 40's database): mutation-only
# children made 73% of the final front from a quarter of the children;
# crossover, then 60% of variation, was twelve times less productive per
# child - so less of it (EVOLVE_XOVER). Its uniform choice gene by gene split
# genes linked on the front (mutual information 0.67-1.00): LINKS are
# inherited whole, from one parent. varcall's and doesfar's mutants were not
# dominated by their parent 0.5% and 0.2% of the time - 3.5% of a run's
# evaluations: drawn one time in ten (SLOW_GENES).

/* ---- the main loop: the screen and the gated children measured again (lines 2101-2175) ---- */
        items = list(pending.items()); pending.clear()
        gen_now = max((it[1][3] for it in items), default=0)
        if SCREEN and items and gen_now >= SCREEN_FROM:          # Iteration 200: the screen
            if SCR['model'] is None or gen_now - SCR['fit'] >= SCREEN_EVERY:
                recs = [r for r in R.values() if r['status'] == 'ok' and r.get('speed') and ov(r, 'total') and r.get('gen', 0) < gen_now]
                if len(recs) >= SCREEN_MIN:
                    SCR['model'], SCR['fit'] = screen_fit(recs), gen_now
                    print('  the screen: fitted on %d designs at generation %d' % (len(recs), gen_now), flush=True)
            if SCR['model'] is not None:
                stair = screen_stair([r for r in R.values() if r['status'] == 'ok' and r.get('speed') and ov(r, 'total') and r.get('gen', 0) < gen_now])
                keep, n_scr, n_aud = [], 0, 0
                for i, (g, parents, how, gen) in items:
                    ps, pt = screen_predict(SCR['model'], canon(g))
                    if gen >= SCREEN_FROM and screen_beaten(stair, ps, pt):
                        if int(i, 16) % SCREEN_AUDIT == 0:
                            n_aud += 1; keep.append((i, (g, parents, how + '; screened, audited', gen))); continue
                        n_scr += 1
                        rec = {'status': 'screened', 'pred': [round(ps, 4), round(pt)], 'secs': 0,
                               'id': i, 'genome': canon(g), 'parents': parents, 'how': how, 'gen': gen}
                        R[i] = rec; save(rec)
                    else: keep.append((i, (g, parents, how, gen)))
                if n_scr or n_aud: print('  the screen: %d of %d children not measured, %d audited' % (n_scr, len(items), n_aud), flush=True)
                items = keep
        gate = fast_gate(R)                                   # Iteration 391
        args = [(canon(g), ROUNDS, False, gate) for i, (g, parents, how, gen) in items]
        # Iteration 446: the gated children of the generation before, measured again in this batch - among other
        # co-runners, at another moment - their speed the geometric mean of the two readings then
        again = [i for i, r in R.items() if r.get('gated') == 1 and r.get('status') == 'ok'] if items else []
        args += [(R[i]['genome'], ROUNDS, False, None, True) for i in again]
        results = list(WORKERS[0].imap(_job, args) if WORKERS[0] else map(_job, args))
        for i, rec2 in zip(again, results[len(items):]):
            r = R[i]
            if rec2.get('status') == 'ok' and rec2.get('t'):
                t1, raw1 = r['t'], r.get('raw', {})
                r['speed1'], r['speed2'] = r['speed'], rec2['speed']
                r['t'] = t = {w: math.sqrt(t1[w] * rec2['t'][w]) for w in t1 if w in rec2['t']}
                r['raw'] = {w: math.sqrt(raw1[w] * rec2['raw'][w]) for w in raw1 if w in rec2.get('raw', {})}
                r['speed'] = math.exp(sum(math.log(t[w]) for w in WORK_SEL) / len(WORK_SEL))
            r['gated'] = 2; save(r)
            print('    %s measured again: %.4g, then %s - %s' % (i, r.get('speed1', r['speed']), ('%.4g' % r['speed2']) if 'speed2' in r else rec2.get('status'), ('speed %.4g' % r['speed'])), flush=True)
        for (i, (g, parents, how, gen)), rec in zip(items, results[:len(items)]):
            rec.update(id=i, genome=canon(g), parents=parents, how=how, gen=gen)
            R[i] = rec; save(rec)
            print('    %s %-24s %s' % (i, rec['status'] if rec['status'] != 'ok' else
                  'speed %.4g size %d%s' % (rec['speed'], rec['size'], ' twice %.4g/%.4g' % (rec['speed1'], rec['speed2']) if 'speed1' in rec else ''), how[:70]), flush=True)
    # Iteration 115 (the owner: "sod32 from nothing"): --fromzero - the first
    # generation all random genomes, uniform over the whole space: no hand-made
    # design, no founder, nothing carried, no mutant of a hand-made one (the
    # seeded fill). Hand-made s6 stays the yardstick, outside the population.
    FROMZERO = '--fromzero' in argv
    NOEVOLVED = '--noevolved' in argv   # Iteration 387: no founder drawn from an earlier run's record (results/review-methodology-386.md, 1)
    if FROMZERO:
        pop = []
        while len(pop) < N:
            g = random_genome(rnd); g = require(g)
            pop.append(get(g, [], 'random', 0))
        print('  from zero: %d random genomes' % len(pop), flush=True)
    pop = pop if FROMZERO else [get(g, [], 'hand-made ' + n, 0) for n, g in HUMAN.items()]
    # Founders carrying superinstructions, so the gene enters with a population
    # behind it rather than waiting on one mutation in seventeen.
    if not FROMZERO: pop += [get(dict(HUMAN['s4-cv8'], supers=SUPER_POOL[:24], rtfuse=1), [], 'founder: s4-cv8 + 24 pairs, run-time fusion', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2]), [], 'founder: s6-cv8b + 2 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], supers=SUPER_POOL[:2], rtfuse=1), [], 'founder: s6-cv8b + 2 pairs, run-time fusion', 0),
            get(dict(HUMAN['s4-cv8'], ops10=list(OPS10_POOL), supers=SUPER_POOL[:20]), [], 'founder: s4-cv8 + format-10 opcodes + 20 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], ops10=OPS10_POOL[:2]), [], 'founder: s6-cv8b + EXECUTE, I as opcodes', 0),
            get(dict(HUMAN['s6-cv8b'], escape=1, ops10=list(OPS10_POOL), supers=list(SUPER_POOL)), [], 'founder: s6-cv8b + escape, 7 words, 24 pairs', 0),
            get(dict(HUMAN['s6-cv8b'], escape=1, ops10=list(OPS10_POOL), supers=list(SUPER_POOL), rtfuse=1), [], 'founder: s6-cv8b + escape, all format-10 opcodes, pairs, tests fused at run time', 0)]
    # Iteration 155 (the owner): founders carrying the JIT's new genes, so jitloop and
    # jitinl enter with designs behind them - through seed 38 they were dormant, no
    # genome has them, and jitinl is two mutations (jitx too) from most JIT designs.
    # One competitive - seed 37's fastest, its record from results/ - and one any
    # tree can make, from hand-made s6; crossover lends their genes on.
    if not FROMZERO:
        pop += [get(dict(HUMAN['s6-cv8b'], tag2=1, jit=1, jitx=1, jitloop=1, jitinl=1), [], 'founder: s6-cv8b + the tag, the JIT, jitx, jitloop, jitinl', 0)]   # 441: the JIT needs the tag
        f37 = None if NOEVOLVED else recorded_genome('38446e6c09')
```

*Excerpts of lab/evolve/evolve.py at cf0e9da Iter; names used but not shown (express, canon, build, sh, program, private_work, LONGF, OBJECTIVES, MEM_TOL, TWO_WIDTHS) behave as their names and the comments say.*
