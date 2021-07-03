# Import Discord Packages
import os
import discord 
import asyncio
from dotenv import load_dotenv
from discord.ext import commands 
import requests   
import json 
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

'''
testingtestingtesting
1
2
3
'''

#Initalize Variables
load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
guild_ids = os.getenv('DISCORD_GUILD')
guild_ids = guild_ids.split() 
guild_ids = guild_ids[2:-2] 

# Client       
client = commands.Bot(
    command_prefix="!",
    case_insensitive = True
) 

slash = SlashCommand(client, sync_commands = True)

@slash.slash(name="ping", description = "shows the bot latency", guild_ids = guild_ids )
async def _ping(ctx: SlashContext):
    print("Hello")
    await ctx.send(f"Bot speed - {round(client.latency * 1000)} ms")

# Changes Bot Details
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Game('w/ Shaan Pepe')
    )
    print(
        f'\n',
        f'Logged in as {client.user.name}#{client.user.discriminator},',
        f'User ID: {client.user.id}, Version: {discord.__version__}\n',
        f'DISCORD BOT WRITTEN BY Shushawn Saha\n'
    )


#Get Roster Function 
def getRoster(ctx,team):
    #Creates and Runs API Request [Roster Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/teams/{}/roster'
    url = base_url.format(team)
    response = requests.get(url)
    print(response.status_code)
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

#Gets Player Function
def getPlayer(ctx, id):
    #Creates and Runs API Request [Player Details]
    base_url = 'https://statsapi.web.nhl.com/api/v1/people/{}'
    url = base_url.format(id)
    response = requests.get(url)
    print(response.status_code)
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
    myEmbed = discord.Embed(title = 'Player Details For: ', description = f" {playerData['people'][0]['fullName']} {leadership} \n \n", color = 0x00ff00)            
    myEmbed.set_author(name=ctx.author.display_name, url="https://www.nhl.com/", icon_url=ctx.author.avatar_url) 
    myEmbed.set_footer(text = "NHL BOT -- CREATED BY: SHUSHAWN & SHAILEN") 
    myEmbed.set_thumbnail(url=f"http://nhl.bamcontent.com/images/headshots/current/168x168/{id}.jpg")

    #Creates a Field For Each Piece of Information
    myEmbed.add_field(name = "**Basic Details: **", value = f" > *Age:* {playerData['people'][0]['currentAge']} \n > Birth Date: {playerData['people'][0]['birthDate']} \n > Birth City: {playerData['people'][0]['birthCity']} \n > Nationality: {playerData['people'][0]['nationality']} \n > Height: {playerData['people'][0]['height']} \n > Weight: {playerData['people'][0]['weight']} ", inline = True) 
    myEmbed.add_field(name = "**Current Team: **", value = f" > Organization: {playerData['people'][0]['currentTeam']['name']} \n > Jersey Number: {playerData['people'][0]['primaryNumber']}", inline = True)

    if playerData['people'][0]['primaryPosition']['code'] != 'G' and (playerStatsData['stats'][0]['splits']):
        myEmbed.add_field(name = f"**Player Stats For: ** [{playerStatsData['stats'][0]['splits'][0]['season']}]", value = f" > GP: {playerStatsData['stats'][0]['splits'][0]['stat']['games']} \n > G: {playerStatsData['stats'][0]['splits'][0]['stat']['goals']} \n > A: {playerStatsData['stats'][0]['splits'][0]['stat']['assists']} \n > TP: {playerStatsData['stats'][0]['splits'][0]['stat']['points']} \n > +/-: {playerStatsData['stats'][0]['splits'][0]['stat']['plusMinus']}  ", inline = True) 
    elif playerData['people'][0]['primaryPosition']['code'] == 'G' and (playerStatsData['stats'][0]['splits']):
        myEmbed.add_field(name = f"**Player Stats For: ** [{playerStatsData['stats'][0]['splits'][0]['season']}]", value = f" > GP: {playerStatsData['stats'][0]['splits'][0]['stat']['games']} \n > W: {playerStatsData['stats'][0]['splits'][0]['stat']['wins']} \n > L: {playerStatsData['stats'][0]['splits'][0]['stat']['losses']} \n > SO: {playerStatsData['stats'][0]['splits'][0]['stat']['shutouts']} \n > GAA: {playerStatsData['stats'][0]['splits'][0]['stat']['goalAgainstAverage']} \n > SV%: {playerStatsData['stats'][0]['splits'][0]['stat']['savePercentage']} ", inline = True) 

    return myEmbed 

#Handles '!' commands
@client.command(name='nhl')
async def _nhl(ctx, *args): 
    if (args):

        # Gets Author Details 
        author = discord.User.id       
        
        if args[0] == 'roster':
            rosterEmbed = getRoster(ctx, args[1]) 
            await ctx.send(embed = rosterEmbed)
             
        elif args[0] == 'player':
            playerEmbed = getPlayer(ctx, args[1])
            await ctx.send(embed = playerEmbed) 
        
        elif args[0] == 'teamstats': 

            teamID = 1 if len(args)<2 else int(args[1])
            print(f"teamID is {teamID}...")
            maxTeamID = 30
            brokenIDs = [11,27] 

            def statsEmbed(teamID):

                #Creates and Runs API Request [Team Stats Details]
                #print(f"GETTING TEAMID DATA {teamID} !!!!!\n\n\n")
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

            teamEmbed = await ctx.send(embed = statsEmbed(teamID))

            await teamEmbed.add_reaction("⬅️")
            await teamEmbed.add_reaction("➡️")

            def check(reaction, user):
                return user == ctx.message.author and reaction.message == teamEmbed and (reaction.emoji == "⬅️" or reaction.emoji == "➡️")


            wrongNavs = 0

            while True:

                if wrongNavs==4:
                    await ctx.send(content="...",delete_after=1.5)
                elif wrongNavs==6:
                    await ctx.send(content="bro",delete_after=1.5)
                elif wrongNavs==10:
                    await teamEmbed.edit(embed = discord.Embed(title="nice one", description="self.shit()"))
                    await teamEmbed.clear_reactions()
                    await teamEmbed.add_reaction("❌")
                    await asyncio.sleep(1)
                    await ctx.send(content="you're actually a dumbass wtf",delete_after=3)
                    break

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=15, check=check)
                except asyncio.TimeoutError:
                    await teamEmbed.edit(content="Timed out (15s).",embed=None)
                    await teamEmbed.clear_reactions()
                    await teamEmbed.add_reaction("❌")
                    break
                else:
                    if(reaction.emoji == "⬅️"):
                        if teamID > 1:
                            teamID -= 1
                            await teamEmbed.edit(embed = statsEmbed(teamID))
                        else:
                            wrongNavs+=1
                            await reaction.remove(user)
                    elif(reaction.emoji == "➡️"):
                        if teamID < maxTeamID:
                            teamID += 1
                            await teamEmbed.edit(embed = statsEmbed(teamID))
                        else:
                            wrongNavs +=1
                            await reaction.remove(user)
        
    await ctx.send('{} {} arguments: {}'.format(len(args), format(ctx.message.author.mention), ', '.join(args)))

#Handles '/' Commands

#[roster] slash command
@slash.slash(
    name="roster", 
    description = "want to find roster details?", 
    guild_ids = guild_ids,
    options = [
        create_option (
            name = "team",
            description = "here is where you get the roster mmmmm",
            option_type = 3,
            required = True
        )
    ]
) 
async def _roster(ctx:SlashContext, team):
    #print(f"THIS IS CRAZY: {team}")
    #await ctx.send(f"{team}")  
    rosterEmbed = getRoster(ctx, team) 
    await ctx.send(embed = rosterEmbed) 

#[player] slash command
@slash.slash(
    name="player", 
    description = "want to find player details?", 
    guild_ids = guild_ids,
    options = [
        create_option (
            name = "id",
            description = "here is where you get the player mmmmm",
            option_type = 3,
            required = True
        )
    ]
) 
async def _roster(ctx:SlashContext, id):
    #print(f"THIS IS CRAZY: {team}")
    #await ctx.send(f"{team}")  
    playerEmbed = getPlayer(ctx, id)
    await ctx.send(embed = playerEmbed) 

#[teamstats] slash command
@slash.slash(
    name="teamstats", 
    description = "want to find team details?", 
    guild_ids = guild_ids,
    options = [
        create_option (
            name = "team",
            description = "here is where you get the team stats mmmmm",
            option_type = 3,
            required = True
        )
    ]
) 
async def _roster(ctx:SlashContext, team):
    #print(f"THIS IS CRAZY: {team}")
    #await ctx.send(f"{team}")  
    playerEmbed = getPlayer(ctx, team) 
    await ctx.send(embed = playerEmbed)


# Run the client on discord server
client.run(Token)