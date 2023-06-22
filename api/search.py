

from api import request
import requests



token = request.get_token()

def search_music(name):
    url = 'https://api.spotify.com/v1/search?'
    headers = request.get_auth_header(token)
    query = f'q={name}&type=track&limit=1&include_external=audio'
    query_url = url + query

    res = requests.get(query_url, headers=headers)
    json_res = res.json()

    return json_res['tracks']['items'][0]['preview_url'], json_res

    