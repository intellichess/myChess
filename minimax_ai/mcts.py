from collections import defaultdict
from math import log10, sqrt
import time
import sys
checkmateBonus = 10000
checkBonus = 50
mobilityMultiplier = 2
attackMultiplier = 2
allBishopBonus = 50
isolatedPawnPenalty = 15
doubledPawnPenalty = 35

def depthBonus(depth):
    if (depth==0):
        return 1
    else:
        return 100*depth

class standardBoardEvaluator:
    def __init__(self, board):
        self.board = board

    def evaluate(self, board):
        return (self.scorePlayer(board, board.whitePlayer) - \
                self.scorePlayer(board, board.blackPlayer))

    def scorePlayer(self, board, player):
        a = self.pieceValue(player)
        b = self.mobilityRatio(player)*mobilityMultiplier
        c = self.kingThreats(player)
        e = self.isolatedPenalty(player) * isolatedPawnPenalty #self.pawnBlock(player, board.board) * self.pawnDouble(player) * isolatedPawnPenalty #
        f = self.doubledPenalty(player) * doubledPawnPenalty #self.pawnIsolated(player, board.board) * doubledPawnPenalty
        g = 0 #self.calcKingTropism(player).tropismScore()
        h = self.attack(player) * attackMultiplier
        i = self.castled(player)
        reduce = e+f
#        print(player.getAllianceName(), d)
        return a + b + c + h + i - reduce
               #+ self.castled(player)

    def pieceValue(self, player):
        pieceValueScore = 0
        numBishops = 0
        pieceList = player.getActivePieces()
#        print("player", player.getAllianceName())
        for i in range(len(pieceList)):
            pieceValueScore += pieceList[i].pieceValue + pieceList[i].locationBonus()
            if(pieceList[i].pieceType=="b"):
                numBishops+=1
        if (numBishops == 2):
            pieceValueScore += allBishopBonus
        return pieceValueScore

    def attack(self,player):
        attackScore = 0
        for i in range(len(player.legalMoves)):
            if(player.legalMoves[i].isAttack()):
#                        print("in attack",player.legalMoves[i][j])
                movedPiece = player.legalMoves[i].movedPiece
                attackedPiece = player.legalMoves[i].getAttackedPiece()
                if (movedPiece.pieceValue<=attackedPiece.pieceValue):
                    attackScore+=1

        return attackScore

    def mobilityRatio(self, player):
        curPlayer = self.mobility(player)
        oppPlayer = self.mobility(player.getOpponent())
        return curPlayer/oppPlayer

    def mobility(self, player):
        mobilityScore = 0
#        print("mobility", player.getAllianceName())
        for i in range(len(player.legalMoves)):
            mobilityScore += 1
#        print("mobilityScore",mobilityScore)
        return mobilityScore

    def check(self, player):
#        print("opponent in check",player.getOpponent().getAllianceName(),player.getOpponent().isInCheck)
        if (player.getOpponent().isInCheck):
#            print("check",50)
            return checkBonus
        else:
#            print("check",0)
            return

    def kingThreats(self, player):
        if (player.getOpponent().isCheckmate()):
            return  checkmateBonus * 100
        else:
            return self.check(player)

    def calculatePlayerPawns(self, player):
        pawnList = []
        for piece in player.getActivePieces():
            if (piece.pieceType == "p"):
                pawnList.append([piece])
        return pawnList


    def createPawnColumnTable(self, pawnList):
        pawnColumnList = defaultdict(list)
        for i in range(len(pawnList)):
            pawnColumnList[pawnList[i][0].piecePosition % 8] = pawnList[i]
        return pawnColumnList


    def calculatePawnDoublePenalty(self, pawnTable):
        double = 0
        for i in range(8):
            if (len(pawnTable[i]) > 1):
                double += len(pawnTable[i])
        return double


    def calculatePawnIsolatedPenalty(self, pawnTable):
        isolated = 0
        for i in range(8):
            if (len(pawnTable[i - 1]) == 0 and len(pawnTable[i + 1]) == 0):
                isolated += len(pawnTable[i])
        return isolated


    def isolatedPenalty(self, player):
        return self.calculatePawnIsolatedPenalty(self.createPawnColumnTable(self.calculatePlayerPawns(player)))


    def doubledPenalty(self, player):
        return self.calculatePawnDoublePenalty(self.createPawnColumnTable(self.calculatePlayerPawns(player)))

    def castled(self, player):
        if (player.isCastled()):
            return 60
        else:
            return 0
###############################################################################################

class Tree:
    def __init__(self, startBoard):
        self.root = Node(startBoard, None, startBoard.currentPlayer.legalMoves)

    def getRoot(self):
        return self.root

    def setRoot(self, root):
        self.root = root

class Node:
    def __init__(self, state, parent, childList):
        self.state = state
        self.parent = parent
        self.childList = childList

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getChildList(self):
        return self.childList

    def setState(self, state):
        self.state = state

    def setParent(self, parent):
        self.parent = parent

class State:
    def __init__(self, board):
        self.board = board
        self.score = standardBoardEvaluator(board)
        self.visitCount = self.getVisitCount()

    def getBoard(self):
        return self.board

    def getScore(self):
        return self.score

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self, int):
        self.visitCount = int

    def incrementVisit(self):
        self.visitCount+=1

    def getAllStates(self):
        moveList = self.board.currentPlayer.legalMoves
        boardStates = []
        for i in range(len(moveList)):
            boardStates.append(State(moveList.execute()))
        return boardStates

    def randomPlay(self, boardStates):
        import random
        number = random.randint(0,len(boardStates))
        return boardStates[number]

    def setBoard(self, board):
        self.board = board

class monteCarloTreeSearch:
    def __init__(self, level):
        self.level = level

    def getMillisForCurrentLevel(self):
        return 2*(self.level-1)+1

    def findNextMove(self, board):
        from test import Board, Builder
        tree = Tree(Board(Builder()).createStandardBoard())
        rootNode = tree.getRoot()
        rootNode.getState().setBoard(board)
        start = int(round(time.time()*1000))
        end = start + 60 * self.getMillisForCurrentLevel()
        while (int(round(time.time()*1000))<end):
            #select / run evaluation on all moves generated
            promisingNode = selectPromisingNode(rootNode)
            #expand / all moves in children are done
            if (promisingNode.getState().getBoard())

class UCT:
    def uctValue(self, totalVisit, nodeScore, nodeVisit):
        if (nodeVisit==0):
            return sys.maxsize
        return (nodeScore / nodeVisit) + 1.41 * sqrt(log10(totalVisit) / nodeVisit)

    def findBestNodeWithUCT(self, node):
        parentVisit = node.getState().get