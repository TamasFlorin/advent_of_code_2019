import sys
import math
from collections import defaultdict

def read_grid(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            grid.append(line.rstrip('\n'))
        return grid

def build_points_map(grid):
    points = []
    asteroid = '#'
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == asteroid:
                points.append((y, x))
    return points

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dist = math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)
    return math.sqrt(dist)

def solve(grid):
    """ This solution is based on the fact that if a given point B is on the same line as A->C
        then the distance(A, C) == distance(A, B) + distance(B, C).
        Obviously, due to the precission of floating point numbers we can use a good enough approximation
        for the difference between the two distances.
    """
    points = build_points_map(grid=grid)
    max_visible = 0
    for A in points:
        points_except_this = list(filter(lambda x: x != A, points))
        sorted_points = sorted(points_except_this, key = lambda x: distance(A, x))
        result = []

        # Choose only the point C that does not have any other point B on the line A->C
        for i in range(len(sorted_points) - 1, -1, -1):
            ok = True
            C = sorted_points[i]
            for j in range(0, i):
                if i == j: continue
                B = sorted_points[j]
                a_c = distance(A, C)
                add = distance(A, B) + distance(B, C)
                if math.isclose(a_c, add, rel_tol=1e-09):
                    ok = False
                    break

            if ok:
                result.append(sorted_points[i])
        if len(result) > max_visible:
            max_visible = len(result)

    return max_visible

if __name__ == "__main__":
    grid = read_grid(sys.argv[1])
    print(solve(grid))
