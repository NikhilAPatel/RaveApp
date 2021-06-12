import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config
import csv
from song import Song

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(config('SPOTIPY_CLIENT_ID'), config('SPOTIPY_CLIENT_SECRET')))
songs = []

def get_id(song):
    name = song.name
    artist = song.artist
    results = spotify.search(q='track:' + name, type='track', limit=1)
    items = results['tracks']['items']
    if len(items) > 0:
        track = items[0]
        return track['id']
        # print(track['name'], name, track['artists'][0]['name'], artist)
        # if(track['name']==name and track['artists'][0]['name']==artist):
        #     print("success")
        #     # We have found the correct song and can add the id
        #     return track['id']

def get_features(song):
    id = song.id
    results = spotify.audio_features(id)
    return results


with open('SongEmotionScore.csv', 'r') as file:
    i=0
    reader = csv.reader(file)
    for row in reader:
        song = Song(row[1], row[2], row[3])
        song.id=get_id(song)
        try:
            song.assign_features(get_features(song))
            songs.append(song)
            print((str)(i)+"/4159")
        except:
            print("Song Not Found")
        i+=1
        
        
with open("output.csv", "w") as outputfile:
    csvwriter = csv.writer(outputfile)

    # Write the header row
    csvwriter.writerow(vars(songs[0]).keys())
    
    # Write the remaining rows
    for song in songs:
        row = []
        for key in vars(song).keys():
            row.append(vars(song)[key])

        csvwriter.writerow(row)