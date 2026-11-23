#!/bin/sh
# results/drafts/guard-challengers-740.sh [OUT] - the guard challengers' path through a follow-up chain, rehearsed here
# (Iteration 740): results/candidates-guard-740.md's three beside their holders (results/relf-designs-718.md's
# fastest-x86-64, fastest-x86-32, small-jit) as a chain's list; the chain's two steps as the laptop runs them -
# measure-ids.py (both widths; 1 round here), dream's two lines (xcheck.py's sample with --also @LIST and its bundle, then the
# host's --prebuilt measure; this machine standing in) and loadtest.py --ids (3 sessions, 2 rounds, 1 load here) - laid out
# by session as chain-sessions.py lays a chain's (OUT/sK/loadtest.md, OUT/sK/dream.lan-prebuilt64.out.json and -32); then
# followup-roles.py's rule on them, the three x86 roles
# with their holders. This sandbox's numbers, so the verdicts are not the laptop's - what is checked is the path: every
# design built and alive at both widths, dream's sample finding all six genomes (the challengers' in results/candidates-
# guard-740.md, the holders' in results/relf-designs-718.md - xcheck.py's lookup, fixed at 740), each session measuring all six, the rule naming each challenger against its holder. PASS or FAIL. As the build user, from the repository's top; ~45 minutes.
set -u
O=${1:-/tmp/guard-challengers-740}; rm -rf "$O"; mkdir -p "$O"
L=$O/list.md
{ echo '# the rehearsal list: three holders, three challengers'; echo
  grep -h '^{"' results/relf-designs-718.md | python3 -c '
import json, sys
for l in sys.stdin:
    r = json.loads(l)
    if r["id"] in ("9b15ba26f7", "11f956db93", "15eda54ebd"): print(l.strip())'
  grep '^{"' results/candidates-guard-740.md; } > "$L"
python3 -B lab/evolve/measure-ids.py --ids "$L" --rounds 1 > "$O/measure-ids.md" 2> "$O/measure-ids.err" || { echo "guard-challengers: FAIL - measure-ids"; exit 1; }
# the candidates as the processing makes them: the list's records with the chain's own measurements
python3 - "$L" "$O/measure-ids.md" "$O/candidates.md" <<'PY'
import json, sys
L, M, C = sys.argv[1:]
m = {json.loads(l)['id']: json.loads(l) for l in open(M) if l.startswith('{"')}
with open(C, 'w') as f:
    f.write('# the rehearsal candidates: the list\'s six, measure-ids.py\'s records\n\n')
    for l in open(L):
        if not l.startswith('{"'): continue
        r = json.loads(l); x = dict(m.get(r['id'], r)); x['why'] = r['why']; x.setdefault('jit', 1); f.write(json.dumps(x, sort_keys=True) + '\n')
PY
# dream's two lines as remote-checks.sh runs them (prebuilt64, prebuilt32): the laptop's sample with the list's ids asked
# for (--also @LIST - their genomes from the results files and results/candidates-*.md) and its binaries bundled; the host
# measures those binaries (--prebuilt) - here, as the stand-in, three sessions each, 1 round
RES=results/evolve-amd-ryzen-7-pro-8840hs-seed96.md
for w in 64 32; do
    mkdir -p "$O/x$w/pre"; c=; [ $w = 32 ] && c='--cell 4'
    python3 -B lab/evolve/xcheck.py --sample $RES "$O/x$w/designs.json" --n 0 --also "@$L" $c --bundle "$O/x$w/bins.tar.gz" > "$O/x$w/sample.log" 2>&1 ||
        { echo "guard-challengers: FAIL - xcheck's sample at $w ($(tail -n 1 "$O/x$w/sample.log"))"; exit 1; }
    tar xzf "$O/x$w/bins.tar.gz" -C "$O/x$w/pre" || { echo "guard-challengers: FAIL - the $w bundle"; exit 1; }
    for k in 1 2 3; do
        mkdir -p "$O/sessions/s$k"
        python3 -B lab/evolve/xcheck.py "$O/x$w/designs.json" "$O/sessions/s$k/dream.lan-prebuilt$w.out.json" --prebuilt "$O/x$w/pre" --rounds 1 \
            > "$O/x$w/host-s$k.log" 2>&1 || { echo "guard-challengers: FAIL - xcheck on the host, $w, session $k"; exit 1; }
    done
done
for k in 1 2 3; do
    mkdir -p "$O/sessions/s$k"
    python3 -B lab/evolve/loadtest.py --ids "$L" --rounds 2 --load 1 > "$O/sessions/s$k/loadtest.md" 2> "$O/sessions/s$k/loadtest.err" ||
        { echo "guard-challengers: FAIL - loadtest session $k"; exit 1; }
done
python3 -B lab/evolve/followup-roles.py "$O/candidates.md" "$O/sessions" --handoff results/handoff-relf-726.md \
    --roles fast64=9b15ba26f7,fast32=11f956db93,smalljit=15eda54ebd > "$O/roles.md" 2> "$O/roles.err"
rc=$?; f=
[ $rc = 0 ] || f="$f followup-roles (exit $rc: $(tail -n 1 "$O/roles.err" | cut -c1-100))"
n=$(grep -c '^{"' "$O/measure-ids.md"); [ "$n" = 6 ] || f="$f measure-ids-$n-of-6"
grep -q '"status": "ok"' "$O/measure-ids.md" || f="$f measure-ids-status"
for k in 1 2 3; do for i in 9b15ba26f7 11f956db93 15eda54ebd fba7d5be3d b7a09aec76 7a6c182638; do
    grep -q "\"id\": \"$i\"" "$O/sessions/s$k/loadtest.md" || f="$f s$k-$i"; done; done
for i in fba7d5be3d b7a09aec76 7a6c182638; do grep -q "$i" "$O/roles.md" || f="$f rule-$i"; done
for w in 64 32; do grep -q '6 of 6 asked for by id' "$O/x$w/sample.log" || f="$f xcheck-asked-$w"; done   # the holders too (740's xcheck fix)
echo "guard-challengers: ${f:+FAIL -$f}${f:-PASS}"
