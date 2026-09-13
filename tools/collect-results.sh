#!/bin/bash
# collect-results.sh run [BENCH WIDTH] | report
#
# Gathers every measurement into build/results/ and assembles RESULTS.md
# from what is there. Two commands rather than one because a full sweep
# takes several minutes and is worth being able to resume.
#
#   collect-results.sh run                  everything, both widths
#   collect-results.sh run kernel 64        one benchmark, one width
#   collect-results.sh report               assemble RESULTS.md
#
# RESULTS.md is GENERATED. Every number in it comes from a file in
# build/results/ written by a harness that gated on correctness first,
# so a figure cannot reach the report from a run that failed its checks.
set -u

# Every engine this script runs is a measured subject, so it runs in a
# predictable environment rather than in whatever the caller happens to
# have exported.
#
# LD_PRELOAD is the one that actually bites. A desktop session that
# preloads a library into everything will have it loaded into every
# engine here too, which is unwanted work inside the thing being timed;
# and when the engine is a 32-bit binary and the library is 64-bit,
# ld.so cannot load it and writes a line of complaint per process. That
# was reported from a real machine: six copies of "object
# 'libgtk3-nocsd.so.0' from LD_PRELOAD cannot be preloaded" during the
# dictionary dumps. Harmless there, because a dump captures stdout and
# ld.so writes to stderr - but not something to leave in a benchmark.
unset LD_PRELOAD

cd "$(dirname "$0")/.."
ROOT=$PWD
O=$ROOT/build
R=$O/results
mkdir -p "$R"

# loop is NOT in the default sweep. Its resolution floor is 17.5% here
# and it swung 20.9% between two runs of the same ARM board - it cannot
# support a claim, and anything printed in a table gets quoted. The
# benchmark and its harness stay in the repository as the worked example
# of a microbenchmark that does not reproduce; run it explicitly with
#     tools/collect-results.sh run loop 32
BENCHES="kernel corpus fib parse"
# layout-noise is not a stage comparison; it measures the floor below
# which stage comparisons are meaningless, and the report quotes it.
WIDTHS="64 32"

script_for() {
    case "$1" in
        kernel) echo bench/kernel-compile.sh;;
        corpus) echo bench/corpus-run.sh;;
        loop)   echo bench/loop-bench.sh;;
        fib)    echo bench/fib-bench.sh;;
        parse)  echo bench/parse-bench.sh;;
        *) echo "unknown benchmark: $1" >&2; exit 1;;
    esac
}

reps_for() {
    # Enough repetitions that the minimum settles, without spending
    # minutes on the slow workloads.
    case "$1" in
        kernel) echo 6;; corpus) echo 5;; loop) echo 4;; fib) echo 5;; parse) echo 4;;
    esac
}

case "${1:-}" in
    run|report|sweep) ;;
    *)
        cat <<'USAGE'
usage: collect-results.sh sweep [N]                    N full runs, saved
       collect-results.sh run [BENCH...] [WIDTH...]   take the measurements
       collect-results.sh report [--save PATH]        assemble RESULTS.md

Run the sweep first; it takes several minutes and writes build/results/.
`report` only assembles what is already there, so calling it on its own
produces a report with no timings in it.

  collect-results.sh run                 everything, both cell widths
  collect-results.sh run kernel 64       one benchmark, one width
  collect-results.sh sweep 2             measure twice and compare
  collect-results.sh report
  collect-results.sh report --save results/my-laptop.md

`sweep` is the one to use. It measures everything N times, saves each
run under a name taken from this machine, and then reports how far the
runs disagree - which is the check that has caught every bad number in
this project. One run of anything is not evidence.
USAGE
        exit 2;;
esac

if [ "$1" = sweep ]; then
    N=${2:-2}
    [ "$N" -ge 1 ] 2>/dev/null || { echo "sweep needs a count"; exit 2; }
    bash "$0" run >/dev/null 2>&1 || true      # populates host.txt
    # A readable machine name: drop the vendor noise a CPU model string
    # carries, keep the part a person would recognise.
    TAG=$(sed -n 's/^cpu: //p' "$R/host.txt" 2>/dev/null \
          | sed 's/([A-Za-z]*)//g; s/ CPU//; s/ Processor//; s/ w\/.*//;
                 s/ @.*//; s/^ *//; s/ *$//' \
          | tr 'A-Z ' 'a-z-' | tr -s '-' | tr -cd 'a-z0-9-' | cut -c1-24)
    TAG="${TAG}-$(uname -m)"
    [ -n "$TAG" ] || TAG=$(uname -m)
    echo
    echo "sweeping $N times as '$TAG' ..."
    i=1
    while [ "$i" -le "$N" ]; do
        echo
        echo "===== run $i of $N ====="
        bash "$0" run
        bash "$0" report --save "results/$TAG-run$i.md" >/dev/null
        echo "saved results/$TAG-run$i.md"
        i=$((i + 1))
    done
    if [ "$N" -ge 2 ]; then
        echo
        python3 "$ROOT/tools/agree.py" $(seq 1 "$N" | sed "s|^|results/$TAG-run|; s|$|.md|")
    fi
    exit 0
fi

if [ "$1" = run ]; then
    if ! ls "$O"/s0-cell-*-v1 >/dev/null 2>&1; then
        cat >&2 <<'WARN'
-------------------------------------------------------------------
 Only ONE build of each engine is present, so the tables will carry
 no error bars and the per-build layout bias - the largest source of
 variation here, worth up to 12% - will be invisible.

 Rebuild with several layouts first:

     LAYOUTS=5 tools/build-stages.sh

 then re-run this sweep.
-------------------------------------------------------------------
WARN
    fi
    bl=${2:-$BENCHES}
    wl=${3:-$WIDTHS}
    # Remove results for workloads no longer in the sweep. `report` used
    # to read whatever .txt files were lying about, so a loop-32.txt from
    # an older sweep - or from another machine - was printed as if it had
    # just been measured.
    for f in "$R"/*.txt; do
        [ -e "$f" ] || continue
        _n=$(basename "$f" .txt)
        case "$_n" in
            layout-noise-*) _b=${_n#layout-noise-} ;;
            *-32|*-64)      _b=${_n%-*} ;;
            *)              continue ;;
        esac
        case " $BENCHES " in
            *" $_b "*) ;;
            *) echo "  discarding stale $_n (workload not in the sweep)"
               rm -f "$f" ;;
        esac
    done
    for b in $bl; do
        for w in $wl; do
            rm -f "$R/$b-$w.txt"
            printf 'running %-7s at %s-bit cells ... ' "$b" "$w"
            WIDTH=$w bash "$(script_for "$b")" "$O" "$(reps_for "$b")" \
                > "$R/$b-$w.txt" 2>/dev/null
            # A table HEADER is printed even when every stage was
            # excluded, so matching it reported "ok" for a cell width
            # that does not exist on this host. Count data rows.
            if [ "$(grep -cE '^[a-z0-9-]+ +[0-9.]+ +[0-9.]+' \
                    "$R/$b-$w.txt")" -gt 0 ]; then echo ok
            elif ! ls "$O"/s0-cell-"$w" >/dev/null 2>&1; then
                echo "not built on this host"
            elif grep -q 'not built\|SKIP\|EXCLUDED' "$R/$b-$w.txt"; then
                echo "no stages at this width"
            else echo "NO TABLE - see $R/$b-$w.txt"; fi
        done
    done
    # What ran this. RESULTS.md used to state the machine in prose, which
    # was correct on exactly one machine and wrong everywhere else.
    {
        echo "date: $(date -u '+%Y-%m-%d %H:%MZ')"
        echo "uname: $(uname -srm)"
        echo "cpu: $(sed -n 's/^model name[ \t]*: //p' /proc/cpuinfo 2>/dev/null | head -1)"
        echo "cores: $(nproc 2>/dev/null)"
        echo "cc: $(cc --version 2>/dev/null | head -1)"
    } > "$R/host.txt"

    # layout-noise.sh is no longer run here. It existed to measure the
    # per-build bias as a single "floor" figure; every harness now
    # measures that bias per stage, as the error bar beside each ratio,
    # by timing all the layout variants. Keeping both would spend
    # minutes to produce a worse version of a number already in the
    # table. The script remains for anyone who wants it standalone.
    exit 0
fi

SAVE=
[ "${2:-}" = --save ] && SAVE=${3:?--save needs a path}

python3 - "$ROOT" "$SAVE" "$BENCHES" <<'PY'
import os, re, sys, csv

root = sys.argv[1]
save = sys.argv[2] if len(sys.argv) > 2 else ''
# The columns are whatever the sweep measures. Hardcoding them here let a
# dropped workload keep appearing from a stale file.
WORK = (sys.argv[3].split() if len(sys.argv) > 3 and sys.argv[3].strip()
        else ['kernel', 'corpus', 'fib', 'parse'])
R = os.path.join(root, 'build', 'results')
STAGES = ['sod32', 's0-cell', 'p4-pack4', 'p8-pack8', 's1-sod16',
          's2-cpt16', 's3-cpt16f', 's4-cv8', 's5-cv8spec', 's6-cv8b']
NICE = {
    'sod32':      'SOD32 (Benschop, 5-bit packed, 32-bit only)',
    's0-cell':    'RelF cell threading',
    'p4-pack4':   'tagged nibble  (rejected 157, built here)',
    'p8-pack8':   'tagged byte    (rejected 157, built here)',
    's1-sod16':   'SOD16  16-bit tokens + word table',
    's2-cpt16':   'CPT16  table deleted, computed target',
    's3-cpt16f':  'CPT16 + folded prim;EXIT',
    's4-cv8':     'CV8    byte stream',
    's5-cv8spec': 'CV8 + specialisations',
    's6-cv8b':    'CV8 + byte-granular dictionary headers',
}


def read(bench, width):
    """stage -> (ms, ratio, standard error or None)."""
    p = os.path.join(R, '%s-%s.txt' % (bench, width))
    if not os.path.exists(p):
        return {}
    out = {}
    for line in open(p):
        m = re.match(r'^(\S+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+|1 build)\s*$',
                     line)
        if m and m.group(1) in STAGES:
            se = None if m.group(4) == '1 build' else float(m.group(4))
            out[m.group(1)] = (float(m.group(2)), float(m.group(3)), se)
    return out


def table(width):
    data = {b: read(b, width) for b in WORK}
    base = data['kernel'].get('s0-cell') and 's0-cell'
    lines = []
    lines.append('| stage | ' + ' | '.join(WORK) + ' |')
    lines.append('|' + '---|' * (len(WORK) + 1))
    for s in STAGES:
        cells = []
        for b in WORK:
            d = data[b]
            if s not in d:
                cells.append('--')
            elif d[s][2] is None:
                cells.append('%.3f' % d[s][1])
            else:
                cells.append('%.3f ±%.3f' % (d[s][1], d[s][2]))
        if all(c == '--' for c in cells):
            continue
        lines.append('| `%s` | %s |' % (s, ' | '.join(cells)))
    return '\n'.join(lines)


def abstable(width):
    data = {b: read(b, width) for b in WORK}
    lines = ['| stage | ' + ' | '.join(w + ' ms' for w in WORK) + ' |',
             '|' + '---|' * (len(WORK) + 1)]
    for s in STAGES:
        cells = []
        for b in WORK:
            v = data[b].get(s)
            cells.append('--' if v is None else '%.2f' % v[0])
        if all(c == '--' for c in cells):
            continue
        lines.append('| `%s` | %s |' % (s, ' | '.join(cells)))
    return '\n'.join(lines)


sizes = {}
sp = os.path.join(root, 'build', 'sizes.csv')
if os.path.exists(sp):
    for row in list(csv.reader(open(sp)))[1:]:
        sizes[row[0]] = row[1:]

out = []
out.append('# Results\n')
out.append('Generated by `tools/collect-results.sh report` from the files in')
out.append('`build/results/`. Every harness gates on correctness before it')
out.append('times anything: the kernel-compile figures are only recorded for')
out.append('stages whose output image is byte-identical to the reference, and')
out.append('the rest only for runs that reach the end-of-corpus sentinel with')
out.append('zero failing cases.\n')
out.append('Each engine is built several times with flags that move code')
out.append('and change nothing it computes. Every build is timed; the')
out.append('figure is the MEAN across builds, each build being the minimum')
out.append('of several interleaved rounds, net of process startup. The ±')
out.append('is one standard error of the ratio.\n')
out.append('That structure is deliberate. The variation here is dominated')
out.append('by per-BUILD bias rather than run-to-run noise: repeated runs')
out.append('of the same binaries agree to 1-2%, but a rebuild moves a stage')
out.append('by five or ten, and on this project the cell-engine BASELINE -')
out.append('which divides every ratio below - had the widest spread of all')
out.append('at 12.6%. Averaging runs cannot remove a constant; averaging')
out.append('builds can, and the ± includes what is left.\n')
out.append('Ratios travel between machines; absolute milliseconds do not.\n')

hp = os.path.join(R, 'host.txt')
if os.path.exists(hp):
    out.append('Measured on:\n')
    out.append('```')
    out.append(open(hp).read().rstrip())
    out.append('```\n')
else:
    out.append('**The machine was not recorded** - these results predate')
    out.append('`build/results/host.txt`, or were assembled by hand.\n')
out.append('Every number here was taken AFTER the hashed word list was')
out.append('restored (see `FINDINGS-OUTER-INTERPRETER.md`). Figures from')
out.append('before that change are not comparable and are not reproduced.\n')

# The old "How small a difference is real" section is gone. It read a
# single floor per workload out of layout-noise-*.txt and printed it as
# the resolution of every table - which, once the harnesses began timing
# all the layout variants, was both redundant and WRONG: it kept showing
# figures from whatever stale run had last written those files, beside
# error bars that disagreed with them. The per-stage +/- is the same
# measurement, made per stage and in the same run as the number it
# qualifies.

out.append('## The stages\n')
for s in STAGES:
    out.append('- `%s` - %s' % (s, NICE[s]))
out.append('')

out.append('## Image size, bytes\n')
out.append('The unit is the FORTH IMAGE - the smallest image that boots into')
out.append('the interpreter and can rebuild the system - following SOD32\'s own')
out.append('Makefile, where `forth.img` is the finished artefact. Shell images')
out.append('are measured separately in `build/sizes-shell.csv`.\n')
out.append('*run-only* images carry an identical word set at every stage, so a')
out.append('difference between two rows is the encoding and nothing else.')
out.append('*self-hosting* images also carry that stage\'s own emitter overlay,')
out.append('which is what lets them compile their own encoding.\n')
out.append('`p4-pack4` and `p8-pack8` rewrite the cell image in place and leave')
out.append('the cells they skip where they were, so the FILE they produce is')
out.append('stage 0\'s size. The *packed* column below is what the image')
out.append('becomes once those cells are removed.\n')
out.append('That figure is arithmetic, not an estimate and not a model. These')
out.append('schemes are cell-granular: a pack replaces exactly N cells with one,')
out.append('nothing changes alignment, and every reference in a RelF image is')
out.append('relative. So compacting removes exactly (cells folded) x (cell size)')
out.append('bytes and can change nothing else. A relocating build would')
out.append('demonstrate the number; it would not alter it.\n')
packed = {}
for st in ('p4-pack4', 'p8-pack8'):
    for w in ('64', '32'):
        lg = os.path.join(root, 'build', '%s-k%s.log' % (st, w))
        if os.path.exists(lg):
            m = re.search(r'image (\d+) bytes; (\d+) bytes would be saved',
                          open(lg).read())
            if m:
                packed[(st, w)] = int(m.group(1)) - int(m.group(2))
if packed:
    out.append('| stage | packed 64 | packed 32 | vs stage 0, 64 | vs stage 0, 32 |')
    out.append('|---|---|---|---|---|')
    def ratio(v, base):
        try:
            return '%.3f' % (v / int(base))
        except (TypeError, ValueError):
            return '--'

    def num(v):
        return '--' if v is None else str(v)

    s0 = sizes.get('s0-cell', ['NA', 'NA', 'NA', 'NA'])
    for st in ('p4-pack4', 'p8-pack8'):
        a, b = packed.get((st, '64')), packed.get((st, '32'))
        out.append('| `%s` | %s | %s | %s | %s |'
                   % (st, num(a), num(b), ratio(a, s0[0]), ratio(b, s0[1])))
    out.append('')
out.append('| stage | run-only 64 | run-only 32 | self-hosting 64 | self-hosting 32 |')
out.append('|---|---|---|---|---|')
for s in STAGES:
    if s in sizes:
        out.append('| `%s` | %s |' % (s, ' | '.join(sizes[s])))
out.append('')

missing = []
for w in ('64', '32'):
    have = [b for b in WORK if read(b, w)]
    if not have:
        missing.append(w)
        continue
    out.append('## Speed, %s-bit cells, relative to the cell engine\n' % w)
    if len(have) < 4:
        out.append('Only %s measured at this width; run the rest with'
                   ' `tools/collect-results.sh run`.\n' % ', '.join(have))
    out.append(table(w))
    out.append('')
    out.append('Absolute, for scale only:\n')
    out.append(abstable(w))
    out.append('')

# "Not measured" and "cannot exist here" are different, and telling
# someone on a 32-bit host to run the sweep again is bad advice: no
# amount of running it will produce an 8-byte column on that machine.
absent = [w for w in missing
          if not os.path.exists(os.path.join(root, 'build', 's0-cell-%s' % w))]
unmeasured = [w for w in missing if w not in absent]
if absent:
    out.append('## Speed, %s-bit cells: not built on this host\n'
               % ' and '.join(absent))
    out.append('This machine has no engines at that cell width, so there is')
    out.append('nothing to time. On a 32-bit host the native build IS the')
    out.append('4-byte one and an 8-byte column does not exist; on a 64-bit')
    out.append('host the 4-byte column needs a 32-bit libc installed.\n')
if unmeasured:
    out.append('## Speed, %s-bit cells: not measured\n'
               % ' and '.join(unmeasured))
    out.append('The engines are built but `build/results/` has no harness')
    out.append('output for them, so the tables are omitted rather than')
    out.append('printed empty. Take the measurements with:\n')
    out.append('    tools/collect-results.sh run\n')

text = '\n'.join(out) + '\n'
open(os.path.join(root, 'RESULTS.md'), 'w').write(text)
if save:
    sp = save if os.path.isabs(save) else os.path.join(root, save)
    os.makedirs(os.path.dirname(sp), exist_ok=True)
    open(sp, 'w').write(text)
    print('also wrote', save)
if unmeasured:
    print('wrote RESULTS.md - WITHOUT timings for %s-bit cells.'
          % ' or '.join(unmeasured))
    print('Run `tools/collect-results.sh run` first; it takes a few minutes.')
elif absent:
    print('wrote RESULTS.md (%s-bit cells are not built on this host)'
          % ' and '.join(absent))
else:
    print('wrote RESULTS.md')
PY
