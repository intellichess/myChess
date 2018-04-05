from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte
from ai import minimax
import sys

def moveExecute(move, board1, board2):
    for i in range(len(board1.currentPlayer.legalMoves)):
        if (board1.currentPlayer.legalMoves[i] == 0):
            pass
        else:
            for j in range(len(x.currentPlayer.legalMoves[i])):
                foundMove = board1.currentPlayer.legalMoves[i][j]
                if (move == foundMove):
                    board2 = board1.currentPlayer.legalMoves[i][j].execute()
                    prettyBoard(board2.board)
    return board2


sys.setrecursionlimit(10000)
a = 0

y = Board(Builder()).createStandardBoard()
x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
for a in range(10):
#while (y.currentPlayer.isCheckmate()==False):
#    a=a+1
    x = y
    depth = 3
    evaluate = minimax(x,depth)
    bestMove=evaluate.execute()
    #byte conversion here
    moveByte = moveToByte(bestMove)
    print("string in bytes",moveByte)
#   moveToString(bestMove, y.currentPlayer))
    print("best move",bestMove)
    print("loop number",a)
    y = moveExecute(bestMove, x, y)