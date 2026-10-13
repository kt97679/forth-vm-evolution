import subprocess
prog = b"' DUP . ' OPEN-FILE . ' (PRIMITIVES-END) . ' PRIMITIVE? . CR ' PRIMITIVE? DUP @ . CELL+ DUP @ . CELL+ DUP @ . CELL+ @ . CR START @ . CR\n"
r = subprocess.run(['./relf-64', 's1.img'], input=prog + b'BYE\n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20, cwd='/tmp/rs2')
print(r.stdout.replace(b'\r', b'').decode())
