# Import Discord Packages
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

import functions

'''
fixed current player error
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
        activity=discord.Game("message.text.exe")
    )
    print(
        f'\n',
        f'Logged in as {client.user.name}#{client.user.discriminator},',
        f'User ID: {client.user.id}, Version: {discord.__version__}\n',
        f'DISCORD BOT WRITTEN BY Shushawn Saha\n'
    )

# 
# 
#  END OF FUNCTIONS, COMMANDS BELOW
# 
# 

#Handles '!' commands
@client.command(name='nhl')
async def _nhl(ctx, *args): 
    if (args):

        # Gets Author Details 
        author = discord.User.id       
        
        if args[0] == 'roster':
            rosterEmbed = functions.getRoster(ctx, args[1]) 
            await ctx.send(embed = rosterEmbed)
             
        elif args[0] == 'player': 
            if (args[2]):
                name = args[1] + " " + args[2]
            id = functions.getPlayerID(ctx, name)
            playerEmbed = functions.getPlayer(ctx, id)
            
            await ctx.send(embed = playerEmbed) 
        
        elif args[0] == 'schedule': 
            scheduleEmbed = functions.getSchedule(ctx)
            await ctx.send(embed = scheduleEmbed) 
        
        elif args[0] == 'standings':
            print("Hi") 
            standingsEmbed = functions.getStandings(ctx)
            await ctx.send(embed = standingsEmbed) 
        
        elif args[0] == 'teamstats': 

            teamID = 1 if len(args)<2 else int(args[1])
            print(f"teamID is {teamID}...")
            maxTeamID = 30
            brokenIDs = [11,27] 

            teamEmbed = await ctx.send(embed = functions.getTeamEmbed(ctx,teamID))

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
                            await teamEmbed.edit(embed = functions.getTeamEmbed(ctx,teamID))
                        else:
                            wrongNavs+=1
                            await reaction.remove(user)
                    elif(reaction.emoji == "➡️"):
                        if teamID < maxTeamID:
                            teamID += 1
                            await teamEmbed.edit(embed = functions.getTeamEmbed(ctx,teamID))
                        else:
                            wrongNavs +=1
                            await reaction.remove(user)
        
    await ctx.send('{} {} arguments: {}'.format(len(args), format(ctx.message.author.mention), ', '.join(args)))

@client.command(name='testing')
#FIGURING OUT DROPDOWNS
async def _testing(ctx):
    select = create_select(
        options=[# the options in your dropdown
            create_select_option("Lab Coat", value="coat", emoji="🥼"),
            create_select_option("Test Tube", value="tube", emoji="🧪"),
            create_select_option("Petri Dish", value="dish", emoji="🧫"),
        ],
        placeholder="Choose your option",  # the placeholder text to show when no options have been chosen
        min_values=1,  # the minimum number of options a user must select
        max_values=1,  # the maximum number of options a user can select
    )

    components=[create_actionrow(select),create_actionrow(select)]

    msg = await ctx.send("ok!", components=components)

    while True:
        try:
            button_ctx: ComponentContext = await wait_for_component(client, components=components,timeout=15)
            await button_ctx.edit_origin(content=f"you selected {button_ctx.selected_options}")
        except asyncio.TimeoutError:
            await msg.edit(components=[],embed=functions.deadEmbed("timeout"))


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
    rosterEmbed = functions.getRoster(ctx, team) 
    await ctx.send(embed = rosterEmbed) 

#[player] slash command
@slash.slash(
    name="player", 
    description = "want to find player details?", 
    guild_ids = guild_ids,
    options = [
        create_option (
            name = "name",
            description = "here is where you get the player mmmmm",
            option_type = 3,
            required = True
        ), 
        create_option (
            name = "season",
            description = "looking for regular season or playoff stats",
            option_type = 3,
            required = False
        )
    ]
) 

async def _player(ctx:SlashContext, name):
    #print(f"THIS IS CRAZY: {team}")
    #await ctx.send(f"{team}") 

    id = functions.getPlayerID(ctx, name) 
    playerEmbed = functions.getPlayer(ctx, id)
    await ctx.send(embed = playerEmbed)   

#[team] slash command
@slash.slash(
    name="team", 
    description = "want to find team details?", 
    guild_ids = guild_ids,
    options = [
        create_option (
            name = "team",
            description = "here is where you get the team stats mmmmm",
            option_type = 4,
            required = True
        )
    ]
) 

async def _team(ctx:SlashContext, team):
#given ID, show team stats

    teamID = int(team)
    teamIndex = 0

    validTeams = [1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,29,30,52,53,54]

    if(team in validTeams):
        teamIndex = validTeams.index(teamID)
    else:
        await ctx.send(content="Invalid ID. Try again.",delete_after=3)
        return


    '''needs polishing/commenting'''
    buttons = [
            create_button(
                style=ButtonStyle.primary,
                emoji="⬅️",
                custom_id="left"),
            create_button(
                style=ButtonStyle.danger,
                emoji="❌",
                custom_id="x"),
            create_button(
                style=ButtonStyle.primary,
                emoji="➡️",
                custom_id="right")
            ]

    buttonsStart = [
            create_button(
                style=ButtonStyle.primary,
                emoji="⬅️",
                custom_id="left",
                disabled=True),
            create_button(
                style=ButtonStyle.danger,
                emoji="❌",
                custom_id="x"),
            create_button(
                style=ButtonStyle.primary,
                emoji="➡️",
                custom_id="right")
            ]
    
    buttonsEnd = [
            create_button(
                style=ButtonStyle.primary,
                emoji="⬅️",
                custom_id="left"),
            create_button(
                style=ButtonStyle.danger,
                emoji="❌",
                custom_id="x"),
            create_button(
                style=ButtonStyle.primary,
                emoji="➡️",
                custom_id="right",
                disabled=True)
            ]
    
    action_row = create_actionrow(*buttons)

    def getComponents(a):
        #a is index of team in list of team IDs
        if(a == 0):
            return [create_actionrow(*buttonsStart)]
        if(a == len(validTeams)-1):
            return [create_actionrow(*buttonsEnd)]
        else:
            return [create_actionrow(*buttons)]

    embedMsg = await ctx.send(embed=functions.getTeamEmbed(ctx,validTeams[teamIndex]), components=getComponents(teamIndex))

    def check(buttctx):
        return buttctx.origin_message_id == embedMsg.id and ctx.author_id == buttctx.author_id

    while True:
        try:
            button_ctx: ComponentContext = await wait_for_component(client, components=action_row,timeout=15,check=check)

            if button_ctx.custom_id == "x":
                await embedMsg.edit(embed=functions.deadEmbed("kill"),components=[])
                break
            elif button_ctx.custom_id == "left":
                teamIndex -= 1
            elif button_ctx.custom_id == "right":
                teamIndex += 1

            #edit msg via the returned button_ctx objects, acts as a response to the interaction
            #interaction fails if edited via embedMsg.edit()
            await button_ctx.edit_origin(
                embed=functions.getTeamEmbed(ctx,validTeams[teamIndex]),
                components=getComponents(teamIndex))

        except asyncio.TimeoutError:
            await embedMsg.edit(embed=functions.deadEmbed("timeout"),components=[])
            break

@slash.slash(
    name="test",
    description="This is just a test command, nothing more.",
    options=[
        create_option(
            name="optone",
            description="This is the first option we have.",
            option_type=3,
            required=True,
            choices=[
                create_choice(
                    name="ChoiceOne",
                    value="DOGE!"
                ),
                create_choice(
                    name="ChoiceTwo",
                    value="NO DOGE"
                )
            ]
        )
    ]
)

async def _test(ctx: SlashContext,optone: str):
    await ctx.send(f"YOU CHOSE {optone}!!!")

# Run the client on discord server
client.run(Token)