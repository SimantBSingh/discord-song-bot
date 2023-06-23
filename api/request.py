
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64

Client_ID = 'af39d029b1a94bee8fbb53a864a2d1e1'
Client_secret = '6b3528f6285d42708c114f6037210fdf'

def get_token():
    auth_string = Client_ID + ":" + Client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    res = requests.post(url, headers=headers, data=data)
    json_res = res.json()
    token = json_res['access_token']
    # print("first", json_res, token)
    return token


def deezer_search_music(name):
    url = "https://deezerdevs-deezer.p.rapidapi.com/search"

    querystring = {
        "q":name,
        'type': 'track',
        'offset': '0',
        'limit': '1',
        'numberOfTopResults': '1'
        }

    headers = {
        "X-RapidAPI-Key": "e07dbc7bc3msh3c828679fdd99aep119c0ejsnebd423c61ada",
        "X-RapidAPI-Host": "deezerdevs-deezer.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    # print("hello")

    # print(response.json())
    return response.json()




def get_auth_header(token):
    return {'Authorization': 'Bearer '+ token}


# def user_token():
#     auth_string = Client_ID + ":" + Client_secret
#     auth_bytes = auth_string.encode('utf-8')
#     auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

#     url = 'https://accounts.spotify.com/api/token'
#     headers = {
#         'Authorization': 'Basic ' + auth_base64,
#         'Content-Type' : 'application/x-www-form-urlencoded'
#     }
#     data = {'grant_type': 'authorization_code'}
#     res = requests.post(url, headers=headers, data=data)
#     json_res = res.json()
#     token = json_res['access_token']
#     # print("first", json_res, token)
#     return token


# token = get_token()
# get_userID()
# def user_id(token):
#     url = 'https://api.spotify.com/v1/playlists/3cEYpjA9oz9GiPac4AsH4n'
#     headers = get_auth_header(token)
    
#     data = requests.get(url=url, headers=headers)
#     print(data)
#     res = data.json()
#     print(res)

# user_id(get_token())

def get_userID():
    return "31uibi3m5im2tghf3h77zzm4rucy"




