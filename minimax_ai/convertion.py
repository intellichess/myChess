#from test import Board, Builder
#from ai import minimax
toByteBoard = ["0|7", "1|7", "2|7", "3|7", "4|7", "5|7", "6|7", "7|7",
               "0|6", "1|6", "2|6", "3|6", "4|6", "5|6", "6|6", "7|6",
               "0|5", "1|5", "2|5", "3|5", "4|5", "5|5", "6|5", "7|5",
               "0|4", "1|4", "2|4", "3|4", "4|4", "5|4", "6|4", "7|4",
               "0|3", "1|3", "2|3", "3|3", "4|3", "5|3", "6|3", "7|3",
               "0|2", "1|2", "2|2", "3|2", "4|2", "5|2", "6|2", "7|2",
               "0|1", "1|1", "2|1", "3|1", "4|1", "5|1", "6|1", "7|1",
               "0|0", "1|0", "2|0", "3|0", "4|0", "5|0", "6|0", "7|0"]

def moveToByte(move):
    startPos = move.movedPiece.piecePosition
    endPos = move.destinationCoordinate
    startStr = toByteBoard[startPos]
    endStr = toByteBoard[endPos]
    moveStr = startStr+"|"+endStr
    byteStr = bytes(moveStr, "ascii")
    return byteStr

def stringParser(string):
    tilesInts = [0,0]
    stringPieces = string.split("|")
    tilesInts[0] = tileGet(int(stringPieces[1]), int(stringPieces[2]))
    tilesInts[1] = tileGet(int(stringPieces[3]), int(stringPieces[4]))
    return tilesInts

def tileGet(x, y):
    row = 7-y
    col = x
    return 8*row+col

def moveGet(startTile, endTile, board):
    for i in range(len(board.currentPlayer.legalMoves)):
        foundMove = board.currentPlayer.legalMoves[i]
        if (foundMove.movedPiece.piecePosition == startTile and foundMove.destinationCoordinate == endTile):
            return foundMove