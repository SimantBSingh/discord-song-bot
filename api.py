# import discord
# import requests


async def search(query):
    url = 'https://deezerdevs-deezer.p.rapidapi.com/search'

    headers = {
        'X-RapidAPI-Key': 'e07dbc7bc3msh3c828679fdd99aep119c0ejsnebd423c61ada',
        'X-RapidAPI-Host': 'deezerdevs-deezer.p.rapidapi.com'
    }
    params = {
        'q': query,
        'type': 'track',
        'offset': '0',
        'limit': '1',
        'numberOfTopResults': '1'
    }
    
    return url, headers, params

