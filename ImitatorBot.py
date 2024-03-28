import discord
from discord.ext import commands
import configparser
from gptsummarizer import generate_summary

#Notifies discord API that bot wants messages and message content from server
intents = discord.Intents.default()
intents.message_content = True

#Creates bot with given command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

#Gets bot_token from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config['Credentials']['DISCORD_BOT_TOKEN']

person = "Barack Obama"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def summarize(ctx, *, arg):
    
    channel = ctx.channel
    num_messages = int(arg)
    raw_messages = [message async for message in channel.history(limit=num_messages)]
    
    # Create a list of dictionaries representing each message
    messages = [{"role": "system", "content": f"Summarize the following discord messages."}]
    for message in raw_messages:
        msg = {"role": "user", "content": str(message.content)}
        messages.append(msg)
    summary = await generate_summary(messages=messages)
    print(summary)
    # await ctx.send(summary)

bot.run(bot_token)