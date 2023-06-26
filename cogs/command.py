import os
import discord
from discord.ext import commands
from api import search
from embeds import music_embed
from db import admin



class command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.voice_client = None
        self.cur_audio = []
        # self.playlist_names = []
        # self.playlist_tracks = {}
        # self.playlist_url = ''
        self.collection = None



    @commands.Cog.listener()
    async def on_ready(self):
        print("My Song Bot is Online")
        # self.get_playlist()
        # dbname = admin.get_database()
        # self.collection = dbname['songData']


            

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

        # print(is_playing, is_paused, track['track_name'])

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
        res = music_embed.playlist_embed(ctx)
        if not res: 
            await ctx.send('No songs')
            return
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


        if (admin.check_playlist_exist(ctx.author.id, name) <= 0):
            await ctx.send("Playlist of given name doesn't exist")
            return


        result = admin.get_playlist(ctx.author.id, name)
        arr = []

        for document in result:
            playlist = document["playlists"][0]
            for track in playlist["tracks"]:
                arr.append([track['preview_url'], track])

        if not arr: await ctx.send('No tracks in the playlist given')

        self.queue = arr.copy()
        self.play_next(ctx)



    @commands.command()
    async def create_playlist(self, ctx, *args):
        user_id = ctx.author.id
        playlist_name = ' '.join(args)
        existing_object = admin.check_userID(user_id)

        if existing_object:
            query_result = admin.check_playlist_exist(user_id, playlist_name)
            if query_result > 0:
                print('hehe')
                await ctx.send("Playlist object with playlist name already exists.")
                return
            else:
                # Add the new playlist_obj to the existing object
                admin.create_playlist(user_id, playlist_name)
        else:
            # Create the object and add user_id attribute
            admin.create_user_playlist(user_id, playlist_name)

        await ctx.send("New Playlist Created")
        

    @commands.command()
    async def add_music(self, ctx, *args):
        user_id = ctx.author.id
        string_args = ' '.join(args)
        arguments = str(string_args).split(",")
        if len(arguments) <= 1:
            await ctx.send('PLaylist name or music or both not typed properly')
        playlist_name, song = arguments[0].strip(), arguments[1].strip()

        # print(playlist_name, song)
        audio_file, track = search.spotify_search_music(song)
        if audio_file == None: 
            audio_file, track = search.fetch_audio_stream(song)

        if_track_exists = admin.check_track_exists_using_url(user_id, playlist_name, audio_file)

        if_playlist_exists = admin.check_playlist_exist(user_id, playlist_name)
        if (if_playlist_exists <= 0):
            await ctx.send("Playlist with that name doesn't exist. Create a playlist")
        elif if_track_exists > 0:
            await ctx.send('track already exists')
        else:
            result = admin.add_track(user_id, playlist_name, track)
            if result.modified_count > 0:
                await ctx.send("Track added to the playlist.")
            else: 
                await ctx.send("DB ERROR")




    @commands.command()
    async def remove_music(self, ctx, *args):
        user_id = ctx.author.id
        string_args = ' '.join(args)
        arguments = str(string_args).split(",")
        if len(arguments) <= 1:
            await ctx.send('PLaylist name or music or both not typed properly')
        playlist_name, song = arguments[0].strip(), arguments[1].strip()

        if (admin.check_playlist_exist(user_id, playlist_name) <= 0):
            await ctx.send("Playlist with that name doesn't exist. Create a playlist")
            return
        result = admin.remove_music(user_id, playlist_name, song)

        if result.modified_count > 0: await ctx.send('Track removed successfully')
        else: await ctx.send('Track not found in the given playlist')


    @commands.command()
    async def remove_playlist(self, ctx, *args):
        user_id = ctx.author.id
        playlist_name = ' '.join(args)

        result = admin.remove_playlist(user_id, playlist_name)

        if result.modified_count > 0:
            await ctx.send("Playlist removed successfully.")
        else:
            await ctx.send("Playlist not found.")





        
async def setup(bot):
    await bot.add_cog(command(bot))