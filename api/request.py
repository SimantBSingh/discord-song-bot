
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
    res= requests.post(url, headers=headers, data=data)
    json_res = res.json()

    token = json_res['access_token']
    return token



def get_auth_header(token):
    return {'Authorization': 'Bearer '+ token}





