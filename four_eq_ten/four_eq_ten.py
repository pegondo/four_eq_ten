from enum import Enum
from simpleai.search import SearchProblem
from itertools import permutations, product


VALID_OPERATORS = ["+", "-", "*", "/"]
VALID_BRACKETS = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]]

VALID_NUMBERS_SWAP = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]


class ActionType(Enum):
    SWAP_NUMBERS = 1
    CHANGE_OPERATOR = 2
    ADD_BRACKETS = 3


class Action:
    def __init__(self, action: ActionType, index, target=None):
        self.action = action
        self.index = index
        self.target = target

    def __str__(self):
        if self.action == ActionType.SWAP_NUMBERS:
            return f"Swap number in pos {self.index[0]} to pos {self.index[1]}"
        if self.action == ActionType.CHANGE_OPERATOR:
            return f"Change operator in pos {self.index} to {self.target}"
        if self.action == ActionType.ADD_BRACKETS:
            return f"Add brackets in {self.index}"
        return "Invalid action"


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

    def __get_operator(self, index):
        return self.operators[index]

    def __get_brackets(self):
        return self.brackets

    def calculate(self):
        str = self.__format()
        try:
            return eval(str)
        except:
            return None

    def actions(self, allowed_operators):
        actions = []

        # Swap numbers.
        for swaps in VALID_NUMBERS_SWAP:
            action = Action(ActionType.SWAP_NUMBERS, index=swaps)
            actions.append(action)
        # Change operator.
        for op_index in range(3):
            for op in allowed_operators:
                if self.__get_operator(op_index) != op:
                    action = Action(
                        ActionType.CHANGE_OPERATOR, index=op_index, target=op
                    )
                    actions.append(action)
        # Change bracket.
        current_brackets = self.__get_brackets()
        for bracket in VALID_BRACKETS:
            if (None if current_brackets is None else list(current_brackets)) != list(
                bracket
            ):
                action = Action(ActionType.ADD_BRACKETS, index=bracket)
                actions.append(action)
        if current_brackets is not None:
            action = Action(ActionType.ADD_BRACKETS, index=None)
        actions.append(action)

        return actions

    def result(self, action: Action):
        numbers = self.numbers.copy()
        operators = self.operators.copy()
        brackets = None if self.brackets is None else self.brackets.copy()

        # Swap numbers.
        if action.action == ActionType.SWAP_NUMBERS:
            numbers[action.index[0]], numbers[action.index[1]] = (
                numbers[action.index[1]],
                numbers[action.index[0]],
            )
            return State(numbers, operators, brackets)
        # Change operator.
        if action.action == ActionType.CHANGE_OPERATOR:
            operators[action.index] = action.target
            return State(numbers, operators, brackets)
        # Change bracket.
        if action.action == ActionType.ADD_BRACKETS:
            brackets = action.index
            return State(numbers, operators, brackets)

        return None


class Game(SearchProblem):
    def __init__(self, initial_state, allowed_operators=VALID_OPERATORS):
        super().__init__(initial_state)
        self.allowed_operators = allowed_operators

    def actions(self, state: State):
        return state.actions(self.allowed_operators)

    def result(self, state: State, action: Action):
        return state.result(action)

    def is_goal(self, state: State):
        return state.calculate() == 10
