#!/usr/local/bin/python3

from argparse import ArgumentParser
from pathlib import Path


from tokens import (
    Pointer_Right,
    Pointer_Left,
    Value_Increase,
    Value_Decrease,
    While_Start,
    While_End,
    Char_Get,
    Char_Put,
    Repeatable_Token,
)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--output", "-o", required=False)
    parser.add_argument("input")
    return parser.parse_args()


def load_file(filename):
    with open(filename, "r") as file:
        data = file.read().strip()
    return data


def tokenise(data):
    token_dict = {
        ">": Pointer_Right,
        "<": Pointer_Left,
        "+": Value_Increase,
        "-": Value_Decrease,
        "[": While_Start,
        "]": While_End,
        ",": Char_Get,
        ".": Char_Put,
    }

    tokens = []

    for char in data:
        if char not in token_dict:
            continue

        if not tokens:
            tokens.append(token_dict[char]())
            continue

        if isinstance(tokens[-1], token_dict[char]) and isinstance(tokens[-1], Repeatable_Token):
            tokens[-1].add()
            continue

        tokens.append(token_dict[char]())

    return tokens


def generate(tokens):
    code_dict = {
        Pointer_Right: "pointer += {}\n",
        Pointer_Left: "pointer -= {}\n",
        Value_Increase: "memory[pointer] += {}\n",
        Value_Decrease: "memory[pointer] -= {}\n",
        While_Start: "while memory[pointer] > 0:\n",
        While_End: "",
        Char_Get: "memory[pointer] = ord(input()[0])\n",
        Char_Put: "print(chr(memory[pointer]), end='')\n",
    }
    loop_counter = 0
    code = "#!/usr/local/bin/python3\n\nmemory = [0] * 30000\npointer = 0\n\n"

    for token in tokens:
        if isinstance(token, While_End):
            loop_counter -= 1
            continue

        code += "    " * loop_counter

        if isinstance(token, Repeatable_Token):
            code += code_dict[type(token)].format(token.times)  # type: ignore
        else:
            code += code_dict[type(token)]

        if isinstance(token, While_Start):
            loop_counter += 1

    return code


def save_file(code, infile, outfile):
    if not outfile:
        outfile = Path(infile).with_suffix("")

    with open(outfile, "w") as file:
        file.write(code)


def main():
    args = get_args()
    data = load_file(filename=args.input)
    tokens = tokenise(data)
    code = generate(tokens)
    save_file(code=code, infile=args.input, outfile=args.output)


if __name__ == "__main__":
    main()
