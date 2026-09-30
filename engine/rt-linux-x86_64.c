/*
 *  rt-linux-x86_64.c - what an engine needs from the C library, without it.
 *
 *  WHY. A dynamically linked C program cannot start faster than the C
 *  library can be loaded. On the development VM /bin/true takes 0.62 ms,
 *  a program with no library 0.066 ms, and the CV8 engine 0.67 ms - its
 *  own start-up work is the last 0.05. Of its 1,264 KB resident, 1,132 KB
 *  are the C library and the dynamic loader. Linking statically does not
 *  help: the library moves into the engine and 716 KB of it stays
 *  resident. The engines use little of it - system calls, an allocator,
 *  the environment, one user-database lookup and, in SPN's diagnostics,
 *  snprintf - so this file is exactly that, over raw Linux system calls,
 *  for x86-64. An engine linked with
 *
 *      -static -no-pie -nostdlib -fno-stack-protector -D_FORTIFY_SOURCE=0
 *      engine/rt-linux-x86_64.c -lgcc
 *
 *  has no C library at all (libgcc supplies the 128-bit division helper).
 *  tools/build-stages.sh does this with ENGINE_RT=nolibc.
 *
 *  WHAT IS GIVEN UP. getpwnam reads /etc/passwd only. The C library's
 *  goes through NSS - LDAP, SSSD, systemd-homed - and an engine built
 *  with it resolves ~name for users this one cannot see. That is the one
 *  behaviour this file changes.
 *
 *  It compiles against the C library's HEADERS, so each definition here
 *  has the prototype the engine was compiled against; only the library is
 *  left out. Failures follow the library's convention - -1, or NULL, and
 *  errno - not the kernel's negative error numbers.
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

/* ---- system calls ---------------------------------------------------- */
static long sc(long n, long a, long b, long c, long d, long e, long f)
{
    register long r10 __asm__("r10") = d;
    register long r8 __asm__("r8") = e;
    register long r9 __asm__("r9") = f;
    long r;
    __asm__ volatile ("syscall" : "=a"(r)
                      : "a"(n), "D"(a), "S"(b), "d"(c), "r"(r10), "r"(r8), "r"(r9)
                      : "rcx", "r11", "memory");
    return r;
}
static long ok(long r)       /* the kernel's -errno to the library's -1 */
{
    if (r < 0 && r > -4096) { rt_errno = (int)-r; return -1; }
    return r;
}
#define S(n, a, b, c) ok(sc((n), (long)(a), (long)(b), (long)(c), 0, 0, 0))

ssize_t read(int fd, void *b, size_t n)        { return S(0, fd, b, n); }
ssize_t write(int fd, const void *b, size_t n) { return S(1, fd, b, n); }
int close(int fd)                              { return (int)S(3, fd, 0, 0); }
off_t lseek(int fd, off_t o, int w)            { return S(8, fd, o, w); }
int pipe(int fd[2])                            { return (int)S(22, fd, 0, 0); }
int dup2(int a, int b)                         { return (int)S(33, a, b, 0); }
pid_t getpid(void)                             { return (pid_t)S(39, 0, 0, 0); }
pid_t fork(void)                               { return (pid_t)S(57, 0, 0, 0); }
int execve(const char *p, char *const a[], char *const e[]) { return (int)S(59, p, a, e); }
pid_t waitpid(pid_t p, int *s, int o)          { return (pid_t)ok(sc(61, p, (long)s, o, 0, 0, 0)); }
char *getcwd(char *b, size_t n)                { return S(79, b, n, 0) < 0 ? NULL : b; }
int chdir(const char *p)                       { return (int)S(80, p, 0, 0); }
int unlink(const char *p)                      { return (int)S(87, p, 0, 0); }
int getrlimit(__rlimit_resource_t r, struct rlimit *l)       { return (int)S(97, r, l, 0); }
int setrlimit(__rlimit_resource_t r, const struct rlimit *l) { return (int)S(160, r, l, 0); }
int open(const char *p, int flags, ...)
{
    int mode = 0;
#ifndef O_TMPFILE
#define O_TMPFILE (020000000 | O_DIRECTORY)     /* only with _GNU_SOURCE */
#endif
    if ((flags & O_CREAT) || (flags & O_TMPFILE) == O_TMPFILE) {
        va_list ap; va_start(ap, flags); mode = va_arg(ap, int); va_end(ap);
    }
    return (int)S(2, p, flags, mode);
}
void *mmap(void *a, size_t n, int prot, int flags, int fd, off_t o)
{
    long r = sc(9, (long)a, (long)n, prot, flags, fd, o);
    if (r < 0 && r > -4096) { rt_errno = (int)-r; return MAP_FAILED; }
    return (void *)r;
}
int munmap(void *a, size_t n)                  { return (int)S(11, a, n, 0); }
void _exit(int s)                              { for (;;) sc(231, s, 0, 0, 0, 0, 0); }
void exit(int s)                               { _exit(s); }   /* no stdio to flush */
void abort(void)
{
    sc(62, sc(39, 0, 0, 0, 0, 0, 0), SIGABRT, 0, 0, 0, 0);
    _exit(128 + SIGABRT);
}
void __stack_chk_fail(void) { abort(); }   /* built with -fno-stack-protector: unused */

/* ---- signals: the kernel's struct, and a restorer to return through ---- */
__asm__(".text\n.globl rt_restorer\n.type rt_restorer,@function\nrt_restorer:\n"
        "\tmov $15, %eax\n\tsyscall\n\thlt\n");
void rt_restorer(void);
struct k_sigaction { void *handler; unsigned long flags; void *restorer; unsigned long mask; };
int sigemptyset(sigset_t *s) { unsigned char *p = (unsigned char *)s; for (size_t i = 0; i < sizeof *s; i++) p[i] = 0; return 0; }
int sigaction(int sig, const struct sigaction *restrict act, struct sigaction *restrict old)
{
    struct k_sigaction k, ko;
    if (act) {
        k.handler = (void *)act->sa_handler;           /* a union with sa_sigaction */
        k.flags = (unsigned long)act->sa_flags | 0x04000000UL;   /* SA_RESTORER */
        k.restorer = (void *)rt_restorer;
        k.mask = *(const unsigned long *)&act->sa_mask;          /* the kernel's 64 */
    }
    long r = ok(sc(13, sig, act ? (long)&k : 0, old ? (long)&ko : 0, 8, 0, 0));
    if (r == 0 && old) {
        sigemptyset(&old->sa_mask);
        old->sa_handler = (void (*)(int))ko.handler;
        old->sa_flags = (int)ko.flags;
        *(unsigned long *)&old->sa_mask = ko.mask;
    }
    return (int)r;
}

/* ---- memory and strings --------------------------------------------------
 * rep movsb/stosb rather than loops: GCC recognises a copying loop and
 * turns it into a call to memcpy - which, here, is this function. */
void *memcpy(void *restrict d, const void *restrict s, size_t n)
{
    void *r = d;
    __asm__ volatile ("rep movsb" : "+D"(d), "+S"(s), "+c"(n) : : "memory");
    return r;
}
void *memmove(void *d, const void *s, size_t n)
{
    if ((uintptr_t)d - (uintptr_t)s >= n) return memcpy(d, s, n);   /* no overlap from the end */
    unsigned char *e = (unsigned char *)d + n - 1; const unsigned char *f = (const unsigned char *)s + n - 1;
    __asm__ volatile ("std\n\trep movsb\n\tcld" : "+D"(e), "+S"(f), "+c"(n) : : "memory");
    return d;
}
void *memset(void *d, int c, size_t n)
{
    void *r = d;
    __asm__ volatile ("rep stosb" : "+D"(d), "+c"(n) : "a"(c) : "memory");
    return r;
}
__attribute__((optimize("no-tree-loop-distribute-patterns")))
int memcmp(const void *a, const void *b, size_t n)
{
    const unsigned char *p = a, *q = b;
    for (; n; n--, p++, q++) if (*p != *q) return *p - *q;
    return 0;
}
__attribute__((optimize("no-tree-loop-distribute-patterns")))
size_t strlen(const char *s) { const char *p = s; while (*p) p++; return (size_t)(p - s); }
static int same(const char *a, const char *b, size_t n) { return memcmp(a, b, n) == 0; }

/* ---- malloc ----------------------------------------------------------------
 * Blocks of a power of two, 32 bytes to 32 KB, each with a 16-byte header,
 * cut from 256 KB regions and kept on a free list per size once freed.
 * Larger requests are their own mapping, returned to the kernel on free:
 * the SPN tables are these, and one of them is freed and remade per boot.
 * Pages count as resident only once touched, so the regions cost nothing
 * until used. Single-threaded, as the engines are. */
#define HDR 16
#define BIG 32768
#define REGION (256 * 1024)
struct hdr { size_t size; size_t cls; };           /* usable bytes; class, or 0 = own mapping */
static void *freel[16];
static char *bump, *bump_end;
static int cls_of(size_t total) { int c = 5; while (((size_t)1 << c) < total) c++; return c; }
void *malloc(size_t n)
{
    if (n > ((size_t)1 << 60)) { rt_errno = ENOMEM; return NULL; }
    size_t total = n + HDR;
    struct hdr *h;
    if (total > BIG) {
        size_t len = (total + 4095) & ~(size_t)4095;
        void *m = mmap(NULL, len, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (m == MAP_FAILED) { rt_errno = ENOMEM; return NULL; }
        h = m; h->size = len - HDR; h->cls = 0;
        return (char *)h + HDR;
    }
    int c = cls_of(total);
    if (freel[c]) {
        h = freel[c]; freel[c] = *(void **)((char *)h + HDR);
    } else {
        size_t sz = (size_t)1 << c;
        if (!bump || (size_t)(bump_end - bump) < sz) {
            void *m = mmap(NULL, REGION, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
            if (m == MAP_FAILED) { rt_errno = ENOMEM; return NULL; }
            bump = m; bump_end = bump + REGION;        /* the old region's tail is left unused */
        }
        h = (struct hdr *)bump; bump += sz;
    }
    h->size = ((size_t)1 << c) - HDR; h->cls = (size_t)c;
    return (char *)h + HDR;
}
void free(void *p)
{
    if (!p) return;
    struct hdr *h = (struct hdr *)((char *)p - HDR);
    if (h->cls == 0) { munmap(h, h->size + HDR); return; }
    *(void **)p = freel[h->cls]; freel[h->cls] = h;
}
void *realloc(void *p, size_t n)
{
    if (!p) return malloc(n);
    struct hdr *h = (struct hdr *)((char *)p - HDR);
    if (n <= h->size) return p;
    void *q = malloc(n);
    if (!q) return NULL;
    memcpy(q, p, h->size);
    free(p);
    return q;
}

/* ---- the environment -------------------------------------------------------
 * environ starts as the kernel's array on the stack; the first change copies
 * it to the heap so it can grow. execve passes environ on, so a child sees
 * every change. Replaced strings are never freed - they may be the kernel's -
 * which is what the C library does too. */
static char **own; static size_t own_n, own_cap;
static int name_ok(const char *n) { if (!n || !*n) return 0; for (; *n; n++) if (*n == '=') return 0; return 1; }
static int take_env(void)
{
    if (own) return 0;
    size_t n = 0;
    if (environ) while (environ[n]) n++;
    own_cap = n + 8;
    if (!(own = malloc(own_cap * sizeof *own))) return -1;
    for (size_t i = 0; i < n; i++) own[i] = environ[i];
    own[n] = NULL; own_n = n; environ = own;
    return 0;
}
char *getenv(const char *n)
{
    size_t l = strlen(n);
    if (environ) for (char **e = environ; *e; e++)
        if (same(*e, n, l) && (*e)[l] == '=') return *e + l + 1;
    return NULL;
}
int setenv(const char *n, const char *v, int overwrite)
{
    if (!name_ok(n)) { rt_errno = EINVAL; return -1; }
    if (take_env() < 0) return -1;
    size_t l = strlen(n), vl = strlen(v), i;
    for (i = 0; i < own_n; i++) if (same(own[i], n, l) && own[i][l] == '=') break;
    if (i < own_n && !overwrite) return 0;
    char *s = malloc(l + vl + 2);
    if (!s) return -1;
    memcpy(s, n, l); s[l] = '='; memcpy(s + l + 1, v, vl + 1);
    if (i < own_n) { own[i] = s; return 0; }
    if (own_n + 1 >= own_cap) {
        char **g = realloc(own, own_cap * 2 * sizeof *g);
        if (!g) return -1;
        own = g; own_cap *= 2; environ = own;
    }
    own[own_n++] = s; own[own_n] = NULL;
    return 0;
}
int unsetenv(const char *n)
{
    if (!name_ok(n)) { rt_errno = EINVAL; return -1; }
    if (take_env() < 0) return -1;
    size_t l = strlen(n), j = 0;
    for (size_t i = 0; i < own_n; i++)
        if (!(same(own[i], n, l) && own[i][l] == '=')) own[j++] = own[i];
    own_n = j; own[j] = NULL;
    return 0;
}

/* ---- the one user-database lookup: /etc/passwd only (see WHAT IS GIVEN UP) - */
struct passwd *getpwnam(const char *name)
{
    static struct passwd pw;
    static char dir[1024], buf[65536];
    int fd = open("/etc/passwd", O_RDONLY);
    if (fd < 0) return NULL;
    ssize_t n = 0, r;
    while (n < (ssize_t)sizeof buf - 1 && (r = read(fd, buf + n, sizeof buf - 1 - n)) > 0) n += r;
    close(fd);
    buf[n] = 0;
    size_t l = strlen(name);
    for (char *p = buf; *p; ) {
        char *e = p;
        while (*e && *e != '\n') e++;
        if ((size_t)(e - p) > l && same(p, name, l) && p[l] == ':') {
            char *f = p; int k = 0;                 /* name:pw:uid:gid:gecos:DIR:shell */
            while (f < e && k < 5) { if (*f == ':') k++; f++; }
            if (k == 5) {
                char *d = f;
                while (d < e && *d != ':') d++;
                if ((size_t)(d - f) >= sizeof dir) return NULL;
                memcpy(dir, f, (size_t)(d - f)); dir[d - f] = 0;
                memset(&pw, 0, sizeof pw); pw.pw_dir = dir;
                return &pw;
            }
        }
        p = *e ? e + 1 : e;
    }
    return NULL;
}

/* ---- snprintf: what SPN's diagnostics use, and a little more -------------- */
static void put(char **o, char *end, char c) { if (*o < end) **o = c; (*o)++; }
int vsnprintf(char *restrict buf, size_t size, const char *restrict f, va_list ap)
{
    char *o = buf, *end = size ? buf + size - 1 : buf;
    for (; *f; f++) {
        if (*f != '%') { put(&o, end, *f); continue; }
        int alt = 0, zero = 0, left = 0, width = 0, lng = 0;
        for (f++; ; f++) {
            if (*f == '#') alt = 1; else if (*f == '0') zero = 1; else if (*f == '-') left = 1;
            else break;
        }
        while (*f >= '0' && *f <= '9') width = width * 10 + (*f++ - '0');
        while (*f == 'l' || *f == 'z' || *f == 'j' || *f == 't' || *f == 'h') { if (*f != 'h') lng = 1; f++; }
        char tmp[32], *s = tmp; int len = 0, neg = 0;
        unsigned long long u = 0; unsigned base = 10; int upper = 0;
        switch (*f) {
        case '%': put(&o, end, '%'); continue;
        case 'c': tmp[0] = (char)va_arg(ap, int); len = 1; break;
        case 's': s = va_arg(ap, char *); if (!s) s = "(null)"; len = (int)strlen(s); break;
        case 'd': case 'i': {
            long long v = lng ? va_arg(ap, long long) : va_arg(ap, int);
            neg = v < 0; u = neg ? 0ULL - (unsigned long long)v : (unsigned long long)v; goto num; }
        case 'p': u = (uintptr_t)va_arg(ap, void *); base = 16; alt = 1; goto num;
        case 'X': upper = 1; /* fall through */
        case 'x': base = 16; /* fall through */
        case 'o': if (*f == 'o') base = 8; /* fall through */
        case 'u': u = lng ? va_arg(ap, unsigned long long) : va_arg(ap, unsigned int);
        num: {
            char d[24]; int k = 0;
            do { unsigned x = (unsigned)(u % base); d[k++] = (char)(x < 10 ? '0' + x : (upper ? 'A' : 'a') + x - 10); u /= base; } while (u);
            if (neg) tmp[len++] = '-';
            if (alt && base == 16) { tmp[len++] = '0'; tmp[len++] = upper ? 'X' : 'x'; }
            if (alt && base == 8) tmp[len++] = '0';
            while (zero && !left && len + k < width) tmp[len++] = '0';
            while (k) tmp[len++] = d[--k];
            break; }
        default: put(&o, end, '%'); if (*f) put(&o, end, *f); else f--; continue;
        }
        if (!left) for (int i = len; i < width; i++) put(&o, end, ' ');
        for (int i = 0; i < len; i++) put(&o, end, s[i]);
        if (left) for (int i = len; i < width; i++) put(&o, end, ' ');
    }
    if (size) *(o < end ? o : end) = 0;
    return (int)(o - buf);
}
int snprintf(char *restrict buf, size_t size, const char *restrict f, ...)
{
    va_list ap; va_start(ap, f); int n = vsnprintf(buf, size, f, ap); va_end(ap);
    return n;
}

/* ---- the entry point: the kernel's stack is argc, argv..., 0, envp..., 0 ---- */
int main(int, char **);
__attribute__((used, noreturn)) void rt_main(long argc, char **argv, char **envp)
{
    environ = envp;
    exit(main((int)argc, argv));
}
__asm__(".text\n.globl _start\n.type _start,@function\n_start:\n"
        "\txor %ebp, %ebp\n"
        "\tmov (%rsp), %rdi\n"            /* argc */
        "\tlea 8(%rsp), %rsi\n"           /* argv */
        "\tlea 8(%rsi,%rdi,8), %rdx\n"    /* envp: past argv's null */
        "\tand $-16, %rsp\n"
        "\tcall rt_main\n"
        "\thlt\n");
