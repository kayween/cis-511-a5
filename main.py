# python programs better start with a comment

OPCODES = {"add": 1, "tail": 2, "clr": 3, "assign": 4, "gotoa": 5, "gotob": 6, "jmpa": 7, "jmpb": 8, "continue": 9}


def human2machine(instruction, alphabet):
    """
    Translate a human readable instruction to a 0/1 instruction
    """
    line, idx_reg_x, opcode, a, whatever = instruction

    return (
        -1 if line.strip() == "" else int(line[-1]),
        0 if idx_reg_x.strip() == "" else int(idx_reg_x[-1]),
        OPCODES[opcode.strip()],
        0 if alphabet.find(a) == -1 else alphabet.find(a) + 1,
        0 if whatever.strip() == "" else int(whatever[-1]),
    )


def machine2human(instruction, alphabet):
    """
    Translate a 0/1 machine instruction to a human readable instruction
    """
    line, idx_reg_x, opcode, j, whatever = instruction

    line = "  " if line < 0 else "L{:d}".format(line)
    idx_reg_x = "  " if idx_reg_x == 0 else "R{:d}".format(idx_reg_x)
    a = ' ' if j == 0 else alphabet[j - 1]

    if opcode in [1, 2, 3, 4]:
        whatever = "R{:d}".format(whatever)

    elif opcode in [5, 6, 7, 8]:
        whatever = "L{:d}".format(whatever)

    elif opcode == 9:
        whatever = "  "

    opcode = list(OPCODES)[opcode - 1]

    return (line, idx_reg_x, opcode, a, whatever)


def search(program, pc, target, forward=True):
    i = pc

    while i in range(len(program)):
        if target == program[i][0]:
            return i

        i = i + 1 if forward else i - 1

    assert 0, "invalid jump"


def interpreter(program, registers, alphabet, verbose=True):
    """
    The RAM program interpreter
    It is caller's responsibility to make sure the alphabet contains all symbols in the registers!!

    Args:
        program (list): the program is a list of instructions,
            where each instruction is a tuple of the form (N, X, opcode, j, Y/N)
        registers (tuple): a sequence of strings representing the initial values of registers
        alphabet (string): a string a_1 a_2 ... a_k representing the alphabet

    Return: the return value of the RAM program
    """
    pc = 0

    while pc in range(len(program)):
        instruction = program[pc]
        if verbose:
            print("(pc = {:2d}) --> ({:2}, {}, {:8}, {}, {}), registers: {}".format(
                pc, *machine2human(instruction, alphabet), str(registers)))

        _, idx_reg_x, opcode, j, whatever = instruction

        if opcode in [1, 2, 3, 4]:
            idx_reg_y = whatever
        elif opcode in [5, 6, 7, 8]:
            target = whatever

        if opcode == OPCODES["add"]:
            registers[idx_reg_y - 1] += alphabet[j - 1]

        elif opcode == OPCODES["tail"]:
            registers[idx_reg_y - 1] = registers[idx_reg_y - 1][1:]

        elif opcode == OPCODES["clr"]:
            registers[idx_reg_y - 1] = ""

        elif opcode == OPCODES["assign"]:
            registers[idx_reg_x - 1] = registers[idx_reg_y - 1]

        elif opcode == OPCODES["gotoa"] or opcode == OPCODES["gotob"]:
            pc = search(program, pc, target, forward=opcode == OPCODES["gotob"])
            continue

        elif opcode == OPCODES["jmpa"] or opcode == OPCODES["jmpb"]:
            if registers[idx_reg_x - 1][:1] == alphabet[j - 1]:
                pc = search(program, pc, target, forward=opcode == OPCODES["jmpb"])
                continue

        elif opcode == OPCODES["continue"]:
            pass

        pc += 1

    return registers[0]


def test_concatenate(verbose):
    concatenate = [
        [-1,    3,     4,    0,   1],
        [-1,    4,     4,    0,   2],
        [0,     4,     8,    1,   1],
        [-1,    4,     8,    2,   2],
        [-1,    0,     6,    0,   3],
        [1,     0,     1,    1,   3],
        [-1,    0,     2,    0,   4],
        [-1,    0,     5,    0,   0],
        [2,     0,     1,    2,   3],
        [-1,    0,     2,    0,   4],
        [-1,    0,     5,    0,   0],
        [3,     1,     4,    0,   3],
        [-1,    0,     9,    0,   0]
        ]

    alphabet = "ab"
    # print([machine2human(xx, alphabet) for xx in concatenate])

    # Each row is a test case. Append new inputs at the end of the list.
    lst_inputs = [
        ["", ""],
        ["", "a"],
        ["a", ""],
        ["b", "aa"],
        ["abab", "aa"],
        ]

    print("------ concatenate function ------ ")

    for inputs in lst_inputs:
        program = concatenate
        registers = [*inputs, "", ""]

        result = interpreter(program, registers, alphabet, verbose=verbose)

        print("inputs = '{}' and '{}',".format(*inputs),
              "return = '{}'".format(result))


def test_reverse(verbose):
    reverse = [
        ("  ",  "R2", "assign", ' ', "R1"),
        ("  ",  "  ", "clr   ", ' ', "R1"),

        ("L0",  "R2", "jmpb  ", 'a', "L1"),
        ("  ",  "R2", "jmpb  ", 'b', "L3"),
        ("  ",  "R2", "gotob ", ' ', "L4"),
        # --- start of branch for a ---
        ("L1",  "  ", "tail  ", ' ', "R2"),
        ("  ",  "R2", "jmpb  ", 'a', "L2"),
        ("  ",  "R2", "jmpb  ", 'b', "L2"),

        ("  ",  "R2", "assign", ' ', "R3"),
        ("  ",  "  ", "clr   ", ' ', "R3"),
        ("  ",  "  ", "add   ", 'a', "R1"),
        ("  ",  "  ", "gotoa ", ' ', "L0"),

        ("L2",  "  ", "add   ", 'a', "R3"),
        ("  ",  "  ", "gotoa ", ' ', "L0"),
        # --- end of branch for a ---

        # --- start of branch for b ---
        ("L3",  "  ", "tail  ", ' ', "R2"),
        ("  ",  "R2", "jmpb  ", 'a', "L2"),
        ("  ",  "R2", "jmpb  ", 'b', "L2"),

        ("  ",  "R2", "assign", ' ', "R3"),
        ("  ",  "  ", "clr   ", ' ', "R3"),
        ("  ",  "  ", "add   ", 'b', "R1"),
        ("  ",  "  ", "gotoa ", ' ', "L0"),

        ("L2",  "  ", "add   ", 'b', "R3"),
        ("  ",  "  ", "gotoa ", ' ', "L0"),
        # --- end of branch for b ---

        ("L4", "", "continue", '', ""),
    ]

    alphabet = "ab"

    # append new inputs in the end of the list
    lst_inputs = ["", "a", "b", "aa", "bb", "aba", "bab", "abab", "baba", "aaabb"]

    print("------ reverse function ------ ")

    for inputs in lst_inputs:
        # translate the human readable code to 0/1 machine code
        program = [human2machine(xx, alphabet) for xx in reverse]
        registers = [inputs, "", ""]

        result = interpreter(program, registers, alphabet, verbose=verbose)

        print("inputs = '{}',".format(inputs),
              "return = '{}'".format(result))


def test_triple(verbose):
    triple = [
        ("  ",  "R2", "assign", ' ', "R1"),
        ("  ",  "R3", "assign", ' ', "R1"),

        # append R2 to R1
        ('L0', 'R2', 'jmpb ', 'a', 'L1'),
        ('  ', 'R2', 'jmpb ', 'b', 'L2'),
        ('  ', '  ', 'gotob', ' ', 'L3'),
        ('L1', '  ', 'add  ', 'a', 'R1'),
        ('  ', '  ', 'tail ', ' ', 'R2'),
        ('  ', '  ', 'gotoa', ' ', 'L0'),
        ('L2', '  ', 'add  ', 'b', 'R1'),
        ('  ', '  ', 'tail ', ' ', 'R2'),
        ('  ', '  ', 'gotoa', ' ', 'L0'),

        # if R3 is not empty:
        #     R2 = R3
        #     clear R3
        #     append R2 to R1 again
        # else:
        #     it is done
        ("L3", "R3", "jmpb  ", 'a', "L4"),
        ("  ", "R3", "jmpb  ", 'b', "L4"),
        ("  ", "  ", "gotob ", ' ', "L5"),
        ("L4", "R2", "assign", ' ', "R3"),
        ("  ", "  ", "clr   ", ' ', "R3"),
        ("  ", "  ", "gotoa ", ' ', "L0"),

        # end of the program
        ("L5", "", "continue", '', ""),
        ]

    alphabet = "ab"

    # Each row is a test case. Append new inputs at the end of the list.
    lst_inputs = ["", "a", "b", "aa", "abab"]

    print("------ triple function ------ ")

    for inputs in lst_inputs:
        program = [human2machine(xx, alphabet) for xx in triple]
        registers = [inputs, "", ""]

        result = interpreter(program, registers, alphabet, verbose=verbose)

        print("inputs = '{}',".format(inputs),
              "return = '{}'".format(result))


if __name__ == "__main__":
    """
    Python version: 3.7
    Certain parts of the code cannot be run under python 2!!
    """
    verbose = False

    test_concatenate(verbose=verbose)
    test_reverse(verbose=verbose)
    test_triple(verbose=verbose)
