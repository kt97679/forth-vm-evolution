# forth-vm-evolution: the search's winning Forth designs, built from source - designs/README.md.
# `make` builds every one (x86-64 Linux); `make NAME` one; `make libc` the portable ones with the C library, for any
# other host; `make 32` the 4-byte-cell engines (gcc-multilib); `make test` builds and runs each; `make selfhost` each
# image rebuilt from its source (designs/forth/, its genes) by its own engine, byte for byte, at both widths - all
# but those designs/TRANSLATOR-BUILT names, if any: their images are the converter's.

DESIGNS = fastest-x86-64 fastest-x86-32 best-all-round small-jit portable-fastest portable-arm portable-knee portable-small least-memory smallest
PORTABLE = portable-fastest portable-arm portable-knee portable-small least-memory smallest

all: $(DESIGNS)

$(DESIGNS):
	$(MAKE) -C designs/$@

libc:
	for d in $(PORTABLE); do $(MAKE) -C designs/$$d forth-libc || exit 1; done

arm:
	for d in $(PORTABLE); do $(MAKE) -C designs/$$d forth-arm || exit 1; done

32:
	for d in $(DESIGNS); do $(MAKE) -C designs/$$d forth32 || exit 1; done

test: all
	sh designs/test.sh $(DESIGNS)

selfhost:
	for d in $(DESIGNS); do if grep -q "^$$d " designs/TRANSLATOR-BUILT 2> /dev/null; then \
		echo "$$d: translator-built (designs/TRANSLATOR-BUILT) - not rebuilt"; continue; fi; \
		$(MAKE) -s -C designs/$$d selfhost selfhost32 || exit 1; done

clean:
	for d in $(DESIGNS); do $(MAKE) -C designs/$$d clean; done

.PHONY: all libc arm 32 test selfhost clean $(DESIGNS)
