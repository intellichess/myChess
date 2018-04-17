from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte
from mcts import monteCarloTreeSearch

x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
mcts = monteCarloTreeSearch(15, 3)

for i in range(20):
    x = mcts.findNextMove(x).execute()
    print("move count", i)
    prettyBoard(x.board)