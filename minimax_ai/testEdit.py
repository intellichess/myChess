from math import ceil

def createPGNString():

    def addToHeader(header_str, header_data):
        myheader = "[%s \"%s\"]" % (header_str, header_data)
        myheader = myheader + "\n"
        return myheader

    PGNStr = addToHeader("Event", "")
    PGNStr = PGNStr + addToHeader("Site", "")
    PGNStr = PGNStr + addToHeader("Date", "")
    PGNStr = PGNStr + addToHeader("Round", "")
    PGNStr = PGNStr + addToHeader("White", "User")
    PGNStr = PGNStr + addToHeader("Black", "AI")
    PGNStr = PGNStr + addToHeader("Result", "")
    PGNStr = PGNStr + addToHeader("WhiteElo", "")
    PGNStr = PGNStr + addToHeader("BlackElo", "")
    PGNStr = PGNStr + addToHeader("Eco", "") + "\n"
    return PGNStr


def addToPGN(move_number, move):
    cur_move = move_number + 1
    if (cur_move % 2 == 1):
        return str(int(move_number/2)+1) + "." + move
    else:
        return " " + move + " "

