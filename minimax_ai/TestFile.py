from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte, tileGet, moveGet, stringParser
from ai import minimax
import sys
x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
depth = 3
sys.setrecursionlimit(10000)

string = "PMOV|4|1|4|3"

tiles = stringParser(string)
move = moveGet(tiles[0], tiles[1], x)
x = move.execute()
prettyBoard(x.board)


