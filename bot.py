import discord
from discord.ext import commands
import responses
import botCommands



async def send_msg(msg, user_msg, is_private):
    try:
        response = await responses.handle_responses(user_msg)
        await msg.author.send(response) if is_private else await msg.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    TOKEN = 'MTExOTc4MTc1NjA0OTA0NzU3Mg.GPXVSB.Y0MreNhR3eVj4_xXGIJ1XRvsW8GV80kbkDjHrs'
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is running')

    @bot.event
    async def on_message(msg):
        if msg.author == bot.user:
            return

        username = str(msg.author)
        user_msg = str(msg.content)
        channel = str(msg.channel)

        if user_msg[0] == 'p':
            user_msg = user_msg[1:]
            await send_msg(msg, user_msg, is_private=True)
        else:
            await send_msg(msg, user_msg, is_private=False)


    @bot.command()
    async def play(ctx, url):
        await botCommands.play(ctx, url)
        
    bot.run(TOKEN)

run_discord_bot()
