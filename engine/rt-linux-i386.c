/*
 *  rt-linux-i386.c - rt-linux-x86_64.c's twin for 32-bit x86 (Iteration 140):
 *  what an engine needs from the C library, without it, over i386's int $0x80
 *  system calls - so the 4-byte half leaves the C library too. This file gives
 *  what differs: the system calls and their numbers, the signals, the entry
 *  point. The rest - memory and strings, the allocator, the environment, the
 *  user database, snprintf - is that file's, included below with
 *  RT_PORTABLE_ONLY: one copy, fixed once. An engine linked with
 *
 *      -m32 -static -no-pie -nostdlib -fno-stack-protector -D_FORTIFY_SOURCE=0
 *      engine/rt-linux-i386.c -lgcc
 *
 *  has no C library at all (libgcc supplies the 64-bit division helpers).
 *  tools/build-stages.sh does this with ENGINE_RT=nolibc. No
 *  _FILE_OFFSET_BITS=64 anywhere: off_t and rlim_t are 32 bits, so lseek and
 *  ugetrlimit, not their 64-bit forms. WHAT IS GIVEN UP is that file's.
 */
#include <stddef.h>
#include <stdarg.h>
#include <stdint.h>
#include <errno.h>
#include <unistd.h>
#include <pwd.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/types.h>
#include <sys/wait.h>

char **environ;
static int rt_errno;
int *__errno_location(void) { return &rt_errno; }

/* ---- system calls: int $0x80, the number in eax and six arguments in ebx,
 * ecx, edx, esi, edi and ebp - the frame pointer, so the call is a function
 * of its own that reads them from its stack frame and restores what it used */
__asm__(".text\n.globl rt_sc6\n.type rt_sc6,@function\nrt_sc6:\n"
        "\tpush %ebp\n\tpush %edi\n\tpush %esi\n\tpush %ebx\n"
        "\tmov 20(%esp), %eax\n\tmov 24(%esp), %ebx\n\tmov 28(%esp), %ecx\n"
        "\tmov 32(%esp), %edx\n\tmov 36(%esp), %esi\n\tmov 40(%esp), %edi\n"
        "\tmov 44(%esp), %ebp\n"
        "\tint $0x80\n"
        "\tpop %ebx\n\tpop %esi\n\tpop %edi\n\tpop %ebp\n\tret\n");
long rt_sc6(long n, long a, long b, long c, long d, long e, long f);
static long sc(long n, long a, long b, long c, long d, long e, long f) { return rt_sc6(n, a, b, c, d, e, f); }
static long ok(long r)       /* the kernel's -errno to the library's -1 */
{
    if (r < 0 && r > -4096) { rt_errno = (int)-r; return -1; }
    return r;
}
#define S(n, a, b, c) ok(sc((n), (long)(a), (long)(b), (long)(c), 0, 0, 0))

ssize_t read(int fd, void *b, size_t n)        { return S(3, fd, b, n); }
ssize_t write(int fd, const void *b, size_t n) { return S(4, fd, b, n); }
int mprotect(void *a, size_t n, int p)        { return (int)S(125, a, n, p); }
int getrusage(__rusage_who_t w, struct rusage *u) { return (int)S(77, w, u, 0); }
long syscall(long n, ...)
{
    va_list ap; long a[6]; int i;
    va_start(ap, n); for (i = 0; i < 6; i++) a[i] = va_arg(ap, long); va_end(ap);
    return ok(sc(n, a[0], a[1], a[2], a[3], a[4], a[5]));
}
int close(int fd)                              { return (int)S(6, fd, 0, 0); }
off_t lseek(int fd, off_t o, int w)            { return S(19, fd, o, w); }
int pipe(int fd[2])                            { return (int)S(42, fd, 0, 0); }
int dup2(int a, int b)                         { return (int)S(63, a, b, 0); }
pid_t getpid(void)                             { return (pid_t)S(20, 0, 0, 0); }
pid_t fork(void)                               { return (pid_t)S(2, 0, 0, 0); }
int execve(const char *p, char *const a[], char *const e[]) { return (int)S(11, p, a, e); }
pid_t waitpid(pid_t p, int *s, int o)          { return (pid_t)ok(sc(114, p, (long)s, o, 0, 0, 0)); }   /* wait4 */
char *getcwd(char *b, size_t n)                { return S(183, b, n, 0) < 0 ? NULL : b; }
int chdir(const char *p)                       { return (int)S(12, p, 0, 0); }
int unlink(const char *p)                      { return (int)S(10, p, 0, 0); }
int getrlimit(__rlimit_resource_t r, struct rlimit *l)       { return (int)S(191, r, l, 0); }   /* ugetrlimit */
int setrlimit(__rlimit_resource_t r, const struct rlimit *l) { return (int)S(75, r, l, 0); }
int open(const char *p, int flags, ...)
{
    int mode = 0;
#ifndef O_TMPFILE
#define O_TMPFILE (020000000 | O_DIRECTORY)
#endif
    if ((flags & O_CREAT) || (flags & O_TMPFILE) == O_TMPFILE) {
        va_list ap; va_start(ap, flags); mode = va_arg(ap, int); va_end(ap);
    }
    return (int)S(5, p, flags, mode);
}
void *mmap(void *a, size_t n, int prot, int flags, int fd, off_t o)
{
    long r = sc(192, (long)a, (long)n, prot, flags, fd, (long)((unsigned long)o >> 12));   /* mmap2: pages */
    if (r < 0 && r > -4096) { rt_errno = (int)-r; return MAP_FAILED; }
    return (void *)r;
}
int munmap(void *a, size_t n)                  { return (int)S(91, a, n, 0); }
void _exit(int s)                              { for (;;) sc(252, s, 0, 0, 0, 0, 0); }   /* exit_group */
void exit(int s)                               { _exit(s); }
void abort(void)
{
    sc(37, sc(20, 0, 0, 0, 0, 0, 0), SIGABRT, 0, 0, 0, 0);
    _exit(128 + SIGABRT);
}
void __stack_chk_fail(void) { abort(); }

/* ---- signals: i386's kernel struct - its mask two words - and a restorer
 * returning through rt_sigreturn (173) */
__asm__(".text\n.globl rt_restorer\n.type rt_restorer,@function\nrt_restorer:\n"
        "\tmov $173, %eax\n\tint $0x80\n\thlt\n");
void rt_restorer(void);
struct k_sigaction { void *handler; unsigned long flags; void *restorer; unsigned long mask[2]; };
int sigemptyset(sigset_t *s) { unsigned char *p = (unsigned char *)s; for (size_t i = 0; i < sizeof *s; i++) p[i] = 0; return 0; }
int sigaction(int sig, const struct sigaction *restrict act, struct sigaction *restrict old)
{
    struct k_sigaction k, ko;
    if (act) {
        k.handler = (void *)act->sa_handler;
        k.flags = (unsigned long)act->sa_flags | 0x04000000UL;   /* SA_RESTORER */
        k.restorer = (void *)rt_restorer;
        memcpy(k.mask, &act->sa_mask, sizeof k.mask);            /* the kernel's 64 */
    }
    long r = ok(sc(174, sig, act ? (long)&k : 0, old ? (long)&ko : 0, 8, 0, 0));
    if (r == 0 && old) {
        sigemptyset(&old->sa_mask);
        old->sa_handler = (void (*)(int))ko.handler;
        old->sa_flags = (int)ko.flags;
        memcpy(&old->sa_mask, ko.mask, sizeof ko.mask);
    }
    return (int)r;
}
int sigaltstack(const stack_t *restrict ss, stack_t *restrict old) { return (int)ok(sc(186, (long)ss, (long)old, 0, 0, 0, 0)); }

#define RT_PORTABLE_ONLY 1
#include "rt-linux-x86_64.c"

/* ---- the entry point: argc, argv..., 0, envp..., 0 on the stack; three
 * arguments pushed, the stack 16-aligned at the call as gcc assumes ---- */
int main(int, char **);
__attribute__((used, noreturn)) void rt_main(long argc, char **argv, char **envp)
{
    environ = envp;
    exit(main((int)argc, argv));
}
__asm__(".text\n.globl _start\n.type _start,@function\n_start:\n"
        "\txor %ebp, %ebp\n"
        "\tmov (%esp), %eax\n"              /* argc */
        "\tlea 4(%esp), %ecx\n"             /* argv */
        "\tlea 4(%ecx,%eax,4), %edx\n"      /* envp: past argv's null */
        "\tand $-16, %esp\n"
        "\tsub $4, %esp\n"
        "\tpush %edx\n\tpush %ecx\n\tpush %eax\n"
        "\tcall rt_main\n"
        "\thlt\n");
