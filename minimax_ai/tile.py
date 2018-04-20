class Tile:
    def __init__(self, tileCoordinate):
        self.tileCoordinate = tileCoordinate

    # def occupied(self, tileCoordinate):

    # def getPiece(self, tileCoordinate):

    def createAllEmptyTiles(self, board):
        i, j = 8
        for i in range(0,i):
            for j in range(0,j):
                board[i][j] = emptyTile

        return board


class emptyTile(Tile):
    def __init__(self, tileCoordinate):
        self.tileCoordinate = tileCoordinate

    def occupied(self, tileCoordinate):
        return False

    def getPiece(self, tileCoordinate):
        return None


class occupiedTile(Tile):
    # pieceOnTile = piece

    def __init__(self, tileCoordinate, pieceOnTile):
        super(tileCoordinate)
        self.pieceOnTile = pieceOnTile

    def occupied(self, tileCoordinate):
        return True

    def getPiece(self, tileCoordinate):
        return self.pieceOnTile
