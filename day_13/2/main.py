import sys
import copy
from collections import defaultdict
from PIL import Image

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
        self.inputs.append(str(inpt))

    def set_memory(self, address, value):
        self.memory[address] = str(value)

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

def draw_grid(grid):

    max_x = max([v[1] for v in grid.keys()])
    max_y = max([v[0] for v in grid.keys()])
    for _ in range(max_x + 1): print('=', end='')
    print()

    for y in range(0, max_y + 1):
        for x in range(0, max_x + 1):
            if (y, x) in grid:
                tile_id = grid[(y, x)]
                print(tile_id, end='')
            else:
                print(0, end='')
        print()

def play_game(program):
    # set the quarters so we can play
    program[0] = str(2)
    interpreter = IntCodeInterpreter(program)

    # play the game by sending commands to the IntComputer
    current_action = 0
    score = 0
    while not interpreter.is_halted():
        grid = {}
        interpreter.add_input(current_action)
        output = interpreter.execute()
        # prepare the grid for parsing
        paddle = (0, 0)
        ball = (0, 0)
        for i in range(0, len(output), 3):
            command = output[i:i + 4]
            x, y = int(command[0]), int(command[1])
            tile_id = int(command[2])
            if x == -1 and y == 0:
                score = tile_id # it's actually the score of the player
            else:
                grid[(y, x)] = tile_id
                if tile_id == 3:
                    paddle = (y, x)
                elif tile_id == 4:
                    ball = (y, x)

        _, ball_x = ball
        _, paddle_x = paddle

        if paddle_x < ball_x:
            current_action = 1
        elif paddle_x > ball_x:
            current_action = -1
        else:
            current_action = 0

    return score

if __name__ == "__main__":
    program = read_program(sys.argv[1])
    print('Score = {0}'.format(play_game(program)))