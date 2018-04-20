def pawnBonus(pos, alliance):
    if alliance == 1:
        return blackPawnPreference[pos]
    else:
        return whitePawnPreference[pos]


def knightBonus(pos, alliance):
    if alliance == 1:
        return blackKnightPreference[pos]
    else:
        return whiteKnightPreference[pos]


def rookBonus(pos, alliance):
    if alliance == 1:
        return blackRookPreference[pos]
    else:
        return whiteRookPreference[pos]


def bishopBonus(pos, alliance):
    if alliance == 1:
        return blackBishopPreference[pos]
    else:
        return whiteBishopPreference[pos]


def queenBonus(pos, alliance):
    if alliance == 1:
        return blackQueenPreference[pos]
    else:
        return whiteQueenPreference[pos]


def kingBonus(pos, alliance):
    if alliance == 1:
        return blackKingPreference[pos]
    else:
        return whiteKingPreference[pos]


def initColumn(colNumber):
    column = [False] * 64
    while colNumber < 64:
        column[colNumber] = True
        colNumber += 8
    return column


def initRow(rowNumber):
    row = [False] * 64
    for i in range(rowNumber, rowNumber+8):
        row[i] = True
    return row


def lastNMoves(board, num):
    move_history = []
    current_move = board.getTransitionMove()
    i = 0
    while current_move != None and i < num:
        move_history.append(current_move)
        current_move = current_move.getBoard().getTransitionMove()
        i += 1
    return move_history


col1 = col2 = col7 = col8 = []

numTiles = 64
numTilesPerRow = 8

# add one col# and row# variable for each row and col on board
col1 = initColumn(0)  # [0,8,16,24,32,40,48,56] array of booleans in these spots
col2 = initColumn(1)  # [1,9,17,25,33,41,49,57
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

algebraBoard = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"
]

rowSumBoard = [
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
    [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
    [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7],
    [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7],
    [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [4, 7],
    [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7],
    [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5], [6, 6], [6, 7],
    [7, 0], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7]
]


whiteKingPreference = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20,  20,   0,   0,   0,   0,  20,  20,
    20,  30,  10,   0,   0,  10,  30,  20
]

blackKingPreference = [
    20,  30,  10,   0,   0,  10,  30,  20,
    20,  20,   0,   0,   0,   0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

blackQueenPreference = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  5,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

whiteQueenPreference = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,   0,   0,  0,  0,   0,   0, -10,
    -10,   0,   5,  5,  5,   5,   0, -10,
    -5,    0,   5,  5,  5,   5,   0,  -5,
    0,     0,   5,  5,  5,   5,   0,  -5,
    -10,   5,   5,  5,  5,   5,   0, -10,
    -10,   0,   5,  0,  0,   0,   0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

blackRookPreference = [
    0,   0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5,  20, 20, 20, 20, 20, 20,  5,
    0,   0,  0,  0,  0,  0,  0,  0
]

whiteRookPreference = [
    0,   0,  0,  0,  0,  0,  0,  0,
    5,  20, 20, 20, 20, 20, 20,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,   0,  0,  5,  5,  0,  0,  0
]

whiteBishopPreference = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

blackBishopPreference = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

blackKnightPreference = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

whiteKnightPreference = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

blackPawnPreference = [
    0,  0,   0,   0,   0,   0,  0,  0,
    5, 10,  10, -20, -20,  10, 10,  5,
    5, -5, -10,   0,   0, -10, -5,  5,
    0,  0,   0,  20,  20,   0,  0,  0,
    5,  5,  10,  25,  25,  10,  5,  5,
    10, 10, 20,  30,  30,  20, 10, 10,
    50, 50, 50,  50,  50,  50, 50, 50,
    0,   0,  0,   0,   0,   0,  0,  0
]

whitePawnPreference = [
    0,   0,   0,   0,   0,   0,  0,  0,
    50, 50,  50,  50,  50,  50, 50, 50,
    10, 10,  20,  30,  30,  20, 10, 10,
    5,   5,  10,  25,  25,  10,  5,  5,
    0,   0,   0,  20,  20,   0,  0,  0,
    5,  -5, -10,   0,   0, -10, -5,  5,
    5,  10,  10, -20, -20,  10, 10,  5,
    0,   0,   0,   0,   0,   0,  0,  0
]
