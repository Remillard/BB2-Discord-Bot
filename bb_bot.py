#! python3
# See https://realpython.com/how-to-make-a-discord-bot-python/
import os
import argparse
import bb_trivia
from dotenv import load_dotenv
from discord.ext import commands


##################
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
##################

################################################################################
# Read the invocation arguments and initialize the various files.
################################################################################
parser = argparse.ArgumentParser(
    prog="bb_trivia", description="Prints out a random Blood Bowl trivia fact."
)
parser.add_argument("filename", help="The trivia data file (YAML format).")
args = parser.parse_args()
trivia_file = bb_trivia.TriviaFile(args.filename)



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
    print(trivia_file)
    await ctx.send(trivia_file)


################################################################################
# Initialize and launch the bot
# Token is obtained from the environment
################################################################################
load_dotenv()
token = os.getenv("BBB_DISCORD_TOKEN")
print(f"Proceeding with BloodBowlBot Token: {token}")
bot.run(token)


