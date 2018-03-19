#algebraic notation filler vid 37 18:00 and 40 17:00
from piece import Piece, pawn, bishop, rook, knight, queen, king
from color import Alliance

#board stuff
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
#        self.currentPlayer = self.whitePlayer #Alliance.choosePlayer(builder.nextMoveMaker, whitePlayer, blackPlayer)

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
            print(pieces[i].findLegalMoves(self))
            if (pieces[i].findLegalMoves(self)==0):
                continue
            else:
                for j in range(len(pieces[i].findLegalMoves(self))):
                    print(i,pieces[i].findLegalMoves(self)[j].destinationCoordinate, pieces[i].findLegalMoves(self)[j].movedPiece);

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

        building.setMoveMaker(color.Alliance.white)

        #print(building.boardConfig[0])
        #print(building.boardConfig)
        #print(building.build().board[0])

        return building.build()

#    def createBoard(self, builder):
#        import piece
#        import color
#        board = {}
#        colorCode = color.Alliance.black.value
#        for i in range(64):
#                #black 0-15          #white 48-63
#            if (i==30):
#                colorCode=color.Alliance.white.value
#            if ((i==0 or i==7) and (colorCode==1)) or ((i==56 or i==63)and(colorCode==-1)):
#                board[i] = occupiedTile(i,piece.rook(i,colorCode))
#            elif ((i==1 or i==6) and (colorCode==1)) or ((i==57 or i==62)and(colorCode==-1)):
#                board[i] = occupiedTile(i,piece.knight(i,colorCode))
#            elif ((i==2 or i==5)and(colorCode==1)) or ((i==58 or i==61)and(colorCode==-1)):
#                board[i] = occupiedTile(i,piece.bishop(i,colorCode))
#            elif ((i==3 and colorCode==1) or (i==59 and colorCode==-1)):
#                board[i] = occupiedTile(i,piece.queen(i,colorCode))
#            elif ((i==4 and colorCode==1) or (i==60 and colorCode==-1)):
#                board[i] = occupiedTile(i,piece.king(i,colorCode))
#            elif (((8<=i<=15)and colorCode==1) or((48<=i<=55)and colorCode==-1)):
#                board[i] = occupiedTile(i,piece.pawn(i,colorCode))
#            else:
#                board[i] = emptyTile(i)

#        builder = board
#        return builder

##########################################################

class Builder(Board):
    def __init__(self):
        self.boardConfig = [None]*64
        self.nextMoveMaker = 0
        self.pawn = None

    def build(self):
        #print("self", self.boardConfig)
        return Board(self)

    def setMoveMaker(self, nextMoveMaker):
        #get alliance
        self.nextMoveMaker = nextMoveMaker
        return self

    def setPiece(self, piece):
#        print("piece",piece)
#        print("self.boardConfig before",self.boardConfig[piece.getPiecePosition()])
#        print(occupiedTile(piece.getPiecePosition(), piece))
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



x= Board(Builder()).createStandardBoard()
import piece
#print("start board", x.blackPieces[0].pieceType, x.blackPieces[0].piecePosition, x.blackPieces[0].Alliance)
from move import majorMove
#print(x.whiteStandardLegalMoves)
#print(x.blackStandardLegalMoves)
#print((len(x.whitePieces)))
#print((len(x.blackPieces)))