from collections import defaultdict
from math import log10, sqrt
import time
import sys
###############################################################################################
whiteWins = -1
blackWins = 1
stalemate = 0
inProgress = 2

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

    def getRandomChildNode(self):
        import random
        numMoves = len(self.childList)
        randomNum = random.randint(0,numMoves)
        return self.childList[randomNum]

    def getChildWithMaxScore(self):
        import operator
        return max(self.childList, key=operator.attrgetter('score'))

###################################################################################

class State:
    def __init__(self, board):
        self.board = board
        self.score = self.getScore()
        self.visitCount = self.getVisitCount()
        self.player = board.currentPlayer.getAlliance()

    def getPlayer(self):
        return self.player

    def setPlayer(self, player):
        self.player = player

    def getBoard(self):
        return self.board

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
                boardStates.append(State(moveTransition.getExecuteBoard()))
        #boardStatesSorted = sorted(boardStates, key=operator.attrgetter('score'))
        return boardStates

    def randomPlay(self, boardStates):
        import random
        number = random.randint(0,len(boardStates))
        return boardStates[number]

    def setBoard(self, board):
        self.board = board

###########################################################################

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
            promisingNode = self.selectPromisingNode(rootNode)
            #expand / all moves in children are done
            if (promisingNode.getState().getBoard().getStatus()==inProgress):
                self.expandNode(promisingNode)

            #simulate / pick random node and simulate play
            nodeToExplore = promisingNode
            if (len(promisingNode.getChildArray) > 0):
                nodeToExplore = promisingNode.getRandomChildNode()
            playResult = self.simulateRandomPlayout(nodeToExplore)
            #backProp
            self.backPropogation(nodeToExplore, playResult)

        winnerNode = rootNode.getChildWithMaxScore()
        tree.setRoot(winnerNode)
        return winnerNode.getState().getBoard()

    def selectPromisingNode(self, rootNode):
        node = rootNode
        while (len(node.getChildList())!=0):
            node = findBestNodeWithUCT(node)
        return node

    def expandNode(self, node):
        allStates = node.getState().getAllStates()
        for state in allStates:
            newNode = Node(state)
            newNode.getState().setPlayer(node.getState().currentPlayer.getOpponent().getAlliance())
            newNode.setParent(node)

    def simulateRandomPlayout(self, node):
        tempNode = Node(node)
        tempState = tempNode.getState()
        boardStatus = tempState.getBoard().getStatus()

        if (boardStatus == -1*tempState.getPlayer()):
            tempNode.getParent().getState().setWinScore(-sys.maxsize-1)
            return boardStatus

        while (boardStatus==inProgress):
            tempState.togglePlayer()
            tempState.randomPlay()
            boardStatus = tempState.getBoard().getStatus()

        return boardStatus


    def backPropogation(self, nodeToExplore, playerNo):
        tempNode = nodeToExplore
        while (tempNode!=None):
            tempNode.getState().incrementVisit()
            if (tempNode.getState().getPlayer()==playerNo):
                tempNode.getState().addScore(10)
            tempNode = tempNode.getParent()

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
        uctValue = uctValue(parentVisit, boardStates[i].getScore(), boardStates[i].getVisitCount())
        if (uctValue>bestValue):
            bestValue = uctValue
            bestState = boardStates[i]
    return bestState
        #return max(boardStates, key=UCT.uctValue(parentVisit, ))