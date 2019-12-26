import sys
import copy

def read_program(filename):
    with open(filename) as f:
        return [int (v) for v in f.readline().split(',')]
    return None

def execute_program(program):
    current_index = 0
    while current_index < len(program):
        opcode = program[current_index]
        if opcode == 99:
            return program
        elif opcode == 1 or opcode == 2:
            position_1 = program[current_index + 1]
            position_2 = program[current_index + 2]
            result_index = program[current_index + 3]
            
            if opcode == 1:
                program[result_index] = program[position_1] + program[position_2]
            elif opcode == 2:
                program[result_index] = program[position_1] * program[position_2]

            current_index += 4
        else:
            print('unknown opcode {0}'.format(opcode))
            return program

    return program


def find_solution(program):
    for noun in range(0, len(program)):
        for verb in range(0, len(program)):
            current = copy.deepcopy(program)
            current[1] = noun
            current[2] = verb
            result = execute_program(program=current)

            if result[0] == 19690720:
                return 100 * noun + verb
    return None

if __name__ == "__main__":
    program = read_program(sys.argv[1])
    solution = find_solution(program)
    if solution is not None:
        print('found solution {0}'.format(solution))
    else: print('No Solution Found')