import subprocess, os, shutil
W = '/tmp/rs4'; lines = open(W + '/cross32.4').read().split('\n')
def fails(n):
    open(W + '/c32part.4', 'w').write('\n'.join(lines[:n]) + '\n')
    shutil.copy(W + '/s1.img', W + '/t.img')
    r = subprocess.run([W + '/relf-64', 't.img'], cwd=W, input=b'S" extend.4" INCLUDED\nS" c32part.4" INCLUDED\nBYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
    return b'Stack error' in r.stdout
lo, hi = 1, len(lines)
print('whole file fails:', fails(hi))
while hi - lo > 1:
    mid = (lo + hi) // 2
    if fails(mid): hi = mid
    else: lo = mid
print('first failing line %d:' % hi)
for k in range(max(0, hi - 6), hi): print(k + 1, lines[k][:150])
