import sys

def read_program(filename):
    with open(filename) as f:
        return [v for v in f.readline().split(',')]
    return None

def get_value_from_mode(param, mode, program):
    if mode == 0:
        return program[param]
    else:
        return param

def execute_program(program):
    current_index = 0
    supported_opcodes = [1, 2, 3, 4]
    while current_index < len(program):
        instruction = program[current_index]
        opcode = int(instruction[-2:])
        modes = []
        if len(instruction) > 2:
            modes = [int(v) for v in instruction[:-2]]
        if opcode == 99:
            print('halting')
            return program
        elif opcode in supported_opcodes:
            if opcode == 1 or opcode == 2:
                first_param_mode = 0
                second_param_mode = 0
                third_param_mode = 0
                if len(modes) == 1:
                    first_param_mode = modes[0]
                elif len(modes) == 2:
                    first_param_mode = modes[1]
                    second_param_mode = modes[0]
                elif len(modes) == 3:
                    first_param_mode = modes[2]
                    second_param_mode = modes[1]
                    third_param_mode = modes[0]
                position_1 = int(program[current_index + 1])
                position_2 = int(program[current_index + 2])
                result_index = int(program[current_index + 3])
                
                if opcode == 1:
                    program[result_index] = str(int(get_value_from_mode(position_1, first_param_mode, program)) + int(get_value_from_mode(position_2, second_param_mode, program)))
                elif opcode == 2:
                    program[result_index] = str(int(get_value_from_mode(position_1, first_param_mode, program)) * int(get_value_from_mode(position_2, second_param_mode, program)))
                current_index += 4
            elif opcode == 3:
                value = int(input('Value='))
                param = int(program[current_index + 1])
                program[param] = str(value)
                current_index += 2
            elif opcode == 4:
                param_mode = 0
                
                if len(modes) == 1:
                    param_mode = modes[0]
                address = int(program[current_index + 1])
                print(get_value_from_mode(address, param_mode, program))
                current_index += 2
        else:
            print('unknown opcode {0}'.format(opcode))
            return program

    return program


if __name__ == "__main__":
    program = read_program(sys.argv[1])
    result = execute_program(program)