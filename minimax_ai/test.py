#algebraic notation filler vid 37 18:00 and 40 17:00
from piece import Piece, pawn, bishop, rook, knight, queen, king
from color import Alliance

#board stuff
def prettyBoard(board):
    str = ""
    for i in range(len(board)):
        if (i%8==0):
            print("")
            if (board[i].occupied()==True):
                if (board[i].pieceOnTile.Alliance.value>0):
                    str = board[i].pieceOnTile.pieceType + "b"
                else:
                    str = board[i].pieceOnTile.pieceType + "w"
                print(" "+str, end="")
            else:
                print(" --",end="")
        else:
            if (board[i].occupied()==True):
                if (board[i].pieceOnTile.Alliance.value>0):
                    str = board[i].pieceOnTile.pieceType + "b"
                else:
                    str = board[i].pieceOnTile.pieceType + "w"
                print(" "+str, end="")
            else:
                print(" --",end="")
    print("")

def moveToString():
    pass

def calculateLivePieces(board, color):
    import piece
    livePieces = []
    #print("board in calcLivePieces", board)
    for i in range(64):
        OnTile = board[i]
#        print("pieceOnTile",board[i])
        if (board[i].occupied()):
#            print("tile", OnTile)
#            print("piece on tile", OnTile.pieceOnTile)
#            print("1 piece color, 2 color", OnTile.getPiece().getPieceAlliance().value , color)
            if (OnTile.getPiece().getPieceAlliance().value==color):
#                print("livePieces before", livePieces)
                livePieces.append(OnTile.getPiece())
#                print("livePieces after",livePieces)
    return livePieces

def createGameBoard(builder):
    tiles = [None]*64
    for i in range(64):
        tiles[i] = Tile.placeTile(i, builder.boardConfig[i])
    return tiles


######################################################


class Board:
    def __init__(self, builder):
#        print("in board class",builder.nextMoveMaker)
        self.board = createGameBoard(builder)
        self.whitePieces = calculateLivePieces(self.board, -1)
        self.blackPieces = calculateLivePieces(self.board, 1)
        self.enPassantPawn = builder.pawn
        #clean up legal moves in piece.py
        self.whiteStandardLegalMoves = self.calculateLegalMoves(self.whitePieces)
        self.blackStandardLegalMoves = self.calculateLegalMoves(self.blackPieces)
        import player
        from player import whitePlayer, blackPlayer
        self.whitePlayer = whitePlayer(self, self.whiteStandardLegalMoves, self.blackStandardLegalMoves)
        self.blackPlayer = blackPlayer(self, self.blackStandardLegalMoves, self.whiteStandardLegalMoves)
        #change to opposite player after each move
        self.currentPlayer = Alliance.choosePlayer(builder.nextMoveMaker, self.whitePlayer , self.blackPlayer)
#        print("current player in board class",self.currentPlayer)

    def getEnPassantPawn(self):
        return self.enPassantPawn

    def getBoard(self):
        return self.board

    def getTile(self, tileCoordinate):
        return self.board[tileCoordinate]

    def getAllLegalMoves(self):
        whiteMoves = self.calculateLegalMoves(self.whitePieces)
        blackMoves = self.calculateLegalMoves(self.blackPieces)
        return whiteMoves+blackMoves
        #combine legalMoves for white and black player

    def currentPlayer(self):
        return self.currentPlayer


    def getBlackPlayer(self):
        return self.blackPlayer

    def getWhitePlayer(self):
        return self.whitePlayer

    def getBlackPieces(self):
        return self.blackPieces

    def getWhitePieces(self):
        return self.whitePieces

    def calculateLegalMoves(self, pieces):
        import piece
        from piece import bishop, knight, king, rook, pawn, queen
        legalMoves = []
#        print(pieces)
        # for all pieces in the list
        for i in range(len(pieces)):
            from move import majorMove
#            print(pieces[i].findLegalMoves(self))
#            if (pieces[i].findLegalMoves(self)==0):
#                continue
#            else:
#                for j in range(len(pieces[i].findLegalMoves(self))):
#                    print(i,pieces[i].findLegalMoves(self)[j].destinationCoordinate, pieces[i].findLegalMoves(self)[j].movedPiece);
#make legalMoves a single array

            legalMoves.append(pieces[i].findLegalMoves(self))
        return legalMoves

##error here, create tile, builder



    def createStandardBoard(self):
        import piece
        import color
        building = Builder()
        building.setPiece(piece.rook(0, color.Alliance.black))
        building.setPiece(piece.knight(1, color.Alliance.black))
        building.setPiece(piece.bishop(2, color.Alliance.black))
        building.setPiece(piece.queen(3, color.Alliance.black))
        building.setPiece(piece.king(4, color.Alliance.black))
        building.setPiece(piece.bishop(5, color.Alliance.black))
        building.setPiece(piece.knight(6, color.Alliance.black))
        building.setPiece(piece.rook(7, color.Alliance.black))
        building.setPiece(piece.pawn(8, color.Alliance.black))
        building.setPiece(piece.pawn(9, color.Alliance.black))
        building.setPiece(piece.pawn(10, color.Alliance.black))
        building.setPiece(piece.pawn(11, color.Alliance.black))
        building.setPiece(piece.pawn(12, color.Alliance.black))
        building.setPiece(piece.pawn(13, color.Alliance.black))
        building.setPiece(piece.pawn(14, color.Alliance.black))
        building.setPiece(piece.pawn(15, color.Alliance.black))
        #white
        building.setPiece(piece.pawn(48, color.Alliance.white))
        building.setPiece(piece.pawn(49, color.Alliance.white))
        building.setPiece(piece.pawn(50, color.Alliance.white))
        building.setPiece(piece.pawn(51, color.Alliance.white))
        building.setPiece(piece.pawn(52, color.Alliance.white))
        building.setPiece(piece.pawn(53, color.Alliance.white))
        building.setPiece(piece.pawn(54, color.Alliance.white))
        building.setPiece(piece.pawn(55, color.Alliance.white))
        building.setPiece(piece.rook(56, color.Alliance.white))
        building.setPiece(piece.knight(57, color.Alliance.white))
        building.setPiece(piece.bishop(58, color.Alliance.white))
        building.setPiece(piece.queen(59, color.Alliance.white))
        building.setPiece(piece.king(60, color.Alliance.white))
        building.setPiece(piece.bishop(61, color.Alliance.white))
        building.setPiece(piece.knight(62, color.Alliance.white))
        building.setPiece(piece.rook(63, color.Alliance.white))

        building.setMoveMaker(color.Alliance.white.value)

        #print(building.boardConfig[0])
        #print(building.boardConfig)
        #print(building.build().board[0])

        return building.build()


    def createCheckBoard(self):
        import piece
        import color
        building = Builder()
        building.setPiece(piece.rook(0, color.Alliance.black))
        building.setPiece(piece.king(56, color.Alliance.black))
        building.setPiece(piece.king(4, color.Alliance.white))

        building.setMoveMaker(color.Alliance.white.value)


        return building.build()

    def createMateBoard(self):
        import piece
        import color
        building = Builder()
        building.setPiece(piece.rook(0, color.Alliance.black))
        building.setPiece(piece.rook(8, color.Alliance.black))
        building.setPiece(piece.king(56, color.Alliance.black))
        building.setPiece(piece.king(4, color.Alliance.white))

        building.setMoveMaker(color.Alliance.white.value)


        return building.build()

    def createPromoteBoard(self):
        import piece
        import color
        building = Builder()
        building.setPiece(piece.pawn(8, color.Alliance.white))
        building.setPiece(piece.pawn(9, color.Alliance.black))
        building.setPiece(piece.pawn(48, color.Alliance.white))
        building.setPiece(piece.pawn(49, color.Alliance.black))
        building.setPiece(piece.king(63, color.Alliance.black))
        building.setPiece(piece.king(7, color.Alliance.white))

        building.setMoveMaker(color.Alliance.white.value)


        return building.build()

    def createMoveBoard(self):
        import piece
        import color
        building = Builder()

#        building.setPiece(piece.pawn(35, color.Alliance.white))
#        building.setPiece(piece.rook(35, color.Alliance.white))
#        building.setPiece(piece.knight(35, color.Alliance.white))
        building.setPiece(piece.bishop(5, color.Alliance.white))
#        building.setPiece(piece.queen(35, color.Alliance.white))

        building.setPiece(piece.king(63, color.Alliance.white))
        building.setPiece(piece.king(0, color.Alliance.black))

        building.setMoveMaker(color.Alliance.white.value)
        #building.setMoveMaker(color.Alliance.black.value)

        return building.build()

##########################################################

class Builder(Board):
    def __init__(self):
        self.boardConfig = [None]*64
        self.nextMoveMaker = 0
        self.pawn = None

    def build(self):
        #print("self", self.boardConfig)
#        print("in build class",self.nextMoveMaker)
        return Board(self)

    def setMoveMaker(self, nextMoveMaker):
        #get alliance
        self.nextMoveMaker = nextMoveMaker

    def setTiles(self, board):
        for i in range(64):
            if(board[i]==None):
                board[i] = emptyTile(i)
            else:
                continue
        return board

    def setPiece(self, piece):
#        print("piece",piece)
#        print("self.boardConfig before",self.boardConfig[piece.getPiecePosition()])
#        print(occupiedTile(piece.getPiecePosition(), piece))
#        print("inside set piece",piece)
        self.boardConfig[piece.getPiecePosition()] = occupiedTile(piece.getPiecePosition(),piece)
#        print("self.boardConfig after",self.boardConfig[piece.getPiecePosition()])
        return self

    def setEnPassantPawn(self, pawn):
        self.pawn = pawn

##########################################################
class Tile:
    def __init__(self, tileCoordinate):
        self.tileCoordinate = tileCoordinate

    #EMPTY_TILES
    @staticmethod
    def createAllPossibleEmptyTiles():
        emptyTileMap = [None]*64
        for i in range(64):
            print(i)
            emptyTileMap[i] = emptyTile(i)

        return emptyTileMap

    @classmethod
    def occupied(cls):
        pass

    @classmethod
    def getPiece(cls):
        pass


    def getTileCoordinate(cls):
        return cls.tileCoordinate

    #convert to python dictionary


#    def createEmptyBoard():
#        cols = 8
#        rows = 8
#        inc = 0
#        emptyBoard=[[0 for i in range(rows)] for j in range(cols)]
#        for i in range(rows):
#            for j in range(cols):
#                emptyBoard[i][j]=emptyTile(inc)
#                inc = inc + 1

#        return emptyBoard

#piece not piece, is a new tile
    @classmethod
    def createTile(cls, tileCoordinate , piece):
#        print("1 coordinate, 2 piece", tileCoordinate, piece)
        if (piece is not None):
#            print("piece in createTile",piece.getPiece())
            return occupiedTile(tileCoordinate , piece)

        else:
            return emptyTile(tileCoordinate)

    @classmethod
    def placeTile(cls, tileCoordinate, tile):
#        print("1 coordinate, 2 piece", tileCoordinate, tile)
        if (tile is not None):
            return occupiedTile(tileCoordinate, tile.getPiece())

        else:
            return emptyTile(tileCoordinate)

    @classmethod
    def isTileOccupied(cls):
        return cls.occupied()

############################################################

class emptyTile(Tile):
    def __init__(self, tileCoordinate):
        super().__init__(tileCoordinate)

    @classmethod
    def occupied(cls):
        return False

    @classmethod
    def getPiece(cls):
        return None


##################################################

class occupiedTile(Tile):
    #pieceOnTile = piece
    def __init__(self, tileCoordinate, pieceOnTile):
        super().__init__(tileCoordinate)
        self.pieceOnTile = pieceOnTile

    @classmethod
    def occupied(cls):
        return True


    def getPiece(cls):
        return cls.pieceOnTile

