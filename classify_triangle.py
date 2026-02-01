# classify_triangle.py

from typing import Union

Number = Union[int, float]


def classify_triangle(a: Number, b: Number, c: Number) -> str:
    """
    Classify a triangle by side lengths.
    Returns one of:
      - "equilateral"
      - "isosceles"
      - "scalene"
    and appends " right" if it is also a right triangle, e.g. "isosceles right".

    If inputs are invalid or do not form a triangle, returns:
      - "not a triangle"
      - "invalid"
    """

    # Validate types and values
    for x in (a, b, c):
        if not isinstance(x, (int, float)):
            return "invalid"
        if x <= 0:
            return "invalid"

    # Triangle inequality (sort so largest is last)
    sides = sorted([a, b, c])
    x, y, z = sides  # z is largest

    if x + y <= z:
        return "not a triangle"

    # Determine basic type
    if a == b == c:
        tri_type = "equilateral"
    elif a == b or b == c or a == c:
        tri_type = "isosceles"
    else:
        tri_type = "scalene"

    # Right triangle check: x^2 + y^2 == z^2 (use tolerance for floats)
    # Use a small tolerance in case of float inputs
    tol = 1e-9
    is_right = abs((x * x + y * y) - (z * z)) <= tol

    return f"{tri_type} right" if is_right else tri_type


def main():
    # Simple demo runs (counts for your "input/output screenshot" deliverable)
    samples = [
        (3, 4, 5),
        (2, 2, 3),
        (2, 2, 2),
        (1, 2, 3),
        (-1, 2, 2),
        (1.5, 2.0, 2.5),
    ]
    for a, b, c in samples:
        print(f"{(a, b, c)} -> {classify_triangle(a, b, c)}")


if __name__ == "__main__":
    main()