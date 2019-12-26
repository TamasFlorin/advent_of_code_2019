import sys
import math
from collections import defaultdict
import copy
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

def get_visible_asteroids(point, points):
    A = point
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
    return result


def get_max_visible_asteroid(points):
    """ This solution is based on the fact that if a given point B is on the same line as A->C
        then the distance(A, C) == distance(A, B) + distance(B, C).
        Obviously, due to the precission of floating point numbers we can use a good enough approximation
        for the difference between the two distances.
    """
    max_visible = 0
    asteroid = None
    for A in points:
        asteroids = get_visible_asteroids(A, points)
        if len(asteroids) > max_visible:
            max_visible = len(asteroids)
            asteroid = A

    return asteroid, max_visible
 

def save(station, asteroids, width):
    destroy_count = 0
    start = True
    while len(asteroids) > 1:
        print('Remaining asteroids {0}'.format(len(asteroids)))
        visible_asteroids = get_visible_asteroids(station, asteroids)
        upper = filter(lambda  x: x[0] - station[0] < 0, visible_asteroids) # above station
        lower = filter(lambda x: x[0] - station[0] >= 0, visible_asteroids)  # below station
        upper = sorted(upper, key=lambda x: (x[1], x[0]))
        lower = sorted(lower, reverse=True, key=lambda x: (x[1], x[0]))

        if start:
            upper = filter(lambda x: x[1] >= width // 2, upper)
            start = False
        
        for asteroid in upper:
            asteroids.remove(asteroid)
            print('Removing {0} from upper'.format(asteroid))
            destroy_count += 1
            if destroy_count == 200:
                return asteroid
        for asteroid in lower:
            print('Removing {0} from lower'.format(asteroid))
            asteroids.remove(asteroid)
            destroy_count += 1
            if destroy_count == 200:
                return asteroid
    return None


def compute_distance(angle, station, asteroid):
    # d1: a * x + b*y +c = 0 => our equation with given angle: y - tan(m) * x + tan(m)*8 + 3 = 0
    m = math.tan(angle)
    
    y_s, x_s = station
    a, b, c = m, -1, (x_s - m * y_s)
    y,x = asteroid
    top = abs(a * x + b * y + c)
    bottom = math.sqrt(a ** 2 + b ** 2)
    distance = top / bottom
    #print(distance)
    return distance

def is_on_line(angle, station, asteriod):
    # d1: a * x + b*y +c = 0 => our equation with given angle: y - tan(m) * x + tan(m)*8 + 3 = 0
    return compute_distance(angle, station, asteriod) <= 1.0
    m = math.tan(angle)
    y_s, x_s = station
    #c = x_s - m * y_s
    y, x = asteroid
    #print(y, m * (x - x_s) + y_s)
    return math.isclose(y, m * (x - x_s) + y_s)

def destroy(station, asteroids, width):
    # the laser points upwards at first
    remove_count = 0
    while len(asteroids) > 1:
        print('Remaining asteroids {0}'.format(len(asteroids)))
        visible_asteroids = get_visible_asteroids(station, asteroids)
        angles = []
        for asteroid in visible_asteroids:
            x = station[1] - asteroid[1]
            y = station[0] - asteroid[0]
            angle = math.atan2(x, y)
            angle = math.degrees(angle)
            if angle < 0:
                angle += 360.0
            angles.append((asteroid, angle))
        angles = sorted(angles, key=lambda x: (x[1], distance(station, x[0])))

        for item in angles:
            asteroid, angle = item
            asteroids.remove(asteroid)
            remove_count +=1 
            if remove_count == 200:
                return asteroid
            print('Removing asteroid {0} with angle {1}'.format(asteroid, angle))
    return None

if __name__ == "__main__":
    grid = read_grid(sys.argv[1])
    asteroids = build_points_map(grid=grid)
    # prepare station
    asteroid, max_visible = get_max_visible_asteroid(asteroids)
    print('Asteroid={0}, Visible={1}'.format(asteroid, max_visible))
    print(destroy(asteroid, asteroids, len(grid[0])))
