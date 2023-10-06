#!/usr/local/bin/python3

from argparse import ArgumentParser
from pathlib import Path
from src.tokeniser import Tokeniser
from src.generator import get_generator


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--output", "-o")
    parser.add_argument("--language", "-l", default="python", choices=["python", "rust"])
    parser.add_argument("input")
    return parser.parse_args()


def load_file(filename):
    with open(filename, "r") as file:
        data = file.read().strip()
    return data


def save_file(code, infile, outfile, language):
    suffixes = {
        "python": ".py",
        "rust": ".rs",
        "c++": ".cpp",
        "c": ".c",
    }

    if not outfile:
        outfile = Path(infile).stem + suffixes[language]

    if not Path(outfile).suffix:
        outfile += suffixes[language]

    with open(f"target/{outfile}", "w") as file:
        file.write(code)


def main():
    args = get_args()
    data = load_file(filename=args.input)

    tokeniser = Tokeniser()
    tokens = tokeniser.tokenise(data)

    generator = get_generator(language=args.language)
    code = generator.generate(tokens)

    save_file(code=code, infile=args.input, outfile=args.output, language=args.language)


if __name__ == "__main__":
    main()
