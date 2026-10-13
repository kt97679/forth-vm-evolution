import os, sys, shutil, subprocess
sys.argv = ['x']; sys.path.insert(0, '/tmp/b46b/lab/evolve'); import evolve as E
E.setup()
for did in ('add5ec8937', 'cc6d168e0a'):
    g = E.canon(E.recorded_genome(did)); d = os.path.join(E.EV, 't6'); shutil.rmtree(d, ignore_errors=True)
    eng, img = E.build(g, d)
    for f in ('extend.4', 'coreext.4'): shutil.copy('/tmp/b46b/forth/' + f, os.path.join(d, f))
    prog = (b'S" extend.4" INCLUDED\nS" coreext.4" INCLUDED\n'
            b": \xd1\x81\xd1\x83\xd0\xbf 8 . ;\n"
            b"' DUP >NAME NAME>STRING TYPE SPACE ' \xd1\x81\xd1\x83\xd0\xbf >NAME NAME>STRING TYPE SPACE ' \xd1\x81\xd1\x83\xd0\xbf >NAME NAME>INTERPRET EXECUTE :NONAME 1 ; >NAME . CR\nBYE\n")
    r = subprocess.run([eng, img], input=prog, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, cwd=d)
    print(did, r.returncode, r.stdout.replace(b'\r', b'').decode(errors='replace').strip().split('\n')[-2:])
