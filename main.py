import bot

if __name__ == '__main__':
    # running bot
    bot.run_discord_bot()
else:
    print('main method not working')






# import discord
# intents = discord.Intents.all()
# from discord.ext import commands

# import responses


# async def send_msg(msg, user_msg, is_private):
#     try:
#         response = await responses.handle_responses(user_msg)
#         await msg.author.send(response) if is_private else await msg.channel.send(response)
#     except Exception as e:
#         print(e)




# def run_discord_bot():
#     # print('runnig')
#     TOKEN = 'MTExOTc4MTc1NjA0OTA0NzU3Mg.GPXVSB.Y0MreNhR3eVj4_xXGIJ1XRvsW8GV80kbkDjHrs'
#     client = discord.Client(intents=intents)

#     @client.event
#     async def on_ready():
#         print(f'{client.user} is running')

#     @client.event
#     async def on_message(msg):
#         if msg.author == client.user: return

#         username = str(msg.author)
#         user_msg = str(msg.content)
#         channel = str(msg.channel)

#         # print(f'{username} said: "{user_msg}" on channel {channel}')
#         print(msg.author.voice)

#         if user_msg[0] == '/' or user_msg[0:2] == 'p/':
#             if user_msg[0] == 'p':
#                 user_msg = user_msg[1:]
#                 await send_msg(msg, user_msg, is_private=True)
#             else:
#                 await send_msg(msg, user_msg, is_private=False)



#     @client.command()
#     async def play(ctx, url):
#         print(ctx.author.voice.channel)
#         # Check if the command was issued in a text channel
#     #     if ctx.channel.type != discord.ChannelType.text:
#     #         await ctx.send("This command can only be used in a text channel.")
#     #         return

#     #     # Get the voice channel of the bot's author
#     #     voice_channel = ctx.author.voice.channel

#     #     # Check if the author is connected to a voice channel
#     #     if voice_channel is None:
#     #         await ctx.send("You need to be connected to a voice channel to use this command.")
#     #         return

#     #     # Get the voice connection of the bot in the guild
#     #     voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)

#     #     # Check if the bot is already connected to a voice channel
#     #     if voice_client is None:
#     #         # Connect the bot to the voice channel
#     #         voice_client = await voice_channel.connect()
#     #     elif voice_client.channel != voice_channel:
#     #         # Move the bot to the author's voice channel if it's in a different channel
#     #         await voice_client.move_to(voice_channel)

#     #     # Fetch the audio stream (replace with your own logic to fetch the audio)
#     #     audio_stream = await fetch_audio_stream(url)

#     #     # Play the audio stream as a voice message in the text channel
#     #     await ctx.send("Now playing...")
#     #     await ctx.send(file=discord.File(audio_stream, filename="song.mp3"))

#     # # Replace this with your own logic to fetch the audio stream
#     # async def fetch_audio_stream(url):
#     #     # Implement your logic to fetch the audio stream from the URL
#     #     # This could involve downloading the audio file or using an API
#     #     # Return the audio stream as a file-like object (e.g., BytesIO)


#     client.run(TOKEN)
