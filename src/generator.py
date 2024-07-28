import src.tokens as tkns

from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def generate(self, tokens) -> str:
        ...


class PythonGenerator(Generator):
    code_dict = {
        tkns.Pointer_Right: "pointer += {}\n",
        tkns.Pointer_Left: "pointer -= {}\n",
        tkns.Value_Increase: "memory[pointer] += {}\n",
        tkns.Value_Decrease: "memory[pointer] -= {}\n",
        tkns.While_Start: "while memory[pointer] > 0:\n",
        tkns.While_End: "",
        tkns.Char_Get: "memory[pointer] = ord(input()[0])\n",
        tkns.Char_Put: "print(chr(memory[pointer]), end='')\n",
    }

    def generate(self, tokens) -> str:
        loop_counter = 0
        code = "#!/usr/local/bin/python3\n\nmemory = [0] * 30000\npointer = 0\n\n"

        for token in tokens:
            if isinstance(token, tkns.While_End):
                loop_counter -= 1
                continue

            code += " " * 4 * loop_counter

            if isinstance(token, tkns.Repeatable_Token):
                code += self.code_dict[type(token)].format(token.times)  # type: ignore
            else:
                code += self.code_dict[type(token)]

            if isinstance(token, tkns.While_Start):
                loop_counter += 1

        return code


class RustGenerator(Generator):
    code_dict = {
        tkns.Pointer_Right: "pointer += {};\n",
        tkns.Pointer_Left: "pointer -= {};\n",
        tkns.Value_Increase: "memory[pointer] += {};\n",
        tkns.Value_Decrease: "memory[pointer] -= {};\n",
        tkns.While_Start: "while memory[pointer] > 0 {\n",
        tkns.While_End: "}\n",
        tkns.Char_Get: "{let mut var = String::new(); std::io::stdin().read_line(&mut var); memory[pointer] = var.chars().nth(0).unwrap() as u8}\n",
        tkns.Char_Put: 'print!("{}", memory[pointer] as char);\n'
    }

    def generate(self, tokens) -> str:
        indent_counter = 1
        code = "fn main() {\n    let mut memory = vec![0u8; 30000];\n    let mut pointer = 0usize;\n"

        for token in tokens:
            if isinstance(token, tkns.While_End):
                indent_counter -= 1

            code += " " * 4 * indent_counter

            if isinstance(token, tkns.Repeatable_Token):
                code += self.code_dict[type(token)].format(token.times)  # type: ignore
            else:
                code += self.code_dict[type(token)]

            if isinstance(token, tkns.While_Start):
                indent_counter += 1

        return code + "}"


def get_generator(language) -> Generator:
    match language:
        case "python":
            return PythonGenerator()
        case "rust":
            return RustGenerator()
        case _:
            raise Exception("Unknown language, accepts: rust, python")
