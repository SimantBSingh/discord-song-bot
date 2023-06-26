from pymongo import MongoClient
from db import connect
import re



dbname = connect.get_database()
collection = dbname['songData']


def check_userID(id):
    query = {'user_id': id}
    result = collection.find_one(query)
    return result



def get_playlist(id, playlist_name):
    query = {
            "user_id": id,
            "playlists": {
                "$elemMatch": {
                    "playlist_name": playlist_name
                }
            }
        }
    projection = {"_id": 0,"playlists.$": 1}
    result = collection.find(query, projection)
    return result

    

def check_track_exists_using_url(user_id, playlist_name, url):
    query = {
        'user_id': user_id,
        'playlists': {
            '$elemMatch': {
                'playlist_name': playlist_name,
                'tracks.preview_url': url
            }
        }  
    }
    result = collection.count_documents(query)
    # print(result)
    return result



def remove_music(user_id, playlist_name, track_name):
    track_name_pattern = re.compile(track_name, re.IGNORECASE)
    playlist_name_pattern = re.compile(playlist_name, re.IGNORECASE)


    query = {
        'user_id': user_id,
        'playlists': {
            '$elemMatch': {
                'playlist_name': {"$regex": playlist_name_pattern},
                'tracks.track_name': {"$regex": track_name_pattern}
            }
        }
    }

    update = {
        "$pull": {
            "playlists.$.tracks": {"track_name": track_name_pattern}
        }
    }
    result = collection.update_one(query, update)
    return result


def add_track(user_id, playlist_name, track):
    update = {
        '$push': {
            'playlists.$[playlist].tracks': track
        }
    }
    array_filters = [{'playlist.playlist_name': playlist_name}]
    result = collection.update_one({'user_id': user_id}, update, array_filters=array_filters)
    return result




def check_playlist_exist(user_id, playlist_name):
    query = {
            "user_id": user_id,
            "playlists": {
                "$elemMatch": {
                    "playlist_name": playlist_name
                }
            }
        }
    result = collection.find(query)
    return result.count()


def create_playlist(user_id, playlist_name):
    query = {'user_id': user_id}
    new_playlist = {'playlist_name': playlist_name,'tracks': []}
    update = {'$push': {'playlists': new_playlist}}
    collection.update_one(query, update)

def create_user_playlist(user_id, playlist_name):
    new_object = { 'user_id': user_id, 'playlists': [{'playlist_name': playlist_name, 'tracks': []}] }
    collection.insert_one(new_object)


def remove_playlist(user_id, playlist_name):
    query = {
        "user_id": user_id,
        "playlists.playlist_name": playlist_name
    }

    update = {
        "$pull": {
            "playlists": {
                "playlist_name": playlist_name
            }
        }
    }

    result = collection.update_many(query, update)
    return result
    


'''
    songData = {
        user_id: String
        playlists : [playlist_object]
    }       
    playlist_object = {
        playlist_name: String
        tracks = [track_object]
    }
    
    track_object = {
        name: String,
        artist : String
        duration : int
        cover_image_url : String
        preview_url: String
    }


    This is a schema object. Write a query that checks whether a playlist with a given name exists or not. If it does exist then remove that playlist.
'''

    


