import os
import discord 
import asyncio
from discord_components import component
from dotenv import load_dotenv
from discord.ext import commands 
import requests   
import json 
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component,create_select, create_select_option
from discord_slash.model import ButtonStyle

#Get Roster Function 
def getRoster(ctx,team):
    print("OI0EUWHTFOEIUWHRIUEFHRYWIOUEHFIOUEHWWOHIUWEIOUOHIUIH")
    #Creates and Runs API Request [Roster Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/roster'
    url = base_url.format(team)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text) 

    #Makes JSON Information A Python Object
    rosterJSON = response.text 
    rosterData = json.loads(rosterJSON)   

    #Creates and Runs API Request [Team Stats Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/stats'
    url = base_url.format(team)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)

    #Makes JSON Information A Python Object
    nhlJSON = response.text
    nhlData = json.loads(nhlJSON)

    #Create Embed 
    myEmbed = discord.Embed(title = 'Roster Details For: ', description = f"{nhlData['stats'][0]['splits'][0]['team']['name']} \n \n", color = 0x00ff00)            
    myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url) 
    myEmbed.set_footer(text = "NHL BOT -- CREATED BY: SHUSHAWN & SHAILEN") 
    myEmbed.set_thumbnail(url="https://th.bing.com/th/id/R8b66c2b4984717a8844c22fcce69cd57?rik=5k2K87pjvH5CQQ&pid=ImgRaw")

    #Finds Length of Object and Adds Embed Field [Each ]
    length = len(rosterData['roster'])
    x = 0
    for x in range(length):
        myEmbed.add_field(name = f"**{rosterData['roster'][x]['person']['fullName']} **", value = f" \n > Position: {rosterData['roster'][x]['position']['name']} [{rosterData['roster'][x]['position']['code']}] \n > Jersey Number: {rosterData['roster'][x]['jerseyNumber']} \n > ID: {rosterData['roster'][x]['person']['id']} ", inline = True)
    
    return myEmbed
    #ctx.send(embed = myEmbed) 

#Gets Player ID
def getPlayerID(ctx, name):
    print(name)
    playerName = name
    #Creates and Runs API Request [Player Details]
    base_url = 'https://suggest.svc.nhl.com/svc/suggest/v1/minplayers/{}'
    url = base_url.format(playerName)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text) 

    #Makes JSON Information A Python Object
    nhlJSON = response.text
    nhlData = json.loads(nhlJSON) 

    print("Please give me player id \n\n") 
    nhlData = nhlData['suggestions'][0].split('|')

    print(nhlData[0])
    return(nhlData[0])

#Gets Player Function
def getPlayer(ctx, id):
    #Creates and Runs API Request [Player Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/people/{}'
    url = base_url.format(id)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)  

    #Makes JSON Information A Python Object
    playerJSON = response.text 
    playerData = json.loads(playerJSON)  
    
    leadership = ' '
    #Adds Details If A Player Is Leader
    if (playerData['people'][0]['active'] == 'true'):
        if (playerData['people'][0]['captain']):
            leadership = ' [Captain]'
        elif (playerData['people'][0]['alternateCaptain']):
            leadership = ' [Assistant Captain]' 
    
    #Creates and Runs API Request [Player Stats Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/people/{}/stats?stats=statsSingleSeason&season=20202021'
    url = base_url.format(id)
    response = requests.get(url)
    print(response.status_code) 
    #print(response.text) 

    #Makes JSON Information A Python Object
    playerStatsJSON = response.text 
    playerStatsData = json.loads(playerStatsJSON)

    #Create Embed 
    myEmbed = discord.Embed(title = f" {playerData['people'][0]['fullName']} {leadership} \n \n", description = f" > [NHL.com](https://www.nhl.com/player/{playerData['people'][0]['firstName']}-{playerData['people'][0]['lastName']}-{id}) | [TSN.ca](https://www.tsn.ca/nhl/player-bio/{playerData['people'][0]['firstName'].lower()}-{playerData['people'][0]['lastName'].lower()}) \n", color = 0x00ff00)            
    myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url) 
    myEmbed.set_footer(text = "NHL BOT -- CREATED BY: SHUSHAWN & SHAILEN") 
    myEmbed.set_thumbnail(url=f"http://nhl.bamcontent.com/images/headshots/current/168x168/{id}.jpg")

    #Creates a Field For Each Piece of Information
    myEmbed.add_field(name = "**Basic Details: **", value = f" > Age: {playerData['people'][0]['currentAge']} \n > Birth Date: {playerData['people'][0]['birthDate']} \n > Birth City: {playerData['people'][0]['birthCity']} \n > Nationality: {playerData['people'][0]['nationality']} \n > Height: {playerData['people'][0]['height']} \n > Weight: {playerData['people'][0]['weight']} ", inline = True) 
    myEmbed.add_field(name = "**Current Team: **", value = f" > Organization: {playerData['people'][0]['currentTeam']['name']} \n > Jersey Number: {playerData['people'][0]['primaryNumber']}", inline = True)

    if playerData['people'][0]['primaryPosition']['code'] != 'G' and (playerStatsData['stats'][0]['splits']):

        myEmbed.add_field(name = f"**Player Stats For: ** [{playerStatsData['stats'][0]['splits'][0]['season']}]", value = f" > GP: {playerStatsData['stats'][0]['splits'][0]['stat']['games']} \n > G: {playerStatsData['stats'][0]['splits'][0]['stat']['goals']} \n > A: {playerStatsData['stats'][0]['splits'][0]['stat']['assists']} \n > TP: {playerStatsData['stats'][0]['splits'][0]['stat']['points']} \n > +/-: {playerStatsData['stats'][0]['splits'][0]['stat']['plusMinus']}  ", inline = True) 
        
        #myEmbed.add_field(name = "Helpful Links", value = f" [country codes](https://countrycode.org/) ", inline = True)
    elif playerData['people'][0]['primaryPosition']['code'] == 'G' and (playerStatsData['stats'][0]['splits']):
        myEmbed.add_field(name = f"**Player Stats For: ** [{playerStatsData['stats'][0]['splits'][0]['season']}]", value = f" > GP: {playerStatsData['stats'][0]['splits'][0]['stat']['games']} \n > W: {playerStatsData['stats'][0]['splits'][0]['stat']['wins']} \n > L: {playerStatsData['stats'][0]['splits'][0]['stat']['losses']} \n > SO: {playerStatsData['stats'][0]['splits'][0]['stat']['shutouts']} \n > GAA: {playerStatsData['stats'][0]['splits'][0]['stat']['goalAgainstAverage']} \n > SV%: {playerStatsData['stats'][0]['splits'][0]['stat']['savePercentage']} ", inline = True) 

    return myEmbed

def getTeamEmbed(ctx,teamID):
    #Creates and Runs API Request [Team Details]
    print(f"GETTING TEAMID DATA {teamID} !!!!!\n\n\n")
    base_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/stats'
    url = base_url.format(teamID)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)

    #Makes JSON Information A Python Object
    nhlJSON = response.text
    nhlData = json.loads(nhlJSON)

    #Create Embed
    try:
        myEmbed = discord.Embed(title=nhlData['stats'][0]['splits'][0]['team']['name'], description="")
        myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url)
        myEmbed.set_footer(text = f"NHL Stats - Team ID: {teamID}")
        myEmbed.add_field(name="teamname", value=nhlData["stats"][0]["splits"][0]["team"]["name"], inline = True)
    except:
        myEmbed = discord.Embed(title = "Error", description="Something went wrong. This team ID probably doesn't exist or doesn't have any data associated with it.")
        myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url)
        myEmbed.set_footer(text = f"NHL Stats - Team ID: {teamID}")
        #myEmbed.add_field(name="?????", value="This team ID probably doesn't exist.", inline = True)

    return myEmbed


# async def watchTeamEmbed(client,ctx,embedMsg,teamID,action_row):
# #watches teamstats embed for buttonpushes and edits accordingly
#     '''to do later -- figure out how to only let buttons work for the /team command invoker'''
#     def check(buttctx):
#         return buttctx.origin_message_id == embedMsg.id #and buttonclicker = cmd invoker????

#     try:
#         button_ctx: ComponentContext = await wait_for_component(client, components=action_row,timeout=7,check=check)

#         if button_ctx.custom_id == "x":
#             await embedMsg.edit(embed=deadEmbed("kill"),components=[])
#             return
#         elif button_ctx.custom_id == "left":
#             teamID -= 1
#         elif button_ctx.custom_id == "right":
#             teamID += 1

#         await embedMsg.edit(embed=getTeamEmbed(ctx,teamID))
#         await watchTeamEmbed(client,ctx,embedMsg,teamID,action_row)
#         return
            
#     except asyncio.TimeoutError:
#         await embedMsg.edit(embed=deadEmbed("timeout"),components=[])
#         return

'''KEEPING IN CASE BUTTONS DONT WORK WELL'''
# async def pageReactions(ctx,embedMsg,secTimeout):
# #given msg, watch for reactions and return -1,0,1 (⬅️❌➡️) depending on user input
# # 0 = quit,

#     def check(reaction, user):
#     #parameters for a valid reaction
#         print(f"user reacted with {reaction.emoji} on team embed")
            
#         return user == ctx.author and reaction.message.id == embedMsg.id and (reaction.emoji == "⬅️" or reaction.emoji == "➡️" or reaction.emoji == "❌")

#     try:
#         reaction, user = await ctx.bot.wait_for('reaction_add', timeout=secTimeout, check=check)
#         return reaction
#     except asyncio.TimeoutError:
#         return "timeout"

def deadEmbed(type):
    if(type == "timeout"):
        return discord.Embed(title="nice one", description="self.shit()")
    if(type == "kill"):
        return discord.Embed(title="adios", description="i will remember you hermano")

def getSchedule(ctx):

    #Creates and Runs API Request [Roster Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/schedule'
    #url = base_url.format(team)
    response = requests.get(base_url)
    print(response.status_code)
    #print(response.text)  

    #Makes JSON Information A Python Object
    scheduleJSON = response.text 
    scheduleData = json.loads(scheduleJSON)

    totalGames = scheduleData['totalGames']
    print(totalGames) 

    #Create Embed 
    myEmbed = discord.Embed(title = f" Schedule For: ", description = f" Today! \n", color = 0x00ff00)            
    myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url) 
    myEmbed.set_footer(text = "NHL BOT -- CREATED BY: SHUSHAWN & SHAILEN") 
    myEmbed.set_thumbnail(url=f"https://www-league.nhlstatic.com/images/logos/league-dark/133-flat.svg")

    #Adds Details For All Games
    x = 0
    for x in range(totalGames):
        myEmbed.add_field(name = f"** {scheduleData['dates'][0]['games'][x]['teams']['away']['team']['name']} vs. {scheduleData['dates'][0]['games'][x]['teams']['home']['team']['name']} **", value = f" > Arena: {scheduleData['dates'][0]['games'][x]['venue']['name']} \n > ", inline = True)

    return myEmbed

def getStandings(ctx):

    #Creates and Runs API Request [Standings Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/standings'
    response = requests.get(base_url)
    #print(response.status_code)
    #print(response.text)

    #Makes JSON Information A Python Object
    standingsJSON = response.text
    nhlStandings = json.loads(standingsJSON) 

    divisionNum = 3
    numTeams = len(nhlStandings['records'][divisionNum]['teamRecords'])
    x  = 0

    #Create Embed 
    myEmbed = discord.Embed(title = f"Standings For: ", description = f" {nhlStandings['records'][divisionNum]['division']['name']} \n", color = 0x00ff00)            
    myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url) 
    myEmbed.set_footer(text = "NHL BOT -- CREATED BY: SHUSHAWN & SHAILEN") 
    myEmbed.set_thumbnail(url=f"https://www-league.nhlstatic.com/images/logos/league-dark/133-flat.svg") 

    nhlStandings = nhlStandings['records'][divisionNum]['teamRecords']
    
    for x in range(numTeams):
        myEmbed.add_field( name = f"{x+1}. {nhlStandings[x]['team']['name']}", value = f" > Record [{nhlStandings[x]['gamesPlayed']}GP]: ({nhlStandings[x]['leagueRecord']['wins']}W - {nhlStandings[x]['leagueRecord']['losses']}L - {nhlStandings[x]['leagueRecord']['ot']}OT - {nhlStandings[x]['points']}P) \n > League Rank: {nhlStandings[x]['leagueRank']} \n > Streak: {nhlStandings[x]['streak']['streakCode']} \n > GA: {nhlStandings[x]['goalsAgainst']} - GF: {nhlStandings[x]['goalsScored']}  ", inline = False) 

    return myEmbed

