import subprocess
for prog in (b"' DUP PRIMITIVE? . ' OPEN-FILE PRIMITIVE? . ' COLD PRIMITIVE? . ' (PRIMITIVES-END) PRIMITIVE? . CR\n", b': Y DUP + ; 3 Y . CR\n'):
    r = subprocess.run(['./relf-64', 's1.img'], input=prog + b'BYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20, cwd='/tmp/rs2')
    print(repr(prog[:50]), r.returncode, r.stdout.replace(b'\r', b'')[-200:])
r = subprocess.run(['./relf-64', 'kernel.img'], input=b'S" extend.4" INCLUDED\nS" cross.4" INCLUDED\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd='/tmp/rs2')
print('stage 2:', r.returncode, r.stdout.replace(b'\r', b'')[-600:])
