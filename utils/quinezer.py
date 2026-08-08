import sys


def escape_char_reader(source_program: str) -> list:
    # Initialize escape_chars with new line, double quotes and tab
    escape_chars = {10, 9, 34}

    # Cycle through each char and insert into escape chars if is an escapable character
    for char in source_program:
        if ord(char) <= 32 and ord(char):
            escape_chars.add(ord(char))
    return list(escape_chars)
        

def injector(source_program: str, esc_chars: list, replica: str = None) -> str:
    if "#include <stdio.h>" not in source_program:
        source_program = "#include <stdio.h>\n\n" + source_program

    quine_variables_str = [f"char var{char} = {char};" for char in esc_chars]
    quine_variables = [f"var{char}" for char in esc_chars]

    if replica is None:
        quine_function = "\nvoid quine() {\n\t" + '\n\t'.join(quine_variables_str) + f"\n\tchar *self = \"%{len(esc_chars) + 1}$s\";\n\n\tprintf(self, " + ', '.join(quine_variables) + ", self);\n}\n"
    else:
        quine_function = "\nvoid quine() {\n\t" + '\n\t'.join(quine_variables_str) + f"\n\tchar *self = \"{replica}\";\n\n\tprintf(self, " + ', '.join(quine_variables) + ", self);\n}\n"

    quine_function_call = "\nint main() {\n\tquine();\n"
    splitted_source_program = source_program.split('int main() {\n')
    injected_source_program = splitted_source_program[0] + quine_function + quine_function_call + splitted_source_program[1]
    return injected_source_program


def quinizer(injected_source_program: str, esc_chars: list) -> str:
    replica = ""
    for char in injected_source_program:
        if ord(char) in esc_chars:
            replica = replica + f"%{esc_chars.index(ord(char)) + 1}$c"
        else:
            replica = replica + char
    return replica
        

if __name__ == '__main__':
    filepath = sys.argv[1]
    quinized = ""

    with open(filepath, 'rb') as file:
        source_program = file.read().decode("utf-8")
        esc_chars = escape_char_reader(source_program)
        injected_source_program = injector(source_program, esc_chars)
        replica = quinizer(injected_source_program, esc_chars)
        quinized = injector(source_program, esc_chars, replica)

    with open(filepath.split('.c')[0] + ".quine.c", "wb") as file:
        file.write(quinized.encode("utf-8"))
