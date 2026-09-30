# engine-rt.sh - sourced by the build scripts: how the engines are linked.
# Needs ROOT. Sets RT_FLAGS, appended to every 64-bit engine's cc command.
#
# ENGINE_RT=libc (the default): with the C library, as always.
# ENGINE_RT=nolibc: 64-bit engines without it, on engine/rt-linux-x86_64.c.
#   They start in a fraction of the time and keep about a tenth of the
#   memory resident; that file says why and what it measured. x86-64
#   Linux only - elsewhere, and for 32-bit engines, the C library as
#   before. One behaviour differs: ~name comes from /etc/passwd alone,
#   not through NSS (LDAP, SSSD, systemd-homed).
RT_FLAGS=""
case "${ENGINE_RT:-libc}" in
    libc) ;;
    nolibc)
        if [ "$(uname -s)-$(uname -m)" = Linux-x86_64 ]; then
            RT_FLAGS="-static -no-pie -nostdlib -fno-stack-protector"
            RT_FLAGS="$RT_FLAGS -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0"
            RT_FLAGS="$RT_FLAGS $ROOT/engine/rt-linux-x86_64.c -lgcc"
        else
            echo "note: ENGINE_RT=nolibc is for x86-64 Linux; linking with the C library" >&2
        fi ;;
    *)  echo "ENGINE_RT must be libc or nolibc, not '$ENGINE_RT'" >&2; exit 1 ;;
esac
