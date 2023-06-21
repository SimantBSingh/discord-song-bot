import os
import re
import discord
from discord.ext import commands
from api import search
from embeds import music_embed


class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice_client = None
        self.cur_audio = []

    @commands.Cog.listener()
    async def on_ready(self):
        print("My Song Bot is Online")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("How are you")


    @commands.command()
    async def play(self, ctx, *args):
        url = ' '.join(args)
        if ctx.channel.type != discord.ChannelType.text:
                await ctx.send("This command can only be used in a text channel.")
                return

        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("You need to be connected to a voice channel to use this command.")
            return

        self.voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if self.voice_client == None or not self.voice_client.is_connected():
            self.voice_client = await voice_channel.connect()
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)

        audio_file, track = await search.fetch_audio_stream(url)


        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        print(is_playing, is_paused, track['title'])

        if is_playing == False and is_paused == False:
            self.queue.append([audio_file, track])
            self.play_next(ctx)
        elif is_playing == False and is_paused == True:
            self.queue.insert(0, [audio_file, track])
            self.play_next(ctx)
        else:
            self.queue.append([audio_file, track])
            embed = music_embed.play_embed(ctx, track, len(self.queue))
            await ctx.send(embed=embed)




    def play_next(self, ctx):
        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        print('play_next')
        if self.queue and is_playing == False:
            # TODO: SONG ENDING MESSAGE
            # if is_playing == True:
            #     print('song ended')
            #     self.bot.loop.create_task(ctx.send(f"{filename} song ended"))
            
            array = self.queue.pop(0)
            audio, track = discord.FFmpegPCMAudio(array[0]), array[1]
            self.cur_audio = array
            
            self.bot.loop.create_task(ctx.send(embed = music_embed.play_embed(ctx, track, 0)))

            self.voice_client.play(audio, after=lambda e: self.play_next(ctx))
            os.remove(audio)


    @commands.command()
    async def pause(self, ctx):
        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        print(is_playing, is_paused)
        if is_paused == False:
            self.voice_client.pause()
            await ctx.send("Music paused")
        else:
            await ctx.send("No Music is playing")

    @commands.command()
    async def queue(self, ctx):
        if (not self.queue):
            await ctx.send("No music in the queue")
        else:
            await ctx.send(embed=music_embed.queue_embed(ctx, self.queue))

    @commands.command()
    async def clear(self, ctx):
        if (not self.queue):
            await ctx.send("No music in the queue to clear")
        else:
            self.queue.clear()
            await ctx.send("The queue is clear")



    @commands.command()
    async def play_now(self, ctx, url):
        print('play_now')
        if ctx.channel.type != discord.ChannelType.text:
                await ctx.send("This command can only be used in a text channel.")
                return

        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("You need to be connected to a voice channel to use this command.")
            return

        self.voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if self.voice_client == None or not self.voice_client.is_connected():
            self.voice_client = await voice_channel.connect()
        elif self.voice_client.channel != voice_channel:
            await self.voice_client.move_to(voice_channel)

        audio_file, track = await search.fetch_audio_stream(url)

        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        self.voice_client.stop()
        await ctx.send(embed = music_embed.play_embed(ctx, track, 0))
        self.cur_audio = [ audio_file, track ]
        self.voice_client.play(discord.FFmpegPCMAudio(audio_file), after=lambda e: self.play_next(ctx))


    @commands.command()
    async def skip(self, ctx):
        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()
        
        if (is_playing or is_paused):
            await ctx.send("Skipped!")
            self.voice_client.stop()
            self.play_next(ctx)
        else:
            await ctx.send("No song to skip")


    @commands.command()
    async def seek(self, ctx, time):
        await ctx.send("Seeked")
        self.voice_client.stop()
        self.voice_client.play(discord.FFmpegPCMAudio(self.cur_audio[0], before_options=f'-ss {time}'), after=lambda e: self.play_next(ctx))
        


    @commands.command()
    async def resume(self, ctx):
        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        if is_paused == True:
            self.voice_client.resume()
            await ctx.send("Music resumed")
            self.play_next(ctx)
        else:
            await ctx.send("No Music was paused before to resume")






                
    # @commands.Cog.

        
async def setup(bot):
    await bot.add_cog(command(bot))