from enum import Enum
class Alliance(Enum):
    black = 1
    white = -1

    @classmethod
    def choosePlayer(cls, alliance, blackPlayer, whitePlayer):
        nextAlliance = -1*alliance
        if (nextAlliance==-1):
            return whitePlayer
        else:
            return blackPlayer



