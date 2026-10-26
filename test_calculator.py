"""Tests for the Day 3 CLI calculator. Run with:

    python -m unittest test_calculator -v
"""

import unittest

from calculator import (
    add,
    calculate,
    divide,
    evaluate_expression,
    modulo,
    multiply,
    power,
    subtract,
)


class TestBasicOperations(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)

    def test_subtract(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(4, 10), -6)

    def test_multiply(self):
        self.assertEqual(multiply(3, 7), 21)
        self.assertEqual(multiply(-2, 5), -10)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(1, 3), 1 / 3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)

    def test_power(self):
        self.assertEqual(power(2, 10), 1024)
        self.assertEqual(power(5, 0), 1)

    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)
        with self.assertRaises(ZeroDivisionError):
            modulo(10, 0)


class TestCalculate(unittest.TestCase):
    def test_all_operators(self):
        cases = [("+", 2, 3, 5), ("-", 5, 3, 2), ("*", 4, 3, 12),
                 ("/", 8, 2, 4), ("%", 10, 3, 1), ("**", 2, 3, 8)]
        for op, a, b, expected in cases:
            with self.subTest(op=op):
                self.assertEqual(calculate(a, op, b), expected)

    def test_unknown_operator(self):
        with self.assertRaises(ValueError):
            calculate(1, "@", 2)

    def test_calculate_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate(1, "/", 0)


class TestEvaluateExpression(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(evaluate_expression("2 + 3"), 5)

    def test_operator_precedence(self):
        # Multiplication binds tighter than addition.
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)

    def test_power_and_modulo(self):
        self.assertEqual(evaluate_expression("2 ** 3 + 10 % 3"), 9)

    def test_negative_numbers(self):
        self.assertEqual(evaluate_expression("-5 + 3"), -2)
        self.assertEqual(evaluate_expression("5 - -3"), 8)

    def test_decimals(self):
        self.assertAlmostEqual(evaluate_expression("1.5 * 2"), 3.0)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            evaluate_expression("1 / 0")

    def test_rejects_non_arithmetic_code(self):
        # eval() would run this; our ast parser must refuse it.
        with self.assertRaises(ValueError):
            evaluate_expression("__import__('os').system('echo hi')")
        with self.assertRaises(ValueError):
            evaluate_expression("2 +")

    def test_rejects_names(self):
        with self.assertRaises(ValueError):
            evaluate_expression("x + 1")


if __name__ == "__main__":
    unittest.main()
