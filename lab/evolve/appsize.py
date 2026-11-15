"""lab/evolve/appsize.py - an application's code bytes, one definition for genapps.py and evolve.py (Iteration 677:
step 0 of results/drafts/search-reopen-plan-677.md - the size score counts the selection's four applications).

code = HERE's advance over the program's load, less its data: what the program's own ALLOT , and C, lay. Two loads,
each a driver file INCLUDED from standard input that INCLUDEs the program (genapps.py's driver since 674, moved here
unchanged): 'size' reads HERE's advance alone; 'count' reads the data, with ALLOT , and C, redefined to count through
their old xts. The count's own advance is not used: a redefined , is a call where the kernel's may be one byte.
The driver's text and file names stand before HERE's first reading, so a caller uses these, not its own."""
import collections, json, re, sys

SELECTION = ('sim16', 'gc16', 'scan', 'evo')      # the `apps` workload's four (evolve.py's APPS_IN), in its order
FILES = {'sim16': 'sim16.fth', 'gc16': 'gc16.fth', 'scan': 'scan.fth', 'evo': 'evo.fth'}
COUNT = ("VARIABLE DATA#  0 DATA# !\n' ALLOT CONSTANT 'ALLOT  ' , CONSTANT ',  ' C, CONSTANT 'C,\n"
         ": ALLOT DUP DATA# +! 'ALLOT EXECUTE ;  : , 1 CELLS DATA# +! ', EXECUTE ;  : C, 1 DATA# +! 'C, EXECUTE ;\n")

def text(inc, mode, pre=''):
    """The driver for mode 'size' or 'count': pre (a prelude's INCLUDED line), inc (the program's INCLUDE line)."""
    t = pre + (COUNT if mode == 'count' else '')
    return t + 'VARIABLE H0  HERE H0 !\n' + inc + '777001 . HERE H0 @ - . %s 777002 . CR\n' % ('DATA# @ .' if mode == 'count' else '') + 'BYE\n'

def lab_text(app, mode):
    """The driver for one of the lab's own programs (no prelude): genapps.py's for kind 'lab'."""
    return text('S" %s" INCLUDED\n' % FILES[app], mode)

def driver_name(app, mode, kind='lab'):
    return '%s-%s-%s.fs' % (kind, app, mode)

def stdin(app, mode, kind='lab'):
    """What a lab or relf system reads to run the driver."""
    return ('S" %s" INCLUDED\n' % driver_name(app, mode, kind)).encode()

def parse(out_size, out_count):
    """(total, data) from the two loads' output, or None if either has no reading."""
    m1 = re.search(r'777001 (-?\d+) +777002', out_size); m2 = re.search(r'777001 (-?\d+) (-?\d+) +777002', out_count)
    if not m1 or not m2: return None
    return int(m1.group(1)), int(m2.group(2))

def new_size(r):
    """Iteration 679: a record's total counts the applications' code (Iteration 678's measure) - it has 'app'."""
    return 'app' in r

def one_size(recs, what):
    """Iteration 679 (the plan's step 0): the alive records of the two sizes - total with the applications' code and
    without - are never pooled; exits naming both counts. recs: records (an iterable, read once); what: the caller.
    True when they count the applications' code."""
    k = collections.Counter(new_size(r) for r in recs if r.get('status') == 'ok' and r.get('speed') and r.get('total'))
    if len(k) > 1:
        sys.exit('%s: %d designs sized with the applications\' code (Iteration 678) and %d without - two measures, '
                 'never pooled: re-measure the old ones, or compare each with its own' % (what, k[True], k[False]))
    return bool(k[True])

def db_records(path):
    """A database's JSON lines, the unreadable skipped."""
    for l in open(path, errors='replace'):
        try: yield json.loads(l)
        except ValueError: pass
