import os, sys, shutil
tree = sys.argv[1]; out = sys.argv[2]; ids = sys.argv[3:]
sys.argv = ['x']; sys.path.insert(0, os.path.join(tree, 'lab', 'evolve')); import evolve as E
E.setup()
for i in ids:
    d = os.path.join(E.EV, 'engid'); eng, img = E.build(E.canon(E.recorded_genome(i)), d)
    shutil.copy(eng, os.path.join(out, i + '.engine')); shutil.copy(img, os.path.join(out, i + '.image'))
    print(i, os.path.getsize(eng), os.path.getsize(img), flush=True)
