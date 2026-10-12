#!/usr/bin/env python3
"""lookup-cache-model.py [ID] - the open item "a lookup cache beside the threads
gene" (results/loop-audit.md, "What would cut the lookup loop", 2), priced
offline (Iteration 221), as loop-audit-chains.py priced the chains.

The cost of a lookup is the dictionary entries it visits: a name found at
position p of its chain (newest first) visits p, a name not found (a number,
a name being defined) the whole chain. Modelled over the workload's own token
stream - comments and strings skipped, the dictionary growing as it defines,
each repeated pass of the long workload defining its words again - with the
kernel's hash of the length and two characters at 16, 32, 64 and 128 chains.

A direct-mapped cache of N entries, by the same hash: a lookup whose entry
holds its name costs one visit; a name found by the walk is put in its entry;
a definition clears the entry of its name (exact invalidation). Misses still
walk - a cache of names not found would be cleared by every definition.
Reported: entry visits per lookup, now and with the cache, and the share of
lookups the cache serves; also the share of visits spent on names not found,
which a cache cannot serve. The dictionary: the design's image, by the
converter's symbol map, oldest first."""
import collections, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
args = sys.argv[1:]; DID = args[0] if args else 'add5ec8937'
sys.argv = ['x']; sys.path.insert(0, os.path.join(ROOT, 'lab', 'evolve')); import evolve as E
E.setup()
d = os.path.join(E.EV, 'lcache'); shutil.rmtree(d, ignore_errors=True)
sm = d + '.sym'; os.environ['SYMMAP'] = sm; E.PROFILING[0] = True
try: E.build(E.canon(E.recorded_genome(DID)), d)
finally: E.PROFILING[0] = False; del os.environ['SYMMAP']
image = []
for l in open(sm):
    n = l.split(None, 2)[2].strip()
    if n and not n.startswith('('): image.append(n)
image = list(dict.fromkeys(image))            # image order, oldest first; one entry a name

def h(n, T):
    b = n.encode('latin-1', 'replace'); v = (b[0] << 1) ^ ((b[1] << 2) if len(b) > 1 else 0) ^ len(b)
    return v & (T - 1)

DEFINERS = {':', 'CREATE', 'VARIABLE', 'CONSTANT', 'VALUE', 'DEFER', '2CONSTANT', '2VARIABLE', 'BUFFER:', 'MARKER'}
TICKS = {"'", "[']", 'POSTPONE', '[COMPILE]'}
def lookups(text):
    """(kind, name): 'find' a lookup of a token, 'def' a name defined (a lookup first, then added)."""
    out, toks = [], re.findall(r'\S+', text)
    i = 0
    while i < len(toks):
        t = toks[i]; u = t.upper()
        if u == '\\':                                     # to the end of the line: re-split by lines instead
            i += 1; continue
        if u in ('(', '.('): 
            while i < len(toks) and not toks[i].endswith(')'): i += 1
            i += 1; continue
        if u in ('S"', '."', 'ABORT"', 'C"', 'S\\"'):
            out.append(('find', u)); i += 1
            while i < len(toks) and not toks[i].endswith('"'): i += 1
            i += 1; continue
        out.append(('find', u))
        if u in DEFINERS and i + 1 < len(toks): out.append(('def', toks[i + 1].upper())); i += 2; continue
        if u in ('CHAR', '[CHAR]') and i + 1 < len(toks): i += 2; continue
        if u in TICKS and i + 1 < len(toks): out.append(('find', toks[i + 1].upper())); i += 2; continue
        i += 1
    return out

def strip_line_comments(text):
    return '\n'.join(re.sub(r'(^|\s)\\\s.*$', ' ', l) if not l.strip().startswith('\\') else '' for l in text.split('\n'))

def price(stream, T, N):
    chains = collections.defaultdict(list)
    for n in image: chains[h(n, T)].insert(0, n)
    cache = {}
    now = withc = served = finds = missv = 0
    for kind, name in stream:
        c = chains[h(name, T)]
        try: p = c.index(name) + 1
        except ValueError: p = 0
        finds += 1
        cost = p if p else len(c)                       # found at p, or the whole chain
        now += cost
        if not p: missv += cost
        slot = h(name, N) if N else None
        if N and cache.get(slot) == name: withc += 1; served += 1
        else:
            withc += cost
            if N and p: cache[slot] = name
        if kind == 'def':
            c.insert(0, name)
            if N and cache.get(h(name, N)) == name: del cache[h(name, N)]
    return now / finds, withc / finds, served / finds, finds, missv / max(now, 1)

works = {}
LONGF = E.LONGF if E.LONGF else {}
works['corpus'] = strip_line_comments(open(E.CORPUS).read()) * E.LONG['corpus']
pf = LONGF.get('parse') or os.path.join(E.ROOT, 'bench', 'parse.fth')
works['parse'] = strip_line_comments(open(pf).read()) * (E.LONG['parse'] if 'parse' not in LONGF else E.LONG['parse'])
print('%s: %d names in the image\n' % (DID, len(image)))
print('| workload | lookups | chains | visits a lookup now | of them by names not found | with a cache of 16 / 64 / 256 | served by it |')
print('|---|---|---|---|---|---|---|')
for w, text in works.items():
    stream = lookups(text)
    for T in (16, 32, 64, 128):
        base = price(stream, T, 0)
        rs = [price(stream, T, N) for N in (16, 64, 256)]
        print('| %s | %s | %d | %.1f | %.0f%% | %s | %s |' % (w, format(base[3], ','), T, base[0], 100 * base[4], ' / '.join('%.1f' % r[1] for r in rs),
              ' / '.join('%.0f%%' % (100 * r[2]) for r in rs)))
shutil.rmtree(d, ignore_errors=True)
