# test_classify_triangle.py

import unittest
from classify_triangle import classify_triangle


class TestClassifyTriangle(unittest.TestCase):
    # ---- Valid triangle type tests ----
    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "equilateral")

    def test_isosceles(self):
        self.assertEqual(classify_triangle(5, 5, 8), "isosceles")
        self.assertEqual(classify_triangle(5, 8, 5), "isosceles")
        self.assertEqual(classify_triangle(8, 5, 5), "isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(4, 5, 6), "scalene")

    # ---- Right triangle tests ----
    def test_right_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "scalene right")
        self.assertEqual(classify_triangle(5, 3, 4), "scalene right")

    def test_right_isosceles(self):
        # 1, 1, sqrt(2) is right isosceles (use float)
        self.assertEqual(classify_triangle(1, 1, 2 ** 0.5), "isosceles right")

    def test_not_right(self):
        self.assertEqual(classify_triangle(2, 3, 4), "scalene")

    # ---- Triangle inequality / invalid input tests ----
    def test_not_a_triangle(self):
        self.assertEqual(classify_triangle(1, 2, 3), "not a triangle")  # degenerate
        self.assertEqual(classify_triangle(10, 1, 1), "not a triangle")

    def test_invalid_zero_or_negative(self):
        self.assertEqual(classify_triangle(0, 2, 2), "invalid")
        self.assertEqual(classify_triangle(-1, 2, 2), "invalid")

    def test_invalid_types(self):
        self.assertEqual(classify_triangle("3", 4, 5), "invalid")  # type: ignore
        self.assertEqual(classify_triangle(None, 4, 5), "invalid")  # type: ignore

    # ---- Boundary-ish tests ----
    def test_large_values(self):
        self.assertEqual(classify_triangle(3000000, 4000000, 5000000), "scalene right")

    def test_float_right_triangle(self):
        self.assertEqual(classify_triangle(1.5, 2.0, 2.5), "scalene right")


if __name__ == "__main__":
    unittest.main()