#!/bin/sh
# tools/update-relf.sh [REV] - refresh vendor/relf from github.com/kt97679/relf.
#
# relf is where the shell and CV8-as-a-product live; this lab carries it as
# a REFERENCE SYSTEM, like vendor/sod32: its engine and kernel images, built
# here exactly as relf builds them, measured beside the stages. REV is a
# branch, tag or commit (default origin/article-2026, where relf is being
# stabilised); the commit it resolves to is recorded in vendor/relf/UPSTREAM,
# so every measurement says which relf it was.
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
REV=${1:-origin/article-2026}
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
git clone -q https://github.com/kt97679/relf "$T/relf"
git -C "$T/relf" checkout -q "$REV"
D="$ROOT/vendor/relf"; mkdir -p "$D"
for f in engine/cv8.c engine/cv8-ops.h engine/opcodes.tab forth/kernel64.img forth/kernel32.img; do
    cp "$T/relf/$f" "$D/$(basename "$f")"
done
# relf's licence is GPL version 2 only; its README's Licence section, verbatim.
awk '/^## Licen[cs]e/{f=1} f&&/^## /&&!/^## Licen[cs]e/{exit} f' "$T/relf/README.md" > "$D/LICENCE.md"
[ -s "$D/LICENCE.md" ] || { echo "no Licence section in relf's README"; exit 1; }
{ echo "url     https://github.com/kt97679/relf"
  echo "rev     $REV"
  git -C "$T/relf" log -1 --format='commit  %H%ndate    %ad%nsubject %s' --date=short
} > "$D/UPSTREAM"
echo "vendor/relf now at $(git -C "$T/relf" log -1 --format=%h): $(git -C "$T/relf" log -1 --format=%s | cut -c1-60)"
