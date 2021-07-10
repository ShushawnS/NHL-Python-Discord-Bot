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
    #Creates and Runs API Request [Roster Details]
    #print(f"GETTING TEAMID DATA {teamID} !!!!!")
    base_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/stats'
    url = base_url.format(teamID)
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)

    #Makes JSON Information A Python Object
    nhlJSON = response.text
    nhlData = json.loads(nhlJSON)

    stat = nhlData['stats'][0]['splits'][0]['stat']
    rank = nhlData['stats'][1]['splits'][0]['stat']

    #Create Embed
    try:
        myEmbed = discord.Embed(
            title=nhlData['stats'][0]['splits'][0]['team']['name'],
            description="",
            color=0x2f3136
        )

        myEmbed.set_author(
            name=ctx.author.display_name,
            url="https://www.nhl.com/",
            icon_url=ctx.author.avatar_url)

        myEmbed.set_footer(text = f"NHL Stats - Team ID: {teamID}")

        
        count = 0

        #SHOW (MOST) DATA FROM JSON IN EMBED (for testing)
        # for x in stat:

        #     valueString = str(stat[x])

        #     #if no rank data, dont print it
        #     if x in rank.keys():
        #         valueString += f"\n*{rank[x]}*"
            
        #     myEmbed.add_field(
        #     name=f"{x}",
        #     value=valueString,
        #     inline = True
        #     )

        #     count += 1

        #     if(count >= 25):
        #         break
        

        myEmbed.add_field(
            name="__Overview__",
            value=f"**GP**: {stat['gamesPlayed']}\n{stat['wins']}W {stat['losses']}L {stat['ot']}OT",
            inline = True
        )

        myEmbed.add_field(
            name="__Points__",
            value=f"**PTS**: {stat['pts']} (*{rank['pts']}*)\n**PT%**: {stat['ptPctg']}",
            inline = True
        )

        myEmbed.add_field(
            name="__Goals__",
            value=f"**GPG**: {stat['goalsPerGame']} (*{rank['goalsPerGame']}*)\n**GAA**: {stat['goalsAgainstPerGame']} (*{rank['goalsAgainstPerGame']}*)",
            inline = True
        )

        myEmbed.add_field(
            name="__Shots/Saves__",
            value=f"**SF/G**: {stat['shotsPerGame']} (*{rank['shotsPerGame']}*)\n**SF%**: {stat['shootingPctg']} (*{rank['shootingPctRank']}*)\n**SA/G**: {stat['shotsAllowed']} (*{rank['shotsAllowed']}*)\n**SV%**: {stat['savePctg']} (*{rank['savePctRank']}*)",
            inline = True
        )

        myEmbed.add_field(
            name="__Powerplay__",
            value=f"**PPs**: {stat['powerPlayOpportunities']} (*{rank['powerPlayOpportunities']}*)\n**PPG**: {stat['powerPlayGoals']} (*{rank['powerPlayGoals']}*)\n**PP%**: {stat['powerPlayPercentage']} (*{rank['powerPlayPercentage']}*)\n**PPGA**: {stat['powerPlayGoalsAgainst']} (*{rank['powerPlayGoalsAgainst']}*)\n**PK%**: {stat['penaltyKillPercentage']} (*{rank['penaltyKillPercentage']}*)",
            inline = True
        )

        myEmbed.add_field(
            name="__Faceoffs__",
            value=f"**FO**: {stat['faceOffsTaken']} (*{rank['faceOffsTaken']}*)\n**FOW**: {stat['faceOffsWon']} (*{rank['faceOffsWon']}*)\n**FOL**: {stat['faceOffsLost']} (*{rank['faceOffsLost']}*)\n**FO%**: {stat['faceOffWinPercentage']} (*{rank['faceOffWinPercentage']}*)",
            inline = True
        )

    except:
        return deadEmbed("error")

    return myEmbed

def deadEmbed(type):
    if(type == "timeout"):
        return discord.Embed(description="⏲ This session timed out (15s).",color=0xED4245)
    elif(type == "kill"):
        return discord.Embed(description="👋 Au revoir, mon ami.",color=0xED4245)
    elif(type == "error"):
        return discord.Embed(description="🤔 Something went wrong. Please try again.",color=0xED4245)

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
    