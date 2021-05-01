from emojies import *

betStorage = {}
balanceStorage = {}
#balanceStorage[key]={}

def storeBetInfo(betMsgId, playerId, stake, numberOfOutcomes):
    betStorage[betMsgId]={   'OutcomeEmojies' : [], 'bookie' : playerId, 'stake': stake, 'bets' : {} }
    for i in range(numberOfOutcomes):   
        betStorage[betMsgId]['OutcomeEmojies'].append(letterEmoji(i))   #Store OutcomeEmojies.


def storePlayerBet(betId, player, input):
    betStorage[betId]['bets'][player]=input


class BetBotStorage:

    def __init__(self):
        self.betStorage = {}
        self.balanceStorage = {}

    def storeBetInfo(self,betMsgId, playerId, stake, numberOfOutcomes):
        betStorage[betMsgId]={   'OutcomeEmojies' : [], 'bookie' : playerId, 'stake': stake, 'bets' : {} }
        for i in range(numberOfOutcomes):   
            betStorage[betMsgId]['OutcomeEmojies'].append(letterEmoji(i))   #Store OutcomeEmojies.

    def storePlayerBet(betId, player, input):
        betStorage[betId]['bets'][player]=input

