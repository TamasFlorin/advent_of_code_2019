import copy
import sys

def number_to_list(num):
    res = []
    while num > 0:
        res.append(num % 10)
        num = num // 10
    return list(reversed(res))

def is_solution(digits):
    if len(digits) != 6:
        return False
    
    for i in range(0, len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False
    
    found_eq = False
    for i in range(0, len(digits) - 1):
        if digits[i] == digits[i + 1]:
            if not found_eq:
                found_eq = True

    return found_eq
    

def compute_variants(current_value, max_value):
    total = 0
    for i in range(current_value, max_value):
        digits = number_to_list(i)
        total += is_solution(digits)
    return total

if __name__ == "__main__":
    min_value = 123257
    max_value = 647015
    total = compute_variants(min_value, max_value)
    print('Number of different passwords {0}'.format(total))