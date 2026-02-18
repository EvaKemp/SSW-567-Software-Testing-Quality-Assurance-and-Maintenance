"""Unit tests for the classify_triangle module."""

import unittest

from classify_triangle import classify_triangle


class TestClassifyTriangle(unittest.TestCase):
    """Test cases for classify_triangle()."""

    def test_invalid_non_numeric(self) -> None:
        """Non-numeric input returns 'invalid'."""
        self.assertEqual(classify_triangle("3", 4, 5), "invalid")

    def test_invalid_non_positive(self) -> None:
        """Zero or negative side returns 'invalid'."""
        self.assertEqual(classify_triangle(0, 4, 5), "invalid")
        self.assertEqual(classify_triangle(-1, 4, 5), "invalid")

    def test_not_a_triangle_triangle_inequality(self) -> None:
        """Failing triangle inequality returns 'not a triangle'."""
        self.assertEqual(classify_triangle(1, 2, 3), "not a triangle")
        self.assertEqual(classify_triangle(10, 1, 1), "not a triangle")

    def test_equilateral(self) -> None:
        """All equal sides returns 'equilateral'."""
        self.assertEqual(classify_triangle(2, 2, 2), "equilateral")

    def test_isosceles(self) -> None:
        """Two equal sides returns 'isosceles'."""
        self.assertEqual(classify_triangle(2, 2, 3), "isosceles")
        self.assertEqual(classify_triangle(3, 2, 2), "isosceles")

    def test_scalene(self) -> None:
        """All different sides returns 'scalene'."""
        self.assertEqual(classify_triangle(4, 5, 6), "scalene")

    def test_right_triangle_scalene(self) -> None:
        """3-4-5 triangle returns 'scalene right'."""
        self.assertEqual(classify_triangle(3, 4, 5), "scalene right")
        self.assertEqual(classify_triangle(5, 3, 4), "scalene right")

    def test_right_triangle_with_floats(self) -> None:
        """Float right triangle should still be detected as right."""
        self.assertEqual(classify_triangle(1.5, 2.0, 2.5), "scalene right")


if __name__ == "__main__":
    unittest.main()
