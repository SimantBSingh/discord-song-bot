import discord 
from tabulate import tabulate
from table2ascii import table2ascii, Alignment, PresetStyle
from db import connect




def play_embed(ctx, track, queue_pos):
    dur = ''
    duration = int(track['duration']) // 1000

    while duration > 60:
        temp = duration // 60
        dur += str(temp) + ':'
        duration -= (temp * 60)


    remaining = str(duration).zfill(2)
    dur += str(remaining)
    embed=discord.Embed(title=f"{track['track_name']} - {track['artist']}")

    
    if ctx.author.avatar:
        embed.set_author(name=ctx.author.display_name, url='https://github.com/Simant-Singh', icon_url=ctx.author.avatar)
    else:
        embed.set_author(name=ctx.author.display_name, url='https://github.com/Simant-Singh')
    # print('third')
    embed.set_thumbnail(url=track['cover_image_url'])
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
        # print(queue[i][1])
        embed.add_field(name=i+1, value=f"{queue[i][1]['track_name']} - {queue[i][1]['artist']}", inline=False)

    return embed



def playlist_embed(ctx):
    dbname = connect.get_database()
    collection = dbname['songData']
    cursor = collection.find()

    playlist_names, playlist_tracks = [], {}
    for document in cursor:
        # print(document)
        if (document['user_id'] == ctx.author.id):
            for playlist in document['playlists']:
                playlist_names.append( playlist['playlist_name'] )
                playlist_tracks[ playlist['playlist_name'] ] = [f"{track['track_name']}" for track in playlist['tracks']]
            break

    if not playlist_names: return

    max_tracks = max(len(tracks) for tracks in playlist_tracks.values())
    table = []

    for i in range(max_tracks):
        row = []
        for name in playlist_names:
            track = playlist_tracks[name]
            if i < len(track):
                row.append(track[i])
            else:
                row.append('')

        table.append(row)


    output = table2ascii(
        header=playlist_names,
        body=table,
        alignments=Alignment.LEFT,
        style=PresetStyle.double_thin_compact,
    )

    return output


        
