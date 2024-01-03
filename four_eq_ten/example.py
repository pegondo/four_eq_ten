from four_eq_ten import State, Game
from simpleai.search import breadth_first, depth_first


initial_state = State([0, 1, 3, 6], ["-", "-", "-"], None)
game = Game(initial_state, ["-", "*", "/"])

result = breadth_first(game)
print("state: ", result.state)
print(len(result.path()))
print("path: ", [(str(state), str(action)) for (state, action) in result.path()])
