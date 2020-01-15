#! python3
# See https://realpython.com/how-to-make-a-discord-bot-python/
import os
import argparse
import random
import xdice
import bb_trivia
import bb_tournament
from dotenv import load_dotenv
import discord
from discord.ext import commands


################################################################################
# Test method for getting used to Discord API
################################################################################
def dump_context(ctx):
    print("Message Parameters Dump")
    print("=======================")
    print(f"Message Author Name: {ctx.author.name}")
    print(f"Message Author Discrminator: {ctx.author.discriminator}")
    print(f"Message Author is a Bot: {ctx.author.bot}")
    print(f"Message Content: {ctx.message.content}")
    print(f"Message was in Guild: {ctx.guild}")
    print(f"Message was in channel: {ctx.channel}")
    print(f"Message printed at: {ctx.message.created_at}")


################################################################################
# Read the invocation arguments and initialize the various files.
################################################################################
parser = argparse.ArgumentParser(
    prog="bb_bot", description="Discord Bot handling casual Blood Bowl stuff."
)
parser.add_argument("--trivia_file", help="The trivia data file (YAML format).")
parser.add_argument("--tourney_file", help="The tournament data file (YAML format).")
args = parser.parse_args()
trivia_file = bb_trivia.TriviaFile(args.trivia_file)
tourney_file = bb_tournament.TourneyFile(args.tourney_file)


################################################################################
# Discord Bot Commands
################################################################################
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord.")


@bot.command(name="trivia", help="Responds with a randomly selected bit of trivia.")
async def trivia(ctx):
    dump_context(ctx)
    tidbit = trivia_file.select
    print(tidbit)
    await ctx.send(tidbit)


@bot.command(name="block", help="Rolls the selected number of block dice, 1-3.")
async def block(ctx, num_dice: int):
    SKULL = "<:skull:662928827974156288>"
    BOTH = "<:bothdown:662928827948859392>"
    PUSH = "<:push:662928827772567563>"
    STUMBLE = "<:stumbles:662928827755921449>"
    POW = "<:pow:662928827768373250>"
    block_die = [SKULL, BOTH, PUSH, PUSH, STUMBLE, POW]
    line = ""
    if 0 < num_dice <= 3:
        for i in range(num_dice):
            line += random.choice(block_die)
        await ctx.send(line)
    else:
        await ctx.send("ERROR: Will only roll 1-3 dice.")


@block.error
async def block_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: Missing Required Argument")


@bot.command(
    name="report",
    help="Prints a report on the current tournament.  Valid options: 'team_summary' and 'current_week'",
)
async def report(ctx, option):
    if option == "team_summary":
        strblock = tourney_file.report_teams_short()
        strblock = "```" + strblock + "```"
        await ctx.send(strblock)
    elif option == "current_week":
        strblock = tourney_file.report_current_week()
        strblock = "```" + strblock + "```"
        await ctx.send(strblock)
    else:
        await ctx.send(f"ERROR: Option {option} not currently supported.")

@report.error
async def report_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: Missing Required Argument")

@bot.command(
    name="roll",
    help="""Takes a dice expression as an argument (may contain simple math
    operators as well.  Example: 3d4 + 1"""
)
async def roll(ctx, *, arg):
    print(arg)

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("ERROR: Missing Required Argument")


################################################################################
# Initialize and launch the bot
# Token is obtained from the environment
################################################################################
load_dotenv()
token = os.getenv("BBB_DISCORD_TOKEN")
print(f"Proceeding with BloodBowlBot Token: {token}")
bot.run(token)
