from test import Board, Builder, prettyBoard
from ai import minimax
import sys
depth = 2
sys.setrecursionlimit(10000)


x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
x =x.currentPlayer.legalMoves[5][1].execute()
prettyBoard(x.board)
x =x.currentPlayer.legalMoves[12][0].execute()
prettyBoard(x.board)
x =x.currentPlayer.legalMoves[6][1].execute()
prettyBoard(x.board)
x =x.currentPlayer.legalMoves[3][3].execute()
prettyBoard(x.board)
evaluate = minimax(x, depth)
bestMove = evaluate.execute()
print("best move", bestMove)

for i in range(len(x.currentPlayer.legalMoves)):
    if (x.currentPlayer.legalMoves[i]==0):
        pass
        #print(i, None)
    else:
        print(x.currentPlayer.legalMoves[i])
        for j in range(len(x.currentPlayer.legalMoves[i])):
            print(i,j,x.currentPlayer.legalMoves[i][j].movedPiece.pieceType,x.currentPlayer.legalMoves[i][j].destinationCoordinate,x.currentPlayer.legalMoves[i][j].movedPiece.piecePosition)


#print("checkboard king in check but not mate", x.currentPlayer.isInCheck, x.currentPlayer.isCheckmate())
#print("mateboard king in check and mate", y.currentPlayer.isInCheck, y.currentPlayer.isCheckmate())

#print(x.currentPlayer.legalMoves[0][3])
#x =x.currentPlayer.legalMoves[0][3].execute()

#print("checkboard king not in check or mate", x.currentPlayer.isInCheck, x.currentPlayer.isCheckmate())

#print(z.blackStandardLegalMoves[1][0],'\n',z.whiteStandardLegalMoves[1][0],'\n',z.currentPlayer.legalMoves[1][0])

#z = z.currentPlayer.legalMoves[1][0].execute()


#z = z.currentPlayer.legalMoves[1][0].execute()


#print(z.whitePieces,'\n',z.blackPieces)

