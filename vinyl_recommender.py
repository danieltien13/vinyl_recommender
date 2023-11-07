import json
import os
import requests
from actual_secrets import spotify_token


class VinylRecommender:
    def __init__(self):
        pass

    def recommend_vinyl(self):
        """Recommend a vinyl to purchase based on listening history"""
        time_range = "medium_term"
        song_limit = "50"
        offset = "0"

        query = "https://api.spotify.com/v1/me/top/tracks?time_range={}&limit={}&offset={}".format(
            time_range, song_limit, offset)

        response = requests.get(
            query,
            headers={
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        return response.json()


if __name__ == '__main__':
    rec = VinylRecommender()
    song_list = rec.recommend_vinyl()
    print('Here is a list of 3 albums you might like based your Spotify listening history!')
    print()
    album_dict = {}
    for song in song_list['items']:
        song_name = song['name']
        artist_name = song['artists'][0]['name']
        album_name = song['album']['name']
        if album_name not in album_dict:
            album_dict[album_name] = [[song_name], artist_name, 1]
        else:
            album_dict[album_name][0].append(song_name)
            album_dict[album_name][2] += 1
    i = 0
    for key, value in sorted(album_dict.items(), key=lambda e: e[1][2], reverse=True):
        if i < 3:
            print(key, value)
            print()
            i += 1
