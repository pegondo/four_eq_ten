from simpleai.search import SearchProblem
from itertools import permutations, product


VALID_OPERATORS = ["+", "-", "*", "/"]
VALID_BRACKETS = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]]


class State:
    def __init__(self, numbers, operators, brackets=None):
        assert len(numbers) == 4, "There must be four numbers"
        assert len(operators) == 3, "There must be three operators"
        for operator in operators:
            assert operator in VALID_OPERATORS, f"Invalid operator `{operator}`"
        assert (
            brackets is None or brackets in VALID_BRACKETS
        ), f"Invalid brackets `{brackets}`"

        self.numbers = list(numbers)
        self.operators = list(operators)
        self.brackets = None if brackets is None else list(brackets)

    def __eq__(self, __value) -> bool:
        return (
            isinstance(__value, State)
            and self.numbers == __value.numbers
            and self.operators == __value.operators
            and self.brackets == __value.brackets
        )

    def __hash__(self):
        return hash(
            (
                frozenset(self.numbers),
                frozenset(self.operators),
                None if self.brackets is None else frozenset(self.brackets),
            )
        )

    def __str__(self):
        return self.__format()

    def __format(self):
        res = f"{self.numbers[0]}{self.operators[0]}{self.numbers[1]}{self.operators[1]}{self.numbers[2]}{self.operators[2]}{self.numbers[3]}"
        if self.brackets is None:
            return res
        first = self.brackets[0] * 2
        last = self.brackets[1] * 2 + 1
        res = res[:first] + "(" + res[first:last] + ")" + res[last:]
        return res

    def calculate(self):
        str = self.__format()
        return eval(str)

    def actions(self, allowed_operators):
        numbers_combinations = list(permutations(self.numbers))
        operators_combinations = list(product(allowed_operators, repeat=3))
        brackets_combinations = VALID_BRACKETS + [None]

        actions = []
        for numbers in numbers_combinations:
            for operators in operators_combinations:
                for brackets in brackets_combinations:
                    state = State(numbers, operators, brackets)
                    actions.append(state)
        actions.remove(self)  # Remove this same state.
        return actions


class Game(SearchProblem):
    def __init__(self, initial_state, allowed_operators=VALID_OPERATORS):
        super().__init__(initial_state)
        self.allowed_operators = allowed_operators

    def actions(self, state: State):
        return state.actions(self.allowed_operators)

    def result(self, state, action):
        # TODO: FIX THIS!!
        # The result is the action itself.
        # The actions should list what operations can be performed, and the result should perform them.
        # E.g: (state: 1+2+3, action: 'change first operation to `-`) -> 1-2+3
        return action

    def is_goal(self, state: State):
        return state.calculate() == 10
