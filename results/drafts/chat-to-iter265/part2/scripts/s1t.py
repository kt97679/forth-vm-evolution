import subprocess
for prog in (b': w1 5 . ; w1 CR\n', b': w1 5 . ; : w8 w1 w1 ; w8 CR\n', b': \xd1\x81 5 . ; \xd1\x81 CR\n', b': a 5 . ; : b a ; b CR\n'):
    r = subprocess.run(['./s1-sod16-64', 's1-sod16-s64.img'], input=prog + b'BYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
    print(repr(prog[:40]), r.returncode, r.stdout.replace(b'\r', b'')[:120])
