whiteWins = -1
blackWins = 1
stalemate = 2
inProgress = 0
from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte
from pgnutils import createPGNString, addToPGN, find_directory, create_pgn_file
from tagger import grab_fischer, update_csvs, read_game
from classifier import init_classifier, get_data, grid_cv, format_data
from mctsTagger import monteCarloTreeSearch

pgn_str = createPGNString()
x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
mcts = monteCarloTreeSearch(60, 3, pgn_str, 0)
count = 0


for i in range(20):
    print("current player", x.currentPlayer.getAlliance(), x.currentPlayer.getAllianceName())
    #move = mcts.findNextMove(x)
    #print("move in algebraic notation",moveAlgebra)
    x = mcts.findNextMove(x).execute()
    move = x.transitionMove
    #print("alliance",move.board.currentPlayer.getAlliance())
    moveAlgebra = moveToString(move, move.board.currentPlayer)
    print("algebraic move", moveAlgebra)
    mcts.setString(addToPGN(count, moveAlgebra))
    count += 1
    print("move count", i)
    prettyBoard(x.board)
    print("----------------------------------")