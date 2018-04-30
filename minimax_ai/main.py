from pgnutils import createPGNString, addToPGN, find_directory, create_pgn_file
from tagger import grab_fischer, update_csvs, read_game
from classifier import init_classifier, get_data, grid_cv, format_data


def main():
    pgn_str = createPGNString()
    pgn_str = pgn_str + addToPGN(0, "e4")

    # finds the location of pgnutils.py, it assumes that it's in the same directory with mcts.py
    dest_dir = find_directory()

    # creates the pgn file from pgn_str at dest_dir, pgn_file_location is also the location of the pgn file
    pgn_file_location = create_pgn_file(pgn_str, dest_dir)

    print(pgn_file_location)
    pgn_df = read_game(pgn_file_location)

    X_train, X_test, y_train, y_test = get_data()
    rfclf = init_classifier(X_train, X_test, y_train, y_test)
    X = format_data(pgn_df)
    print(X)

    pred = rfclf.predict(X)
    print("Pred: %s" % pred)



if __name__ == "__main__":
    main()
