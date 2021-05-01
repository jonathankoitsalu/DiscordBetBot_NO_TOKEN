from emojies import *

class bettingPool():
    
    def __init__(self, ctx, bookie, betText, stake, outcomes):
        self._ctx = ctx
        self._bookie = bookie
        self._betText = betText
        self._stake = stake
        self._letterEmojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮']                                       
        self._outcomes = dict(zip(outcomes, self._letterEmojis))

    def getBookie(self):
        return self._bookie

    def saveBettingPoolId(self, bettingPoolId):
        self._bettingPoolId = bettingPoolId

    def getBettingPoolId(self):
        return self._bettingPoolId

    def createMessage(self):
        message = "bet: " + self._betText + "\nstake: " + self._stake + " beer(s)"

        for key, value in self._outcomes.items():
            message = message + "\n" + value + key
        return message
        
        