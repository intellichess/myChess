from enum import Enum


def establishKing(player):
    pieces = player.getActivePieces()
    for i in range(len(pieces)):
        if pieces[i].getPieceType() == "K":
            return pieces[i]  # may not need to typecast


class Player:

    def __init__(self, board, legalMoves):
        self.board = board
        self.legalMoves = legalMoves
        self.isInCheck = None
        self.king = establishKing(self)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getPlayerKing(self):
        return self.king

    def getAlliance(self):
        return None

    def getOpponent(self):
        return None

    def getActivePieces(self):
        return None

    #check if move is in legalmoves for player
    def isMoveLegal(self, move):
        #print("in is move legal", self.board.currentPlayer.getAllianceName(), self.getOpponent().isInCheck)
        for i in range(len(self.legalMoves)):
            if (self.legalMoves[i]==move):
                return True
        return False #return true if move legal

    def calculateAttacksOnTile(self, position, moves):
        return None




    def hasEscapeMoves(self):
#        print("move list size, has escape moves",len(self.legalMoves))
        for i in range(len(self.legalMoves)):
#            print("move made has escape moves",self.legalMoves[i])
            transition = self.makeMove(self.legalMoves[i])
#            print("move status has escape moves",transition.getMoveStatus().value, i)
            if(transition.getMoveStatus().value):
                return True
        return False

    def isCheck(self):
        return self.isInCheck

    def isCheckmate(self):
        return (self.isInCheck) and (not self.hasEscapeMoves())

    def isStalemate(self):
        return (not self.isInCheck) and (not self.hasEscapeMoves())

    def isCastled(self):
        return self.king.isCastled

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        pass

    def makeMove(self, move):

        if (not self.isMoveLegal(move)):
            return MoveTransition(self.board, self.board, move, MoveStatus.illegalMove)

#        print("here", move)
        player = self.board.currentPlayer
#        print("current player",player.isInCheck, player.getAllianceName())
#        print("current opponent", player.getOpponent().isInCheck, player.getOpponent().getAllianceName())
        transitionBoard = move.execute()
#        print("transitionBoard move",transitionBoard.getTransitionMove())
        ##############################################################
        #delete this section if checkmate not possible
        if (transitionBoard.getTransitionMove().isAttack()):
            if (transitionBoard.getTransitionMove().getAttackedPiece().pieceType=='K'):
                return MoveTransition(self.board, self.board, move, MoveStatus.kingKilled)

        if (transitionBoard.currentPlayer.getOpponent().isInCheck and
                transitionBoard.getTransitionMove().getBoard().currentPlayer.isInCheck):
            return MoveTransition(self.board, self.board, move, MoveStatus.illegalMove)
        ##############################################################
        kingAttacks = self.calculateAttacksOnTile(\
            transitionBoard.currentPlayer.getOpponent().getPlayerKing().getPiecePosition(),\
            transitionBoard.currentPlayer.legalMoves)

#        print("attacks on king",len(kingAttacks))
        if(not len(kingAttacks)==0):
            return MoveTransition(self.board, self.board, move, MoveStatus.leavesPlayerInCheck)

        return MoveTransition(self.board, transitionBoard, move, MoveStatus.done)



##########################################################

class blackPlayer(Player):

    def __init__(self, board, legalMoves, opponentLegalMoves):
        super().__init__(board, legalMoves)
        self.opponentLegalMoves = opponentLegalMoves
        self.legalMoves +=  self.calculateKingCastles(self.legalMoves,self.opponentLegalMoves)
        self.king = establishKing(self)
        self.isInCheck = not (len(self.calculateAttacksOnPiece(self.king, opponentLegalMoves))==0)


    def getActivePieces(self):
        return self.board.getBlackPieces()

    def getAlliance(self):
        import color
        return color.Alliance.black.value

    def getAllianceName(self):
        import color
        return color.Alliance.black

    def getOpponent(self):
        return self.board.getWhitePlayer()

    def calculateAttacksOnTile(self, position, moves):
        #return None
        attackMoves = []
        #print(moves)
        for pieceMove in moves:
            #print(pieceMoves)
            if (position == pieceMove.getDestinationCoordinate()):
                attackMoves.append(pieceMove)
        #print(attackMoves)
        return attackMoves

    def calculateAttacksOnPiece(self, piece, moves):
        #return None
        attackMoves = []
        if (hasattr(piece, 'piecePosition')):
            position = piece.getPiecePosition()
            for pieceMove in moves:
                if (position == pieceMove.getDestinationCoordinate()):
                    attackMoves.append(pieceMove)
            #print(attackMoves)
            return attackMoves
        else:
            return attackMoves

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        kingCastles = []
        if (hasattr(self.king, 'firstMove')):
#            print(1)
            if(self.king.isFirstMove() and (not self.isCheck())):
                #black kingsside castle
#                print(2)
                if((not self.board.getTile(5).occupied())and(not self.board.getTile(6).occupied())):
                    rookTile = self.board.getTile(7)
#                    print(3)
                    if (rookTile.occupied() and rookTile.getPiece().isFirstMove()):
#                        print(4)
                        if (len(self.calculateAttacksOnTile(5,opponentLegalMoves))==0 and \
                                len(self.calculateAttacksOnTile(6, opponentLegalMoves))==0 and\
                                rookTile.getPiece().pieceType=="r"):
#                            print(5)
                            #add castle move
                            import move
                            kingCastles.append(move.kingSideCastleMove(self.king, self.board, 6, \
                                    rookTile.getPiece(), rookTile.getTileCoordinate(), 5))
                #queen side castle
                if((not self.board.getTile(1).occupied())and(not self.board.getTile(2).occupied())and\
                        (not self.board.getTile(3).occupied())):
                    rookTile = self.board.getTile(0)
                    if (rookTile.occupied() and rookTile.getPiece().isFirstMove() \
                            and len(self.calculateAttacksOnTile(2, opponentLegalMoves))==0 and \
                            len(self.calculateAttacksOnTile(3, opponentLegalMoves))==0 and \
                            rookTile.getPiece().pieceType=="r"):

                        #add castle move
                        import move
                        kingCastles.append(move.queenSideCastleMove(self.king, self.board, 2, \
                                    rookTile.getPiece(), rookTile.getTileCoordinate(), 3))
        else:
            pass
        return kingCastles

##########################################################

class whitePlayer(Player):

    def __init__(self, board, legalMoves, opponentLegalMoves):
        super().__init__(board, legalMoves)
        self.opponentLegalMoves = opponentLegalMoves
        self.legalMoves += self.calculateKingCastles(self.legalMoves, self.opponentLegalMoves)
        self.king = establishKing(self)
        self.isInCheck = not len(self.calculateAttacksOnPiece(self.king, opponentLegalMoves))==0

    def getActivePieces(self):
        return self.board.getWhitePieces()

    def getAlliance(self):
        import color
        return color.Alliance.white.value

    def getAllianceName(self):
        import color
        return color.Alliance.white

    def getOpponent(self):
        return self.board.getBlackPlayer()

    def calculateAttacksOnTile(self, position, moves):
        #return None
        attackMoves = []

        for pieceMove in moves:
            if (position == pieceMove.getDestinationCoordinate()):
                attackMoves.append(pieceMove)
        #print(attackMoves)
        return attackMoves

    def calculateAttacksOnPiece(self, piece, moves):
        #return None
        attackMoves = []
        if (hasattr(piece, 'piecePosition')):
            position = piece.getPiecePosition()
            for pieceMove in moves:
                if (position == pieceMove.getDestinationCoordinate()):
                    attackMoves.append(pieceMove)
            #print(attackMoves)
            return attackMoves
        else:
            return attackMoves

    def calculateKingCastles(self, playerLegalMoves, opponentLegalMoves):
        kingCastles = []
        if (hasattr(self.king, 'firstMove')):
            if(self.king.isFirstMove() and (not self.isCheck())):
#                print(1)
                #white kingsside castle
                if((not self.board.getTile(61).occupied())and(not self.board.getTile(62).occupied())):
                    rookTile = self.board.getTile(63)
#                    print(2)
                    if (rookTile.occupied() and rookTile.getPiece().isFirstMove()):
#                        print(3)
                        if (len(self.calculateAttacksOnTile(61,opponentLegalMoves))==0 and \
                                len(self.calculateAttacksOnTile(62, opponentLegalMoves))==0 and\
                                rookTile.getPiece().pieceType=="r"):
#                            print(4)
                            #add castle move
                            import move
                            kingCastles.append(move.kingSideCastleMove(self.king, self.board, 62, \
                                    rookTile.getPiece(), rookTile.getTileCoordinate(), 59))
                #queen side castle
                if((not self.board.getTile(59).occupied())and(not self.board.getTile(58).occupied())and\
                        (not self.board.getTile(57).occupied())):
                    rookTile = self.board.getTile(56)
                    if (rookTile.occupied() and rookTile.getPiece().isFirstMove() \
                            and len(self.calculateAttacksOnTile(58, opponentLegalMoves))==0 and \
                            len(self.calculateAttacksOnTile(59, opponentLegalMoves))==0 and \
                            rookTile.getPiece().pieceType=="r"):
                        #add castle move
                        import move
                        kingCastles.append(move.queenSideCastleMove(self.king, self.board, 58, \
                                    rookTile.getPiece(), rookTile.getTileCoordinate(), 59))
        else:
            pass
        return kingCastles

##################################################################

#class MoveStatus:


class MoveTransition:
    def __init__(self,transitionBoard, executeBoard, move, moveStatus):
        self.transitionBoard = transitionBoard
        self.executeBoard = executeBoard
        self.move = move
        self.moveStatus = moveStatus

    def getMove(self):
        return self.move

    def getMoveStatus(self):
        return self.moveStatus

    def getTransitionBoard(self):
        return self.transitionBoard

    def getExecuteBoard(self):
        return self.executeBoard

    #def unMakeMove(self):
    #    return MoveTransition(self.getTransitionBoard(), self.undo(), self.getMove(), MoveStatus.done)


class MoveStatus(Enum):
    done = True
    illegalMove = False
    leavesPlayerInCheck = False
    kingKilled = False