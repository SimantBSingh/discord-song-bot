
from api import request
import requests



token = request.get_token()

def spotify_search_music(name):
    url = 'https://api.spotify.com/v1/search?'
    headers = request.get_auth_header(token)
    query = f'q={name}&type=track&limit=1'
    query_url = url + query

    res = requests.get(query_url, headers=headers)
    json_res = res.json()
    
    # (request.get_userID(token))
    # print(json_res)
    # print(json_res['tracks']['items'][0]['name'])
    # print(json_res['tracks']['items'][0]['artists'][0]['name'])
    # print(json_res['tracks']['items'][0]['duration_ms'])
    # print(json_res['tracks']['items'][0]['album']['images'][0]['url'])
    # print(json_res['tracks']['items'][0]['preview_url'])

    track = {
        'track_name' : json_res['tracks']['items'][0]['name'],
        'artist' : json_res['tracks']['items'][0]['artists'][0]['name'],
        'duration' : int(json_res['tracks']['items'][0]['duration_ms']) ,
        'cover_image_url' : json_res['tracks']['items'][0]['album']['images'][0]['url'],
        'preview_url' : json_res['tracks']['items'][0]['preview_url'],
    }

    # print(json_res['tracks']['items'])
    return json_res['tracks']['items'][0]['preview_url'], track


import tempfile
import aiohttp


def fetch_audio_stream(url):

        track = request.deezer_search_music(url)

        # print(track['data'][0]['title'])
        # print(track['data'][0]['artist']['name'])
        # print(track['data'][0]['duration'])
        # print(track['data'][0]['album']['cover'])
        # print(track['data'][0]['preview'])

        track_obj = {
            'track_name' : track['data'][0]['title'],
            'artist' : track['data'][0]['artist']['name'],
            'duration' : int(track['data'][0]['duration']) * 1000,
            'cover_image_url' : track['data'][0]['album']['cover'],
            'preview_url' : track['data'][0]['preview'],

        }

        return track_obj['preview_url'], track_obj
            







def get_playlist():
    user_id = request.get_userID()
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = request.get_auth_header(token)

    data = requests.get(url, headers=headers)
    # print("res", res)
    res = data.json()
    # print(json_res)
    return res['items']


def get_tracks_from_playlist(playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = request.get_auth_header(token)

    data = requests.get(url, headers=headers)
    res = data.json()

    # print(res)
    return res



