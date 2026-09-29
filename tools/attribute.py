#!/usr/bin/env python3
"""attribute.py MAP PROF - which Forth words consume the dispatches?

Every VM instruction executed is recorded at its address. The symbol map
gives each word's body range in the image. So the dispatch count of a
word is the sum over the addresses inside its body - its SELF cost,
excluding the words it calls, which are attributed to themselves.
"""
import bisect, sys, collections

mp, prof = sys.argv[1], sys.argv[2]
syms = []
for line in open(mp):
    a, b, name = line.split(' ', 2)
    syms.append((int(a), int(b), name.strip()))
syms.sort()
starts = [s[0] for s in syms]

ipc = collections.Counter()
calls = collections.Counter()
for line in open(prof):
    f = line.split()
    if f[0] == 'I':
        ipc[int(f[1])] += int(f[2])

self_cost = collections.Counter()
unmapped = 0
for addr, n in ipc.items():
    i = bisect.bisect_right(starts, addr) - 1
    if i >= 0 and syms[i][0] <= addr < syms[i][1]:
        self_cost[syms[i][2]] += n
    else:
        unmapped += n

total = sum(ipc.values())
print("total VM instructions dispatched: %s" % format(total, ','))
print("attributed to a word: %.1f%%   (unmapped %s)\n"
      % (100.0 * (total - unmapped) / total, format(unmapped, ',')))
print("%-22s %14s %7s %7s" % ("word", "dispatches", "share", "cumul"))
cum = 0
for name, n in self_cost.most_common(25):
    cum += n
    print("%-22s %14s %6.1f%% %6.1f%%"
          % (name[:22], format(n, ','), 100.0 * n / total, 100.0 * cum / total))
