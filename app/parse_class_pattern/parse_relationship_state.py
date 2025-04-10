from abc import ABC, abstractmethod

INVALID = "Invalid multiplicity on relationship"


class MultiplicityValidator:
    def __init__(self, amount_str: str):
        self.amount_str = amount_str
        self.state = StartState()
        self.has_min_number = False
        self.titik_count = 0

    def validate(self):
        for i, char in enumerate(self.amount_str):
            self.state.handle(self, char, i)

        if not (self.has_min_number and self.titik_count == 2) or isinstance(
            self.state, DotState
        ):
            raise ValueError(INVALID)


class MultiplicityState(ABC):
    @abstractmethod
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        pass  # pragma: no cover


class StartState(MultiplicityState):
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        if char.isdigit():
            context.has_min_number = True
            context.state = MinimumNumberState()
        else:
            raise ValueError(INVALID)


class MinimumNumberState(MultiplicityState):
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        if char.isdigit():
            return
        elif char == ".":
            context.titik_count += 1
            context.state = DotState()
        else:
            raise ValueError(INVALID)


class DotState(MultiplicityState):
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        if char == ".":
            context.titik_count += 1
            return
        if char.isdigit():
            context.state = MaximumNumberState()
        elif char == "*" and index == len(context.amount_str) - 1:
            context.state = EndState()
        else:
            raise ValueError(INVALID)


class MaximumNumberState(MultiplicityState):
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        if char.isdigit():
            return
        else:
            raise ValueError(INVALID)


class EndState(MultiplicityState):
    def handle(self, context: MultiplicityValidator, char: str, index: int):
        return  # pragma: no cover
