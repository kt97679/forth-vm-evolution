import os, re, json, shutil, glob, time
OUT = '/tmp/pk2/forth-vm-evolution-prev-chat-files-2'
shutil.rmtree('/tmp/pk2', ignore_errors=True); os.makedirs(OUT)
A = json.load(open('/tmp/pk2-attr2.json'))
first = set(os.listdir('/tmp/pkcheck/forth-vm-evolution-prev-chat-files/scripts')) | set(os.listdir('/tmp/pkcheck/forth-vm-evolution-prev-chat-files/jobs')) | \
        set(os.listdir('/tmp/pkcheck/forth-vm-evolution-prev-chat-files/patches')) | set(os.listdir('/tmp/pkcheck/forth-vm-evolution-prev-chat-files/logs'))
EXT = ('.py', '.sh', '.fth', '.4', '.c', '.h', '.S', '.awk', '.patch', '.diff')
# figures read off the transcripts' tool outputs (T1 = the seed 43-44 chat, Iterations 213-222; T2 = the seed 44-46 chat, 223-241),
# or - for files from the live part of the last chat, after its compaction - from that chat's record
FIG = {
 'alive43.py': 'the gate over seed 42/43 front designs (the check of the after-seed-43 batch); its result in that job\'s logs',
 'audit43.py': 'audited the fast alive run: real builds; fsys 4 images changed by the rebind fix (e.g. 8dab7c6af4 fsys 4: image 9249, recorded 9265; engine 8512)',
 'facts43.py': "seed 43's facts (records 38796, generations 0-153; status ok 31775, screened 6839, 182 reach-limit deaths; children by how made...)",
 'eng-id.py': 'the price switch changes no normal build: engines and images byte for byte (28677d13b1 23192 + 8416, cc6d168e0a 23672 + 10710, fc09f6373d 17048 + 8916, add5ec8937 7456 + 8680)',
 'fsys-count.py': 'the counting harness: dispatches per word and system calls per workload at chosen fsys levels (e.g. be1620e346 kernel at fsys 4 and 5)',
 'sizes.py': 'image bytes of the old, new and cell-copy fsys 5 library',
 'gate5.py': "the gate for the tightened fsys 5 (the after-seed-43 batch's verification); its result in that job's logs",
 'inner.S': 'the INNER loop timed three ways - the stencils as copied, three cells cached, the loop index in registers (results/price-jit-stack.md\'s microbenchmark); "same results: yes"',
 'main.c': "inner.S's C driver (the same timing)",
 'ans-hidden.py': 'the standard suite on three designs with the unused names hidden (the hidden-names finding)',
 'diag.py': 'diagnosed the hidden-names failures: the tools test (add5ec8937 toolstest.fth differs at line 10) and the JIT design crash',
 'diag2.py': 'widened the scan to sources loaded at run time (add5ec8937: hidden 65 by the first scan, 64 with coreext/locals/save-system/shell; written there: NEXT-NFA8) and bisected the crashing hidden name',
 'inl.py': "priced which hidden words could vanish entirely (add5ec8937: 65 hidden names with bodies; savings by kind: 'one call site' 36 ...)",
 'gate44.py': 'the gate for the WRITE-LINE fix (after-seed-44 patch 1); its result in that job\'s logs',
 'gate44b.py': 'the gate for the file-buffer change with the WRITE-LINE fix; its result in that job\'s logs',
 'pages.py': 'counting the pages a design touches (the memory sweep) - the run hit the 300 s limit there',
 'gate44c.py': 'the gate for the READ/FS-SEEK0 change (after-seed-44 patch 3); its result in that job\'s logs',
 'fs3-good.4': 'the fsys 3 library kept good while a fault was planted in READ\'s seekable path (the new check caught it: "READ from a stdin that is a file ... DIFFERS at fsys 3, 4, 5")',
 'pages2.py': 'every selection workload\'s memory with the image loader\'s array off the stack (add5ec8937: fib 80, loop 84, corpus 108, kernel 132, bubble 88, ackermann 80 KB ...)',
 'pm-build.py': 'built d3149e10c6 and add5ec8937 for the page map',
 'pm-run.py': 'mapped which pages a design has present after a workload ("never waited" lines per workload)',
 'gate44d.py': 'the gate on all 165 front designs for the image loader\'s array change (after-seed-44 patch 4); its result in that job\'s logs',
 'dz-designs.py': 'division by zero on each engine kind (f20de05a64 msc: RIGHT, status 0; 4a351e360a tail: RIGHT; cc6d168e0a JIT: RIGHT ...)',
 'gate45.py': "steps 7-9 for seed 44: the gate over seed 44's front and the joint front; its result in that job's logs",
 'lines.py': 'each line of the names program alone on s0 and s6 (s0-cell crashed with -11 on line 2: the UTF-8 name fault)',
 'names-check.py': "the first copy of lab/evolve/names-check.py, before the fix: 'the cell system (s0), the reference: status -11' - later moved into the repository",
 's1t.py': 'definitions tried on the SOD16 stage (w1/w8 crashed with -11 before the fix)',
 'symdiff.py': 'word-by-word comparison of the dumps, to explain the 662-byte image growth (the dump tool kept in every image - LINKC missing from DUMPTOOL)',
 'vm-lab-both.c': 'debugging, no recorded figure: an engine source with both after-seed-44 changes, split into separate patches',
 'vm-lab-jitos.c': 'debugging, no recorded figure: an engine source during the jitos gene (its first form; the command around it failed with a shell syntax error)',
 'gate46.py': "steps 7-9 for seed 45: the gate over seed 45's front and the joint front; its result in that job's logs",
 'cbtime.sh': 'the C baseline\'s first timings with the CPU-time wrapper (sieve 0.95 0.89 0.97 ms, ackermann 0.62 0.62 0.70, loop 0.88 0.91 0.94, parse 2.29 2.34 2.40)',
 'fc-run.sh': 'the counting harness on three more designs (no kinput, the Q-best, the fastest) at fsys 4 and 5, detached; output in fc*.log',
 'gate46b.py': "Iteration 242 (the last chat, after its compaction): made by job52.sh's sed from gate46.py for the primitives-first tree - alive: 128 of 128 (seed 45 front 105, joint front 66, 43 in both)",
 't1.py': 'Iteration 242 (the last chat): the new kernel image tried on simple input, definitions, extend.4 and PRIMITIVE? - PRIMITIVE? read 0 for every word (debugging)',
 't2.py': "Iteration 242 (the last chat): PRIMITIVE? on DUP, OPEN-FILE, COLD, (PRIMITIVES-END) - all 0; the second reseed stage crashed (-11) (debugging)",
 't3.py': "Iteration 242 (the last chat): printed the addresses and PRIMITIVE?'s compiled literal - 1792, START-relative, where the xts were absolute (debugging)",
 't5.fth': 'Iteration 244 (the last chat): written for the coreext >NAME test and not used - t6.py (first archive) ran it; no recorded figure',
 'elf.py': "Iteration 250-251 (the last chat): readelf on 3456ac1e5e's engine - no sections, 2 program headers (LOAD + GNU_STACK), 0xb0 = 176 header bytes: the stack-header row in GOALS.md (Iteration 251). Missed by the first archive's list",
 'job52.sh': 'Iteration 242 (the last chat): the primitives-first checks - run-tests PASS, 7 of 7, the gate 128 of 128, the suite 0 of 6 differ, outbuf and readline PASS (logs j52*.log, in the first archive)',
 'job49.sh': "Iteration 241: the walk regression found - profiling two small designs' dictionary walk (its output in j49.log)",
}
OTHER = {
 'evolve.py.cell': 'Iteration 214: a copy of lab/evolve/evolve.py for the cell-copy fsys 5 variant (image bytes of old, new and cell-copy fsys 5)',
 'evolve.py.new': 'Iteration 214: a copy of lab/evolve/evolve.py for the new fsys 5',
 'evolve.py.old': 'Iteration 214: a copy of lab/evolve/evolve.py for the old fsys 5',
 'file-sysc5.4.cell': 'Iteration 214: the cell-copy variant of the fsys 5 library',
 'file-sysc5.4.new': 'Iteration 214: the new fsys 5 library',
 'file-sysc5.4.orig': 'Iteration 214: the original fsys 5 library, kept before rewriting it',
 'vm-lab.c.bak': 'Iteration 263 (the last chat): engine/vm-lab.c kept before the zero-divisor trim was tried in /tmp/mo, and restored from it',
 'gen-tos.py.bak': 'Iteration 263 (the last chat): tools/gen-tos.py kept before the same trial, and restored from it',
}
rows = []
os.makedirs(OUT + '/scripts'); os.makedirs(OUT + '/jobs'); os.makedirs(OUT + '/logs'); os.makedirs(OUT + '/sources-other-suffixes')
cands = sorted(f for f in os.listdir('/tmp') if os.path.isfile('/tmp/' + f) and f.endswith(EXT) and not f.startswith('relf-run-') and f not in first)
for f in cands:
    a = A.get(f)
    it = a['it'] if a else ('see figure' if f in FIG else '?')
    if f.startswith('job') and f.endswith('.sh'):
        dest = 'jobs/'; fig = FIG.get(f) or ('background checks: %s - no recorded figure of its own; what it wrote is in logs/' % (a['ran'] if a else 'not in the transcripts'))
    else:
        dest = 'scripts/'; fig = FIG.get(f) or ('%s - no recorded figure found' % (a['ran'] if a else 'not in the transcripts'))
    shutil.copy2('/tmp/' + f, OUT + '/' + dest + f)
    src = 'T%d' % a['tr'] if a else 'the last chat\'s live record'
    rows.append(('/tmp/' + f, it if a else '-', fig, src, 'as found', dest + f))
for f, fig in OTHER.items():
    p = '/tmp/' + f
    if os.path.isfile(p): shutil.copy2(p, OUT + '/sources-other-suffixes/' + f); rows.append((p, '-', fig, 'T1' if 'Iteration 214' in fig else "the last chat's live record", 'as found', 'sources-other-suffixes/' + f))
    else: rows.append((p, '-', fig, '-', 'GONE', '-'))
# the logs the jobs 1-52 wrote
L = {}
for line in open('/tmp/pk2-joblogs.txt'):
    k, _, v = line.rstrip('\n').partition('\t')
    L[k] = [x for x in v.split() if x]
logrows = []
for job, outs in sorted(L.items(), key=lambda kv: int(re.sub(r'\D', '', kv[0]) or 0)):
    for p in outs:
        b = os.path.basename(p)
        if b.endswith('.py') or b in first: continue
        if os.path.isfile(p):
            if not os.path.exists(OUT + '/logs/' + b): shutil.copy2(p, OUT + '/logs/' + b)
            logrows.append((job, p, 'as found'))
        else: logrows.append((job, p, 'GONE'))
json.dump({'rows': rows, 'logs': logrows}, open('/tmp/pk2/m.json', 'w'))
print(len(rows), 'files;', len(logrows), 'log entries;', len(os.listdir(OUT + '/logs')), 'log files')
