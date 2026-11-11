/*
 *  rt-linux-armv7.c - rt-linux-i386.c's twin for 32-bit ARM, EABI hard-float
 *  (Iteration 570): what an engine needs from the C library, without it, over
 *  ARM's svc #0 system calls - so an ARM engine is the design's own bytes, as
 *  on x86 (static glibc made one 347,688 bytes against x86's 12,916:
 *  results/drafts/tegra-cross-568.py). This file gives what differs: the
 *  system calls (the number in r7, six arguments in r0-r5; the numbers are
 *  i386's but exit_group, 248 here), the signals, the entry point, and memcpy,
 *  memmove and memset (the portable part's are x86 string instructions:
 *  RT_OWN_MEM). The rest - the allocator, the environment, the user database,
 *  snprintf - is rt-linux-x86_64.c's, included below with RT_PORTABLE_ONLY:
 *  one copy, fixed once. evolve.py's rt() links it so on an ARM host (the
 *  Tegra, GCC) and for a clang design cross-built on the laptop
 *  (EVOLVE_TARGET=armv7):
 *
 *      -static -no-pie -nostdlib -fno-stack-protector -D_FORTIFY_SOURCE=0
 *      engine/rt-linux-armv7.c -lgcc
 *
 *  libgcc supplies the EABI division helpers (__aeabi_idiv, __aeabi_uldivmod).
 *  The assembly is ARM state (.arm), callable from Thumb code too. WHAT IS
 *  GIVEN UP is rt-linux-x86_64.c's.
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

/* ---- system calls: svc #0, the number in r7 and six arguments in r0-r5 -
 * r7 the Thumb frame pointer, so the call is a function of its own: n a b c
 * arrive in r0-r3, d e f on the stack; r4, r5 and r7 saved */
__asm__(".text\n.arm\n.align 2\n.globl rt_sc6\n.type rt_sc6,%function\nrt_sc6:\n"
        "\tpush {r4, r5, r7, lr}\n"
        "\tmov r7, r0\n\tmov r0, r1\n\tmov r1, r2\n\tmov r2, r3\n"
        "\tldr r3, [sp, #16]\n\tldr r4, [sp, #20]\n\tldr r5, [sp, #24]\n"
        "\tsvc #0\n"
        "\tpop {r4, r5, r7, pc}\n"
        ".size rt_sc6, .-rt_sc6\n");
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
int isatty(int fd) { long t[16]; return S(54, fd, 0x5401, t) == 0; }   /* ioctl TCGETS: Iteration 231 */
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
int rt_open(const char *p, int flags, int mode) { return (int)S(5, p, flags, mode); }   /* vm-lab.c's OPEN3 */
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
void _exit(int s)                              { for (;;) sc(248, s, 0, 0, 0, 0, 0); }   /* exit_group: ARM's */
void exit(int s)                               { _exit(s); }
void abort(void)
{
    sc(37, sc(20, 0, 0, 0, 0, 0, 0), SIGABRT, 0, 0, 0, 0);
    _exit(128 + SIGABRT);
}
int raise(int sig) { return (int)S(37, sc(20, 0, 0, 0, 0, 0, 0), sig, 0); }   /* libgcc's __aeabi_idiv0: SIGFPE */
void __stack_chk_fail(void) { abort(); }

/* ---- signals: the kernel's struct - its mask two words, as i386's - and a
 * restorer returning through rt_sigreturn (173), in ARM state */
__asm__(".text\n.arm\n.align 2\n.globl rt_restorer\n.type rt_restorer,%function\nrt_restorer:\n"
        "\tmov r7, #173\n\tsvc #0\n"
        ".size rt_restorer, .-rt_restorer\n");
void rt_restorer(void);
struct k_sigaction { void *handler; unsigned long flags; void *restorer; unsigned long mask[2]; };
int sigemptyset(sigset_t *s) { unsigned char *p = (unsigned char *)s; for (size_t i = 0; i < sizeof *s; i++) p[i] = 0; return 0; }
void rt_fault(void (*h)(int)) {                 /* Iteration 252's, ARM's rt_sigaction 174 */
    struct k_sigaction k = { (void *)h, 0x04000000UL, (void *)rt_restorer, { 0, 0 } };
    sc(174, 11, (long)&k, 0, 8, 0, 0);
}
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

/* ---- memory: byte loops, each with an empty asm in its body - without it
 * GCC and clang recognise the copying loop and turn it into a call to memcpy,
 * which here is this function. Speed does not matter: the engine copies at
 * its start, never in its inner loop. */
void *memcpy(void *restrict d, const void *restrict s, size_t n)
{
    unsigned char *p = d; const unsigned char *q = s;
    while (n--) { *p++ = *q++; __asm__ volatile ("" ::: "memory"); }
    return d;
}
void *memmove(void *d, const void *s, size_t n)
{
    if ((uintptr_t)d - (uintptr_t)s >= n) return memcpy(d, s, n);   /* no overlap from the end */
    unsigned char *p = (unsigned char *)d + n; const unsigned char *q = (const unsigned char *)s + n;
    while (n--) { *--p = *--q; __asm__ volatile ("" ::: "memory"); }
    return d;
}
void *memset(void *d, int c, size_t n)
{
    unsigned char *p = d;
    while (n--) { *p++ = (unsigned char)c; __asm__ volatile ("" ::: "memory"); }
    return d;
}

#define RT_PORTABLE_ONLY 1
#define RT_OWN_MEM 1
#include "rt-linux-x86_64.c"

/* ---- the entry point: argc, argv..., 0, envp..., 0 at sp; three arguments
 * in r0-r2, the stack 8-aligned at the call as the AAPCS asks ---- */
int main(int, char **);
__attribute__((used, noreturn)) void rt_main(long argc, char **argv, char **envp)
{
    environ = envp;
    exit(main((int)argc, argv));
}
__asm__(".text\n.arm\n.align 2\n.globl _start\n.type _start,%function\n_start:\n"
        "\tmov fp, #0\n\tmov lr, #0\n"
        "\tldr r0, [sp]\n"                  /* argc */
        "\tadd r1, sp, #4\n"                /* argv */
        "\tadd r2, r1, r0, lsl #2\n"
        "\tadd r2, r2, #4\n"                /* envp: past argv's null */
        "\tbic sp, sp, #7\n"
        "\tbl rt_main\n"
        "\tudf #0\n"
        ".size _start, .-_start\n");
