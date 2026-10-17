#!/usr/bin/env python3
"""tools/relf-pairs.py [COMMAND] - which adjacent instruction pairs relf's CV8 runs, and how often
(Iteration 358; RELF.md). relf's ledger (its Iteration 716) asks this lab about fused pairs, "some 8 %"
of the realistic script's dispatches; this ranks them. As relf's tools/profile.py does: vendor/relf/tree
copied and its shell built, a counting engine made from engine/cv8.c (PROFIP counting each instruction
address in a shared file), the shell embedded in it, COMMAND run (default: the realistic script); then
tools/image-audit.py decodes the image - patched to record every instruction's word, address and opcode.
A pair is two adjacent instructions of one word whose first does not transfer control (a branch, a
call, EXIT, EXECUTE); it runs about as often as the less run of the two (min - a little more where
the second is also a jump target). GPLv2 only, as relf (much of this is profile.py's)."""
import os, sys, re, subprocess, tempfile, shutil, contextlib, io, array, collections
LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
work = tempfile.mkdtemp(prefix='relf-pairs-'); R = os.path.join(work, 'relf')
shutil.copytree(os.environ.get('RELF_TREE') or os.path.join(LAB, 'vendor', 'relf', 'tree'), R, symlinks=True); os.chdir(R)   # RELF_TREE: another relf (a patched one: Iteration 360)
subprocess.run(['make', '-s', 'relfsh64'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def patch(text, old, new):
    n = text.count(old)
    if n != 1: sys.exit('relf-pairs: the text to patch occurs %d times, not once:\n%s' % (n, old[:200]))
    return text.replace(old, new)
SLOTS = 1 << 18; engine, counts = os.path.join(work, 'relf-prof'), os.path.join(work, 'counts.bin')
src = open('engine/cv8.c').read()
src = patch(src, '#define PROF(k)\n#define PROFIP(a)\n#define PROFDUMP', '#include <sys/mman.h>\nstatic unsigned int *prof_map;\nstatic UNS64 prof_base;\n#define PROF(k)\n#define PROFIP(a) (prof_map[((a) - prof_base) & 0x3FFFF]++)\n#define PROFDUMP')
src = patch(src, '    NEXT();\ndo_call:', '    prof_base = cbase;\n    { int fd = open("%s", O_RDWR);\n      prof_map = mmap(0, %d * sizeof(unsigned int), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);\n      close(fd); }\n    NEXT();\ndo_call:' % (counts, SLOTS))
open(os.path.join(work, 'prof.c'), 'w').write(src)
subprocess.run(['cc', '-O2', '-I', os.path.join(R, 'engine'), '-o', engine, os.path.join(work, 'prof.c')], check=True)
shell = os.path.join(work, 'relfsh')
subprocess.run(['sh', 'tools/embed.sh', engine, 'kernel64-shell.img', shell], check=True)
# Iteration 358: several COMMANDs counted together (--all: the five shell scripts of tests/bench-vm)
args = sys.argv[1:]
if args == ['--all']: args = ['./relfsh tests/bench-vm/%s.sh' % w for w in ('realistic', 'loop', 'fn', 'str', 'arith')]
commands = [a.replace('./relfsh', shell) for a in (args or ['./relfsh tests/bench-vm/realistic.sh'])]
open(counts, 'wb').write(bytes(SLOTS * 4))
for command in commands:
    r = subprocess.run(command, shell=True, env=dict(os.environ, THIS_SH=shell, RELFSH=shell), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
command = '; '.join(commands)
audit = open('tools/image-audit.py').read()
audit = patch(audit, "    ip = xt; far_target = xt\n    while ip < end:\n        op = img[ip]",
                     "    ip = xt; far_target = xt\n    while ip < end:\n        op = img[ip]\n        INS.append((name, ip, op, img[ip + 1] if op == ESCOP else None))")
audit = patch(audit, "CALLS=[]; SLOTS=[];", "CALLS=[]; SLOTS=[]; INS=[];")
g = {'__file__': os.path.join(R, 'tools', 'image-audit.py')}
sys.argv = ['image-audit', 'kernel64-shell.img', '8']
with contextlib.redirect_stdout(io.StringIO()): exec(audit, g)
c = array.array('I'); c.frombytes(open(counts, 'rb').read())
names, sels = {}, {}
for l in open('engine/opcodes.tab'):
    f = l.split()
    if len(f) >= 3 and f[1].startswith('0x') and not f[0].startswith('#'):   # every kind: direct synth branch8 tiny spec lit64 esc; escaped by selector
        (sels if f[0] == 'escaped' else names)[int(f[1], 16)] = f[2]
FMT, ESCOP = g['FMT'], g['ESCOP']
def nm(op, sel): return 'CALL' if op >= 0x80 else (sels.get(sel, 'ESC %d' % sel) if op == ESCOP else names.get(op, '0x%02x' % op))
def control(op, sel):
    n = nm(op, sel)
    return op >= 0x80 or FMT.get(op) in ('b16', 'b8') or n in ('EXIT', 'EXECUTE', '?EXIT', 'BRANCH', '?BRANCH', '(LOOP)', '(+LOOP)', '(?DO)', '(DO)')
total = sum(c[ip] for _, ip, _, _ in g['INS'])
single = collections.Counter(); pairs = collections.Counter()
for k, (w, ip, op, sel) in enumerate(g['INS']):
    single[nm(op, sel)] += c[ip]
    if k + 1 < len(g['INS']) and g['INS'][k + 1][0] == w and not control(op, sel):
        _, ip2, op2, sel2 = g['INS'][k + 1]
        pairs[(nm(op, sel), nm(op2, sel2))] += min(c[ip], c[ip2])
print('ran: %s (status %d); %s dispatches in the shell image\'s code' % (command.replace(shell, './relfsh'), r.returncode, format(total, ',')))
print('\nthe instructions run most:')
for n, v in single.most_common(15): print('  %12s  %5.1f %%  %s' % (format(v, ','), 100 * v / total, n))
print('\nthe adjacent pairs run most (the first not transferring control) - fusion candidates:')
for (a, b), v in pairs.most_common(25): print('  %12s  %5.1f %%  %s %s' % (format(v, ','), 100 * v / total, a, b))
# Iteration 358: relf's 64 one-byte opcodes (QUESTIONS.md A15) - a fused instruction takes the slot of
# an operation that then runs escaped, a dispatch more each time: the k-th best pair against the k-th
# coldest one-byte operation, the net its saving
one = {}
for l in open('engine/opcodes.tab'):
    f = l.split()
    if len(f) >= 3 and f[1].startswith('0x') and f[0] not in ('escaped',) and not f[0].startswith('#'): one[f[2]] = f[0]
# not to displace: ESC itself; DOVAR and DODOES - data words' code fields, run each time a variable or a
# CREATE'd word is, but in no code body, so uncounted here; NOOP - the alignment pad
cold = sorted((single.get(n, 0), n) for n in one if n not in ('ESC', 'DOVAR', 'DODOES', 'NOOP'))
print('\nthe %d one-byte operations, the coldest first (ESC, DOVAR, DODOES and NOOP kept - see above):' % len(one))
print('  ' + ', '.join('%s %s' % (n, format(v, ',')) for v, n in cold[:16]))
print('\nthe budget: each candidate pair displacing the next coldest one-byte operation into the escape band')
cum = 0
for k, ((a, b), v) in enumerate(pairs.most_common(12)):
    dv, dn = cold[k]; net = v - dv; cum += net
    print('  %2d  %-22s %5.2f %%  displaces %-12s %5.3f %%  net %5.2f %%  together %5.2f %%' % (k + 1, a + ' ' + b, 100 * v / total, dn, 100 * dv / total, 100 * net / total, 100 * cum / total))
shutil.rmtree(work, ignore_errors=True)
