from test import Board, Builder, prettyBoard
from ai import minimax
import sys
sys.setrecursionlimit(10000)


y = Board(Builder()).createStandardBoard()
x = Board(Builder()).createStandardBoard()
#print(x.currentPlayer.getActivePieces())
prettyBoard(x.board)
for a in range(40):
    #print("\n","\n")
    x = y
    #print(x==y)
    depth = 3
    evaluate = minimax(x,depth)
    bestMove=evaluate.execute()
    print("best move",bestMove)
    print("loop number",a)
    #not passing 9 because king is in check and isnt getting rid of it, not generating any attack moves
    for i in range(len(x.currentPlayer.legalMoves)):
        list = x.currentPlayer.legalMoves[i]
        if (x.currentPlayer.legalMoves[i] == 0):
            pass
            # print(i, None)
        else:
#            print(x.currentPlayer.legalMoves[i])
            for j in range(len(x.currentPlayer.legalMoves[i])):
#                print(i,j)
                move = x.currentPlayer.legalMoves[i][j]
#                print("moves in list",x.currentPlayer.legalMoves[i][j],i,j)
                if (bestMove==move):
#                    print("index numbers",i,j)
                    y=x.currentPlayer.legalMoves[i][j].execute()
                    prettyBoard(y.board)
#print(y.currentPlayer.getOpponent(), len(y.currentPlayer.getActivePieces()))
#for i in range(len(y.currentPlayer.getOpponent().legalMoves)):
#    if (y.currentPlayer.getOpponent().legalMoves[i] == 0):
#        pass
        # print(i, None)
#    else:
#        print(y.currentPlayer.getOpponent().legalMoves[i])
#        for j in range(len(y.currentPlayer.legalMoves[i])):
#            pass#print(y.currentPlayer.legalMoves[i][j])

#print(y.board[21].getPiece())
#print(y.board[12].getPiece())