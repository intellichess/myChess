#from piece import Piece
#from test import Tile

class Move:

    def __init__(self, movedPiece, board, destinationCoordinate):
        self.movedPiece = movedPiece
        self.board = board
        self.destinationCoordinate = destinationCoordinate
        self.isFirstMove = movedPiece.isFirstMove()

    def getMovedPiece(self):
        return self.movedPiece

    def getCurrentCoordinate(self):
        return self.getMovedPiece().getPiecePosition()

    def getDestinationCoordinate(self):
        return self.destinationCoordinate

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isAttack(self):
        return False

    def isCastlingMove(self):
        return False

    def isPromotionMove(self):
        return False

    def getAttackedPiece(self):
        return None

    def execute(self):
        import test
        from test import Builder
        building = Builder()
        #if pieces on board weren't moved, make new board with pieces still there
        for piece in self.board.currentPlayer.getActivePieces():
            if(not self.movedPiece==piece):
                building.setPiece(piece)

        #keep oponents pieces there
        for piece in self.board.currentPlayer.getOpponent().getActivePieces():
            building.setPiece(piece)

        #move piece and swap turns
        #print("inside execute",self.movedPiece.movePiece(self))
        #print("moved piece",self.movedPiece)
        #band-aid
        #print("destination",self.destinationCoordinate)
        #if not(isinstance(self.destinationCoordinate, int)):
        #when checking checkmate, self.destinationCoordinate contains a tile
        #    print("destinationTile", self.destinationCoordinate.tileCoordinate)
        building.setPiece(self.movedPiece.movePiece(self))
        building.setMoveMaker(self.board.currentPlayer.getOpponent().getAlliance())
        return  building.build()


class majorMove(Move):

    def __init__(self, movedPiece, board, destinationCoordinate):
        super().__init__(movedPiece, board, destinationCoordinate)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class attackMove(Move):
    def __init__(self, movedPiece, board, destinationCoordinate, attackedPiece):
        super().__init__(movedPiece, board, destinationCoordinate)
        self.attackedPiece = attackedPiece


    def isAttack(self):
        return True

    def getAttackedPiece(self):
        return self.attackedPiece

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class majorAttackMove(attackMove):
    def __init__(self, movedPiece, board, destinationCoordinate, attackedPiece):
        super().__init__(movedPiece, board, destinationCoordinate, attackedPiece)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class pawnPromotion(Move):
    def __init__(self, decoratedMove, movedPiece, board, destinationCoordinate):
        super().__init__(movedPiece, board, destinationCoordinate)
        self.decoratedMove = decoratedMove
        self.pawn = decoratedMove.movedPiece

    def isPromotionMove(self):
        return True

    def execute(self):
        pawnMovedBoard = self.decoratedMove.execute()
        from test import Builder, createGameBoard
        building = Builder()
        # if pieces on board weren't moved, make new board with pieces still there
        for piece in pawnMovedBoard.currentPlayer.getActivePieces():
            if (not self.pawn == piece):
                building.setPiece(piece)

        # keep oponents pieces there
        for piece in pawnMovedBoard.currentPlayer.getOpponent().getActivePieces():
            building.setPiece(piece)

        # move piece and swap turns
        building.setPiece(self.pawn.getPromotionPiece().movePiece(self))

        building.setMoveMaker(pawnMovedBoard.currentPlayer.getAlliance())

        return building.build()


    def isAttack(self):
        return self.decoratedMove.isAttack()

    def getAttackedPiece(self):
        return self.decoratedMove.getAttackedPiece()

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class pawnMove(Move):

    def __init__(self, movedPiece, board, destinationCoordinate):
        super().__init__(movedPiece, board, destinationCoordinate)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class pawnAttackMove(attackMove):
    def __init__(self, movedPiece, board, destinationCoordinate, attackedPiece):
        super().__init__(movedPiece, board, destinationCoordinate, attackedPiece)
        self.attackedPiece = attackedPiece

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class pawnEnPassantAttackMove(pawnAttackMove):
    def __init__(self, movedPiece, board, destinationCoordinate, attackedPiece):
        super().__init__(movedPiece, board, destinationCoordinate, attackedPiece)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def execute(self):
        import test
        from test import Builder
        building = Builder()
        #if pieces on board weren't moved, make new board with pieces still there
        for piece in self.board.currentPlayer.getActivePieces():
            if(not self.movedPiece==piece):
                building.setPiece(piece)

        #keep oponents pieces there
        for piece in self.board.currentPlayer.getOpponent().getActivePieces():
            if(not self.attackedPiece==piece):
                building.setPiece(piece)

        #move piece and swap turns
        building.setPiece(self.movedPiece.movePiece(self))
        building.setMoveMaker(self.board.currentPlayer.getOpponent().getAlliance())
        return  building.build()

class pawnJump(Move):
    def __init__(self, movedPiece, board, destinationCoordinate):
        super().__init__(movedPiece, board, destinationCoordinate)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def execute(self):
        import test
        from test import Builder
        building = Builder()
        #print("before",building.boardConfig)
        for i in range(64):
            if (building.boardConfig[i] is not None):
                print(building.boardConfig[i].getPiece())
            else:
                continue
#        print("board object",self.board.currentPlayer.getActivePieces())
        #print("movedPiece",self.movedPiece)
        #if pieces on board weren't moved, make new board with pieces still there
        for piece in self.board.currentPlayer.getActivePieces():
            #print("piece Comparison",piece, self.movedPiece, not self.movedPiece==piece)
            if(not self.movedPiece==piece):
                building.setPiece(piece)

        #keep oponents pieces there
        for piece in self.board.currentPlayer.getOpponent().getActivePieces():
            building.setPiece(piece)

        #move piece and swap turns
        import piece
        #print("after",building.boardConfig)
        #for i in range(64):
        #    if (building.boardConfig[i] is not None):
        #        print(building.boardConfig[i].getPiece())
        #    else:
        #        continue
        movedPawn = piece.pawn(self.destinationCoordinate, self.movedPiece.Alliance)
        movedPawn.firstMove =False
        #print("movedPawn var",movedPawn)
        #print("opponent alliance",self.board.currentPlayer.getOpponent().getAlliance())
        building.setPiece(movedPawn)
        building.setEnPassantPawn(movedPawn)
        #print("before set move maker",building.nextMoveMaker)
        building.setMoveMaker(self.board.currentPlayer.getOpponent().getAlliance())
#        print("after set move maker",building.nextMoveMaker)

        return  building.build()


class castleMove(Move):
    def __init__(self, movedPiece, board, destinationCoordinate, castleRook, castleRookStart, castleRookDestination):
        super().__init__(movedPiece, board, destinationCoordinate)
        self.castleRook = castleRook
        self.castleRookStart = castleRookStart
        self.castleRookDestination = castleRookDestination

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getCastleRook(self):
        return self.castleRook

    def isCastlingMove(self):
        return True

    def execute(self):
        import test
        from test import Builder
        building = Builder()
        #if pieces on board weren't moved, make new board with pieces still there
        for piece in self.board.currentPlayer.getActivePieces():
            if((not self.movedPiece==piece) and (not self.castleRook==piece)):
                building.setPiece(piece)

        #keep oponents pieces there
        for piece in self.board.currentPlayer.getOpponent().getActivePieces():
            building.setPiece(piece)

        #move piece and swap turns
        #king
        building.setPiece(self.movedPiece.movePiece(self))
        #rook, look into first move for normal pieces
        from piece import rook
        building.setPiece(rook(self.castleRookDestination,self.castleRook.Alliance))
        building.setMoveMaker(self.board.currentPlayer.getOpponent().getAlliance())
        return  building.build()

class kingSideCastleMove(castleMove):
    def __init__(self, movedPiece, board, destinationCoordinate, castleRook, castleRookStart, castleRookDestination):
        super().__init__(movedPiece, board, destinationCoordinate, castleRook, castleRookStart, castleRookDestination)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class queenSideCastleMove(castleMove):
    def __init__(self, movedPiece, board, destinationCoordinate, castleRook, castleRookStart, castleRookDestination):
        super().__init__(movedPiece, board, destinationCoordinate, castleRook, castleRookStart, castleRookDestination)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class nullMove(Move):
    def __init__(self):
        super().__init__(None, None, -1)

    def execute(self):
        pass
        #runtime exception

class moveFactory:
    def __init__(self):
        self = self

    def createMove(self, board, currentCoordinate, destinationCoordinate):
        for move in board.getAllLegalMoves():
            if(move.getCurrentCoordinate()==currentCoordinate and\
                    move.getDestinationCoordinate() == destinationCoordinate):
                return move
        return nullMove()