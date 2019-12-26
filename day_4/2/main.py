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
    
    num_eq = 0
    for i in range(0, len(digits) - 1):
        if digits[i] == digits[i + 1]:
            num_eq += 1
        else:
            if num_eq == 1:
                return True
            num_eq = 0

    return num_eq == 1
    

def compute_variants(current_value, max_value):
    total = 0
    for i in range(current_value, max_value + 1):
        digits = number_to_list(i)
        #if is_solution(digits):
            #print(i)
        total += is_solution(digits)
    return total

if __name__ == "__main__":
    #print(is_solution(number_to_list(112233)))
    #print(is_solution(number_to_list(123444)))
    #print(is_solution(number_to_list(111122)))
    min_value = 123257
    max_value = 647015
    total = compute_variants(min_value, max_value)
    print('Number of different passwords {0}'.format(total))