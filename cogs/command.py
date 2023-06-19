import os
import discord
from discord.ext import commands
import tempfile
import api
import aiohttp
import responses
import asyncio



class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("ONline")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("How are you")


    @commands.command()
    async def play(self, ctx, url):
        if ctx.channel.type != discord.ChannelType.text:
                await ctx.send("This command can only be used in a text channel.")
                return

        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("You need to be connected to a voice channel to use this command.")
            return

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client == None or not voice_client.is_connected():
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)

        audio_file, filename = await self.fetch_audio_stream(url)
        # print(audio_file)

        # if (self.is_playing == False):
        #     voice_client.play(discord.FFmpegPCMAudio(audio_file))
        #     await ctx.send(f"Now playing: {filename}")
        #     os.remove(audio_file)
        # else:
        #     self.queue.append[[audio_file, filename]]

        # if (self.is_playing == False):
        # print(self.queue, self.is_playing)

            # if (self.queue):
            #     audio_file, filename = self.queue.pop()
            #     print(filename)
        
            # voice_client.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: self.play_next(voice_client, ctx))
            # voice_client.play(discord.FFmpegPCMAudio(audio_file), after = lambda e: self.play_next(voice_client, ctx))
            # await ctx.send(f"Now playing: {filename}")
            # os.remove(audio_file)
        self.queue.append([audio_file, filename])
        if (self.is_playing == False):
            await self.play_next(voice_client, ctx)

        print('first method')
        # elif (self.is_playing == True):
        #     print('playing')
        #     print(self.queue[0])

        # print(self.is_playing)








        # if (self.is_playing == False):
            # self.queue.append[[audio_file, filename]]
                # voice_client.play(discord.FFmpegPCMAudio(audio_file))
                # return
        # self.play_next(voice_client, ctx)

        # # Play the audio stream as a voice message in the text channel
        # voice_client.play(discord.FFmpegPCMAudio(audio_file))
        # await ctx.send(f"Now playing: {filename}")

        # # Clean up the temporary file after playback

    # async def play_next_callback(self, voice_client, ctx):
    #     print('next_callback')
    #     await self.play_next(voice_client, ctx)


    async def play_next(self, voice_client, ctx):
        if self.queue:
            self.is_playing = True
            array  = (self.queue.pop(0))
            audio, filename = discord.FFmpegPCMAudio(array[0]), array[1]
            print(filename)
            await ctx.send(f"Now playing: {filename}")

            async def music():
                await self.play_next(voice_client, ctx)
                # await voice_client.play(audio, after=lambda e: self.play_next(voice_client, ctx))
            voice_client.play(audio, after=await music())
        else:
            self.is_playing = False



    def play_music(self, voice_client):
        if self.queue:
            array  = (self.queue.pop(0))
            audio, filename = discord.FFmpegPCMAudio(array[0]), array[1]
            voice_client.play(audio, after=lambda e: self.play_music(voice_client))



    # @commands.command()
    async def fetch_audio_stream(self, url):
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
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(audio_bytes)

                # Return the path to the temporary file and filename
                return tmp_file.name, track['title']
                
    # @commands.Cog.

        
async def setup(bot):
    await bot.add_cog(command(bot))