from four_eq_ten import State, Game
from simpleai.search import breadth_first, astar, depth_first


initial_state = State([0, 1, 3, 6], ["-", "-", "-"], None)
game = Game(initial_state, ["-", "*", "/"])

result = breadth_first(game)
print("state: ", result.state)
print("path: ", [str(path[0]) for path in result.path()])
