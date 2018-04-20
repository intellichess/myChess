from test import Board, Builder, prettyBoard, moveToString
from convertion import moveToByte, tileGet, moveGet, stringParser
from ai import minimax
import sys
from collections import defaultdict
x = Board(Builder()).createStandardBoard()
prettyBoard(x.board)
depth = 3
sys.setrecursionlimit(10000)

string = "PMOV|4|1|4|3"

tiles = stringParser(string)
move = moveGet(tiles[0], tiles[1], x)
x = move.execute()
prettyBoard(x.board)

arr = [[29], [60], [44], [55], [21], [7], [86], [99]]
l = defaultdict(list)
for i in range(len(arr)):
    l[arr[i][0] % 11] = l[arr[i][0] % 11] + arr[i]
print(l[3])
