import subprocess, sys
lines = [': суп 5 . ;  : обед суп суп ;  обед CR', ': café 9 . ;  : menu café ;  menu CR', ': voilà 3 . ;  : w2 voilà voilà ;  w2 CR',
         ': a°b 4 . ;  : w3 a°b ;  w3 CR', ': x123456789012345678901234567890 1 . ;  : w5 x123456789012345678901234567890 ;  w5 CR',
         ': ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ 2 . ;  : w6 ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ ;  w6 CR', ': ёж 11 . ; IMMEDIATE  : w7 ёж ;  CR', ': w1 5 . ; : w8 w1 w1 ; w8 CR']
for i, l in enumerate(lines, 1):
    for s in ('s0-cell', 's6-cv8b'):
        r = subprocess.run(['./%s-64' % s, '%s-s64.img' % s], input=(l + '\nBYE\n').encode(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
        print(i, s, r.returncode, r.stdout.replace(b'\r', b'').split(b'\n', 1)[-1][:70])
