import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyManager:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.sp = None

    def authenticate(self):
        auth_manager = SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope="playlist-modify-public playlist-modify-private")
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        print("Login Success")

    def remove_tracks_from_playlist(self, playlist_id: str, track_uris: list):
        self.sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
        print("Tracks removed from playlist")

    def get_tracks_from_playlist(self, playlist_id: str):
        results = self.sp.playlist_tracks(playlist_id)
        return [item['track']['uri'] for item in results['items']]

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list):
        self.sp.playlist_add_items(playlist_id, track_uris)
        print("Tracks added to playlist")

    def search_artist(self, artist_name: str):
        results = self.sp.search(q=artist_name, type='artist', limit=1, market='KR')
        return results['artists']['items'][0]['uri']

    def change_playlist_details(self, playlist_id: str, name: str, description: str):
        self.sp.playlist_change_details(playlist_id, name=name, description=description)
        print("Playlist details changed")

    def search_track(self, track_name: str, artist_name: str):
        artist_id = self.search_artist(artist_name.split()[0])
        artist_id2= self.search_artist(artist_name.split()[-1])
        artist_id3 = self.search_artist(artist_name.split(",")[0])
        if artist_id or artist_id2 or artist_id3:
            results = self.sp.search(q=f"{track_name} {artist_name.split()[0]}", type='track', limit=10, market='KR')
            for item in results['tracks']['items']:
                if artist_id in item["album"]["artists"][0]["uri"] or artist_id2 in item["album"]["artists"][0]["uri"] or artist_id3 in item["album"]["artists"][0]["uri"]:
                    return item['uri']
            return results['tracks']['items'][0]['uri']
        else:
            results = self.sp.search(q=f"{track_name} {artist_name.split()[0]}", type='track', limit=1, market='KR')
            return results['tracks']['items'][0]['uri']
