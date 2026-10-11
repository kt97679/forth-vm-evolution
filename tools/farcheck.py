"""tests/core/far.fth's verdict (Iteration 158): line k prints k*100000 plus its
answer; every answer right, and any missing one refused out loud - never
something else computed. Used by run-tests.sh and the evolution's gate."""
import sys, re
WANT = {1: 144, 2: 7, 3: 42, 4: 12, 5: 233, 6: 11, 7: 8, 8: 44, 9: 16, 10: 1, 11: 1}   # 10, 11: the gaps taken (Iteration 161)
def verdict(out, code):
    """'all' | 'refused N' | a failure - right or refused out loud, never else."""
    out = out.replace('\r', ''); got = {}
    for l in out.split('\n'):
        if re.fullmatch(r'[0-9]+ ', l):
            n = int(l); k, v = divmod(n, 100000)
            if WANT.get(k) != v or k in got: return 'WRONG line %d: %d' % (k, v)
            got[k] = v
    if code not in (0,): return 'died (exit %s) after %d answers' % (code, len(got))
    if len(got) == len(WANT): return 'all'
    if re.search(r'out of reach|beyond|dictionary full', out): return 'refused %d of %d' % (len(WANT) - len(got), len(WANT))
    return 'MISSING %d answers, no refusal' % (len(WANT) - len(got))
if __name__ == '__main__': print(verdict(sys.stdin.read(), int(sys.argv[1])))
