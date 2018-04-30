from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np
import itertools
import pandas as pd


def get_data():
    aggro = pd.read_csv("aggressive.csv")
    defen = pd.read_csv("defensive.csv")
    total = pd.concat([aggro, defen])
    drops = ["Black", "BlackElo", "BlackTeam", "BlackTeamCountry", "Date", "Event",
             "EventCategory", "EventCountry", "EventDate", "EventRounds", "EventType", "FEN", "PlyCount", "Result",
             "Round", "SetUp", "Site", "Source", "SourceDate", "White", "WhiteElo", "WhiteTeam", "WhiteTeamCountry"]
    total = total.drop(drops, axis=1)

    number = LabelEncoder()
    total["ECO"] = number.fit_transform(total["ECO"].astype('str'))
    X = total.drop(["Aggressive"], axis=1)
    y = total["Aggressive"]
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    return X_train, X_test, y_train, y_test


def format_data(pgn_df):
    drops = ["Black", "BlackElo", "BlackTeam", "BlackTeamCountry", "Date", "Event",
             "EventCategory", "EventCountry", "EventDate", "EventRounds", "EventType", "FEN", "PlyCount", "Result",
             "Round", "SetUp", "Site", "Source", "SourceDate", "White", "WhiteElo", "WhiteTeam", "WhiteTeamCountry"]
    for column in pgn_df.columns:
        if column in drops:
            pgn_df = pgn_df.drop(column, axis=1)

    cols = ['Average Board Evaluation', 'Average Material Threatened', 'Check Count', 'ECO', 'Gambit Count',
            'Move Count']
    pgn_df = pgn_df[cols]
    number = LabelEncoder()
    pgn_df["ECO"] = number.fit_transform(pgn_df["ECO"].astype('str'))
    print(pgn_df)
    X = StandardScaler().fit_transform(pgn_df)
    return X


def init_classifier(X_train, X_test, y_train, y_test):
    forest = RandomForestClassifier(n_estimators=150)
    forest.fit(X_train, y_train)
    print(forest.score(X_test, y_test))
    return forest


def grid_cv(rfclf, X_train, X_test, y_train, y_test):
    cvscore = cross_val_score(rfclf, X_train, y_train, cv=10)
    print(np.mean(cvscore))
    clf = RandomForestClassifier(n_jobs=-1)
    arr = [i * 5 for i in range(1, 20)]
    param_grid = {
        'n_estimators': arr,  # up to 100 trees
        'max_depth': arr,
        'max_features': ['auto', 'sqrt', 'log2']
    }

    grid_clf = GridSearchCV(clf, param_grid, cv=10)
    grid_clf.fit(X_train, y_train)
    return grid_clf
