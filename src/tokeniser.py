import src.tokens as tkns

"""
    not really sure why I made this a class
    it doesn't really make sense to have multiple instances of it but i can't be bothered to change it for the python implementation

    when i write a rust version of the transpiler, i'd want a more idiomatic way of doing this
"""


class Tokeniser:
    token_dict = {
        ">": tkns.Pointer_Right,
        "<": tkns.Pointer_Left,
        "+": tkns.Value_Increase,
        "-": tkns.Value_Decrease,
        "[": tkns.While_Start,
        "]": tkns.While_End,
        ",": tkns.Char_Get,
        ".": tkns.Char_Put,
    }

    def tokenise(self, src: str) -> list[tkns.Token]:
        tokens = []

        for char in src:
            if char not in self.token_dict:
                continue

            if not tokens:
                tokens.append(self.token_dict[char]())
                continue

            if isinstance(tokens[-1], self.token_dict[char]) and isinstance(tokens[-1], tkns.Repeatable_Token):
                tokens[-1].add()
                continue

            tokens.append(self.token_dict[char]())

        return tokens
