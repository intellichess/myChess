from enum import Enum
class Alliance(Enum):
    black = 1
    white = -1

    #return alliance value
    @classmethod
    def choosePlayer(cls, alliance, blackPlayer, whitePlayer):
#        print("alliance before",alliance)
        #print("alliance before",alliance)
        nextAlliance = -1*alliance
        #print("alliance after",nextAlliance)
#        print("alliance after",nextAlliance)
#        if (alliance==1):
        if (nextAlliance==1):
            return blackPlayer
        else:
            return whitePlayer



