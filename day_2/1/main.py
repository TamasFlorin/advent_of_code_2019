import sys

def read_program(filename):
    with open(filename) as f:
        return [int (v) for v in f.readline().split(',')]
    return None

def execute_program(program):
    current_index = 0
    print('executing {0}'.format(program))
    while current_index < len(program):
        opcode = program[current_index]
        if opcode == 99:
            print('halting')
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


if __name__ == "__main__":
    program = read_program(sys.argv[1])
    program[1] = 12
    program[2] = 2
    result = execute_program(program)
    print(result[0])