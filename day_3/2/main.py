import sys

def read_paths(filename):
    with open(filename) as f:
        first_path = [(value[0], int(value[1:])) for value in f.readline().split(',')]
        second_path = [(value[0], int(value[1:])) for value in f.readline().split(',')]

        return first_path, second_path
    return None

def move_on_grid(central_port, path, grid, symbol):
    y, x = central_port
    total_steps = 0
    num_steps = {}
    for move in path:
        direction, steps = move

        for _ in range(steps):
            total_steps += 1
            if direction == 'U':
                (y, x) = (y - 1, x)
            elif direction == 'D':
                (y ,x) = (y + 1, x)
            elif direction == 'R':
                (y, x) = (y, x + 1)
            elif direction == 'L':
                (y, x) = (y, x - 1)
            
            if (y, x) not in grid:
                grid[(y, x)] = symbol
                num_steps[(y, x)] = total_steps

    return num_steps
             
def manhattan_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def solve(central_port, first_path, second_path):
    grid_1 = {}
    steps_1 = move_on_grid(central_port, first_path, grid_1, '1')
    grid_2 = {}
    steps_2 = move_on_grid(central_port, second_path, grid_2, '1')
    
    min_dist = 2 ** 31
    for value in grid_1:
        if value in grid_2:
            total_steps = steps_1[value] + steps_2[value]
            if total_steps < min_dist:
                min_dist = total_steps

    return min_dist

if __name__ == "__main__":
    central_port = (0, 0)
    first_path, second_path = read_paths(sys.argv[1])
    min_dist = solve(central_port, first_path, second_path)
    print('Minimum distance to central point {0}'.format(min_dist))
