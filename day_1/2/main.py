from math import floor
import sys

def compute_required_fuel(mass):
    return floor(mass // 3) - 2

def compute_required_fuel_recursive(mass, total=0):
    current_value = compute_required_fuel(mass)
    if current_value <= 0:
        return total
    else:
        return current_value + compute_required_fuel_recursive(current_value)

def solve(masses):
    result = 0
    for mass in masses:
        result += compute_required_fuel_recursive(mass)

    return result

def read_data(filename):
    data = []
    with open(filename) as f:
        for value in f:
            mass = int(value)
            data.append(mass)
    return data

if __name__ == "__main__":
    masses = read_data(sys.argv[1])
    total = solve(masses=masses)
    print(total)