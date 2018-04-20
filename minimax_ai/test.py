# algebraic notation filler vid 37 18:00 and 40 17:00
from piece import Piece, pawn, bishop, rook, knight, queen, king
from color import Alliance
whiteWins = -1
blackWins = 1
stalemate = 2
inProgress = 0


# board stuff
def prettyBoard(board):
    for i in range(len(board)):
        if i % 8 == 0:
            print("")
            if board[i].occupied():
                s = ""
                if board[i].pieceOnTile.Alliance.value > 0:
                    s = board[i].pieceOnTile.pieceType + "b"
                else:
                    s = board[i].pieceOnTile.pieceType + "w"
                print(" " + s, end="")
            else:
                print(" --", end="")
        else:
            if board[i].occupied():
                if board[i].pieceOnTile.Alliance.value > 0:
                    s = board[i].pieceOnTile.pieceType + "b"
                else:
                    s = board[i].pieceOnTile.pieceType + "w"
                print(" " + s, end="")
            else:
                print(" --", end="")
    print("")


def moveToString(move, player):
    from boardutils import algebraBoard
    string = ""
    legal_moves = player.legalMoves
    if move.isCastlingMove():
        if move.movedPiece.Alliance.value == 1:
            # kingCastle
            if((move.destinationCoordinate == 6 and move.castleMoveDestination == 5) or
                    (move.destinationCoordinate == 62 and move.castleMoveDestination == 61)):
                string = "0-0 "
                return string
        else:
            # queenCastle
            if ((move.destinationCoordinate == 2 and move.castleMoveDestination == 3) or
                    (move.destinationCoordinate == 58 and move.castleMoveDestination == 59)):
                string = "0-0-0 "
                return string

    elif move.isAttack():
        string = move.movedPiece.pieceType
        for i in range(len(legal_moves)):
            if legal_moves[i] == 0:
                pass
            else:
                for j in range(len(legal_moves[i])):
                    if (legal_moves[i][j].destinationCoordinate == move.destinationCoordinate and
                            legal_moves[i][j].movedPiece.pieceType == move.movedPiece.pieceType):
                        print("is same move", legal_moves[i][j] == move)
                        string = string + algebraBoard[i][0]

        string = string + "x" + algebraBoard[move.destinationCoordinate]
        if player.getOpponent().isInCheck:
            string = string + "+" + " "
        else:
            string = string + " "
        return string

    else:
        string = move.movedPiece.pieceType
        for i in range(len(legal_moves)):
            if legal_moves[i] == 0:
                pass
            else:
                for j in range(len(legal_moves[i])):
                    if (legal_moves[i][j].destinationCoordinate == move.destinationCoordinate and
                            legal_moves[i][j].movedPiece.pieceType == move.movedPiece.pieceType):
                        print("is same move", legal_moves[i][j] == move)
                        string = string + algebraBoard[i][0]

        string = string + algebraBoard[move.destinationCoordinate]
        if player.getOpponent().isInCheck:
            string = string + "+" + " "
        else:
            string = string + " "
        return string


def calculateLivePieces(board, color):
    import piece
    live_pieces = []
    for i in range(64):
        on_tile = board[i]
        if board[i].occupied():
            if on_tile.getPiece().getPieceAlliance().value == color:
                live_pieces.append(on_tile.getPiece())
    return live_pieces

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
        # clean up legal moves in piece.py
        self.whiteStandardLegalMoves = self.calculateLegalMoves(self.whitePieces)
        self.blackStandardLegalMoves = self.calculateLegalMoves(self.blackPieces)
        import player
        from player import whitePlayer, blackPlayer
        self.whitePlayer = whitePlayer(self, self.whiteStandardLegalMoves, self.blackStandardLegalMoves)
        self.blackPlayer = blackPlayer(self, self.blackStandardLegalMoves, self.whiteStandardLegalMoves)
        #change to opposite player after each move
        self.currentPlayer = Alliance.choosePlayer(builder.nextMoveMaker, self.whitePlayer , self.blackPlayer)
        if (builder.transitionMove is not None):
            self.transitionMove = builder.transitionMove
        else:
            self.transitionMove = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getStatus(self):
        if(self.currentPlayer.getAlliance()==-1):
            if(self.currentPlayer.isCheckmate()):
                return blackWins
            elif(self.currentPlayer.getOpponent().isCheckmate()):
                return whiteWins
            elif(self.currentPlayer.isStalemate() or self.currentPlayer.getOpponent().isStalemate()):
                return stalemate
            else:
                return inProgress
        else:
            if (self.currentPlayer.isCheckmate()):
                return whiteWins
            elif (self.currentPlayer.getOpponent().isCheckmate()):
                return blackWins
            elif (self.currentPlayer.isStalemate() and self.currentPlayer.getOpponent().isStalemate()):
                return stalemate
            else:
                return inProgress

    #def undo(self):
    #    building = Builder()

    def getEnPassantPawn(self):
        return self.enPassantPawn

    def getTransitionMove(self):
        return self.transitionMove

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

        # for all pieces in the list
        for i in range(len(pieces)):
            legalMoves = legalMoves + pieces[i].findLegalMoves(self)
        return legalMoves

        ## error here, create tile, builder


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
        # white
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



##########################################################

class Builder(Board):
    def __init__(self):
        self.boardConfig = [None]*64
        self.nextMoveMaker = 0
        self.pawn = None
        self.transitionMove = None

    def build(self):
        #print("self", self.boardConfig)
#        print("in build class",self.nextMoveMaker)
        return Board(self)

    def setTransitionMove(self, move):
        self.transitionMove = move

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

    # piece not piece, is a new tile
    @classmethod
    def createTile(cls, tileCoordinate , piece):
        if piece is not None:
            return occupiedTile(tileCoordinate , piece)

        else:
            return emptyTile(tileCoordinate)

    @classmethod
    def placeTile(cls, tileCoordinate, tile):
        if tile is not None:
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
    def __init__(self, tileCoordinate, pieceOnTile):
        super().__init__(tileCoordinate)
        self.pieceOnTile = pieceOnTile

    @classmethod
    def occupied(cls):
        return True

    def getPiece(cls):
        return cls.pieceOnTile

