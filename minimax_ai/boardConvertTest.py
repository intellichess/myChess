from test import Board, Builder, prettyBoard, OneDToTwoDRow, TwoDToOneDRow

x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
twoDBoard = OneDToTwoDRow(x.board)
oneDBoard = TwoDToOneDRow(twoDBoard)
prettyBoard(oneDBoard)
