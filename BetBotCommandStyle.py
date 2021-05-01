import os
import discord
from discord.ext import commands
from BetBotStorage import *

description = '''a betbot.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='|', intents=intents)

#@has_permissions(manage_emojies=True, manage_messages=True)

@bot.event
async def on_raw_reaction_add(payload):

    if payload.user_id  == bot.user.id:       #make sure the command comes from a user and not the bot: payload.user_id = the one who reacts. client.user.id = the bot.
        return

    for betMsgId in betStorage:     #check if the message is a bet.
        if payload.message_id != betMsgId:
            return

    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    if payload.emoji.name not in betStorage[payload.message_id]['OutcomeEmojies']:  #remove reaction if it is not an outcome
        await message.remove_reaction(payload.emoji, payload.member)

    if payload.member.id not in betStorage[payload.message_id]['bets']:  #if first time reacting, add player and bet.
        betStorage[payload.message_id]['bets'][payload.member.id] = payload.emoji
        return

    elif betStorage[payload.message_id]['bets'][payload.member.id] == '':   #if player adds reaction, add bet.
        betStorage[payload.message_id]['bets'][payload.member.id] = payload.emoji

    else:   #if player changes reaction, change bet.
        await message.remove_reaction(betStorage[payload.message_id]['bets'][payload.member.id], payload.member)
        betStorage[payload.message_id]['bets'][payload.member.id] = payload.emoji

@bot.event
async def on_raw_reaction_remove(payload):

    if payload.user_id  == bot.user.id:       #make sure the command comes from a user and not the bot: payload.user_id = the one who reacts. client.user.id = the bot.
        return

    for betMsgId in betStorage:     #check if the message is a bet.
        if payload.message_id != betMsgId:
            return
    
    if betStorage[payload.message_id]['bets'][payload.user_id] == payload.emoji:  #if player removes reaction, remove bet.
        betStorage[payload.message_id]['bets'][payload.user_id] = ''
       

@bot.command()
async def bet(ctx, bet, stake, *outcomes):
    for betId in betStorage:
        if ctx.author.id == betStorage[betId]['bookie']:
            await ctx.send('Only one active bet allowed per player. Close your bet to create a new one.')
            return
    ToSend = "bet: " + bet + "\nstake: " + stake + " beer(s)"
    for i in range(len(outcomes)):
        ToSend = ToSend + "\n" + letterEmoji(i) + outcomes[i]
    betMsg = await ctx.send(ToSend)
    for i in range(len(outcomes)):
        await betMsg.add_reaction(letterEmoji(i))
    storeBetInfo(betMsg.id, ctx.author.id, stake, len(outcomes))    #Stores betMsgId and outcomeEmojies.

@bot.command()
async def endbet(ctx, winningOutcome):
    for betId in betStorage:
        if ctx.author.id == betStorage[betId]['bookie']:            
            stake = betStorage[betId]['stake']
            winners = []
            losers = []
            for player in betStorage[betId]['bets']:
                member = str(ctx.guild.get_member(player))
                if betStorage[betId]['bets'][player].name == LetterToEmoji(winningOutcome.upper()):
                    winners.append(member)
                else:
                    losers.append(member)
            if len(winners) == 0 or len(losers) == 0:
                await ctx.send('Bet ended. Not enough players.')
                del betStorage[betId]   #delete bet from storage
                return
            
            debt = int(stake)/len(winners)
 
            for winner in winners:
                if winner not in balanceStorage:
                        balanceStorage[winner] = {}        
                for loser in losers:
                    if loser not in balanceStorage[winner]:
                        balanceStorage[winner][loser] = 0
                    balanceStorage[winner][loser] = balanceStorage[winner][loser] + debt      #positive debts are winnings.
            for loser in losers:
                if loser not in balanceStorage:
                    balanceStorage[loser] = {}  
                for winner in winners:
                    if winner not in balanceStorage[loser]:
                        balanceStorage[loser][winner] = 0
                    balanceStorage[loser][winner] = balanceStorage[loser][winner] - debt      #negative debts are debts.
  
            toSend = 'winners: '
            for winner in winners:
                toSend = toSend + winner + ' '
            toSend = toSend + '\nlosers: '
            for loser in losers:
                toSend = toSend + loser + ' '
            toSend = toSend + '\n\"|balance\" to check your new balance.'
            await ctx.send(toSend)
            del betStorage[betId]   #delete bet from storage
            return  

@bot.command()
async def balance(ctx):
    if str(ctx.author) not in balanceStorage:
        await ctx.send('Your tab is clean.' )
        return
    toSend = ''
    for player in balanceStorage[str(ctx.author)]:
        if balanceStorage[str(ctx.author)][player] > 0:
            toSend = toSend + player + ' owes you ' + str(balanceStorage[str(ctx.author)][player]) + ' beer(s).\n'
        else:
            toSend = toSend + 'You owe ' + player + ' ' + str(abs(balanceStorage[str(ctx.author)][player])) + ' beer(s).\n'
    await ctx.send(toSend)

@bot.command()
async def redeem(ctx, amount: int, player):
    if amount < 0:
        await ctx.send('Amount needs to be positive.' )
        return
    if str(ctx.author) not in balanceStorage:
        await ctx.send('Your tab is clean.' )
        return
    if player not in balanceStorage[str(ctx.author)]:
        await ctx.send('You have no beef with this player.' )
        return
    if balanceStorage[str(ctx.author)][player] < 0:
        await ctx.send('You are ' + player + '\'s bitch, you owe him/her ' + str(abs(balanceStorage[str(ctx.author)][player])) + ' beer(s).' )
        return
    if balanceStorage[str(ctx.author)][player] == amount:
        balanceStorage[str(ctx.author)][player] = 0
        balanceStorage[player][str(ctx.author)] = 0
        await ctx.send(player + '\'s debt is settled.' )    
        return
    if balanceStorage[str(ctx.author)][player] < amount:
        balanceStorage[str(ctx.author)][player] = 0
        balanceStorage[player][str(ctx.author)] = 0
        await ctx.send('Well that\'s more beers then he owed you. ' + player + ' can consider his debt settled.' )    
        return
    if balanceStorage[str(ctx.author)][player] > amount:
        balanceStorage[str(ctx.author)][player] = balanceStorage[str(ctx.author)][player] - amount
        balanceStorage[player][str(ctx.author)] = balanceStorage[str(ctx.author)][player] + amount
        await ctx.send(player + '\'s debt to you is ' + str(amount) + ' beer(s) lighter.' )
        return

        

bot.run('')
#bot.run(os.getenv('TOKEN'))