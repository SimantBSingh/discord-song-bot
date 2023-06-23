import os
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
        self.playlist_names = []
        self.playlist_tracks = {}
        self.playlist_url = ''



    @commands.Cog.listener()
    async def on_ready(self):
        print("My Song Bot is Online")

        spotify_playlist = search.get_playlist()
        self.playlist_url = spotify_playlist[0]['external_urls']['spotify']

        for items in spotify_playlist:
            id = items['id']
            tracks = search.get_tracks_from_playlist(id)['tracks']['items']
            tracks_arr = []

            for track in tracks:
                if track['track']['preview_url'] ==  None:
                    preview_url, trackobj = search.fetch_audio_stream(track['track']['name'])
                else:
                    preview_url = track['track']['preview_url']
                tracks_arr.append({
                'track_name' : track['track']['name'],
                'artist' : track['track']['artists'][0]['name'],
                'duration' : track['track']['duration_ms'],
                'cover_image_url' : track['track']['album']['images'][0]['url'],
                'preview_url' : preview_url,
            })

            self.playlist_names.append(items['name'])

            self.playlist_tracks[items['name']] = tracks_arr
        # print("finished")

            

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("How are you")


    @commands.command()
    async def play(self, ctx, *args):
        url = ' '.join(args)
        if ctx.channel.type != discord.ChannelType.text:
                await ctx.send("This command can only be used in a text channel.")
                return

        if ctx.author.voice == None:
            await ctx.send('Connect to a voice channel')
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


        # audio_file, track = await search.fetch_audio_stream(url)
        audio_file, track = search.spotify_search_music(url)
        print(audio_file)
        if audio_file == None: 
            audio_file, track = search.fetch_audio_stream(url)
        # print(audio_file)
        # self.voice_client.play(discord.FFmpegPCMAudio(audio_file))


        is_playing, is_paused = self.voice_client.is_playing(), self.voice_client.is_paused()

        print(is_playing, is_paused, track['track_name'])

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

        # print('play_next')
        if self.queue and is_playing == False:
            # TODO: SONG ENDING MESSAGE
            # if is_playing == True:
            #     print('song ended')
            #     self.bot.loop.create_task(ctx.send(f"{filename} song ended"))
            
            array = self.queue.pop(0)
            audio, track = discord.FFmpegPCMAudio(array[0]), array[1]
            self.cur_audio = array
            
            self.bot.loop.create_task(ctx.send(embed = music_embed.play_embed(ctx, track, 0)))
            print("play_next                                                                                                        ")

            self.voice_client.play(audio, after=lambda e: self.play_next(ctx))
            # os.remove(audio)


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


    @commands.command()
    async def my_playlist(self, ctx):
        res = music_embed.playlist_embed(self.playlist_names, self.playlist_tracks)
        await ctx.send(f"Your spotify playlist:  {self.playlist_url}")
        await ctx.send(f"```\n{res}\n```")

    @commands.command()
    async def p_list(self, ctx, *args):
        name = ' '.join(args)
        if ctx.channel.type != discord.ChannelType.text:
                await ctx.send("This command can only be used in a text channel.")
                return

        if ctx.author.voice == None:
            await ctx.send('Connect to a voice channel')
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

        self.voice_client.stop()
        if name.isdigit():
            name = self.playlist_names[int(name)-1] 

        print(name)
        if name in self.playlist_names:
            self.queue = []
            for track in self.playlist_tracks[name]:
                # print(f"{track}\n")
                self.queue.append([track['preview_url'], track])

            self.play_next(ctx)



                
    # @commands.Cog.

        
async def setup(bot):
    await bot.add_cog(command(bot))