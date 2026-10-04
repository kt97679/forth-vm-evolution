#!/usr/bin/env python3
"""callsites.py ID [ID ...] [--db FILE] - one-byte calls through a table of
hot words, priced before anything is built (prompts/10).

GOALS.md (Iteration 12): "mostly size (a call is 2-3 bytes), so count the
static call sites by target". For each design, from its database record:

  1. The census. The converter writes every call site in the image's code
     bodies (CALLMAP, tools/layout.py): offset, length, target. Counted by
     target, ranked by the bytes a one-byte call would save there.
  2. The dynamic side. Built with the engine's profiler (VMPROF), the
     per-address dispatch counts joined with the sites: how many of each
     workload's calls go to each target. Calls compiled at run time - fib's
     FIB, the corpus's own words - are not in the image, and no table the
     converter fills can reach them.
  3. The exact price. The converter lays the image out again with the top
     K targets as one-byte calls (--hotcalls-file): exact, alignment and
     byte-header links included. Image only - no engine runs them yet. The
     table of K targets is charged at 2 bytes an entry, as it would sit in
     the image (the size measure counts only the image: a table compiled
     into the engine would be free there, and the saving would be false).
  4. The rival use of a slot. A design's free opcodes are all taken, by
     format-10 opcodes and pairs: each slot user with its static sites
     (about a byte each) and its dispatches; and, exactly, the image with
     the K fewest-site pairs taken out for the K hot words.

Audits - each stops the tool: converted with SOD16_OLD_BODYCHECK=1, the
image is the size the database recorded (the census itself uses the
converter as it stands, Iteration 13's fix included);
every site's bytes decode to its target; every dispatched address in the
image whose byte is a call is a census site; the profile's per-address
counts sum to its pair counts, less one per escaped primitive (L_esc
profiles its selector as well, with no address: 0.03% of kernel's
dispatches) and, with the 256-entry dispatch, one per call (NEXT profiles
the call's first byte, do_call profiles 256: 8% of kernel's) - price.py
counted both twice until Iteration 13; in a priced image, exactly the hot targets' sites became one
byte.
"""
import collections, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; db = os.path.join(HERE, '..', '..', 'build', 'evolve', 'db.jsonl')
if '--db' in args: i = args.index('--db'); db = args[i + 1]; del args[i:i + 2]
if not args or any(a.startswith('-') for a in args): sys.exit(__doc__)
sys.argv = ['x']; sys.path.insert(0, HERE); import evolve as E
E.setup()
recs = {}
for l in open(db):
    try: r = json.loads(l); recs[r['id']] = r
    except ValueError: pass
KS, TABLE, WORKS = (4, 8, 16, 32), 2, E.WORK_SEL + E.WORK_HELD
HOTBASE = 0xE0      # any byte sizes the image the same; these are where a carve-out would put them

def convert(g, d, extra=(), profile=False):
    """Build g into d with a call map; -> (engine, image, header bytes, image bytes, scale, sites, ops)."""
    cm = d.rstrip('/') + '.map'                    # beside d: build() wipes d
    if os.path.exists(cm): os.remove(cm)
    os.environ['CALLMAP'] = cm; E.CONVERT_EXTRA[:] = list(extra); E.PROFILING[0] = profile
    try: eng, img = E.build(dict(g, tail=0, msc=0), d)     # the image does not depend on tail or msc
    finally:
        E.PROFILING[0] = False; E.CONVERT_EXTRA[:] = []; del os.environ['CALLMAP']
    lines = [l.split() for l in open(cm)]
    assert lines[0][0] == 'H', 'no header line in the call map'
    hdr, n, cpt = map(int, lines[0][1:4])
    sites = [dict(at=int(f[1]), len=int(f[2]), toff=int(f[3]), old=int(f[4]), forced=int(f[5]), caller=f[6], target=f[7])
             for f in lines[1:] if f[0] == 'C']
    ops = [(int(f[1]), f[2], int(f[3])) for f in lines[1:] if f[0] == 'O']
    return eng, img, hdr, n, cpt, sites, ops

def check_sites(g, img, hdr, n, cpt, sites, hot={}):
    im = open(img, 'rb').read()[hdr:]
    assert len(im) == n, 'image %d bytes, the map says %d' % (len(im), n)
    for s in sites:
        b, a = im[s['at']], s['at']
        if s['len'] == 1:
            assert b == hot[s['old']], 'one-byte site %d holds %#x, not its opcode' % (a, b); continue
        if g['varcall']:
            assert (0x80 <= b < 0xC0) if s['len'] == 2 else b >= 0xC0, 'site %d: byte %#x, length %d' % (a, b, s['len'])
            v = ((b & 0x3F) << 8 | im[a + 1]) if s['len'] == 2 else ((b & 0x3F) << 16 | im[a + 1] << 8 | im[a + 2])
        else:
            assert b >= 0x80 and s['len'] == 2; v = (b & 0x7F) << 8 | im[a + 1]
        assert v << cpt == s['toff'], 'site %d decodes to %d, the map says %d' % (a, v << cpt, s['toff'])
    return im

for did in args:
    if did not in recs: sys.exit('no design %s in %s' % (did, db))
    g = E.canon(recs[did]['genome'])
    d = os.path.join(E.EV, 'callsites'); shutil.rmtree(d, ignore_errors=True)
    os.environ['SOD16_OLD_BODYCHECK'] = '1'                 # the converter the database was made with
    try: _, old, *_ = convert(g, d)
    finally: del os.environ['SOD16_OLD_BODYCHECK']
    assert os.path.getsize(old) == recs[did]['size'], 'image %d bytes, the database says %d' % (os.path.getsize(old), recs[did]['size'])
    eng, img, hdr, n, cpt, sites, ops = convert(g, d, profile=True)      # and the converter as it stands
    size0 = os.path.getsize(img)
    im = check_sites(g, img, hdr, n, cpt, sites)
    code = [s for s in sites if s['caller'] != '(prologue)']
    at = {s['at']: s for s in sites}
    opat = {a: (k, b) for a, k, b in ops}

    # ---- the dynamic side: one fresh profile file per workload (the profiler appends)
    pw = E.private_work(d)
    D, CALLS, IMG_CALLS, ODD = {}, {}, {}, collections.Counter()
    ipcw = {}                                               # workload -> address -> count, in the image
    dyn = collections.defaultdict(collections.Counter)      # site -> workload -> count
    for w in WORKS:
        pf = os.path.join(d, 'prof-' + w)
        E.sh([eng, img], cwd=pw, inp=E.program(w), timeout=240, cpu=10, env=dict(os.environ, VMPROF=pf))
        ipc, npair, ncall, nesc = collections.Counter(), 0, 0, 0
        for line in open(pf):
            f = line.split()
            if f[0] == 'I': ipc[int(f[1])] += int(f[2])
            elif f[0] != 'C':
                npair += int(f[2])
                if int(f[1]) == 256: ncall += int(f[2])
                if int(f[0]) == 0x7D: nesc += int(f[2])     # L_esc profiles its selector too, with no address
                if 128 <= int(f[1]) <= 255: nesc += int(f[2])   # with d256 a call is profiled as its byte AND as 256
        npair -= nesc                                       # so each is one dispatch, not two
        assert sum(ipc.values()) == npair, '%s: %d dispatches by address, %d by pair' % (w, sum(ipc.values()), npair)
        ipcw[w] = {a: k for a, k in ipc.items() if a < n}
        for a, k in ipc.items():
            if a >= n: continue
            if a in at: dyn[a][w] = k
            elif im[a] >= 0x80: sys.exit('%s: a call dispatched at %d is not in the census' % (w, a))
            elif a not in opat: ODD[(w, im[a])] += k                  # padding NOOPs, data bodies' opcodes
        D[w], CALLS[w] = npair, ncall
        IMG_CALLS[w] = sum(dyn[a][w] for a in at)

    # ---- by target
    T = {}
    for s in code:
        t = T.setdefault(s['old'], dict(name=s['target'], sites=0, save=0, forced=0, dyn=collections.Counter(), callers=set()))
        t['sites'] += 1; t['save'] += s['len'] - 1; t['forced'] += s['forced']; t['callers'].add(s['caller'])
        for w in WORKS: t['dyn'][w] += dyn[s['at']][w]
    for t in T.values(): t['free'] = t['save'] - 2 * t['forced']          # forced sites' 2 bytes depend on alignment
    rank = sorted(T, key=lambda o: (-T[o]['free'], -T[o]['save'], -sum(T[o]['dyn'].values()), T[o]['name']))
    lens = collections.Counter(s['len'] for s in code)
    print('## %s - %d bytes (%d as recorded, before the body-check fix); %d call sites in code to %d targets\n'
          % (did, size0, recs[did]['size'], len(code), len(T)))
    print('Sites by length: %s; %d of them before an inline operand (always long); '
          '%d targets called from one site only.\n' % (', '.join('%d bytes %d' % (k, lens[k]) for k in sorted(lens)),
          sum(s['forced'] for s in code), sum(1 for t in T.values() if t['sites'] == 1)))
    print('| workload | dispatches | calls | share | calls from the image\'s code | of all calls |')
    print('|---|---|---|---|---|---|')
    for w in WORKS:
        print('| %s | %d | %d | %.1f%% | %d | %.1f%% |' % (w, D[w], CALLS[w], 100 * CALLS[w] / D[w], IMG_CALLS[w], 100 * IMG_CALLS[w] / max(1, CALLS[w])))
    sh = lambda o, w: '%.1f%%' % (100 * T[o]['dyn'][w] / max(1, CALLS[w]))
    print('\nThe top 32 targets by bytes a one-byte call would save (sites before an inline operand last: their saving '
          'depends on alignment), and each one\'s share of the workload\'s calls:\n')
    print('| # | target | sites | bytes | callers | ' + ' | '.join(WORKS) + ' |')
    print('|---|---|---|---|---|' + '---|' * len(WORKS))
    for i, o in enumerate(rank[:32]):
        print('| %d | %s | %d | %d | %d | %s |' % (i + 1, T[o]['name'], T[o]['sites'], T[o]['save'], len(T[o]['callers']),
                                                ' | '.join(sh(o, w) for w in WORKS)))
    cum = lambda k: sum(T[o]['save'] for o in rank[:k])
    print('\nCumulative, the raw count (a byte per near site, two per far): '
          + ', '.join('top %d %d' % (k, cum(k)) for k in (1, 2, 4, 8, 16, 32, 64, len(rank))) + ' bytes.')
    hottest = sorted(T, key=lambda o: -sum(T[o]['dyn'][w] / max(1, CALLS[w]) for w in E.WORK_SEL))[:8]
    print('The most-called targets, by mean share of calls over the selection workloads: '
          + ', '.join('%s %.1f%% (%d sites)' % (T[o]['name'], 100 * sum(T[o]['dyn'][w] / max(1, CALLS[w]) for w in E.WORK_SEL) / 4, T[o]['sites']) for o in hottest))

    # ---- the exact price: the image laid out again with the top K as one-byte calls
    print('\nThe price, exact - the image converted again with the top K as one-byte calls '
          '(the slot question aside), the table at %d bytes an entry:\n' % TABLE)
    print('| K | sites | raw bytes | image bytes saved | table | net | net per slot | calls through the table: ' + ', '.join(E.WORK_SEL) + ' |')
    print('|---|---|---|---|---|---|---|---|')
    for k in KS:
        hot = rank[:k]
        f = os.path.join(E.EV, 'hotcalls.json')
        json.dump([[o, HOTBASE + i, T[o]['name']] for i, o in enumerate(hot)], open(f, 'w'))
        d2 = os.path.join(E.EV, 'callsites-k'); shutil.rmtree(d2, ignore_errors=True)
        _, img2, hdr2, n2, cpt2, sites2, _ = convert(g, d2, extra=['--hotcalls-file', f])
        check_sites(g, img2, hdr2, n2, cpt2, sites2, {o: HOTBASE + i for i, o in enumerate(hot)})
        one = [s for s in sites2 if s['len'] == 1]
        assert sorted(s['old'] for s in one) == sorted(s['old'] for s in code if s['old'] in hot), 'not exactly the hot sites became one byte'
        saved = size0 - os.path.getsize(img2)
        print('| %d | %d | %d | %d | %d | %d | %.1f | %s |' % (k, len(one), cum(k), saved, TABLE * k, saved - TABLE * k, (saved - TABLE * k) / k,
              ', '.join('%.1f%%' % (100 * sum(T[o]['dyn'][w] for o in hot) / max(1, CALLS[w])) for w in E.WORK_SEL)))
        shutil.rmtree(d2, ignore_errors=True)

    # ---- the rival use of a slot: what holds the design's slots now
    slots = [(op, w) for w, op in E.ops10_in(g)] + [(op, '%s %s' % (a, b)) for a, b, op in E.supers_in(g)]
    st = collections.Counter(b for a, k, b in ops)
    sdyn = collections.defaultdict(collections.Counter)
    for a, k, b in ops:
        for w in WORKS: sdyn[b][w] += ipcw[w].get(a, 0)
    print('\nWhat holds the slots now: %d slot users (%d format-10, %d pairs), fewest static sites first - '
          'each site is about a byte saved:\n' % (len(slots), len(E.ops10_in(g)), len(E.supers_in(g))))
    print('| opcode | user | static sites | dispatches: ' + ', '.join(E.WORK_SEL) + ' |')
    print('|---|---|---|---|')
    for op, w in sorted(slots, key=lambda x: (st[x[0]], x[0])):
        print('| %d | %s | %d | %s |' % (op, w, st[op], ', '.join(str(sdyn[op][x]) for x in E.WORK_SEL)))
    # exactly: the K fewest-site pairs taken out, their slots given to the K hottest targets
    pairs = sorted(E.supers_in(g), key=lambda x: (st[x[2]], x[2]))
    print()
    for k in (4, 8):
        if k > len(pairs): break
        drop = {(a, b) for a, b, _ in pairs[:k]}
        g2 = dict(g, supers=[x for x in g['supers'] if tuple(x) not in drop][:len(E.supers_in(g)) - k])
        d2 = os.path.join(E.EV, 'callsites-k'); shutil.rmtree(d2, ignore_errors=True)
        _, img3, *_ = convert(g2, d2)
        lost = os.path.getsize(img3) - size0
        f = os.path.join(E.EV, 'hotcalls.json')
        json.dump([[o, HOTBASE + i, T[o]['name']] for i, o in enumerate(rank[:k])], open(f, 'w'))
        _, img4, *_ = convert(g2, d2, extra=['--hotcalls-file', f])
        both = size0 - os.path.getsize(img4) - TABLE * k
        print('Taking the %d fewest-site pairs\' slots (%s): the image grows %d bytes without them; with the %d hottest targets '
              'in their place, net of the table, %+d bytes; the pairs removed %s dispatches on %s.'
              % (k, ', '.join('%s %s' % (a, b) for a, b, _ in pairs[:k]), lost, k, -both,
                 '/'.join(str(sum(sdyn[op][w] for _, _, op in pairs[:k])) for w in E.WORK_SEL), '/'.join(E.WORK_SEL)))
        shutil.rmtree(d2, ignore_errors=True)
    if ODD:
        print('\n(Dispatched in the image off the census\'s operation starts - padding and data bodies: %s.)'
              % ', '.join('%s byte %d: %d' % (w, b, k) for (w, b), k in sorted(ODD.items())[:12]))
    print()
    shutil.rmtree(d, ignore_errors=True)
