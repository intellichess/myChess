from enum import Enum

def establishKing(player):
    pieces = player.getActivePieces()
    for i in range(len(pieces)):
        if (pieces[i].getPieceType()=="K"):
            return (pieces[i])  # may not need to typecast
        # else throw RunTimeException



#######################################################

class Player:

    def __init__(self, board, legalMoves):
        self.board = board
        self.legalMoves = legalMoves
        self.isInCheck = None
        self.king = establishKing(self)


    def getPlayerKing(self):
        return self.king

    def getAlliance(self):
        return None

    def getOpponent(self):
        return None

    def getActivePieces(list):
        return None

    def isMoveLegal(self, move):
        return None #return true if move legal

    def calculateAttacksOnTile(self, position, moves):
        return None


    def isCheck(self):
        return self.isInCheck

    def isCheckmate(self):
        return (self.isInCheck()) and (not self.hasEscapeMoves())

    def hasEscapeMoves(self):
        for i in range(len(self.legalMoves)):
            transition = self.makeMove(self.legalMoves[i])
            if(transition.getMoveStatus().isDone()):
                return True
        return False

    def isStalemate(self):
        return (not self.isCheck()) and (not self.hasEscapeMoves())

    def isCastled(self):
        return False

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        pass

    def makeMove(self, move):

        if (not self.isMoveLegal(move)):
            return MoveTransition(self.board, MoveStatus.illegalMove)

        transitionBoard = move.execute()
        kingAttacks = self.calculateAttacksOnTile(\
            transitionBoard.currentPlayer().getOpponent().getPlayerKing().getPiecePosition(),\
            transitionBoard.currentPlayer().getLegalMoves())

        if(not kingAttacks.isEmpty()):
            return MoveTransition(self.board, MoveStatus.leavesPlayerInCheck)

        return MoveTransition(self.board, MoveStatus.done)



##########################################################

class blackPlayer(Player):

    def __init__(self, board, legalMoves, opponentLegalMoves):
        super().__init__(board, legalMoves)
        self.opponentLegalMoves = opponentLegalMoves
        self.legalMoves = self.legalMoves # + self.calculateKingCastles(self.legalMoves,self.opponentLegalMoves)
        self.king = establishKing(self)
        #self.isInCheck = not (self.calculateAttacksOnTile(self.king.getPiecePosition(), opponentLegalMoves)==0)

    def getActivePieces(self):
        return self.board.getBlackPieces()

    def getAlliance(self):
        import color
        return color.Alliance.black.value

    def getOpponent(self):
        return self.board.getWhitePlayer()

    def calculateAttacksOnTile(self, position, moves):
        #return None
        attackMoves = []
        #print(moves)
        for pieceMoves in moves:
            #print(pieceMoves)
            for move in pieceMoves:
                if (position == move.getDestinationCoordinate()):
                    attackMoves.append(move)
        #print(attackMoves)
        return attackMoves.copy()

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        kingCastles = []
        if(self.king.isFirstMove() and (not self.isCheck())):
            #black kingsside castle
            if((not self.board.getTile(5).occupied())and(not self.board.getTile(6).occupied())):
                rookTile = self.board.getTile(7)
                if (rookTile.occupied() and rookTile.getPiece().isFirstMove()):
                    if (self.calculateAttacksOnTile(5,opponentLegalMoves)==0 and \
                            self.calculateAttacksOnTile(6, opponentLegalMoves)==0 and\
                            rookTile.getPiece().pieceType=="r"):
                        #add castle move
                        import move
                        kingCastles.append(move.kingSideCastleMove(self.king, self.board, 6, \
                                rookTile.getPiece(), rookTile.getTileCoordinate(), 5))
            #queen side castle
            if((not self.board.getTile(1).occupied())and(not self.board.getTile(2).occupied())and\
                    (not self.board.getTile(3).occupied())):
                rookTile = self.board.getTile(0)
                if (rookTile.occupied() and rookTile.getPiece().isFirstMove() \
                        and self.calculateAttacksOnTile(2, opponentLegalMoves)==0 and \
                        self.calculateAttacksOnTile(3, opponentLegalMoves)==0 and \
                        rookTile.getPiece().pieceType=="r"):

                    #add castle move
                    import move
                    kingCastles.append(move.queenSideCastleMove(self.king, self.board, 2, \
                                rookTile.getPiece(), rookTile.getTileCoordinate(), 3))

        return kingCastles.copy()

##########################################################

class whitePlayer(Player):

    def __init__(self, board, legalMoves, opponentLegalMoves):
        super().__init__(board, legalMoves)
        self.opponentLegalMoves = opponentLegalMoves
        self.legalMoves = self.legalMoves #+ self.calculateKingCastles(self.legalMoves, self.opponentLegalMoves)
        self.king = establishKing(self)
        #self.isInCheck = self.calculateAttacksOnTile(self.king.getPiecePosition(), opponentLegalMoves)==0

    def getActivePieces(self):
        return self.board.getWhitePieces()

    def getAlliance(self):
        import color
        return color.Alliance.white.value

    def getOpponent(self):
        return self.board.getBlackPlayer()

    def calculateAttacksOnTile(self, position, moves):
        #return None
        attackMoves = []

        for pieceMoves in moves:
#            print(pieceMoves)
            for move in pieceMoves:
#                print(move, move.destinationCoordinate)
                if (position == move.getDestinationCoordinate()):
                    attackMoves.append(move)
        #print(attackMoves)
        return attackMoves.copy()

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        kingCastles = []
        if(self.king.isFirstMove() and (not self.isCheck())):
            #white kingsside castle
            if((not self.board.getTile(61).occupied())and(not self.board.getTile(62).occupied())):
                rookTile = self.board.getTile(63)
                if (rookTile.occupied() and rookTile.getPiece().isFirstMove()):
                    if (self.calculateAttacksOnTile(61,opponentLegalMoves)==0 and \
                            self.calculateAttacksOnTile(62, opponentLegalMoves)==0 and\
                            rookTile.getPiece().pieceType=="r"):
                        #add castle move
                        import move
                        kingCastles.append(move.kingSideCastleMove(self.king, self.board, 62, \
                                rookTile.getPiece(), rookTile.getTileCoordinate(), 59))
            #queen side castle
            if((not self.board.getTile(59).occupied())and(not self.board.getTile(58).occupied())and\
                    (not self.board.getTile(57).occupied())):
                rookTile = self.board.getTile(56)
                if (rookTile.occupied() and rookTile.getPiece().isFirstMove() \
                        and self.calculateAttacksOnTile(58, opponentLegalMoves)==0 and \
                        self.calculateAttacksOnTile(59, opponentLegalMoves)==0 and \
                        rookTile.getPiece().pieceType=="r"):
                    #add castle move
                    kingCastles.append(move.queenSideCastleMove(self.king, self.board, 58, \
                                rookTile.getPiece(), rookTile.getTileCoordinate(), 59))

        return kingCastles.copy()

##################################################################

#class MoveStatus:


class MoveTransition:
    def __init__(self,transitionBoard, move, moveStatus):
        self.transitionBoard = transitionBoard
        self.move = move
        self.moveStatus = moveStatus

    def getMoveStatus(self):
        return self.moveStatus

    def getBoardTransition(self):
        return self.transitionBoard

class MoveStatus(Enum):
    done = True
    illegalMove = False
    leavesPlayerInCheck = False