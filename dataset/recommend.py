import pandas as pd
from db import admin
from api import search
from scipy.spatial.distance import euclidean
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler


def euclidean(x, y):
    return distance.euclidean(x, y)



def list_similar_songs(user_id, playlist_name, recommended_indices):
    df = pd.read_csv('dataset/genres_v2.csv', low_memory=False)
    attributes = {}
    n = 0
    for document in admin.get_playlist(user_id, playlist_name):
        playlist = document["playlists"][0]
        for track in playlist['tracks']:
            track_id = track['track_id']
            track_attribute = search.get_attributes(track_id)
            n += 1
            for key, value in track_attribute.items():
                attributes[key] = attributes.get(key, 0) + value
        


    updated_dict = {key: value / n for key, value in attributes.items()}

    desired_attributes = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
    
    # scaler = MinMaxScaler()
    # input_attributes = scaler.fit_transform([list(updated_dict.values())])
    # input_attributes = pd.DataFrame(input_attributes, columns=desired_attributes)    
    # df[desired_attributes] = scaler.transform(df[desired_attributes])

    df['distance'] = df[desired_attributes].apply(lambda x: euclidean(x.values, list(updated_dict.values())), axis=1)
    df = df.sort_values('distance')

    similar_songs = []

    for _, row in df.iterrows():
        uri = row['uri']
        track_id = uri[14::]

        if track_id not in recommended_indices and not admin.check_track_exists(user_id, playlist_name, track_id):
            track_obj = search.spotify_get_track(track_id)
            recommended_indices.append(track_id)

            if track_obj['preview_url'] == None:
                track_preview_url, track_obj = search.fetch_audio_stream(track_obj['track_name'])

            track_obj['track_id'] =track_id
            similar_songs.append(track_obj)

        if len(similar_songs) >= 5:
            break

    return similar_songs, recommended_indices


