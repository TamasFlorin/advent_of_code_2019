import sys
import copy

class IntCodeInterpreter(object):
    def __init__(self, program):
        self.instruction_pointer = 0
        self.outputs = []
        self.inputs = []
        self.input_pointer = 0
        self.program = program
        self.supported_opcodes = [1, 2, 3, 4, 5, 6, 7 ,8]
        self._is_halted = False
        self._is_error = False

    def execute(self):
        while self.instruction_pointer < len(self.program):
            instruction = self.program[self.instruction_pointer]
            opcode = int(instruction[-2:])
            print('{0} {1} {2}'.format(self.instruction_pointer, instruction, opcode))
            modes = []
            if len(instruction) > 2:
                modes = [int(v) for v in instruction[:-2]]
            
            if len(modes) < 3:
                for _ in range(3 - len(modes)):
                    modes.insert(0, 0)
            if opcode == 99:
                self._is_halted = True
                #print('halting')
                return self.outputs[-1]
            elif opcode in self.supported_opcodes:
                if opcode == 1 or opcode == 2:
                    position_1 = int(self.program[self.instruction_pointer + 1])
                    position_2 = int(self.program[self.instruction_pointer + 2])
                    result_index = int(self.program[self.instruction_pointer + 3])
                    if opcode == 1:
                        self.program[result_index] = str(int(self.get_value_from_mode(position_1, modes[2])) + int(self.get_value_from_mode(position_2, modes[1])))
                    elif opcode == 2:
                        self.program[result_index] = str(int(self.get_value_from_mode(position_1, modes[2])) * int(self.get_value_from_mode(position_2, modes[1])))
                    self.instruction_pointer += 4
                elif opcode == 3:
                    if self.input_pointer >= len(self.inputs):
                        return self.outputs[-1]
                    value = self.inputs[self.input_pointer]
                    self.input_pointer += 1
                    #int(input('Value='))
                    param = int(self.program[self.instruction_pointer + 1])
                    self.program[param] = str(value)
                    self.instruction_pointer += 2
                elif opcode == 4:
                    address = int(self.program[self.instruction_pointer + 1])
                    self.outputs.append(int(self.get_value_from_mode(address, modes[2])))
                    self.instruction_pointer += 2
                elif opcode == 5:
                    val_if = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    if val_if != 0:
                        self.instruction_pointer = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
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
                    if value_1 < value_2:
                        self.program[int(program[self.instruction_pointer + 3])] = str(1)
                    else:
                        self.program[int(program[self.instruction_pointer + 3])] = str(0)
                    self.instruction_pointer += 4
                elif opcode == 8:
                    value_1 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 1]), modes[2]))
                    value_2 = int(self.get_value_from_mode(int(self.program[self.instruction_pointer + 2]), modes[1]))
                    if value_1 == value_2:
                        self.program[int(program[self.instruction_pointer + 3])] = str(1)
                    else:
                        self.program[int(program[self.instruction_pointer + 3])] = str(0)
                    self.instruction_pointer += 4
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

    def _addition_handler(self):
        pass
    def _multiplication_handler(self):
        pass

    def get_value_from_mode(self, param, mode):
        if mode == 0:
            return self.program[param]
        else:
            return param

def read_program(filename):
    with open(filename) as f:
        return [v for v in f.readline().split(',')]
    return None

def solve(program, min_signal, max_signal):
    max_result = 0
    max_sequence = []
    for a in range(min_signal, max_signal):
        for b in range(min_signal, max_signal):
            for c in range(min_signal, max_signal):
                for d in range(min_signal, max_signal):
                    for e in range(min_signal, max_signal):
                        sequence = [a, b, c, d, e]
                        if len(set(sequence)) == 5:
                            interpreters = []
                            for i in range(5):
                                interpreters.append(IntCodeInterpreter(copy.deepcopy(program)))
                                interpreters[i].add_input(sequence[i])
                            first_input = str(0)
                            r_e, r_a, r_b, r_c, r_d = 0, 0, 0, 0, 0
                            while not any(p.is_halted() or p.is_error() for p in interpreters):
                                interpreters[0].add_input(first_input)
                                r_a = interpreters[0].execute()
                                interpreters[1].add_input(r_a)
                                r_b = interpreters[1].execute()
                                interpreters[2].add_input(r_b)
                                r_c = interpreters[2].execute()
                                interpreters[3].add_input(r_c)
                                r_d = interpreters[3].execute()
                                interpreters[4].add_input(r_d)
                                r_e = interpreters[4].execute()
                                first_input = r_e
                            print('{0} {1}'.format(sequence, r_e))
                            if int(r_e) >= max_result:
                                max_result = r_e
                                max_sequence = sequence

    return max_sequence, max_result

if __name__ == "__main__":
    program = read_program(sys.argv[1])
    print(solve(program, 5, 10))