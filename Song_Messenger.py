import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random 
from twilio.rest import Client
from datetime import datetime
import schedule
import time

def get_song():
    CLIENT_ID = ''
    CLIENT_SECRET = ''

    client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
    playlist = sp.playlist(playlist_id)

    tracks = playlist['tracks']['items']

    all_songs = []

    for track in tracks:
        song_name = track['track']['name']
        all_songs.append(song_name)

    chosen_song = random.choice(all_songs)

    results = sp.search(q=chosen_song, type="track", limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_name = track['name']
        artists = [artist['name'] for artist in track['artists']]
        return (f"The Song of the Day is: Track: {song_name}, Artists: {', '.join(artists)}")
    else:
        return None


def send_song():
    
    account_SID  = ''
    auth_token = ''
    twilio_number = ''
    target_number = ''
    
    
    client = Client(account_SID, auth_token)

    song_of_day = get_song()
    
    message = client.messages.create(
        body=song_of_day,
        from_=twilio_number,
        to=target_number
    )
    

def main():
    schedule.every().day.at("14:22").do(send_song)
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    main()
