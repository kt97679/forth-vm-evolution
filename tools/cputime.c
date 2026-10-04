/*
 *  cputime.c - run a command and report how much CPU it used.
 *
 *      cputime PROG ARG...      -> "CPUNS <nanoseconds>" on stderr,
 *                                  then "MAXRSS <kilobytes>": peak resident
 *                                  memory, from the same rusage record,
 *                                  then, where the hardware counters can
 *                                  be read, "CYCLES <n>" and "INSTR <n>"
 *
 *  CYCLES AND INSTRUCTIONS. CPU time excludes the time spent waiting
 *  while other processes run, but not how fast the CPU runs while this
 *  one is on it: boost, thermal throttling and a powersave governor all
 *  change CPU seconds for the same work - and a governor that ramps up
 *  slowly would penalise short runs most. Cycles do not depend on the
 *  clock; instructions are deterministic. Both are counted for the child
 *  only, in USER SPACE - the kernel's part of a run, starting the process
 *  and page faults, is in CPU time but not here; tools/clockfit.py tells
 *  the two effects apart - from the moment it execs (enable_on_exec, attached
 *  while the child waits on a pipe), and scaled if the kernel had to
 *  multiplex the counters. Where they cannot be opened - a VM without
 *  the PMU, or kernel.perf_event_paranoid above 2, Ubuntu's default being
 *  4 - the lines are simply absent and callers use CPU time.
 *
 *  WHY. Wall-clock timing on a shared machine measures the machine as
 *  much as the program: another process gets scheduled, this one waits,
 *  and the wait lands in the number. Taking the minimum of several
 *  rounds hides most of that, but not on a busy box, and it is why the
 *  laptop in this project could not resolve anything under 13%.
 *
 *  CPU time counts only the cycles this process was actually running.
 *  It is not a complete answer: a noisy neighbour that evicts our cache
 *  lines still makes us take MORE cycles, so contention for memory
 *  bandwidth and last-level cache is still in the figure. What goes
 *  away is time spent descheduled, which on a loaded machine is the
 *  larger term. It does nothing at all about per-BUILD layout bias -
 *  that needs several builds, which is what LAYOUTS is for.
 *
 *  getrusage(RUSAGE_CHILDREN) rather than the shell's `time`: the
 *  fields are microseconds and on Linux come from per-task accounting
 *  rather than the old 100 Hz tick, so a 12 ms workload is resolvable.
 *  User and system time are added because a Forth cross-compile does
 *  real work in both.
 *
 *  The timing goes to stderr so it cannot be confused with whatever the
 *  program under test writes to stdout.
 */
#include <sys/resource.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/resource.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <unistd.h>
#include <linux/perf_event.h>

static int perf_open(pid_t pid, unsigned type, unsigned long long config)
{
    struct perf_event_attr a;
    memset(&a, 0, sizeof a);
    a.size = sizeof a;
    a.type = type;
    a.config = config;
    a.disabled = 1;
    a.enable_on_exec = 1;               /* from the child's exec on */
    a.exclude_kernel = 1;               /* user space: allowed at paranoid 2 */
    a.exclude_hv = 1;
    a.read_format = PERF_FORMAT_TOTAL_TIME_ENABLED | PERF_FORMAT_TOTAL_TIME_RUNNING;
    return (int)syscall(SYS_perf_event_open, &a, pid, -1, -1, PERF_FLAG_FD_CLOEXEC);
}

static long long perf_value(int fd)     /* -1 if there is no usable count */
{
    unsigned long long v[3];            /* value, time enabled, time running */
    if (fd < 0 || read(fd, v, sizeof v) != (ssize_t)sizeof v || v[2] == 0) return -1;
    if (v[2] < v[1]) return (long long)((double)v[0] * (double)v[1] / (double)v[2]);
    return (long long)v[0];
}

/* CPUTIME_JAIL (set by lab/evolve): the command is an engine the evolver
 * runs - possibly a broken design executing arbitrary code, and FORK is
 * one of its primitives. Iteration 10: a run forked without bound and
 * froze the owner's laptop. No workload forks, so the engine gets no new
 * processes at all (RLIMIT_NPROC - not binding for root, which the
 * evolver refuses), and bounded memory, file sizes and open files, and no
 * core dumps. Set in the child, after the one fork cputime needs. */
static void jail(void) {
    struct rlimit none = {0, 0}, as = {1UL << 30, 1UL << 30}, fsz = {64UL << 20, 64UL << 20}, nof = {64, 64};
    setrlimit(RLIMIT_NPROC, &none); setrlimit(RLIMIT_CORE, &none);
    setrlimit(RLIMIT_AS, &as); setrlimit(RLIMIT_FSIZE, &fsz); setrlimit(RLIMIT_NOFILE, &nof);
}

int main(int argc, char **argv)
{
    pid_t pid;
    int status = 0, go[2], fc, fi;
    struct rusage ru;
    unsigned long long ns;
    long long cyc, ins;
    char c = 'g';

    if (argc < 2) {
        fprintf(stderr, "usage: cputime PROG [ARG...]\n");
        return 2;
    }
    if (pipe(go) < 0) { perror("pipe"); return 2; }
    pid = fork();
    if (pid < 0) { perror("fork"); return 2; }
    if (pid == 0) {
        /* Wait until the parent has attached the counters, then exec. */
        close(go[1]);
        if (read(go[0], &c, 1) != 1) _exit(126);
        close(go[0]);
        if (getenv("CPUTIME_JAIL")) jail();
        execvp(argv[1], argv + 1);
        _exit(127);                       /* exec failed */
    }
    close(go[0]);
    fc = perf_open(pid, PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES);
    fi = perf_open(pid, PERF_TYPE_HARDWARE, PERF_COUNT_HW_INSTRUCTIONS);
    if (write(go[1], &c, 1) != 1) { perror("write"); return 2; }
    close(go[1]);
    if (waitpid(pid, &status, 0) < 0) { perror("waitpid"); return 2; }
    if (getrusage(RUSAGE_CHILDREN, &ru) < 0) { perror("getrusage"); return 2; }

    ns = (unsigned long long)ru.ru_utime.tv_sec * 1000000000ULL
       + (unsigned long long)ru.ru_utime.tv_usec * 1000ULL
       + (unsigned long long)ru.ru_stime.tv_sec * 1000000000ULL
       + (unsigned long long)ru.ru_stime.tv_usec * 1000ULL;
    fprintf(stderr, "CPUNS %llu\n", ns);
    fprintf(stderr, "MAXRSS %ld\n", (long)ru.ru_maxrss);
    cyc = perf_value(fc);
    ins = perf_value(fi);
    if (cyc > 0) fprintf(stderr, "CYCLES %lld\n", cyc);
    if (ins > 0) fprintf(stderr, "INSTR %lld\n", ins);

    if (WIFEXITED(status)) return WEXITSTATUS(status);
    return 128 + (WIFSIGNALED(status) ? WTERMSIG(status) : 0);
}
