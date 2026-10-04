/* lab/evolve/forklog.c - which designs try to fork (diagnosis, Iteration 10).
 *
 *   cc -shared -fPIC -O2 -o forklog.so lab/evolve/forklog.c
 *   LD_PRELOAD=$PWD/forklog.so FORKLOG=/tmp/forks.txt ENGINE IMAGE < workload
 *
 * Every fork() the engine calls (its FORK primitive is libc fork) is
 * logged as one line and REFUSED, so a fork bomb stays one process even
 * outside the jail. It found the third run's: 8cfd49f24c, 8,181 attempts. */
#define _GNU_SOURCE
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
pid_t fork(void) {
    const char *f = getenv("FORKLOG");
    if (f) { int fd = open(f, O_WRONLY | O_CREAT | O_APPEND, 0666); if (fd >= 0) { if (write(fd, "F\n", 2) < 0) {} close(fd); } }
    errno = EAGAIN; return -1;
}
