from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte
from ai import minimax
from mcts import monteCarloTreeSearch
import sys

def moveExecute(move, board):
    for i in range(len(board.currentPlayer.legalMoves)):
        if (board.currentPlayer.legalMoves[i] == 0):
            pass
        else:
            for j in range(len(board.currentPlayer.legalMoves[i])):
                foundMove = board.currentPlayer.legalMoves[i][j]
                if (move == foundMove):
                    board = board.currentPlayer.legalMoves[i][j].execute()
                    prettyBoard(board.board)
                    return board


sys.setrecursionlimit(10000)
a = 0

x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
for a in range(20):
#while (y.currentPlayer.isCheckmate()==False):
#    a=a+1
    depth = 3
    evaluate = minimax(x,depth)
    bestMove=evaluate.execute()
    #byte conversion here
    moveByte = moveToByte(bestMove)
    print("string in bytes",moveByte)
#   moveToString(bestMove, y.currentPlayer))
    print("best move",bestMove)
    print("loop number",a)
    x = bestMove.execute()
    prettyBoard(x.board)
    #x = moveExecute(bestMove, x)