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

            code += "    " * loop_counter

            if isinstance(token, tkns.Repeatable_Token):
                code += self.code_dict[type(token)].format(token.times)  # type: ignore
            else:
                code += self.code_dict[type(token)]

            if isinstance(token, tkns.While_Start):
                loop_counter += 1

        return code


class RustGenerator(Generator):
    """IN PROGRESS"""

    code_dict = {
        tkns.Pointer_Right: "pointer += {}\n",
        tkns.Pointer_Left: "pointer -= {}\n",
        tkns.Value_Increase: "memory[pointer] += {}\n",
    }


def get_generator(language) -> Generator:
    match language:
        case "python":
            return PythonGenerator()
        case _:
            raise Exception("Unknown language, accepts: rust, python, c++, c")
