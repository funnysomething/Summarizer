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
    try:
        num_messages = int(arg)
        if (num_messages <= 0):
            raise ValueError("Invalid num_messages")
        if (num_messages > 200):
            await ctx.send("Too many messages requested")
        else:
            raw_messages = await get_messages(ctx.channel, num_messages)
            messages = format_messages(raw_messages=raw_messages)
            summary = await generate_summary(messages=messages)
            await ctx.send(summary)
    except Exception as e:
        print(f"Error generating response: {e}")
        await ctx.send("Invalid usage")

async def get_messages(channel, num_msgs):
    raw_messages = [message async for message in channel.history(limit=num_msgs+1)]
    raw_messages = raw_messages[1:]
    raw_messages.reverse()
    return raw_messages

def format_messages(raw_messages):
    messages = [{"role": "system", "content": f"Go through the list of messages I will give you and summarize the key details from all of the messages. Tell me which user sent which key detail. Ignore messages from yourself, the bot named Summarizer. Provide the information in chronological order. Don't ask a question at the end of your response. Format your response like a script in a play where it is name: summary, name: summary"}]
    for message in raw_messages:
        content = message.author.name + ": " + message.content
        msg = {"role": "user", "content": content}
        messages.append(msg)
    return messages

bot.run(bot_token)