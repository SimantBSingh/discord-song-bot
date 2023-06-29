
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
    # print(json_res['tracks']['items'][0])
    # print(json_res['tracks']['items'][0]['id'])

    track = {
        'track_id': json_res['tracks']['items'][0]['id'],
        'track_name' : json_res['tracks']['items'][0]['name'],
        'artist' : json_res['tracks']['items'][0]['artists'][0]['name'],
        'duration' : int(json_res['tracks']['items'][0]['duration_ms']) ,
        'cover_image_url' : json_res['tracks']['items'][0]['album']['images'][0]['url'],
        'preview_url' : json_res['tracks']['items'][0]['preview_url'],
    }

    # print(json_res['tracks']['items'])
    return json_res['tracks']['items'][0]['preview_url'], track



def spotify_get_track(track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = request.get_auth_header(token)

    res = requests.get(url=url, headers=headers)
    # print(res)
    json_res = res.json()
    # print(json_res)
    
    # (request.get_userID(token))
    # print(json_res)
    # print(json_res['tracks']['items'][0])
    # print(json_res['id'])

    track = {
        'track_id': track_id,
        'track_name' : json_res['name'],
        'artist' : json_res['artists'][0]['name'],
        'duration' : int(json_res['duration_ms']) ,
        'cover_image_url' : json_res['album']['images'][0]['url'],
        'preview_url' : json_res['preview_url'],
    }

    # print(json_res['tracks']['items'])
    return track


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


def get_attributes(track_id):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = request.get_auth_header(token)
    # query = f'q={name}&type=track&limit=1'
    # query_url = url + query

    res = requests.get(url=url, headers=headers)
    json_res = res.json()

    # desired_attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    
    # extracted_dict = {attr: json_res[attr] for attr in desired_attributes}
    print(json_res)

    # return extracted_dict
            







