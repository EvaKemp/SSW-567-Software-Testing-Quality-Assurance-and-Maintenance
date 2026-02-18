"""
Triangle classification module for SSW-567.

This module provides a single function, classify_triangle(), which classifies a
triangle based on three side lengths.
"""

from __future__ import annotations

import math
from typing import Union

Number = Union[int, float]


def classify_triangle(side_a: Number, side_b: Number, side_c: Number) -> str:
    """
    Classify a triangle by side lengths.

    Returns one of:
      - "equilateral"
      - "isosceles"
      - "scalene"
    and appends " right" if it is also a right triangle (e.g., "scalene right").

    If inputs are invalid or do not form a triangle, returns:
      - "invalid"          (non-numeric or <= 0)
      - "not a triangle"   (fails triangle inequality)
    """
    for side in (side_a, side_b, side_c):
        if not isinstance(side, (int, float)):
            return "invalid"
        if side <= 0:
            return "invalid"

    sorted_sides = sorted((float(side_a), float(side_b), float(side_c)))
    small_side, mid_side, large_side = sorted_sides

    if small_side + mid_side <= large_side:
        return "not a triangle"

    tolerance = 1e-9

    ab_equal = math.isclose(side_a, side_b, abs_tol=tolerance)
    bc_equal = math.isclose(side_b, side_c, abs_tol=tolerance)
    ac_equal = math.isclose(side_a, side_c, abs_tol=tolerance)

    if ab_equal and bc_equal:
        triangle_type = "equilateral"
    elif ab_equal or bc_equal or ac_equal:
        triangle_type = "isosceles"
    else:
        triangle_type = "scalene"

    is_right = math.isclose(
        small_side * small_side + mid_side * mid_side,
        large_side * large_side,
        abs_tol=tolerance,
    )

    return f"{triangle_type} right" if is_right else triangle_type


def main() -> None:
    """Run a small demo of triangle classifications."""
    samples = [
        (3, 4, 5),
        (2, 2, 3),
        (2, 2, 2),
        (1, 2, 3),
        (-1, 2, 2),
        (1.5, 2.0, 2.5),
    ]

    for side_a, side_b, side_c in samples:
        result = classify_triangle(side_a, side_b, side_c)
        print(f"{(side_a, side_b, side_c)} -> {result}")


if __name__ == "__main__":
    main()
    