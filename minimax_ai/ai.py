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
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def evaluate(self, board, depth):
        return (self.scorePlayer(board, board.whitePlayer, depth) - \
                self.scorePlayer(board, board.blackPlayer, depth))

    def scorePlayer(self, board, player, depth):
        a = self.pieceValue(player)
        b = self.mobilityRatio(player)*mobilityMultiplier
        c = self.kingThreats(player, depth)
        d = self.pawnBlock(player, board.board)
        e = self.pawnDouble(player) * doubledPawnPenalty
        f = self.pawnIsolated(player, board.board)*isolatedPawnPenalty
        g = 0 #self.calcKingTropism(player).tropismScore()
        h = self.attack(player) * attackMultiplier
        i = 0 #self.castled(player)
        reduce = d+e+f
#        print(player.getAllianceName(), d)
        return a + b + c + h - reduce
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
            if(numBishops==2):
                pieceValueScore+=allBishopBonus
#        print("pieceValueScore",pieceValueScore)
        return pieceValueScore

    def attack(self,player):
        attackScore = 0
        for i in range(len(player.legalMoves)):
            if (player.legalMoves[i] == 0):
                pass
            else:
                for j in range(len(player.legalMoves[i])):
                    if(player.legalMoves[i][j].isAttack()):
#                        print("in attack",player.legalMoves[i][j])
                        movedPiece = player.legalMoves[i][j].movedPiece
                        attackedPiece = player.legalMoves[i][j].getAttackedPiece()
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
            if (player.legalMoves[i] == 0):
                pass
            else:
                for j in range(len(player.legalMoves[i])):
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

    def checkmate(self, player, depth):
#        print("opponent in mate",player.getOpponent().getAllianceName(),player.getOpponent().isCheckmate())
        if (player.getOpponent().isCheckmate()):
#            print("checkmate",10000*depthBonus(depth))
            return checkmateBonus * depthBonus(depth)
        else:
#            print("checkmate",0)
            return 0

    def kingThreats(self, player, depth):
        if (player.getOpponent().isCheckmate()):
            return  checkmateBonus * depthBonus(depth)
        else:
            return self.check(player)

    def pawnBlock(self, player, board):
        block = 0
        for i in range(len(player.getActivePieces())):
            if (player.getActivePieces()[i].pieceType=="p"):
                piece = player.getActivePieces()[i]
                pos = player.getActivePieces()[i].piecePosition
                canidate = pos + piece.Alliance.value*8
#                print("block pawn", piece, pos, canidate, board[canidate].occupied())
                if(board[canidate].occupied()):
                    block+=1
        return block

    def pawnIsolated(self, player, board):
        isolated = 0
        for i in range(len(player.getActivePieces())):
            if (player.getActivePieces()[i].pieceType == "p"):
                piece = player.getActivePieces()[i]
                pos = player.getActivePieces()[i].piecePosition
                from boardutils import col1, col8
                if(col1[pos]):
                    if (board[pos+1].occupied()):
                        if (board[pos+1].getPiece().pieceType=="p" and board[pos+1].getPiece().Alliance.value == piece.Alliance.value):
                            pass
                        else:
                            isolated +=1
                    else:
                        isolated +=1
                elif(col8[pos]):
                    if (board[pos-1].occupied()):
                        if (board[pos-1].getPiece().pieceType=="p" and board[pos-1].getPiece().Alliance.value == piece.Alliance.value):
                            pass
                        else:
                            isolated +=1
                    else:
                        isolated +=1
                else:
                    if (board[pos+1].occupied() or board[pos-1].occupied()):
                        if (board[pos + 1].occupied()):
                            if (board[pos + 1].getPiece().pieceType == "p" and board[
                                pos + 1].getPiece().Alliance.value == piece.Alliance.value):
                                pass
                            else:
                                isolated += 1
                        elif (board[pos - 1].occupied()):
                            if (board[pos - 1].getPiece().pieceType == "p" and board[
                                pos - 1].getPiece().Alliance.value == piece.Alliance.value):
                                pass
                            else:
                                isolated += 1
                        else:
                            isolated += 1
                    else:
                        isolated += 1

        return isolated

    def pawnDouble(self, player):
        double = 0
        for i in range(len(player.getActivePieces())):
            if (player.getActivePieces()[i].pieceType=="p"):
                for j in range(len(player.getActivePieces())):
                    if (player.getActivePieces()[j].pieceType=="p" and player.getActivePieces()[i]!=player.getActivePieces()[j]):
                        pos1 = player.getActivePieces()[i].piecePosition
                        pos2 = player.getActivePieces()[j].piecePosition
                        if ((pos1 - pos2)%8==0):
                            double +=1
                    else:
                        pass
        return double

    def getCollumn(self, coordinate):
        from boardutils import col1,col2,col3,col4,col5,col6,col7,col8
        if (col1[coordinate]):
            return 1
        elif (col2[coordinate]):
            return 2
        elif (col3[coordinate]):
            return 3
        elif (col4[coordinate]):
            return 4
        elif (col5[coordinate]):
            return 5
        elif (col6[coordinate]):
            return 6
        elif (col7[coordinate]):
            return 7
        elif (col8[coordinate]):
            return 8

    def getRow(self, coordinate):
        from boardutils import row1,row2,row3,row4,row5,row6,row7,row8
        if (row1[coordinate]):
            return 1
        elif (row2[coordinate]):
            return 2
        elif (row3[coordinate]):
            return 3
        elif (row4[coordinate]):
            return 4
        elif (row5[coordinate]):
            return 5
        elif (row6[coordinate]):
            return 6
        elif (row7[coordinate]):
            return 7
        elif (row8[coordinate]):
            return 8

    def chebyshevDistance(self, kingTile, enemyTile):
        #tile1 = kingTile
        #tile2 = 0
        #if (isinstance(enemyTile, int)):
        #    tile2 = enemyTile
        #else:
        #    tile2 = enemyTile.tileCoordinate


        kingCollumn = self.getCollumn(kingTile)
        enemyCollumn = self.getCollumn(enemyTile)

        kingRow = self.getRow(kingTile)
        enemyRow = self.getRow(enemyTile)

        collumnDist = abs(kingCollumn - enemyCollumn)
        rowDist = abs(kingRow - enemyRow)

        return max(collumnDist, rowDist)

    def calcKingTropism(self, player):
        playerKingSquare = player.getPlayerKing().piecePosition
        enemyMoves = player.getOpponent().legalMoves
        closestPiece = None
        closestDistance = 1000
        for i in range(len(enemyMoves)):
            if (enemyMoves[i]==0):
                pass
            else:
                for j in range(len(enemyMoves[i])):
                    currentDistance = self.chebyshevDistance(playerKingSquare, enemyMoves[i][j].getDestinationCoordinate())
                    if (currentDistance<closestDistance):
                        closestDistance = currentDistance
                        closestPiece = enemyMoves[i][j].getMovedPiece()

        return kingDistance(closestPiece, closestDistance)

    def castled(self, player):
        if (player.isCastled()):
            return 50
        else:
            return 0

class kingDistance:
    def __init__(self, enemyPiece, distance):
        self.enemyPiece = enemyPiece
        self.distance = distance

    def getEnemyPiece(self):
        return self.enemyPiece

    def getDistance(self):
        return self.distance

    def tropismScore(self):
        return (self.enemyPiece.pieceValue/10)*self.distance

class minimax:
    def __init__(self, board, depth):
        self.boardEvaluator = standardBoardEvaluator(board, depth)

    def execute(self):
        import sys
        bestMove = None
        highestVal = -sys.maxsize-1
        lowestVal = sys.maxsize
        print(self.boardEvaluator.board.currentPlayer.getAllianceName()," thinking at depth: ",self.boardEvaluator.depth)
        for i in range(len(self.boardEvaluator.board.currentPlayer.legalMoves)):
            if (self.boardEvaluator.board.currentPlayer.legalMoves[i] == 0):
                pass
            else:
                for j in range(len(self.boardEvaluator.board.currentPlayer.legalMoves[i])):
                    move=self.boardEvaluator.board.currentPlayer.legalMoves[i][j]
                    moveTranstiotion = self.boardEvaluator.board.currentPlayer.makeMove(move)
                    if(moveTranstiotion.getMoveStatus().value):
                        if (self.boardEvaluator.board.currentPlayer.getAlliance()==-1):
                            currentVal = self.minimum(moveTranstiotion.getExecuteBoard(), self.boardEvaluator.depth-1,\
                                                      highestVal, lowestVal)
                            if (currentVal>highestVal):
#                                print("compare highest")
                                highestVal = currentVal
                                bestMove = move
                                if (moveTranstiotion.getExecuteBoard().getBlackPlayer().isCheckmate()):
                                    break
                        else:
                            currentVal = self.maximum(moveTranstiotion.getExecuteBoard(), self.boardEvaluator.depth-1,\
                                                      highestVal, lowestVal)
                            if (currentVal<lowestVal):
#                                print("compare lowest")
                                lowestVal = currentVal
                                bestMove = move
                                if (moveTranstiotion.getExecuteBoard().getWhitePlayer().isCheckmate()):
                                    break


        return bestMove


    def minimum(self, board, depth, highest, lowest):
        if(depth==0 or self.endGame(board)):
            return self.boardEvaluator.evaluate(board, depth)
        else:
            currentLowest = lowest
            for i in range(len(board.currentPlayer.legalMoves)):
                if (board.currentPlayer.legalMoves[i] == 0):
                    pass
                else:
                    for j in range(len(board.currentPlayer.legalMoves[i])):
                        move = board.currentPlayer.legalMoves[i][j]
                        moveTransition = board.currentPlayer.makeMove(move)
                        if(moveTransition.getMoveStatus().value):
                            currentLowest = min(currentLowest,self.maximum(moveTransition.getExecuteBoard(), \
                                                                     depth-1, highest, currentLowest))
                            if (currentLowest <= highest):
                                return highest

            return currentLowest

    def maximum(self,
                board,
                depth,
                highest,
                lowest):
        if (depth==0 or self.endGame(board)):
            return self.boardEvaluator.evaluate(board, depth)
        else:
            currentHighest = highest
            for i in range(len(board.currentPlayer.legalMoves)):
                if (board.currentPlayer.legalMoves[i] == 0):
                    pass
                else:
                    for j in range(len(board.currentPlayer.legalMoves[i])):
                        move = board.currentPlayer.legalMoves[i][j]
                        moveTransition = board.currentPlayer.makeMove(move)
                        if(moveTransition.getMoveStatus().value):
                            currentHighest = max(currentHighest,self.minimum(moveTransition.getExecuteBoard(), \
                                                      depth-1, currentHighest, lowest))
                            if (currentHighest >= lowest):
                                return lowest

            return currentHighest

    def endGame(self, board):
        return board.currentPlayer.isCheckmate() or board.currentPlayer.isStalemate()