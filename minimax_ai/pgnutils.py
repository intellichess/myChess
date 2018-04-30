import os
import platform


def createPGNString():
    """
    Creates a PGN formatted string, containing only the headers
    and no moves
    :return: A PGN formatted string
    """
    def addToHeader(header_str, header_data):
        """
        Creates the headers with empty strings.
        :param header_str: The header key, eg. Event, Date, WhiteElo etc.
        :param header_data: The header value, in this case all empty strings
        :return: the header for a PGN formatted string
        """
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
    """
    Adds the moves to the PGN formatted string
    :param move_number: move number, eg. Player's first turn is move 0, AI move 1, etc
    :param move: the algebraic notation for the move
    :return: the moves to a PGN formatted string
    """
    cur_move = move_number + 1
    if cur_move % 2 == 1:
        return str(int(move_number/2)+1) + "." + move
    else:
        return " " + move + " "


def find_directory():
    """
    Finds the location of this file, assuming it is stored inside the same directory with mcts.py
    :return: a string containing the path to the directory
    """
    dir_path = os.path.dirname(os.path.realpath("pgnutils.py"))
    return dir_path


def get_separator():
    """
    Determines to use / or \ depending on platform
    :return: \ or / as a string
    """
    desktop_type = platform.system()
    if desktop_type == 'Linux' or desktop_type == 'Darwin':
        slash = '/'
    elif desktop_type == 'Windows':
        slash = '\\'
    return slash


def create_pgn_file(pgn_str, dest_dir):
    """
    Creates a pgn file out of the pgn string
    :param pgn_str: the pgn string
    :param dest_dir: the destination folder
    :return: the location of the pgn file
    """
    pgn_file_location = dest_dir + get_separator() + "temp_pgn"
    f = open(pgn_file_location, "w+")
    f.write(pgn_str)
    return pgn_file_location

