from test import Board, Builder
from ai import minimax
import sys
sys.setrecursionlimit(10000)
depth = 2

x = Board(Builder()).createStandardBoard()
#evaluate = minimax(x,depth)
#print("best move",evaluate.execute(x, depth))
print("currentPlayer before move",x.currentPlayer)
#execute creates new board class, needs to be saved

print("white moves 1",x.whiteStandardLegalMoves[3][1])
x = x.currentPlayer.legalMoves[3][1].execute()
print("currentPlayer after move 1",x.currentPlayer)

print("black moves 2",x.blackStandardLegalMoves[9][1])
x = x.currentPlayer.legalMoves[9][1].execute()
print("currentPlayer after move 2",x.currentPlayer)

print("white moves 3",x.whiteStandardLegalMoves[0][0])
x = x.currentPlayer.legalMoves[0][0].execute()
print("currentPlayer after move 3",x.currentPlayer)

print("black moves 4",x.blackStandardLegalMoves[11][1])
x = x.currentPlayer.legalMoves[11][1].execute()
print("currentPlayer after move 4",x.currentPlayer)
evaluate = minimax(x,depth)
print("best move",evaluate.execute())

#print("white moves available")
#for i in range(len(x.whiteStandardLegalMoves)):
#    if (x.whiteStandardLegalMoves[i]==0):
#        print(i, None)
#    else:
#        for j in range(len(x.whiteStandardLegalMoves[i])):
#            print(i,j,x.whiteStandardLegalMoves[i][j].movedPiece.pieceType,x.whiteStandardLegalMoves[i][j].destinationCoordinate)
#print("black moves available")
#for i in range(len(x.blackStandardLegalMoves)):
#    if (x.blackStandardLegalMoves[i]==0):
#        print(i, None)
#    else:
#        for j in range(len(x.blackStandardLegalMoves[i])):
#            print(i,j,x.blackStandardLegalMoves[i][j].movedPiece.pieceType,x.blackStandardLegalMoves[i][j].destinationCoordinate)

print("white moves 5",x.whiteStandardLegalMoves[0][1])
x = x.currentPlayer.legalMoves[0][1].execute()
print("currentPlayer after move 5",x.currentPlayer)

print("black moves 6",x.blackStandardLegalMoves[11][1])
x = x.currentPlayer.legalMoves[11][1].execute()
print("currentPlayer after move 6",x.currentPlayer)

print("white moves 7",x.whiteStandardLegalMoves[14][0])
x = x.currentPlayer.legalMoves[14][0].execute()
print("currentPlayer after move 7",x.currentPlayer)

print("black moves 8",x.blackStandardLegalMoves[5][4])
x = x.currentPlayer.legalMoves[5][4].execute()
print("currentPlayer after move 8",x.currentPlayer)

print("white moves 9",x.whiteStandardLegalMoves[1][3])
x = x.currentPlayer.legalMoves[1][3].execute()
print("currentPlayer after move 9",x.currentPlayer)

print("black moves 10",x.blackStandardLegalMoves[5][2])
x = x.currentPlayer.legalMoves[5][2].execute()
print("currentPlayer after move 10",x.currentPlayer)

print("white moves 11",x.whiteStandardLegalMoves[4][0])
x = x.currentPlayer.legalMoves[4][0].execute()
print("currentPlayer after move 11",x.currentPlayer)

print("black moves 12",x.currentPlayer.legalMoves[15][0])
x = x.currentPlayer.legalMoves[15][0].execute()
print("currentPlayer after move 12",x.currentPlayer)


#for i in range(len(x.currentPlayer.legalMoves)):
#    if (x.currentPlayer.legalMoves[i]==0):
#        print(i, None)
#    else:
#        print(x.currentPlayer.legalMoves[i])
#        for j in range(len(x.currentPlayer.legalMoves[i])):
#            print(i,j,x.currentPlayer.legalMoves[i][j].movedPiece.pieceType,x.currentPlayer.legalMoves[i][j].destinationCoordinate)



#print((len(x.whitePieces)))
#print((len(x.blackPieces)))
