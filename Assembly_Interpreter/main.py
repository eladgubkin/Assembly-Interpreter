from stack import Stack
import sys


class AsmException(Exception):
    pass


def mov_function(params, stack, var_dict):
    """Defines the variable to the given value"""
    try:
        variable, value = params
    except ValueError:
        raise AsmException('SyntaxError: mov <variable>, <value>')

    if not variable.isdigit():
        if value in var_dict:
            var_dict[variable] = var_dict[value]
        else:
            var_dict[variable] = int(value)
    else:
        raise AsmException('SyntaxError: cannot assign a number as a variable')


def print_function(params, stack, var_dict):
    """Prints out the value of the given variable"""
    try:
        variable, = params
    except ValueError:
        raise AsmException('SyntaxError: print <variable>')

    if variable in var_dict:
        print var_dict[variable]
    else:
        print variable


def add_function(params, stack, var_dict):
    """Adds the given value to the variable"""
    try:
        variable, value = params
    except ValueError:
        raise AsmException('SyntaxError: add <variable>, <value>')

    if value.isdigit():
        var_dict[variable] += int(value)

    elif value in var_dict:
        var_dict[variable] += var_dict[value]


def sub_function(params, stack, var_dict):
    """Subtracts the given value from the variable"""
    try:
        variable, value = params
    except ValueError:
        raise AsmException('SyntaxError: sub <variable>, <value>')

    try:
        var_dict[variable] -= int(value)
    except KeyError:
        raise AsmException('SyntaxError: cannot subtract from a variable which that not exist')


def write_function(params, stack, var_dict):
    """Writes the value of the variable to the given file name"""
    try:
        variable, filename = params
    except ValueError:
        raise AsmException('SyntaxError: write <variable>, <filename>')

    try:
        with open(filename, 'w') as write_file:
            write_file.write(str(var_dict[variable]))
    except KeyError:
        raise AsmException("NameError: name '{}' is not defined".format(variable))


def load_function(params, stack, var_dict):
    """Loads the variable with the value inside the given file name"""
    try:
        variable, filename = params
    except ValueError:
        raise AsmException('SyntaxError: load <variable>, <filename>')

    with open(filename, 'r') as load_file:
        var_dict[variable] = int(load_file.read())


def mul_function(params, stack, var_dict):
    """Multiplies the variable by the given value"""
    try:
        variable, value = params
    except ValueError:
        raise AsmException('SyntaxError: mul <variable>, <value>')

    try:
        if variable and value in var_dict:
            var_dict[variable] *= var_dict[value]
        else:
            var_dict[variable] *= int(value)
    except KeyError:
        raise AsmException('SyntaxError: cannot multiply to a variable which that not exist')


def inc_function(params, stack, var_dict):
    """Increases the variable always by 1"""
    try:
        variable, = params
    except ValueError:
        raise AsmException('SyntaxError: inc <variable>')

    try:
        var_dict[variable] += 1
    except KeyError:
        raise AsmException('SyntaxError: cannot increase a variable that does not exist')


def dec_function(params, stack, var_dict):
    """Decreases the variable always by 1"""
    try:
        variable, = params
    except ValueError:
        raise AsmException('SyntaxError: dec <variable>')

    try:
        var_dict[variable] -= 1
    except KeyError:
        raise AsmException('SyntaxError: cannot decrease from a variable that does not exist')


def nop_function(params, stack, var_dict):
    """Simply does nothing!"""
    pass


def push_function(params, stack, var_dict):
    """Pushes the value to the stack"""
    try:
        variable, = params
    except ValueError:
        raise AsmException('SyntaxError: push <variable>/<value>')

    if variable in var_dict:
        stack.push(var_dict[variable])

    elif variable.isdigit():
        stack.push(int(variable))

    else:
        raise AsmException("NameError: name '{}' is not defined".format(variable))


def pop_function(params, stack, var_dict):
    """Pops the value from the stack"""
    try:
        variable, = params
    except ValueError:
        raise AsmException('SyntaxError: pop <variable>')

    if not variable.isdigit():
        var_dict[variable] = stack.pop()

    else:
        raise AsmException('SyntaxError: cannot pop to a number')


def jmp_function(params, stack, var_dict):
    try:
        value, = params
    except ValueError:
        raise AsmException('SyntaxError: jmp <value>')

    if value.isdigit():
        var_dict['eip'] = int(value) - 2
    elif value in var_dict:
        var_dict['eip'] = var_dict[value] - 2


def cmp_function(params, stack, var_dict):
    try:
        variable1, variable2 = params
    except ValueError:
        raise AsmException('SyntaxError: cmp <variable>, <variable>')

    if not variable2.isdigit():
        if var_dict[variable1] == var_dict[variable2]:
            var_dict['zf'] = 0
        else:
            var_dict['zf'] = 1
    else:
        if var_dict[variable1] == int(variable2):
            var_dict['zf'] = 0
        else:
            var_dict['zf'] = 1


def jz_function(params, stack, var_dict):
    try:
        value, = params
    except ValueError:
        raise AsmException('SyntaxError: jmp <value>')

    if var_dict['zf'] == 0:
        if value.isdigit():
            var_dict['eip'] = int(value) - 2
        elif value in var_dict:
            var_dict['eip'] = var_dict[value] - 2


def call_function(params, stack, var_dict):
    try:
        any_func, = params
    except ValueError:
        raise AsmException('SyntaxError: call <function>')

    var_dict['call_eip'] = var_dict['eip']

    if any_func in var_dict:
        var_dict['eip'] = var_dict[any_func] - 2


def ret_function(params, stack, var_dict):
    _ = params

    var_dict['eip'] = var_dict['call_eip']


def execute_command(line, var_dict, stack):
    if line == '':
        return
    if line[-1] == ':':
        return

    if line.find(' ') == -1:
        command = line
        params = []
    else:
        command = line[:line.find(' ')]
        params = line[line.find(' ')+1:].split(', ')

    commands = {
        'mov': mov_function,
        'print': print_function,
        'add': add_function,
        'sub': sub_function,
        'write': write_function,
        'load': load_function,
        'mul': mul_function,
        'inc': inc_function,
        'dec': dec_function,
        'nop': nop_function,
        'push': push_function,
        'pop': pop_function,
        'jmp': jmp_function,
        'cmp': cmp_function,
        'jz': jz_function,
        'call': call_function,
        'ret': ret_function,
    }

    try:
        func = commands[command]
        func(params, stack, var_dict)
    except KeyError:
        raise AsmException('SyntaxError: invalid command')


def main():
    var_dict = {'eip': 0}
    stack = Stack()

    filename = None
    try:
        _, filename = sys.argv
    except ValueError:
        pass

    if filename is not None:
        with open(filename, 'r') as input_file:
            lines = [x.strip() for x in input_file.readlines()]

            # Add labels to var_dict
            for line_number, line in enumerate(lines):
                if line == '':
                    continue
                if line[-1] == ':':
                    var_dict[line[:-1]] = line_number + 1

            try:
                # Run lines from the given .asm file
                while var_dict['eip'] < len(lines):
                    line = lines[var_dict['eip']]
                    execute_command(line, var_dict, stack)
                    var_dict['eip'] += 1
            except AsmException as e:
                print e.message

    else:
        print 'No file has been found'


if __name__ == '__main__':
    main()
