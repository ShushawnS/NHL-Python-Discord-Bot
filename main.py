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
        activity=discord.Game('w/ Shaan Pepe')
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

    teamID = int(team)

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
    
    action_row = create_actionrow(*buttons)

    embedMsg = await ctx.send(embed=functions.getTeamEmbed(ctx,teamID), components=[action_row])

    #await functions.watchTeamEmbed(client,ctx,embedMsg,teamID,action_row)

    '''to do later -- figure out how to only let buttons work for the /team command invoker'''
    def check(buttctx):
        return buttctx.origin_message_id == embedMsg.id #and buttonclicker = cmd invoker????

    while True:
        try:
            button_ctx: ComponentContext = await wait_for_component(client, components=action_row,timeout=7,check=check)

            if button_ctx.custom_id == "x":
                await embedMsg.edit(embed=functions.deadEmbed("kill"),components=[])
                break
            elif button_ctx.custom_id == "left":
                teamID -= 1
            elif button_ctx.custom_id == "right":
                teamID += 1

            await button_ctx.edit_origin(embed=functions.getTeamEmbed(ctx,teamID))

        except asyncio.TimeoutError:
            await embedMsg.edit(embed=functions.deadEmbed("timeout"),components=[])
            break


# Run the client on discord server
client.run(Token)