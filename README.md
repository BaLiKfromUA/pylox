# pylox

[![codecov](https://codecov.io/gh/BaLiKfromUA/pylox/branch/main/graph/badge.svg?token=Z3FSTHP2JF)](https://codecov.io/gh/BaLiKfromUA/pylox)

**pylox** is Python implementation of Lox programming language which is a demo language
from [Crafting Interpreters](http://www.craftinginterpreters.com/) book by [Bob Nystrom](https://github.com/munificent).

I'm doing this because:

1. I want to learn about programming languages design and implementation.
2. I don't want to just read the book or copy and paste the code from it and I want to do something else than C or Java.
3. I want to become more "fluent" with Python and its dev infrastructure.
4. Fun.

## Features

- [x] Lexer
- [x] Parser
- [x] Basic types (`string`, `boolean`, `number`)
- [x] Floating point arithmetic, string concatenation
- [ ] Conditional expressions (ternary operator `?:`)
- [x] Logical expressions (`and`, `or`)
- [x] Control flow (`for`, `while`, `if` statements)
    - [X] `break` statement
        - [X] Check `break` out of loops
- [X] Functions
    - [X] Check `return` out of function
- [X] Classes
    - [X] Check `this` out of class
    - [X] Check `return` inside constructor `init`
- [X] Inheritance

## Challenges

- [X] Add support to Lox’s scanner for C-style /* ... */ block comments. Make sure to handle newlines in them. Consider
  allowing them to
  nest. [Solution](https://github.com/BaLiKfromUA/pylox/commit/4728a19b990c8e08f5a9d441b4caa59a825f1325)
- [X] Define a visitor class for our syntax tree classes that takes an expression, converts it to RPN, and returns the
  resulting string. [Solution](https://github.com/BaLiKfromUA/pylox/commit/1818796ff74ba32a18bee6597e318c7dcec3f418)
- [ ] Add support for [comma expressions](https://en.wikipedia.org/wiki/Comma_operator). Give them the same precedence
  and associativity as in C. Write the grammar, and then implement the necessary parsing code.
- [ ] Add support for the C-style conditional or “ternary” operator `?:`
- [X] Add error productions to handle each binary operator appearing without a left-hand operand. In other words, detect
  a binary operator appearing at the beginning of an expression. Report that as an error, but also parse and discard a
  right-hand operand with the appropriate
  precedence. [Solution](https://github.com/BaLiKfromUA/pylox/commit/a36d77449bdb175568ab19fdf92b91ca80e126a8)
- [X] Many languages define `+` such that if either operand is a string, the other is converted to a string and the
  results
  are then concatenated. For example, `"scone" + 4 `would yield `scone4`. Extend the code in `visitBinaryExpr()` to
  support that. [Solution](https://github.com/BaLiKfromUA/pylox/commit/b91c23da229ef6c81f30ba6f651d2fa76f8dfa1d)
- [X] What happens right now if you divide a number by zero? What do you think should happen? Justify your choice. How
  do
  other languages you know handle division by zero, and why do they make the choices they do?
  Change the implementation in `visitBinaryExpr()` to detect and report a runtime error for this
  case. [Solution](https://github.com/BaLiKfromUA/pylox/commit/bb5dc4117cb5b6a5947a6165aded331735a9bff4)
- [X] Add support to the REPL to let users type in both statements and expressions. If they enter a statement, execute
  it. If they enter an expression, evaluate it and display the result
  value. [Solution](https://github.com/BaLiKfromUA/pylox/commit/0a9d689365d0cd809bf496b4681d1066b7013c6a)
- [X] Unlike Lox, most other C-style languages also support `break` and `continue` statements inside loops. Add support
  for `break` statements. It should be a syntax error to have a break statement appear outside of any enclosing
  loop. [Solution](https://github.com/BaLiKfromUA/pylox/commit/952af36c44b1d1d5beacd48c48a9671514059942)
- [ ] Languages that encourage a functional style usually support **anonymous functions or lambdas**—an expression
  syntax that creates a function without binding it to a name. Add anonymous function syntax to Lox.
- [ ] Extend the resolver to report an error if a local variable is never used.
- [ ] Extend the resolver to associate a unique index for each local variable declared in a scope.
- [ ] Add support of `static` methods
- [ ] Extend Lox to support `getter` methods.

## My own design/implementation decisions

- [ ] Support of lists. For example:
  ```javascript
  var list = [1, 2, 3, 4, 5];
  print list[0]; // 1

  var result = [];
  for (var i = 0; list[i] != nil; i = i + 1) {
    result[i] = list[i] * 10;
  }
  print result; // [10, 20, 30, 40, 50]
  ```
- [ ] Support of functional list processing. For example:
  ```javascript
  var list = [1, 2, 3, 4, 5];
  print map(lambda(num) { return num * num; }, list); // [1, 4, 9, 16, 25]
  ```
- [X] Support of additional built-in functions:
    - [X] `input`
    - [X] `len`


