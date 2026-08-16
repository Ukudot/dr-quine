import sys
import re

class Quinizer:
    def __init__(self, source_file):
        self._source_file = source_file
        self._source_program = None
        self._quinezed = None

    def _dump_src_program(self, decoder: str = "utf-8") -> None:
        with open(self._source_file, "rb") as file:
            self._source_program = file.read().decode(decoder)

    def _load_qnz_program(self, encoder: str = "utf-8", mode: str = "") -> None:
        if self._quinized is None:
            print("The program isn't quinized yet")
            return
        with open(self._source_file.split('.c')[0] + f"{'_' + mode if mode != '' else ''}_quine.c", "wb") as file:
            file.write(self._quinized.encode(encoder))

    def _escape_char_read(self, initial_set: set = {}) -> list:
        if self._source_program is None:
            print("The program isn't loaded yet")
            return
        # Initialize escape_chars with new line, double quotes and tab
        escape_chars = initial_set

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
        self._mode = "standard"

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
        esc_chars = self._escape_char_read({9, 10, 34})

        # Creates a source program version with the quine function injected.
        # This version will be used as 'Documentation' to recreate the program itself
        program_recipe = self._injector(esc_chars)

        # Replaces each escapable characters with its ASCII code
        replica = self._escape_char_replace(program_recipe, esc_chars)

        # Injects the program 'Documentation' in the quine function
        self._quinized = self._injector(esc_chars, replica)
        self._load_qnz_program(mode=self._mode)


class MacroQuinizer(Quinizer):
    def __init__(self, source_file):
        super().__init__(source_file)
        self._includes = []
        self._mode = "macro"

    def _extract_includes(self) -> None:
        regex = "#include.*"

        p = re.compile(regex)
        self._includes = p.findall(self._source_program)
        self._source_program = re.sub(regex, '',self._source_program)

    def _injector(self, esc_chars: list, replica: str = None) -> str:
        # Checks if the source program has been dumped
        if self._source_program is None:
            print("The program isn't loaded yet")
            return

        # Checks the includes and append the one needed by quine
        if "#include <stdio.h>" not in self._includes:
            self._includes.append("#include <stdio.h>")

        # Creates the list of variables used to escape characters
        quine_variables_str = [f"char var{char} = {char};" for char in esc_chars]
        quine_variables = [f"var{char}" for char in esc_chars]

        # Defines the SELF macro, it contains the 'Documentation' of the program
        if replica is None:
            self_macro = f"#define SELF \"%{len(esc_chars) + 1}$s\""
        else:
            self_macro =  f"#define SELF \"{replica}\""

        # Defines the quine macro
        quine_function = "\n#define quine(str) " + ''.join(quine_variables_str) + f"FILE *stream = fopen(\"{self._source_file.split('.c')[0]}_kid.c\",\"w\"); fprintf(stream, str, " + ', '.join(quine_variables) + ", str); fclose(stream)"

        # Injects the quine macro in the main function
        quine_function_call = "\nint main() {\nquine(SELF);\n"
        splitted_source_program = self._source_program.split('int main() {\n')
        injected_source_program = splitted_source_program[0] + quine_function_call + splitted_source_program[1]

        # Linearizes the program
        one_line_source_program = injected_source_program.replace('\n', '')

        # Creates the macro version of the program
        macro_source_program = '\n'.join(self._includes) + f"\n#define MAIN {one_line_source_program}\n{quine_function}\n{self_macro}\n\n/*\nThis MAIN macro runs the program\n*/\nMAIN\n"
        return macro_source_program

    def quinize(self) -> None:
        # Dumps the source program into memory
        self._dump_src_program()

        # Remove from source_program the tabs
        self._source_program = self._source_program.replace('\t', '')

        # Extract from source program the includes instructions
        self._extract_includes()

        # Reads the source program and creates the list of escapable characters found in the program
        esc_chars = self._escape_char_read({10, 34})

        # Creates a source program version with the quine function injected.
        # This version will be used as 'Documentation' to recreate the program itself
        program_recipe = self._injector(esc_chars)

        # Replaces each escapable characters with its ASCII code
        replica = self._escape_char_replace(program_recipe, esc_chars)

        # Injects the program 'Documentation' in the quine function
        self._quinized = self._injector(esc_chars, replica)
        self._load_qnz_program(mode=self._mode)


class QuinizerFactory:
    def __init__(self, source_file):
        self._source_file = source_file

    def quinizer(self, mode):
        match mode.lower():
            case "macro":
                return MacroQuinizer(self._source_file);
            case "standard":
                return StandardQuinizer(self._source_file);
            case _:
                print("Mode not found, fallback to Standard")
                return StandardQuinizer(self._source_file);


if __name__ == '__main__':
    filepath = sys.argv[1]
    quinized = ""

    QuinizerFactory(filepath).quinizer("standard").quinize()
    QuinizerFactory(filepath).quinizer("macro").quinize()
