import sys

def read_paths(filename):
    with open(filename) as f:
        first_path = [(value[0], int(value[1:])) for value in f.readline().split(',')]
        second_path = [(value[0], int(value[1:])) for value in f.readline().split(',')]

        return first_path, second_path
    return None

def move_on_grid(central_port, path, grid, symbol):
    y, x = central_port
    for move in path:
        direction, steps = move

        for _ in range(steps):
            if direction == 'U':
                (y, x) = (y - 1, x)
                grid[(y, x)] = symbol
            elif direction == 'D':
                (y ,x) = (y + 1, x)
                grid[(y, x)] = symbol
            elif direction == 'R':
                (y, x) = (y, x + 1)
                grid[(y, x)] = symbol
            elif direction == 'L':
                (y, x) = (y, x - 1)
                grid[(y, x)] = symbol

    return grid
             
def manhattan_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def solve(central_port, first_path, second_path):
    grid_1 = {}
    move_on_grid(central_port, first_path, grid_1, '1')
    grid_2 = {}
    move_on_grid(central_port, second_path, grid_2, '1')
    
    min_dist = 2 ** 31
    for value in grid_1:
        if value in grid_2:
            dist = manhattan_dist(central_port, value)
            if dist < min_dist:
                min_dist = dist

    return min_dist

if __name__ == "__main__":
    central_port = (0, 0)
    first_path, second_path = read_paths(sys.argv[1])
    min_dist = solve(central_port, first_path, second_path)
    print('Minimum distance to central point {0}'.format(min_dist))
