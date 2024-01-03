# E.g: python script.py "0,1,3,6" "-,*,/"

from four_eq_ten import State, Game
from simpleai.search import breadth_first, depth_first
import sys

assert len(sys.argv) == 3, f"Invalid number of arguments {len(sys.argv)}"
numbers = [int(number) for number in sys.argv[1].split(",")]
operators = sys.argv[2].split(",")

print(
    f"Solving the 4=10 puzzle with numbers `{numbers}` and allowed operators `{operators}`"
)

initial_state = State(numbers, [operators[0], operators[0], operators[0]], None)
game = Game(initial_state, operators)

result = breadth_first(game)

print("state: ", result.state)
print("path: ", [(str(state), str(action)) for (state, action) in result.path()])
