import subprocess
for prog in (b': X 5 . ; X CR\n', b': Y DUP + ; 3 Y . CR\n', b'S" extend.4" INCLUDED\n', b"' DUP PRIMITIVE? . ' WORDS PRIMITIVE? . ' COLD PRIMITIVE? . CR\n"):
    r = subprocess.run(['./relf-64', 'kernel.img'], input=prog + b'BYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    print(repr(prog[:40]), r.returncode, r.stdout.replace(b'\r', b'')[-160:])
