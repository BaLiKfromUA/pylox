# pylox

**pylox** is Python implementation of Lox programming language which is a demo language
from [Crafting Interpreters](http://www.craftinginterpreters.com/) book by [Bob Nystrom](https://github.com/munificent).

I'm doing this because:

1. I want to learn about programming languages design and implementation.
2. I don't want to just read the book or copy and paste the code from it and I want to do something else than C or Java.
3. I want to become more "fluent" with Python and its dev infrastructure.
4. Fun.

## Challenges

- [X] Add support to Lox’s scanner for C-style /* ... */ block comments. Make sure to handle newlines in them. Consider
  allowing them to
  nest. [Solution](https://github.com/BaLiKfromUA/pylox/commit/4728a19b990c8e08f5a9d441b4caa59a825f1325)
- [X] Define a visitor class for our syntax tree classes that takes an expression, converts it to RPN, and returns the
  resulting string. [Solution](https://github.com/BaLiKfromUA/pylox/commit/1818796ff74ba32a18bee6597e318c7dcec3f418)
- [ ] Add support for [comma expressions](https://en.wikipedia.org/wiki/Comma_operator). Give them the same precedence
  and associativity as in C. Write the grammar, and then implement the necessary parsing code.
- [ ] Add support for the C-style conditional or “ternary” operator `?:`
- [ ] Add error productions to handle each binary operator appearing without a left-hand operand. In other words, detect
  a binary operator appearing at the beginning of an expression. Report that as an error, but also parse and discard a
  right-hand operand with the appropriate precedence.

## My own design/implementation decisions

// todo:


