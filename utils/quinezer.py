import sys

class Quinizer:
    def __init__(self, source_file):
        self._source_file = source_file
        self._source_program = None
        self._quinezed = None

    def _dump_src_program(self, decoder: str = "utf-8") -> None:
        with open(self._source_file, "rb") as file:
            self._source_program = file.read().decode(decoder)

    def _load_qnz_program(self, encoder: str = "utf-8") -> None:
        if self._quinized is None:
            print("The program isn't quinized yet")
            return
        with open(self._source_file.split('.c')[0] + "_quine.c", "wb") as file:
            file.write(self._quinized.encode(encoder))

    def _escape_char_read(self) -> list:
        if self._source_program is None:
            print("The program isn't loaded yet")
            return
        # Initialize escape_chars with new line, double quotes and tab
        escape_chars = {10, 9, 34}

        # Cycle through each char and insert into escape chars if is an escapable character
        for char in self._source_program:
            if ord(char) <= 32 and ord(char):
                escape_chars.add(ord(char))
        return list(escape_chars)

    def _escape_char_replace(self, program_recipe: str, esc_chars: list) -> str:
        replica = ""
        for char in program_recipe:
            if ord(char) in esc_chars:
                replica = replica + f"%{esc_chars.index(ord(char)) + 1}$c"
            else:
                replica = replica + char
        return replica

    def quinize(self) -> None:
        print("This class is 'abstract' and doesn't implement this method")
        return


class StandardQuinizer(Quinizer):
    def __init__(self, source_file):
        super().__init__(source_file)

    def _injector(self, esc_chars: list, replica: str = None) -> str:
        if self._source_program is None:
            print("The program isn't loaded yet")
            return
        if "#include <stdio.h>" not in self._source_program:
            self._source_program = "#include <stdio.h>\n\n" + self._source_program

        quine_variables_str = [f"char var{char} = {char};" for char in esc_chars]
        quine_variables = [f"var{char}" for char in esc_chars]

        if replica is None:
            quine_function = "\nvoid quine() {\n\t" + '\n\t'.join(quine_variables_str) + f"\n\tchar *self = \"%{len(esc_chars) + 1}$s\";\n\n\tprintf(self, " + ', '.join(quine_variables) + ", self);\n}\n"
        else:
            quine_function = "\nvoid quine() {\n\t" + '\n\t'.join(quine_variables_str) + f"\n\tchar *self = \"{replica}\";\n\n\tprintf(self, " + ', '.join(quine_variables) + ", self);\n}\n"

        quine_function_call = "\nint main() {\n\tquine();\n"
        splitted_source_program = self._source_program.split('int main() {\n')
        injected_source_program = splitted_source_program[0] + quine_function + quine_function_call + splitted_source_program[1]
        return injected_source_program

    def quinize(self) -> None:
        # Dumps the source program into memory
        self._dump_src_program()

        # Reads the source program and creates the list of escapable characters found in the program
        esc_chars = self._escape_char_read()

        # Creates a source program version with the quine function injected.
        # This version will be used as 'Documentation' to recreate the program itself
        program_recipe = self._injector(esc_chars)

        # Replaces each escapable characters with its ASCII code
        replica = self._escape_char_replace(program_recipe, esc_chars)

        # Injects the program 'Documentation' in the quine function
        self._quinized = self._injector(esc_chars, replica)
        self._load_qnz_program()


class QuinizerFactory:
    def __init__(self, source_file):
        self._source_file = source_file

    def quinizer(self, mode):
        match mode.lower():
            case "macro":
                return None;
            case "standard":
                return StandardQuinizer(self._source_file);
            case _:
                print("Mode not found, fallback to Standard")
                return StandardQuinizer(self._source_file);


if __name__ == '__main__':
    filepath = sys.argv[1]
    quinized = ""

    QuinizerFactory(filepath).quinizer("standard").quinize()

#    with open(filepath, 'rb') as file:
#        source_program = file.read().decode("utf-8")
#        esc_chars = escape_char_reader(source_program)
#        injected_source_program = injector(source_program, esc_chars)
#        replica = quinizer(injected_source_program, esc_chars)
#        quinized = injector(source_program, esc_chars, replica)
#
#    with open(filepath.split('.c')[0] + ".quine.c", "wb") as file:
#        file.write(quinized.encode("utf-8"))
