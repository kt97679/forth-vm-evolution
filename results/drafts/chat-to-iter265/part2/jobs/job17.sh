#!/bin/sh
cd /tmp/b44
runuser -u claude -- python3 /tmp/pages.py /tmp/b44 d3149e10c6 fib,loop,corpus,kernel > /tmp/p-before.log 2>&1
python3 - <<'PY'
p = '/tmp/b44/engine/vm-lab.c'
s = open(p).read()
old = 'static struct fbuf { int fd, len, pos, raw; UNS8 b[FBUFSZ]; } t_fb[FBUFN];'
new = '''/*  Iteration 225: the slots' state together, their buffers apart. With each
    buffer inside its slot, t_fslot's scan of the fd fields touched one page a
    slot - 8 pages (32 KB) at 4 KB buffers, the first time any file was read -
    and the fbuf gene bought that back with smaller buffers and more read(2).
    Apart, the scan touches the state's one page; a buffer is touched when its
    slot reads.  */
static UNS8 t_fbb[FBUFN][FBUFSZ];
static struct fbuf { int fd, len, pos, raw; UNS8 *b; } t_fb[FBUFN];'''
assert s.count(old) == 1; s = s.replace(old, new)
old = '''    t_fb[free_].fd = fd; t_fb[free_].len = t_fb[free_].pos = 0;'''
new = '''    t_fb[free_].fd = fd; t_fb[free_].len = t_fb[free_].pos = 0; t_fb[free_].b = t_fbb[free_];'''
assert s.count(old) == 1; s = s.replace(old, new)
open(p, 'w').write(s)
PY
runuser -u claude -- env LAYOUTS=1 bash tools/build-stages.sh > /tmp/p-build.log 2>&1
runuser -u claude -- python3 /tmp/pages.py /tmp/b44 d3149e10c6 fib,loop,corpus,kernel > /tmp/p-after.log 2>&1
touch /tmp/job17.done
