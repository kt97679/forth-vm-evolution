/*
 *  cputime.c - run a command and report how much CPU it used.
 *
 *      cputime PROG ARG...      -> "CPUNS <nanoseconds>" on stderr
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
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    pid_t pid;
    int status = 0;
    struct rusage ru;
    unsigned long long ns;

    if (argc < 2) {
        fprintf(stderr, "usage: cputime PROG [ARG...]\n");
        return 2;
    }
    pid = fork();
    if (pid < 0) { perror("fork"); return 2; }
    if (pid == 0) {
        execvp(argv[1], argv + 1);
        _exit(127);                       /* exec failed */
    }
    if (waitpid(pid, &status, 0) < 0) { perror("waitpid"); return 2; }
    if (getrusage(RUSAGE_CHILDREN, &ru) < 0) { perror("getrusage"); return 2; }

    ns = (unsigned long long)ru.ru_utime.tv_sec * 1000000000ULL
       + (unsigned long long)ru.ru_utime.tv_usec * 1000ULL
       + (unsigned long long)ru.ru_stime.tv_sec * 1000000000ULL
       + (unsigned long long)ru.ru_stime.tv_usec * 1000ULL;
    fprintf(stderr, "CPUNS %llu\n", ns);

    if (WIFEXITED(status)) return WEXITSTATUS(status);
    return 128 + (WIFSIGNALED(status) ? WTERMSIG(status) : 0);
}
