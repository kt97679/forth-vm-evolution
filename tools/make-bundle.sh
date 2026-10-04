#!/bin/sh
# tools/make-bundle.sh [DIR] - the handoff bundle, named and checked
# (prompts/07-git-handoff; as relf's tools/make-bundle.sh). From the
# repository's top, after the iteration's commit:
#     sh tools/make-bundle.sh /mnt/user-data/outputs
# prints the bundle's path. DIR defaults to the current directory.
#
# The name is GOALS.md's convention:
#     forth-vm-evolution-claude-iterN-YYYYMMDD-HHMMSS.bundle      (UTC)
# N is the iteration of HEAD's commit, from its subject ("Iteration N:
# ..."); a handoff of several commits is named by the last. Iteration 1
# put this right: the handoffs before it were all called
# forth-vm-evolution.bundle, because 07's `out.bundle` placeholder was
# taken for a name and no convention was written down.
#
# The refs: HEAD, so a plain `git pull FILE` works, and master.
# The check: the bundle is cloned and the clone's HEAD must be ours -
# a deliverable nobody tests is one nobody has tried.
set -e
subject=$(git log -1 --format=%s)
n=$(printf '%s\n' "$subject" | sed -n 's/^Iteration \([0-9][0-9]*\):.*/\1/p')
if [ -z "$n" ]; then
    echo "make-bundle: HEAD's subject does not start with 'Iteration N:': $subject" >&2
    exit 1
fi
dir=${1:-.}
file="$dir/forth-vm-evolution-claude-iter$n-$(date -u +%Y%m%d-%H%M%S).bundle"
git bundle create "$file" HEAD master 2>/dev/null
check=$(mktemp -d)
trap 'rm -rf "$check"' EXIT
git clone -q "$file" "$check/clone"
if [ "$(git rev-parse HEAD)" != "$(git -C "$check/clone" rev-parse HEAD)" ]; then
    echo "make-bundle: the clone's HEAD is not this HEAD - not pullable" >&2
    rm -f "$file"
    exit 1
fi
git bundle list-heads "$file" | sed 's/^/  /' >&2
echo "$file"
