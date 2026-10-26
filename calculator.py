"""CLI calculator — Day 3 of the Daily AI & CS Mini Projects series.

Two ways to use it:

1. Interactive mode (no arguments):

       python calculator.py

2. One-shot mode — evaluate a single expression:

       python calculator.py "2 + 3 * 4"

Expressions support ``+ - * / % **`` and parentheses. They are parsed
with Python's ``ast`` module instead of ``eval()``, so only numbers and
arithmetic operators are ever executed — arbitrary code cannot run.

Every operation lives in its own function, so the arithmetic is easy
to test and to reuse from other code.
"""

import ast
import operator
import sys

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

SYMBOLS = {"+": ast.Add, "-": ast.Sub, "*": ast.Mult,
           "/": ast.Div, "%": ast.Mod, "**": ast.Pow}


def add(a, b):
    """Return a + b."""
    return a + b


def subtract(a, b):
    """Return a - b."""
    return a - b


def multiply(a, b):
    """Return a * b."""
    return a * b


def divide(a, b):
    """Return a / b.

    Raises ZeroDivisionError with a friendly message instead of
    letting Python's default error bubble up unhandled.
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def power(a, b):
    """Return a ** b."""
    return a ** b


def modulo(a, b):
    """Return a % b; raises ZeroDivisionError on a zero divisor."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a % b


def calculate(a, op, b):
    """Apply one operator symbol (e.g. "+") to two numbers.

    Raises ValueError for an unknown operator.
    """
    funcs = {"+": add, "-": subtract, "*": multiply,
             "/": divide, "%": modulo, "**": power}
    if op not in funcs:
        raise ValueError(f"Unknown operator: {op!r}. "
                         f"Use one of: {', '.join(funcs)}")
    return funcs[op](a, b)


def _eval_node(node):
    """Recursively evaluate one node of a parsed arithmetic expression."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Only numbers are allowed, got {node.value!r}")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        value = _eval_node(node.operand)
        return -value if isinstance(node.op, ast.USub) else value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        if isinstance(node.op, ast.Mod) and right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return OPERATORS[type(node.op)](left, right)
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def evaluate_expression(expression):
    """Safely evaluate an arithmetic expression string.

    Raises ValueError for invalid or non-arithmetic input and
    ZeroDivisionError for division/modulo by zero.
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {expression!r}") from exc
    return _eval_node(tree)


def repl():
    """Interactive loop: read expressions until the user quits."""
    print("Simple Calculator — type an expression, or 'q' to quit.")
    print("Operators: +  -  *  /  %  **  and parentheses, e.g. (2 + 3) * 4")
    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        if line.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            return
        if not line:
            continue
        try:
            print(evaluate_expression(line))
        except ZeroDivisionError as exc:
            print(f"Error: {exc}")
        except ValueError as exc:
            print(f"Error: {exc}")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        repl()
        return 0
    if len(argv) == 1:
        try:
            print(evaluate_expression(argv[0]))
        except (ZeroDivisionError, ValueError) as exc:
            print(f"Error: {exc}")
            return 1
        return 0
    if len(argv) == 3:
        try:
            a, b = float(argv[0]), float(argv[2])
        except ValueError:
            print("Error: operands must be numbers, e.g. calculator.py 5 + 3")
            return 1
        try:
            print(calculate(a, argv[1], b))
        except (ZeroDivisionError, ValueError) as exc:
            print(f"Error: {exc}")
            return 1
        return 0
    print("Usage: python calculator.py [\"expression\" | number operator number]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
