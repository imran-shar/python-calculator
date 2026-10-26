# Calculator (CLI) — Day 3

A simple command-line calculator in pure Python (standard library only).
Part of the [Daily AI & CS Mini Projects](https://github.com/imran-shar)
series — one small, runnable project per day, beginner to advanced.

## What it does

- Interactive mode: type expressions, get answers, until you quit.
- One-shot mode: evaluate a single expression from the command line.
- Operators: `+`, `-`, `*`, `/`, `%`, `**` (power), plus parentheses.
- Friendly errors for division by zero and invalid input.
- Expressions are parsed with Python's `ast` module — **not** `eval()` —
  so only numbers and arithmetic operators can run. Arbitrary code
  (like `__import__('os')...`) is rejected.

## How to run

Requires Python 3.8+ — no extra packages to install.

**Interactive mode:**

```bash
python calculator.py
```

```
Simple Calculator — type an expression, or 'q' to quit.
calc> (2 + 3) * 4
20
calc> 2 ** 10
1024
calc> 10 / 0
Error: Cannot divide by zero.
calc> q
Goodbye!
```

**One-shot mode:**

```bash
python calculator.py "2 + 3 * 4"   # prints 14
python calculator.py 5 + 3          # prints 8.0
```

## Run the tests

```bash
python -m unittest test_calculator -v
```

## What you learn

- **Functions** — each operation (`add`, `subtract`, `divide`, ...) is
  its own testable function instead of one long script.
- **Error handling** — `ZeroDivisionError` for `/ 0` and `ValueError`
  for bad operators or bad expressions, caught and shown nicely
  instead of crashing.
- **Safe evaluation** — parsing with `ast` and whitelisting only
  arithmetic nodes, instead of the dangerous `eval()`.
- **Operator precedence** — the parser handles it for free:
  `2 + 3 * 4` is 14, `(2 + 3) * 4` is 20.
- **Testing with `unittest`** — one test class per area, including
  security-style tests that prove hostile input is rejected.

## Files

| File | What it is |
| --- | --- |
| `calculator.py` | The calculator: operations, safe expression parser, CLI |
| `test_calculator.py` | 19 unit tests (operations, precedence, errors, safety) |
| `README.md` | This file |

## Try it next

- Add a `sqrt` function and a history feature (save past results).
- Add a `--help` flag with `argparse`.
- Turn it into a GUI with `tkinter` — a classic next step.
