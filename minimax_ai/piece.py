from enum import Enum
#from test import occupiedTile
#from test import emptyTile
from color import Alliance
from move import majorMove
from move import attackMove
import move
import color


#boardutils
#row8 = black
#row1 = white
from boardutils import col1, col2, col7, col8, row2, row7, row1, row8

#beware of duplicates

def isTileOccupied(self):
    import test
    if (test.occupiedTile.occupied()):
        return True
    else:
        return False

class PieceType(Enum):
    knight = "N"
    pawn = "p"
    king = "K"
    queen = "Q"
    rook = "R"
    bishop = "B"

class Piece:

    #add firstMove to other subclasses
    def __init__(self, piecePosition, Alliance):
        self.piecePosition = piecePosition
        self.Alliance = Alliance
        self.firstMove = True
        self.pieceType = ""
        self.possibleMoves = []
        self.pieceValue = 0
        #more stuff here

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def locationBonus(self):
        return None

    def getPieceValue(self):
        return self.pieceValue

    def isFirstMove(self):
        return self.firstMove

    def findLegalMoves(self, board):
        pass

    def getPiecePosition(self):
        return self.piecePosition

    def getPieceAlliance(self):
        return self.Alliance

    def findLegalMoves(self, board):
        pass
##isValidTileCoordinate
    def isValidCoordinate(self):
        return (0 <= self.piecePosition < 64)

    def getPieceType(self):
        return self.pieceType

    def isKing(self):
        if (self.pieceType.value == "K"):
            return True
        else:
            return False

    def movePiece(self, move):
        pass


########################################################

class bishop(Piece):
    possibleMoves=[-9,-7,7,9]
    def __init__(self,piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.bishop.value
        self.possibleMoves = [-9,-7,7,9]
        self.firstMove = True
        self.pieceValue = 300

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isFirstColumnExclusion(self, currentPosition, canidateOffset):
        return col1[currentPosition] and ((canidateOffset==-9)or(canidateOffset==7))


    def isEighthColumnExclusion(self, currentPosition, canidateOffset):
        return col8[currentPosition] and ((canidateOffset==-7)or(canidateOffset==9))


    def findLegalMoves(self, board):
        legalMoves = []
        for i in range(4):
            canidateDestinationCoordinate = self.piecePosition
            while (0<=canidateDestinationCoordinate<64):

                if(self.isFirstColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])or \
                        self.isEighthColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])):
                    break

                canidateDestinationCoordinate += self.possibleMoves[i]
                if (bishop(canidateDestinationCoordinate,self.Alliance).isValidCoordinate()):

                    destinationTile = board.board[canidateDestinationCoordinate]

                    if (destinationTile.isTileOccupied() is False):  # if no piece there
                        # move
                        legalMoves.append(majorMove(self, board, canidateDestinationCoordinate))
                    else:
                        pieceOnTile = destinationTile.getPiece()
                        pieceAlliance = destinationTile.getPiece().getPieceAlliance()

                        if (self.Alliance != pieceAlliance):
                            # capture
                            legalMoves.append(attackMove(self, board, canidateDestinationCoordinate, pieceOnTile))
                        break

        return legalMoves

    def movePiece(self, move):
        piece = bishop(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def locationBonus(self):
        from boardutils import bishopBonus
        return bishopBonus(self.piecePosition, self.Alliance.value)
##########################################

class knight(Piece):
    possibleMoves = [-17,-15,-10,-6,6,10,15,17]
    def __init__(self, piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.knight.value
        self.possibleMoves = [-17,-15,-10,-6,6,10,15,17]
        self.firstMove =True
        self.pieceValue=300

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isFirstColumnExclusion(self, currentPosition, canidateOffset):
        return col1[currentPosition] and ((canidateOffset==-17)or(canidateOffset==-10)or \
                                          (canidateOffset==6)or(canidateOffset==15))

    def isSecondColumnExclusion(self, currentPosition, canidateOffset):
        return col2[currentPosition] and ((canidateOffset==-10)or(canidateOffset==6))

    def isSeventhColumnExclusion(self, currentPosition, canidateOffset):
        return col7[currentPosition] and ((canidateOffset==-6)or(canidateOffset==10))

    def isEighthColumnExclusion(self, currentPosition, canidateOffset):
        return col8[currentPosition] and ((canidateOffset==-15)or(canidateOffset==-6)or \
                                          (canidateOffset==10)or(canidateOffset==17))

    def findLegalMoves(self, board):
        legalMoves = []
        for i in range(8):
            destination = self.piecePosition + self.possibleMoves[i]
            if knight(destination,self.Alliance).isValidCoordinate(): #if valid move
                #use python dictionary
                destinationTile = board.board[destination]

                #print(self.piecePosition, destination)

                #possibleMoves[i]
                if (self.isFirstColumnExclusion(self.piecePosition, self.possibleMoves[i])or \
                        self.isSecondColumnExclusion(self.piecePosition, self.possibleMoves[i])or \
                        self.isSeventhColumnExclusion(self.piecePosition,self.possibleMoves[i]) or \
                        self.isEighthColumnExclusion(self.piecePosition, self.possibleMoves[i])):
                    continue

                if (destinationTile.isTileOccupied() is False): #if no piece there
                    #move
                    legalMoves.append(majorMove(self,board,destination))
                else:
                    pieceOnTile = destinationTile.getPiece()
                    pieceAlliance = destinationTile.getPiece().getPieceAlliance()

                    if (self.Alliance != pieceAlliance):
                        #capture
                        legalMoves.append(attackMove(self,board,destination,pieceOnTile))

        return legalMoves

    def movePiece(self, move):
        piece = knight(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def locationBonus(self):
        from boardutils import knightBonus
        return knightBonus(self.piecePosition, self.Alliance.value)
##################################################

class rook(Piece):

    def __init__(self, piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.rook.value
        self.possibleMoves = possibleMoves = [-8,-1,1,8]
        self.firstMove = True
        self.pieceValue=500

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isFirstColumnExclusion(self, currentPosition, canidateOffset):
        return col1[currentPosition] and ((canidateOffset==-1))


    def isEighthColumnExclusion(self, currentPosition, canidateOffset):
        return col8[currentPosition] and ((canidateOffset==1))


    def findLegalMoves(self, board):
        legalMoves = []
        for i in range(4):
            canidateDestinationCoordinate = self.piecePosition
            while (0<=canidateDestinationCoordinate<64):

                if(self.isFirstColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])or \
                        self.isEighthColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])):
                    break

                canidateDestinationCoordinate += self.possibleMoves[i]
                if (rook(canidateDestinationCoordinate,self.Alliance).isValidCoordinate()):

                    destinationTile = board.board[canidateDestinationCoordinate]

                    if (destinationTile.isTileOccupied() is False):  # if no piece there
                        # move
                        legalMoves.append(majorMove(self, board, canidateDestinationCoordinate))
                    else:
                        pieceOnTile = destinationTile.getPiece()
                        pieceAlliance = destinationTile.getPiece().getPieceAlliance()

                        if (self.Alliance != pieceAlliance):
                            # capture
                            legalMoves.append(attackMove(self, board, canidateDestinationCoordinate, pieceOnTile))
                        break

        return legalMoves

    def movePiece(self, move):
        piece = rook(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def locationBonus(self):
        from boardutils import rookBonus
        return rookBonus(self.piecePosition, self.Alliance.value)
#############################################

class queen(Piece):
    possibleMoves = [-9,-8,-7,-1,1,7,8,9]
    def __init__(self, piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.queen.value
        self.possibleMoves = [-9,-8,-7,-1,1,7,8,9]
        self.firstMove = True
        self.pieceValue=900

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def isFirstColumnExclusion(self, currentPosition, canidateOffset):
        return col1[currentPosition] and ((canidateOffset==-1)or(canidateOffset==-9)or(canidateOffset==7))


    def isEighthColumnExclusion(self, currentPosition, canidateOffset):
        return col8[currentPosition] and ((canidateOffset==1)or(canidateOffset==9)or(canidateOffset==-7))


    def findLegalMoves(self, board):
        legalMoves = []
        for i in range(8):
            canidateDestinationCoordinate = self.piecePosition
            while (0<=canidateDestinationCoordinate<64):

                if(self.isFirstColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])or \
                        self.isEighthColumnExclusion(canidateDestinationCoordinate, self.possibleMoves[i])):
                    break

                canidateDestinationCoordinate += self.possibleMoves[i]
                if (queen(canidateDestinationCoordinate,self.Alliance).isValidCoordinate()):

                    destinationTile = board.board[canidateDestinationCoordinate]

                    if (destinationTile.isTileOccupied() is False):  # if no piece there
                        # move
                        legalMoves.append(majorMove(self, board, canidateDestinationCoordinate))
                    else:
                        pieceOnTile = destinationTile.getPiece()
                        pieceAlliance = destinationTile.getPiece().getPieceAlliance()

                        if (self.Alliance != pieceAlliance):
                            # capture
                            legalMoves.append(attackMove(self, board, canidateDestinationCoordinate, pieceOnTile))
                        break
        return legalMoves

    def movePiece(self, move):
        piece = queen(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def locationBonus(self):
        from boardutils import queenBonus
        return queenBonus(self.piecePosition, self.Alliance.value)
###################################################

class pawn(Piece):

#    possibleMoves = [8, 16, 7, 9]
    def __init__(self, piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.pawn.value
        self.possibleMoves = [8,16,7,9]
        self.firstMove =True
        self.pieceValue=100

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def isFirstColumnExclusion(self, currentPosition, canidateOffset, alliance):
        if (alliance==1):
            return col1[currentPosition] and ((canidateOffset == 9))
        else:
            return col1[currentPosition] and ((canidateOffset == 7))

    def isEighthColumnExclusion(self, currentPosition, canidateOffset, alliance):
        if (alliance==1):
            return col8[currentPosition] and ((canidateOffset == 7))
        else:
            return col8[currentPosition] and ((canidateOffset == 9))

    def findLegalMoves(self, board):
        from boardutils import col1, col2, col7, col8, row2, row7
        legalMoves = []
        for i in range(4):

            canidateDestinationCoordinate = self.piecePosition + (self.Alliance.value*self.possibleMoves[i])

            #print(i, canidateDestinationCoordinate, self.piecePosition)
            #if piece moves off board skip i and move to next i

            if(not (0<=canidateDestinationCoordinate<64)):
                continue

            if(self.possibleMoves[i]==8 and (not board.board[canidateDestinationCoordinate].occupied())):
                #promotion code here
                if ((self.Alliance.value==1 and row8[canidateDestinationCoordinate]) or\
                        (self.Alliance.value==-1 and row1[canidateDestinationCoordinate])):
                    from move import pawnMove, pawnPromotion
                    legalMoves.append(pawnPromotion(pawnMove(self,board,canidateDestinationCoordinate), self, board, canidateDestinationCoordinate))

                else:
                    from move import pawnMove
                    legalMoves.append(pawnMove(self, board, canidateDestinationCoordinate))

            elif(self.possibleMoves[i]==16 and self.isFirstMove() and \
                 ((row2[self.piecePosition] and self.Alliance.value==1) \
                 or (row7[self.piecePosition] and self.Alliance.value==-1))):
                behindCanidateDestination = self.piecePosition + (self.Alliance.value*8)
                if((not board.board[behindCanidateDestination].occupied()) and \
                    (not board.board[canidateDestinationCoordinate].occupied())):
                    from move import pawnJump
                    legalMoves.append(pawnJump(self, board, canidateDestinationCoordinate))


            elif(self.possibleMoves[i]==7 and \
                (not (col8[self.piecePosition] and self.Alliance.value==-1)) or \
                (col1[self.piecePosition] and self.Alliance.value==1)):
            #elif(self.isFirstColumnExclusion(self.piecePosition,self.possibleMoves[i],self.Alliance.value)):

                if(board.board[canidateDestinationCoordinate].occupied()):
                    pieceOnCanidate = board.board[canidateDestinationCoordinate].getPiece()
                    if(self.Alliance!=pieceOnCanidate.Alliance):
                        if ((self.Alliance.value == 1 and row8[canidateDestinationCoordinate]) or \
                                (self.Alliance.value == -1 and row1[canidateDestinationCoordinate])):
                            from move import pawnPromotion, pawnAttackMove
                            legalMoves.append(pawnPromotion(pawnAttackMove(self, board, canidateDestinationCoordinate, pieceOnCanidate), self, board, canidateDestinationCoordinate))
                        else:
                        #pass
                        #take piece
                            from move import pawnAttackMove
                            legalMoves.append(pawnAttackMove(self, board, canidateDestinationCoordinate,pieceOnCanidate))
                elif(board.getEnPassantPawn() is not None):
                    if(board.getEnPassantPawn().getPiecePosition() == (self.piecePosition+(self.Alliance.value*-1))):
                        pieceOnCanidate = board.getEnPassantPawn()
                        if (self.Alliance!=pieceOnCanidate.Alliance):

                            from move import pawnEnPassantAttackMove
                            legalMoves.append(pawnEnPassantAttackMove(self, board, canidateDestinationCoordinate, pieceOnCanidate))


            elif(self.possibleMoves[i]==9 and \
                (not(col1[self.piecePosition] and self.Alliance.value==-1)) or \
                (col8[self.piecePosition] and self.Alliance.value==1)):
            #elif(self.isEighthColumnExclusion(self.piecePosition,self.possibleMoves[i],self.Alliance.value)):

                if (board.board[canidateDestinationCoordinate].isTileOccupied()):
                    pieceOnCanidate = board.board[canidateDestinationCoordinate].getPiece()
                    if (self.Alliance != pieceOnCanidate.Alliance):
                        if ((self.Alliance.value == 1 and row8[canidateDestinationCoordinate]) or \
                                (self.Alliance.value == -1 and row1[canidateDestinationCoordinate])):
                            from move import pawnAttackMove, pawnPromotion
                            legalMoves.append(pawnPromotion(pawnAttackMove(self, board, canidateDestinationCoordinate,pieceOnCanidate), self, board, canidateDestinationCoordinate))
                        else:
                            #pass
                            # take piece
                            from move import pawnAttackMove
                            legalMoves.append(pawnAttackMove(self, board, canidateDestinationCoordinate,pieceOnCanidate))
                elif (board.getEnPassantPawn() is not None):
                    if (board.getEnPassantPawn().getPiecePosition() == (self.piecePosition - (self.Alliance.value * -1))):
                        pieceOnCanidate = board.getEnPassantPawn()
                        if (self.Alliance != pieceOnCanidate.Alliance):
                            from move import pawnEnPassantAttackMove
                            legalMoves.append(pawnEnPassantAttackMove(self, board, canidateDestinationCoordinate, pieceOnCanidate))

        return legalMoves

    def movePiece(self, move):
        piece = pawn(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def getPromotionPiece(self):
        #check if ai or person, if person, input pieceType if ai, keep queen
        return queen(self.piecePosition, self.Alliance)

    def locationBonus(self):
        from boardutils import pawnBonus
        return pawnBonus(self.piecePosition, self.Alliance.value)
##################################################

class king(Piece):
    possibleMoves = [-9,-8,-7,-1,1,7,8,9]
    def __init__(self, piecePosition, Alliance):
        super().__init__(piecePosition, Alliance)
        self.pieceType = PieceType.king.value
        self.possibleMoves = [-9,-8,-7,-1,1,7,8,9]
        self.firstMove = True
        self.isCastled = False
        self.pieceValue = 10000

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def isFirstColumnExclusion(self, currentPosition, canidateOffset):
        return col1[currentPosition] and ((canidateOffset==-9)or(canidateOffset==-1)or \
                                          (canidateOffset==7))

    def isEighthColumnExclusion(self, currentPosition, canidateOffset):
        return col8[currentPosition] and ((canidateOffset==9)or(canidateOffset==1)or \
                                          (canidateOffset==-7))

    def findLegalMoves(self, board):
        legalMoves = []

        for i in range(8):
            canidateDestinatonCoordinate = self.piecePosition + self.possibleMoves[i]

            if (self.isFirstColumnExclusion(self.piecePosition, self.possibleMoves[i]) or \
                    self.isEighthColumnExclusion(self.piecePosition, self.possibleMoves[i])):
                continue

            if(king(canidateDestinatonCoordinate,self.Alliance).isValidCoordinate()):
                canidateDestinatonTile = board.board[canidateDestinatonCoordinate]
                if (canidateDestinatonTile.isTileOccupied() is False): #if no piece there
                    #move
                    legalMoves.append(majorMove(self,board,canidateDestinatonCoordinate))
                else:
                    pieceOnTile = canidateDestinatonTile.getPiece()
                    pieceAlliance = canidateDestinatonTile.getPiece().getPieceAlliance()

                    if (self.Alliance != pieceAlliance):
                        #capture
                        legalMoves.append(attackMove(self,board,canidateDestinatonCoordinate,pieceOnTile))


        return legalMoves

    def movePiece(self, move):
        piece = king(move.getDestinationCoordinate(), move.getMovedPiece().getPieceAlliance())
        piece.firstMove = False
        return piece

    def locationBonus(self):
        from boardutils import kingBonus
        return kingBonus(self.piecePosition, self.Alliance.value)
########################################################
