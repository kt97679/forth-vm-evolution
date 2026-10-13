import sys, runpy
sys.path.insert(0, '/tmp/b46b/lab/evolve')
sys.argv = ['x']
import evolve as E
orig = E.recorded_genome
FAKE = {'jt28677d13': '28677d13b1', 'jt0af26c8e': '0af26c8e89'}
def rg(i):
    if i in FAKE: return dict(orig(FAKE[i]), jittail=1)
    return orig(i)
E.recorded_genome = rg
sys.argv = ['ans-check.py', '--ids', 'jt28677d13,jt0af26c8e']
runpy.run_path('/tmp/b46b/lab/evolve/ans-check.py', run_name='__main__')
