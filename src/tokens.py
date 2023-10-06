"""
    this would be wayyyyyyy better as an Enum instead but I'm not too sure how to nicely do Enums
    in python with individual attributes unlike in rust where enums can just natively take them

    theres probably a way to do it with a third party version of enums but this is just the first
    draft of the program, hopefully will be a few more iterations
"""


class Token:
    ...


class Repeatable_Token(Token):
    def __init__(self) -> None:
        self.times = 1

    def add(self) -> None:
        self.times += 1


class Pointer_Right(Repeatable_Token):
    ...


class Pointer_Left(Repeatable_Token):
    ...


class Value_Increase(Repeatable_Token):
    ...


class Value_Decrease(Repeatable_Token):
    ...


class While_Start(Token):
    ...


class While_End(Token):
    ...


class Char_Get(Token):
    ...


class Char_Put(Token):
    ...
