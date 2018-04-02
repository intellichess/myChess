def pawnBonus(pos, alliance):
    if (alliance==1):
        return blackPawnPreference[pos]
    else:
        return whitePawnPreference[pos]

def knightBonus(pos, alliance):
    if (alliance==1):
        return blackKnightPreference[pos]
    else:
        return whiteKnightPreference[pos]

def rookBonus(pos, alliance):
    if (alliance==1):
        return blackRookPreference[pos]
    else:
        return whiteRookPreference[pos]

def bishopBonus(pos, alliance):
    if (alliance==1):
        return blackBishopPreference[pos]
    else:
        return whiteBishopPreference[pos]

def queenBonus(pos, alliance):
    if (alliance==1):
        return blackQueenPreference[pos]
    else:
        return whiteQueenPreference[pos]

def kingBonus(pos, alliance):
    if (alliance==1):
        return blackKingPreference[pos]
    else:
        return whiteKingPreference[pos]

def initColumn(colNumber):
    column = [False]*64
    while (colNumber<64):
        column[colNumber] = True
        colNumber+=8
    return column

def initRow(rowNumber):
    row = [False]*64
    for i in range(rowNumber, rowNumber+8):
        #print(i, row[i])
        row[i] = True
        #print(row[i])
    return row

col1=col2=col7=col8=[]



numTiles = 64
numTilesPerRow = 8

#add one col# and row# variable for each row and col on board
col1 = initColumn(0) #[0,8,16,24,32,40,48,56] array of booleans in these spots
col2 = initColumn(1) #[1,9,17,25,33,41,49,57
col3 = initColumn(2)
col4 = initColumn(3)
col5 = initColumn(4)
col6 = initColumn(5)
col7 = initColumn(6)
col8 = initColumn(7)

row1 = initRow(0)
row2 = initRow(8)
row3 = initRow(16)
row4 = initRow(24)
row5 = initRow(32)
row6 = initRow(40)
row7 = initRow(48)
row8 = initRow(56)

whiteKingPreference = [-30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -20, -30, -30, -40, -40, -30, -30, -20, \
                       -10, -20, -20, -20, -20, -20, -20, -10, \
                        20,  20,   0,   0,   0,   0,  20,  20, \
                        20,  30,  10,   0,   0,  10,  30,  20]

blackKingPreference = [20,  30,  10,   0,   0,  10,  30,  20, \
                       20,  20,   0,   0,   0,   0,  20,  20, \
                       -10, -20, -20, -20, -20, -20, -20, -10, \
                       -20, -30, -30, -40, -40, -30, -30, -20, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30, \
                       -30, -40, -40, -50, -50, -40, -40, -30]

blackQueenPreference = [-20,-10,-10, -5, -5,-10,-10,-20,\
                        -10,  0,  5,  0,  0,  0,  0,-10,\
                        -10,  5,  5,  5,  5,  5,  0,-10,\
                          0,  0,  5,  5,  5,  5,  0, -5,\
                          0,  0,  5,  5,  5,  5,  0, -5,\
                        -10,  0,  5,  5,  5,  5,  0,-10,\
                        -10,  0,  0,  0,  0,  0,  0,-10,\
                        -20,-10,-10, -5, -5,-10,-10,-20]

whiteQueenPreference = [-20,-10,-10, -5, -5,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5,  5,  5,  5,  0,-10,
                         -5,  0,  5,  5,  5,  5,  0, -5,
                          0,  0,  5,  5,  5,  5,  0, -5,
                        -10,  5,  5,  5,  5,  5,  0,-10,
                        -10,  0,  5,  0,  0,  0,  0,-10,
                        -20,-10,-10, -5, -5,-10,-10,-20]

blackRookPreference = [0,  0,  0,  5,  5,  0,  0,  0,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        5, 20, 20, 20, 20, 20, 20,  5,
                        0, 0, 0, 0, 0, 0, 0, 0]

whiteRookPreference = [0,  0,  0,  0,  0,  0,  0,  0,
                        5, 20, 20, 20, 20, 20, 20,  5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        0, 0, 0, 5, 5, 0, 0, 0]

whiteBishopPreference = [-20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20]

blackBishopPreference = [-20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20]

blackKnightPreference = [-50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50]

whiteKnightPreference = [-50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50]

blackPawnPreference = [0,  0,  0,  0,  0,  0,  0,  0,
                        5, 10, 10,-20,-20, 10, 10,  5,
                        5, -5,-10,  0,  0,-10, -5,  5,
                        0,  0,  0, 20, 20,  0,  0,  0,
                        5,  5, 10, 25, 25, 10,  5,  5,
                        10, 10, 20, 30, 30, 20, 10, 10,
                        50, 50, 50, 50, 50, 50, 50, 50,
                        0, 0, 0, 0, 0, 0, 0, 0]

whitePawnPreference = [0,  0,  0,  0,  0,  0,  0,  0,
                        50, 50, 50, 50, 50, 50, 50, 50,
                        10, 10, 20, 30, 30, 20, 10, 10,
                        5,  5, 10, 25, 25, 10,  5,  5,
                        0,  0,  0, 20, 20,  0,  0,  0,
                        5, -5,-10,  0,  0,-10, -5,  5,
                        5, 10, 10,-20,-20, 10, 10,  5,
                        0, 0, 0, 0, 0, 0, 0, 0]