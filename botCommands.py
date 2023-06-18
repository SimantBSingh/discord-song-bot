import api
import aiohttp
import io
import discord
from discord.ext import commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)



async def play(ctx, url):
    if ctx.channel.type != discord.ChannelType.text:
            await ctx.send("This command can only be used in a text channel.")
            return

    # Get the voice channel of the bot's author
    voice_channel = ctx.author.voice.channel

    # Check if the author is connected to a voice channel
    if voice_channel is None:
        await ctx.send("You need to be connected to a voice channel to use this command.")
        return

    # Get the voice connection of the bot in the guild
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    # Check if the bot is already connected to a voice channel
    if voice_client is None:
        # Connect the bot to the voice channel
        voice_client = await voice_channel.connect()
    elif voice_client.channel != voice_channel:
        # Move the bot to the author's voice channel if it's in a different channel
        await voice_client.move_to(voice_channel)

    # Fetch the audio stream (replace with your own logic to fetch the audio)
    audio_stream, filename = await fetch_audio_stream(url)

    # Play the audio stream as a voice message in the text channel
    await ctx.send("Now playing...")
    await ctx.send(file=discord.File(audio_stream, filename=f'{filename}.mp3'))






async def fetch_audio_stream(url):
    # Invoke the search method to get the necessary parameters
    search_url, headers, params = await api.search(url)

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers, params=params) as response:
            data = await response.json()
            # Process the search results and extract the necessary information and assuming the first result is the desired track
            track = data['data'][0]

            # Get the preview URL of the track
            preview_url = track['preview']

            # Fetch the audio stream using the preview URL
            async with session.get(preview_url) as audio_response:
                # Read the audio stream as bytes
                audio_bytes = await audio_response.read()

                # Return the audio stream as a file-like object (BytesIO)
                return io.BytesIO(audio_bytes), track['title']


