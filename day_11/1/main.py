import sys
import copy
from collections import defaultdict

class IntCodeInterpreter(object):
    def __init__(self, program):
        self.instruction_pointer = 0
        self.outputs = []
        self.inputs = []
        self.input_pointer = 0
        self.program = copy.deepcopy(program)
        self.supported_opcodes = [1, 2, 3, 4, 5, 6, 7 ,8, 9]
        self._is_halted = False
        self._is_error = False
        self.relative_base = 0
        self.memory = defaultdict(lambda: '0')

    def execute(self):
        while self.instruction_pointer < len(self.program):
            instruction = self.program[self.instruction_pointer]
            opcode = int(instruction[-2:])
            modes = []
            if len(instruction) > 2:
                modes = [int(v) for v in instruction[:-2]]
            if len(modes) < 3:
                for _ in range(3 - len(modes)):
                    modes.insert(0, 0)
            #print(self.program)
            if opcode == 99:
                self._is_halted = True
                #print('halting')
                return self.outputs
            elif opcode in self.supported_opcodes:
                if opcode == 1 or opcode == 2:
                    value_1 = self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2])
                    value_2 = self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1])
                    result_index = int(self.program[self.instruction_pointer + 3])
                    if opcode == 1:
                        value = str(int(value_1) + int(value_2))
                        self.write(result_index, value, modes[0])
                    elif opcode == 2:
                        value = str(int(value_1) * int(value_2))
                        self.write(result_index, value, modes[0])
                    self.instruction_pointer += 4
                elif opcode == 3:
                    if self.input_pointer >= len(self.inputs):
                        return self.outputs
                    value = self.inputs[self.input_pointer]
                    self.input_pointer += 1
                    param = int(self.program[self.instruction_pointer + 1])
                    self.write(param, str(value), modes[2])
                    self.instruction_pointer += 2
                elif opcode == 4:
                    address = int(self.program[self.instruction_pointer + 1])
                    self.outputs.append(int(self.get_value_from_mode(address, modes[2])))
                    self.instruction_pointer += 2
                elif opcode == 5:
                    val_if = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    if val_if != 0:
                        value = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
                        self.instruction_pointer = value
                    else:
                        self.instruction_pointer += 3
                elif opcode == 6:
                    val_if = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    if val_if == 0:
                        self.instruction_pointer = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
                    else:
                        self.instruction_pointer += 3
                elif opcode == 7:
                    value_1 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    value_2 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
                    address = int(self.program[self.instruction_pointer + 3])
                    if value_1 < value_2:
                        self.write(address, str(1), modes[0])
                    else:
                        self.write(address, str(0), modes[0])
                    self.instruction_pointer += 4
                elif opcode == 8:
                    value_1 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    value_2 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
                    address = int(self.program[self.instruction_pointer + 3])
                    if value_1 == value_2:
                        self.write(address, str(1), modes[0])
                    else:
                        self.write(address, str(0), modes[0])
                    self.instruction_pointer += 4
                elif opcode == 9: # relative base
                    argument = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    self.relative_base += argument
                    self.instruction_pointer += 2
            else:
                print('unknown opcode {0} at index {1}'.format(opcode, self.instruction_pointer))
                self._is_error = True
                return None

        return None

    def is_halted(self):
        return self._is_halted

    def is_error(self):
        return self._is_error
    
    def add_inputs(self, inputs):
        self.inputs.extend(inputs)

    def add_input(self, inpt):
        self.inputs.append(inpt)

    def write(self, address, value, mode):
        if address >= len(self.program) and mode != 2:
            self.memory[address] = value
        elif address + self.relative_base >= len(self.program) and mode == 2:
            self.memory[address + self.relative_base] = value
        else:
            if mode == 2:
                self.program[address + self.relative_base] = value
            else:
                self.program[address] = value

    def get_value_from_mode(self, param, mode):
        if mode == 0:
            if param >= len(self.program):
                return self.memory[param]
            return self.program[param]
        elif mode == 2:
            if param + self.relative_base >= len(self.program):
                return self.memory[param + self.relative_base]
            return self.program[param + self.relative_base]
        elif mode == 1:
            return param
        else:
            raise Exception('Invalid mode {0}'.format(mode))

def read_program(filename):
    result = []
    with open(filename) as f:
        for line in f:
            result.extend([v for v in line.split(',')])
        return result

def solve(program):
    interpreter = IntCodeInterpreter(program)
    grid = defaultdict(lambda: (0, 0))
    start_point = (0, 0)
    grid[start_point] = (0, 0)
    current_direction = 'up'
    while not interpreter.is_halted():
        data = grid[start_point]
        current_color, paint_count = data
        interpreter.add_input(str(current_color)) # tell the computer the current cell color
        result = interpreter.execute()
        
        if result is None:
            break

        # we get as output what color we should paint it to
        # and the direction that the robot should turn to
        commands = result[-2:]
        new_color = commands[0]
        new_direction = commands[1]
        grid[start_point] = (new_color, paint_count + 1) # color to paint panel with

        if new_direction == 0:
            if current_direction == 'up':
                current_direction = 'left'
            elif current_direction == 'left':
                current_direction = 'down'
            elif current_direction == 'down':
                current_direction = 'right'
            elif current_direction == 'right':
                current_direction = 'up'
        elif new_direction == 1:
            if current_direction == 'up':
                current_direction = 'right'
            elif current_direction == 'left':
                current_direction = 'up'
            elif current_direction == 'down':
                current_direction = 'left'
            elif current_direction == 'right':
                current_direction = 'down'
        
        (y, x) = start_point
        if current_direction == 'up':
            start_point = (y + 1, x)
        elif current_direction == 'down':
            start_point = (y - 1, x)
        elif current_direction == 'left':
            start_point = (y, x - 1)
        elif current_direction == 'right':
            start_point = (y, x + 1)
    
    return sum([value[1] > 0 for value in grid.values()])

if __name__ == "__main__":
    program = read_program(sys.argv[1])
    print(solve(program))