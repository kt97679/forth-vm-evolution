# Fern - a small scripting language compiled into Forth words (a design note, Iteration 457)

> **Obsolete (Iteration 510, the owner).** Fern is a project of its own now, and it has these notes - this one and
> c4-family-459.md's section 5 - in full. Nothing here is pursued or kept current; kept for the history only.

The owner asked for a minimal, user-friendly scripting language - in the spirit of Ruby or Python - implemented on top of
this Forth, compiled into Forth words, at little cost against bare Forth; and chose to build it in a chat of its own.
This note is that chat's starting point. "Fern" is a working name.

## The language

Lua's weight with Ruby's look: keyword-closed blocks (easier to parse in Forth than significant indentation), infix
expressions with the usual precedence, calls `f(x, y)`, locals made by assignment, the last expression a function's
value.

```ruby
def fib(n)
  if n < 2 then return n end
  fib(n - 1) + fib(n - 2)
end

def sum_to(n)
  total = 0
  for i in 1..n
    total = total + i
  end
  total
end

squares = [1, 4, 9, 16]
print "sum is #{sum_to(10)}, third square #{squares[2]}"
```

Values: the cell (integers; booleans as Forth's 0 and -1), strings and arrays as addresses, hash tables in a library.
Every Fern function is a Forth word, and any Forth word is callable as a function.

## How it compiles

A compiler written in Forth - a tokenizer and a recursive-descent parser that emits code with COMPILE, and LITERAL as it
reads, as Forth compiles itself. No interpreter loop, no type checks at run time. Each `def` a colon definition:

```forth
: fib   1 FRAME  L0 2 < IF L0 UNFRAME EXIT THEN
        L0 1- fib  L0 2 - fib +  UNFRAME ;
```

String interpolation is split at compile time into TYPE and the number words.

**Locals** - the one real design question. A frame on the return stack: FRAME (the arguments moved off the data stack),
`L@ k` / `L! k` (slot k), UNFRAME (released; foldable into EXIT). First in plain Forth (RP@ and arithmetic, a few
dispatches an access), then as VM primitives - one dispatch an access, as cheap as a stack move - and in time genes the
evolver tunes, as it tunes the slot-specialised variable opcodes, the fusions and the JIT.

## The cost against hand-written Forth

| | |
|---|---|
| expressions, control flow | nothing - the same words |
| a call | about two dispatches (the frame in and out) |
| a local's access | one dispatch - against the stack shuffling it replaces |
| array bounds checks | optional, a compile-time switch |

Expected within 0-20% of good hand-written Forth, sometimes ahead: results/wip-regmachine/ found a fifth to a third of
hand-written Forth's dispatches only moving values on the stack, which named locals avoid.

## Left out, to stay light

Dynamic typing (a tag check on every `+` - the largest cost; the compiler picks an operation from what it knows, or the
program names it), garbage collection (strings and arrays from a per-script arena freed at its end - right for
shell-style scripts), floating point (the Forth is integer-only).

## The plan

1. **The core**: integers, functions, locals in plain Forth, if/while/for, print and string literals; measured against
   hand-written Forth on this project's own benchmarks (fib, loop, bubble).
2. Arrays, string operations, interpolation, calling Forth.
3. The locals as VM primitives - genes - and the JIT's support for them.
4. Hash tables, errors (CATCH and THROW as begin/rescue), modules.

About 1,000-1,500 lines of Forth (tokenizer ~150, parser and code generation ~500, library ~300), 10-20 KB of image.
Where it may serve: RelF's shell (RELF.md) - already a language on this Forth - could take it as its scripting language.

## What the Forth gives it

Standard core and core-ext words (the corpus passes them), ALLOCATE and RESIZE, file words through system calls
(fsys), image saving, CATCH and THROW; integer-only; Linux user space on x86-64, 32-bit x86 and 32-bit ARM; little-endian
only (GOALS.md). The hand-made s6 (build/) is the natural first host: its words are the standard ones.
