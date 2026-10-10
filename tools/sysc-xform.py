"""Apply the gene sysc's engine transformation (Iterations 133, 141) to an engine source:
the eighteen shell primitives' table entries and handlers under SYSC, SYSCALL in FORK's slot."""
import re, sys
P1 = ['L_system', 'L_execve', 'L_waitpid', 'L_pipe', 'L_dup2', 'L_getenv', 'L_setenv', 'L_sysexit', 'L_chdir', 'L_getcwd',
      'L_sysargc', 'L_sysarg', 'L_getpwhome', 'L_getfsize', 'L_setfsize', 'L_getpid', 'L_unsetenv']
def xform(path, name):
    s = open(path).read()
    if 'L_syscall' in s: return 'already has SYSC'
    need = ['DS0', 'DS1', 'dsp', 'CELL_BYTES', 'NEXT()', 'g_argc', 'g_argv', 't_flush']
    miss = [t for t in need if t not in s]
    if miss: return 'MISSING %s' % miss
    for l in P1 + ['L_fork']:
        if s.count('&&' + l + ',') + s.count('&&' + l + '\n') != 1: return 'table: %s x%d' % (l, s.count('&&' + l))
    for l in P1: s = re.sub(r'&&' + l + r'(?=[,\n])', 'SYSX(' + l + ')', s)
    s = re.sub(r'&&L_fork(?=[,\n])', 'SYSF', s)
    L = s.split('\n')
    labs = [i for i, x in enumerate(L) if re.match(r'^L_[a-z0-9_]+:', x)]
    nxt = {i: j for i, j in zip(labs, labs[1:])}
    wrap = sorted((i, nxt[i]) for i in labs if L[i].split(':')[0] in P1 + ['L_fork'] and i in nxt)
    if len(wrap) != 18: return 'handlers: %d of 18' % len(wrap)
    for a, b in reversed(wrap): L.insert(b, '#endif /* !SYSC */'); L.insert(a, '#if !SYSC')
    s = '\n'.join(L)
    at = s.index('#if !SYSC\nL_fork:')
    s = s[:at] + '''#if SYSC
/* The gene sysc (Iterations 133, 141; %s from Iteration 142): one system call in
 * FORK's slot, the shell's process and environment words written in Forth on it
 * (forth/shell-sysc.4); the other seventeen gone. ( block num --- r ): the six
 * arguments in the block, r the kernel's result - on failure -errno; num -1, -2,
 * -3: argc, argv, the initial environment. x86-64's numbers; i386's mapped. */
L_syscall: {
    long num = (long)(INT64)DS0, r;
    const UNS64 *a = (const UNS64 *)(uintptr_t)DS1;
    t_flush();
    if (num < 0) r = num == -1 ? (long)g_argc : num == -2 ? (long)(uintptr_t)g_argv : num == -3 ? (long)(uintptr_t)environ : -1;
    else {
        if (num == 60 || num == 231) { PROFDUMP; }
#if defined(__i386__)
        num = sysc_i386(num);
        if (num < 0) r = -38;                                  /* ENOSYS */
        else
#endif
        r = syscall(num, (long)a[0], (long)a[1], (long)a[2], (long)a[3], (long)a[4], (long)a[5]);
        if (r == -1) r = -(long)errno;
    }
    DS1 = (UNS64)(INT64)r;
    dsp += CELL_BYTES;
    NEXT();
}
L_nosys:   /* a primitive the gene sysc removed: the shell's are Forth now */
    t_flush(); _exit(70);
#endif
''' % name + s[at:]
    tab = s.index('SYSF')
    start = s.rfind('\n', 0, s.rfind('{', 0, tab))
    s = s[:start] + '''
#if SYSC
#if !defined(__x86_64__) && !defined(__i386__)
#error "the gene sysc: the image's system-call numbers are x86-64 Linux's (i386's mapped)"
#endif
#define SYSF &&L_syscall
#define SYSX(l) &&L_nosys
#else
#define SYSF &&L_fork
#define SYSX(l) &&l
#endif''' + s[start:]
    L = s.split('\n'); first = [i for i, l in enumerate(L) if l.startswith('#include <')][0]
    L.insert(first, '''#if SYSC
#include <errno.h>      /* SYSCALL's -errno */
#ifndef PROFDUMP
#define PROFDUMP        /* an engine without the profiler */
#endif
#endif
#if SYSC && defined(__i386__)
/* The image's numbers are x86-64 Linux's; i386's for the calls the shell's
   overlay makes (forth/shell-sysc.4). Any other: ENOSYS. */
static long sysc_i386(long n)
{
    switch (n) {
    case 39: return 20;   case 57: return 2;    case 33: return 63;   case 80: return 12;
    case 231: return 252; case 79: return 183;  case 61: return 114;  case 22: return 42;
    case 97: return 191;  case 160: return 75;  case 59: return 11;   default: return -1;
    }
}
#endif''')
    open(path, 'w').write('\n'.join(L)); return 'transformed'
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p, xform(p, p.split('/')[-1]))
