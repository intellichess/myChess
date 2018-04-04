toByteBoard = ["07", "17", "27", "37", "47", "57", "67", "77",
               "06", "16", "26", "36", "46", "56", "66", "76",
               "05", "15", "25", "35", "45", "55", "65", "75",
               "04", "14", "24", "34", "44", "54", "64", "74",
               "03", "13", "23", "33", "43", "53", "63", "73",
               "02", "12", "22", "32", "42", "52", "62", "72",
               "01", "11", "21", "31", "41", "51", "61", "71",
               "00", "10", "20", "30", "40", "50", "60", "70"]

def moveToByte(move):
    startPos = move.movedPiece.piecePosition
    endPos = move.destinationCoordinate
    startStr = toByteBoard[startPos]
    endStr = toByteBoard[endPos]
    moveStr = startStr+endStr
    byteStr = bytes(moveStr, "ascii")
    return byteStr