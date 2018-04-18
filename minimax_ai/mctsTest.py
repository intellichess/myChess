whiteWins = -1
blackWins = 1
stalemate = 2
inProgress = 0
from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte
from mcts import monteCarloTreeSearch

x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
mcts = monteCarloTreeSearch(22, 3)

for i in range(20):
    print("current player", x.currentPlayer.getAlliance(), x.currentPlayer.getAllianceName())
    x = mcts.findNextMove(x).execute()
    print("move count", i)
    prettyBoard(x.board)
    print("----------------------------------")