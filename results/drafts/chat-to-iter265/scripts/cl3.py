import os, sys, shutil, subprocess
os.environ['PATH'] = '/tmp/clangbin:' + os.environ['PATH']
sys.argv = ['x']; sys.path.insert(0, '/home/claude/forth-vm-evolution/lab/evolve'); import evolve as E
E.setup()
GCC_ONLY = ('-fipa-cp-clone', '-ftracer', '-fpeel-loops', '-fno-gcse', '-fno-crossjumping', '-falign-labels=1', '-falign-jumps=1', '-fno-reorder-blocks', '-falign-loops=1')
orig = E.ccflags
E.ccflags = lambda g: ['-Oz' if x in ('-Os', '-O2', '-O3') else x for x in orig(g) if x not in GCC_ONLY]
orig_sh = E.sh
def sh(cmd, **kw):
    r = orig_sh(cmd, **kw)
    if r.returncode and cmd and cmd[0] == 'cc': print('ERR', (r.stdout or b'')[-600:].decode(errors='replace'), (r.stderr or b'')[-600:].decode(errors='replace') if hasattr(r, 'stderr') and r.stderr else '')
    return r
E.sh = sh
g = E.canon(E.recorded_genome('3456ac1e5e')); d = os.path.join(E.EV, 'cl3'); shutil.rmtree(d, ignore_errors=True)
try: E.build(g, d)
except Exception as e: print('died', str(e)[:100])
