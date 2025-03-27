from typing import List, Tuple

Point = Tuple[float, float]

def xywhToPoints(x: float, y: float, w: float, h: float) -> List[Point]:
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]

def cirBox(center, rx, ry):
    cx, cy = center
    return [(cx - rx, cy - ry), (cx + rx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)]

def are_toch(poly_a: List[Point], poly_b: List[Point]) -> bool:
    if not poly_a or not poly_b:
        return False

    for polygon in (poly_a, poly_b):
        for i1 in range(len(polygon)):
            i2 = (i1 + 1) % len(polygon)
            p1, p2 = polygon[i1], polygon[i2]
            normal = (p2[1] - p1[1], p1[0] - p2[0])
            min_a = min_b = float("inf")
            max_a = max_b = -float("inf")
            for px, py in poly_a:
                projection = normal[0] * px + normal[1] * py
                min_a, max_a = min(min_a, projection), max(max_a, projection)
            for px, py in poly_b:
                projection = normal[0] * px + normal[1] * py
                min_b, max_b = min(min_b, projection), max(max_b, projection)
            if max_a <= min_b or max_b <= min_a:
                return False
    return True 


