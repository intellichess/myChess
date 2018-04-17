from collections import defaultdict
from math import log10, sqrt
import time
import sys
###############################################################################################
whiteWins = -1
blackWins = 1
stalemate = 2
inProgress = 0

##############################################################################################
from collections import defaultdict
checkmateBonus = 1000000
checkBonus = 50
mobilityMultiplier = 2
attackMultiplier = 2
allBishopBonus = 50
isolatedPawnPenalty = 15
doubledPawnPenalty = 35

class standardBoardEvaluator:
    def __init__(self, board):
        self.board = board

    def evaluate(self, board):
        return (self.scorePlayer(board, board.whitePlayer) - \
                self.scorePlayer(board, board.blackPlayer))

    def scorePlayer(self, board, player):
        a = self.pieceValue(player)
        b = self.mobilityRatio(player)
        c = self.kingThreats(player)
        e = self.isolatedPenalty(player)
        f = self.doubledPenalty(player)
        h = self.attack(player)
        i = self.castled(player)
        reduce = e+f
        return a + b + c + h + i - reduce

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

        return attackScore * attackMultiplier

    def mobilityRatio(self, player):
        curPlayer = self.mobility(player)
        oppPlayer = self.mobility(player.getOpponent())
        return (curPlayer/oppPlayer)*mobilityMultiplier

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
            return 0

    def kingThreats(self, player):
        if (player.getOpponent().isCheckmate()):
            return  checkmateBonus
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
        return double * doubledPawnPenalty


    def calculatePawnIsolatedPenalty(self, pawnTable):
        isolated = 0
        for i in range(8):
            if (len(pawnTable[i - 1]) == 0 and len(pawnTable[i + 1]) == 0):
                isolated += len(pawnTable[i])
        return isolated * isolatedPawnPenalty


    def isolatedPenalty(self, player):
        return self.calculatePawnIsolatedPenalty(self.createPawnColumnTable(self.calculatePlayerPawns(player)))


    def doubledPenalty(self, player):
        return self.calculatePawnDoublePenalty(self.createPawnColumnTable(self.calculatePlayerPawns(player)))

    def castled(self, player):
        if (player.isCastled()):
            return 60
        else:
            return 0


#############################################################################################

class Tree:
    def __init__(self, startBoard):
        self.root = Node(startBoard)

    def getRoot(self):
        return self.root

    def setRoot(self, root):
        self.root = root

    def addChild(self, parent, child):
        parent.getChildArray().append(child)

#########################################################################################

class Node:
    def __init__(self, state):
        self.state = state
        self.parent = None
        self.childList = []

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

    def setChildList(self, childList):
        self.childList = childList

    def getStateList(self):
        list = self.childList
        stateList = []
        for i in range(len(list)):
            stateList.append(list[i].getState())
        return stateList

    def getRandomChildNode(self):
        import random
        numMoves = len(self.childList)
        randomNum = random.randint(0,numMoves-1)
        return self.childList[randomNum]

    def getChildWithMaxScore(self):
        import operator
        #print("statelist size",len(self.getStateList()))
        state = max(self.getStateList(), key=operator.attrgetter('score'))
        for i in range(len(self.getChildList())):
            if (state!=self.getChildList()[i].getState()):
                pass
            else:
                return self.getChildList()[i]

    def getChildWithMaxScoreIndex(self):
        import operator
        #print("statelist size",len(self.getStateList()))
        state = max(self.getStateList(), key=operator.attrgetter('score'))
        for i in range(len(self.getChildList())):
            if (state!=self.getChildList()[i].getState()):
                pass
            else:
                return i


    def getChildWithMinScore(self):
        import operator
        #print("statelist size",len(self.getStateList()))
        state = min(self.getStateList(), key=operator.attrgetter('score'))
        for i in range(len(self.getChildList())):
            if (state!=self.getChildList()[i].getState()):
                pass
            else:
                #print(i)
                return self.getChildList()[i]

    def getChildWithMinScoreIndex(self):
        import operator
        #print("statelist size",len(self.getStateList()))
        state = min(self.getStateList(), key=operator.attrgetter('score'))
        for i in range(len(self.getChildList())):
            if (state!=self.getChildList()[i].getState()):
                pass
            else:
                #print(i)
                return i

###################################################################################

class State:
    def __init__(self, board):
        self.board = board
        self.player = board.currentPlayer.getAlliance()
        self.score = 0
        self.visitCount = 0
        self.move = None

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getMove(self):
        return self.move

    def setMove(self, move):
        self.move = move

    def getPlayer(self):
        return self.player

    def setPlayer(self, player):
        self.player = player

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board

    def getScore(self):
        return self.score

    def setScore(self, winScore):
        self.score = winScore

    def getVisitCount(self):
        return self.visitCount

    def setVisitCount(self, int):
        self.visitCount = int

    def incrementVisit(self):
        self.visitCount+=1

    def addScore(self, score):
        if (self.score != -sys.maxsize-1):
            self.score += score

    def togglePlayer(self):
        self.player = -1*self.player

    def getAllStates(self):
        import operator
        moveList = self.board.currentPlayer.legalMoves
        player = self.board.currentPlayer
        boardStates = []
        for i in range(len(moveList)):
            #check if move is legal and if it is, add it to the nodes
            moveTransition = player.makeMove(moveList[i])
            if (moveTransition.getMoveStatus().value):
                state = State(moveTransition.getExecuteBoard())
                state.setMove(moveTransition.move)
                boardStates.append(state)
        #boardStatesSorted = sorted(boardStates, key=operator.attrgetter('score'))
        return boardStates

    def randomPlay(self):
        import random
#        from test import prettyBoard
        board = self.board
        number = random.randint(0,len(board.currentPlayer.legalMoves)-1)
        transitionMove = board.currentPlayer.makeMove(board.currentPlayer.legalMoves[number])
        while (transitionMove.getMoveStatus().value!=True):
            #go back to last board and try another move
#            print("in loop")
            board = transitionMove.getTransitionBoard()
            number = random.randint(0,len(board.currentPlayer.legalMoves)-1)
            transitionMove = board.currentPlayer.makeMove(board.currentPlayer.legalMoves[number])
#        print("out of loop")
        #prettyBoard(transitionMove.getExecuteBoard().board)
        return transitionMove.getExecuteBoard()

###########################################################################

class monteCarloTreeSearch:
    def __init__(self, level, depth):
        self.level = level
        self.depth = depth

    def getDepth(self):
        return self.depth

    def setDepth(self, depth):
        self.depth = depth

    def getMillisForCurrentLevel(self):
        return 2*(self.level-1)+1

    def findNextMove(self, board):
        from test import Board, Builder
        tree = Tree(State(Board(Builder()).createStandardBoard()))
        rootNode = tree.getRoot()
        rootNode.getState().setBoard(board)
        rootPlayer = rootNode.getState().getBoard().currentPlayer.getAlliance()
        start = int(round(time.time()*1000))
        end = start + 60 * self.getMillisForCurrentLevel()

        while (int(round(time.time()*1000))<end):
            #select / run evaluation on all moves generated
            promisingNode = self.selectPromisingNode(rootNode)
         #   print("promisingNode",promisingNode.getState().getBoard().getTransitionMove())
            #expand / all moves in children are done

         #   print("status",promisingNode.getState().getBoard().getStatus())
            #doesnt take account of a player in check. allows piece to be taken by other piece
            if (promisingNode.getState().getBoard().getStatus()==inProgress):
                self.expandNode(promisingNode)

            #simulate / pick random node and simulate play
            nodeToExplore = promisingNode
         #   print("nodeToExplore",nodeToExplore.childList)
            if (len(promisingNode.getChildList()) > 0):
                nodeToExplore = promisingNode.getRandomChildNode()
            playResult = self.simulateRandomPlayout(nodeToExplore)
            #backProp
            self.backPropogation(nodeToExplore, playResult, rootPlayer, promisingNode)

        #print("after mcts",rootNode.getStateList())
        from test import prettyBoard
        #print("state lists")
        #for i in range(len(rootNode.getStateList())):
        #    print(i, rootNode.getStateList()[i].score)
        #    print("move", rootNode.getStateList()[i].getMove())
        #    prettyBoard(rootNode.getStateList()[i].board.board)

        #prettyBoard(rootNode.getState().getBoard().board)

        #childList is a hashtable and takes a child from one of the deeper nodes
        if (rootPlayer == -1):
            #winnerIndex = rootNode.getChildWithMaxScoreIndex()
            winnerNode = rootNode.getChildWithMaxScore()
        else:
            #winnerIndex = rootNode.getChildWithMinScoreIndex()
            winnerNode = rootNode.getChildWithMinScore()
        #print("winner board")
        #winningMove = rootNode.getState().getBoard().currentPlayer.legalMoves[winnerIndex]
        #prettyBoard(rootNode.getChildList()[winnerIndex].getState().getBoard().board)
        tree.setRoot(winnerNode)
        #print("child list length", len(tree.getRoot().getChildList()))
        return winnerNode.getState().getMove()

    def selectPromisingNode(self, rootNode):
        node = rootNode
#        print("inside select node", node)
        while (len(node.getChildList())!=0):
            #print("inside select promising node",node)
            node = findBestNodeWithUCT(node)
        return node

    def expandNode(self, node):
        allStates = node.getState().getAllStates()
        for state in allStates:
            newNode = Node(state)
            newNode.setParent(node)
            node.getChildList().append(newNode)
#        self.setDepth(self.depth-1)

    def simulateRandomPlayout(self, node):
        tempNode = node
        tempState = tempNode.getState()
        boardStatus = tempState.getBoard().getStatus()
        depthVal = self.getDepth()
        #print("depth variable",depthVal)

        if (boardStatus == -1*tempState.getPlayer()):
            from test import prettyBoard
            print("tempnode stuff", boardStatus)
            prettyBoard(tempNode.getState().getBoard().board)
            print(tempNode)
            print(tempNode.getParent())
            print(tempNode.getParent().getState())
            tempNode.getParent().getState().setWinScore(-1*sys.maxsize-1)
            return boardStatus

        count = 0
        while (boardStatus==inProgress and self.depth>0):
            tempState.setBoard(tempState.randomPlay())
            boardStatus = tempState.getBoard().getStatus()
#            print("inside while loop", boardStatus, count)
#            count+=1
            self.setDepth(self.depth-1)
        self.setDepth(depthVal)

        return boardStatus


    def backPropogation(self, nodeToExplore, playerNo, rootPlayer, promisingNode):
        tempNode = nodeToExplore
        score = standardBoardEvaluator(tempNode.getState().getBoard()).evaluate(tempNode.getState().getBoard())
        while (tempNode!=None):
            #print("inside backProp", score, tempNode.getState().getPlayer(), playerNo, rootPlayer)
            tempNode.getState().incrementVisit()
            if (tempNode.getState().getPlayer()==playerNo or tempNode.getState().getPlayer()==-1*rootPlayer):
                tempNode.getState().addScore(score)
            tempNode = tempNode.getParent()
        #print("promising node score", promisingNode.getState().getScore(), -1*rootPlayer)
        #from test import prettyBoard
        #prettyBoard(promisingNode.getState().getBoard().board)
        return promisingNode

#################################################################################

def uctValue(totalVisit, nodeScore, nodeVisit):
    if (nodeVisit==0):
        return sys.maxsize
    return (nodeScore / nodeVisit) + 1.41 * sqrt(log10(totalVisit) / nodeVisit)

def findBestNodeWithUCT(node):
    parentVisit = node.getState().getVisitCount()
    #change this to something else, wont work
    boardStates = node.getChildList() #node.getState().getAllStates()
    bestValue = 0
    bestState = None
    for i in range(len(boardStates)):
        uctVal = uctValue(parentVisit, boardStates[i].getState().getScore(),
                          boardStates[i].getState().getVisitCount())
        if (uctVal>bestValue):
            bestValue = uctVal
            bestState = boardStates[i]
    return bestState
        #return max(boardStates, key=UCT.uctValue(parentVisit, ))