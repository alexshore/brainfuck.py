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
