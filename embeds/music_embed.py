import discord    



def play_embed(ctx, track, queue_pos):
    dur = ''
    duration = int(track['tracks']['items'][0]['duration_ms']) // 1000

    while duration > 60:
        temp = duration // 60
        dur += str(temp) + ':'
        duration -= (temp * 60)

    dur += str(duration)
    embed=discord.Embed(title=f"{track['tracks']['items'][0]['name']} - {track['tracks']['items'][0]['artists'][0]['name']}")

    
    if ctx.author.avatar:
        embed.set_author(name=ctx.author.display_name, url='https://github.com/Simant-Singh', icon_url=ctx.author.avatar)
    else:
        embed.set_author(name=ctx.author.display_name, url='https://github.com/Simant-Singh')
    # print('third')
    embed.set_thumbnail(url=track['tracks']['items'][0]['album']['images'][0]['url'])
    # print('fourth')
    embed.add_field(name="Duration", value=dur, inline=True)
    if queue_pos > 0:
        embed.description = "Added song to the queue"
        embed.add_field(name="Position in queue", value=queue_pos, inline=True)
    else:
        embed.description = "Now Playing"

    return embed


def queue_embed(ctx, queue):
    embed = discord.Embed(title="Songs in queue")
    for i in range(len(queue)):

        embed.add_field(name=i+1, value=f"{queue[i][1]['title']} - {queue[i][1]['artist']['name']}", inline=False)
        

    return embed


        
