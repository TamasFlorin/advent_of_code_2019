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
    supported_opcodes = [1, 2, 3, 4, 5, 6, 7, 8]
    while current_index < len(program):
        instruction = program[current_index]
        opcode = int(instruction[-2:])
        modes = []
        if len(instruction) > 2:
            modes = [int(v) for v in instruction[:-2]]
        
        if len(modes) < 3:
            for _ in range(3 - len(modes)):
                modes.insert(0, 0)
        if opcode == 99:
            print('halting')
            return program
        elif opcode in supported_opcodes:
            if opcode == 1 or opcode == 2:
                position_1 = int(program[current_index + 1])
                position_2 = int(program[current_index + 2])
                result_index = int(program[current_index + 3])
                if opcode == 1:
                    program[result_index] = str(int(get_value_from_mode(position_1, modes[2], program)) + int(get_value_from_mode(position_2, modes[1], program)))
                elif opcode == 2:
                    program[result_index] = str(int(get_value_from_mode(position_1, modes[2], program)) * int(get_value_from_mode(position_2, modes[1], program)))
                current_index += 4
            elif opcode == 3:
                value = int(input('Value='))
                param = int(program[current_index + 1])
                program[param] = str(value)
                current_index += 2
            elif opcode == 4:
                address = int(program[current_index + 1])
                print(get_value_from_mode(address, modes[2], program))
                current_index += 2
            elif opcode == 5:
                val_if = int(get_value_from_mode(int(program[current_index + 1]), modes[2], program))
                if val_if != 0:
                    current_index = int(get_value_from_mode(int(program[current_index + 2]), modes[1], program))
                else:
                    current_index += 3
            elif opcode == 6:
                val_if = int(get_value_from_mode(int(program[current_index + 1]), modes[2], program))
                if val_if == 0:
                    current_index = int(get_value_from_mode(int(program[current_index + 2]), modes[1], program))
                else:
                    current_index += 3
            elif opcode == 7:
                value_1 = int(get_value_from_mode(int(program[current_index + 1]), modes[2], program))
                value_2 = int(get_value_from_mode(int(program[current_index + 2]), modes[1], program))
                if value_1 < value_2:
                    program[int(program[current_index + 3])] = str(1)
                else:
                    program[int(program[current_index + 3])] = str(0)
                current_index += 4
            elif opcode == 8:
                value_1 = int(get_value_from_mode(int(program[current_index + 1]), modes[2], program))
                value_2 = int(get_value_from_mode(int(program[current_index + 2]), modes[1], program))
                if value_1 == value_2:
                    program[int(program[current_index + 3])] = str(1)
                else:
                    program[int(program[current_index + 3])] = str(0)
                current_index += 4
        else:
            print('unknown opcode {0}'.format(opcode))
            return program

    return program


if __name__ == "__main__":
    program = read_program(sys.argv[1])
    result = execute_program(program)