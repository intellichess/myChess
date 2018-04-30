whiteWins = -1
blackWins = 1
stalemate = 2
inProgress = 0
from test import Board, Builder, prettyBoard, moveToString
from testEdit import createPGNString, addToPGN
from convertion import moveToByte
from mcts import monteCarloTreeSearch

x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
mcts = monteCarloTreeSearch(22, 3)
count = 0
string = ""

for i in range(20):
    print("current player", x.currentPlayer.getAlliance(), x.currentPlayer.getAllianceName())
    #move = mcts.findNextMove(x)
    #print("move in algebraic notation",moveAlgebra)
    x = mcts.findNextMove(x).execute()
    move = x.transitionMove
    #print("alliance",move.board.currentPlayer.getAlliance())
    moveAlgebra = moveToString(move, move.board.currentPlayer)
    print("algebraic move", moveAlgebra)
    count += 1
    print("move count", i)
    prettyBoard(x.board)
    print("----------------------------------")