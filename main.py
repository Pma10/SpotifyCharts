import asyncio
from dotenv import load_dotenv
import os
from tqdm import tqdm
from datetime import datetime, timezone, timedelta
from Tools.SpotifyManager import SpotifyManager
from Tools.getMelonChart import get_melon_chart
from Tools.getTjSong import get_tj_song

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PLAYLIST_ID_MELON = os.getenv("PLAYLIST_ID_MELON")
PLAYLIST_ID_TJ = os.getenv("PLAYLIST_ID_TJ")

async def update_playlist(spotify, playlist_id, chart, chart_name):
    print(f"Getting {chart_name} chart...")
    chart_data = await chart()
    uris = [spotify.search_track(title, artist) for title, artist in tqdm(chart_data)]
    print(f"Finished searching for tracks on Spotify for {chart_name} chart")

    current_tracks = spotify.get_tracks_from_playlist(playlist_id)
    if current_tracks:
        print(f"Removing current tracks from {chart_name} playlist...")
        spotify.remove_tracks_from_playlist(playlist_id, current_tracks)

    print(f"Adding new tracks to {chart_name} playlist...")
    spotify.add_tracks_to_playlist(playlist_id, uris)

    KST = timezone(timedelta(hours=9))
    date = datetime.now(KST).strftime("%y%m%d")
    description = f"📅 {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}에 자동으로 업데이트 됨. 자세한 문의는 디스코드 pma10으로 부탁드립니다"
    if chart_name == "멜론":
        spotify.change_playlist_details(playlist_id, f"실시간 멜론 차트 TOP 100 {date} [ 멜론 Chart]", description)
    elif chart_name == "TJ노래방":
        spotify.change_playlist_details(playlist_id, f"TJ노래방 {date} [ {chart_name}]", description)
    else:
        spotify.change_playlist_details(playlist_id, f"실시간 {chart_name} 차트 TOP 100 {date} [ {chart_name} Chart]", description)
    print(f"Finished updating {chart_name} playlist")

async def main():
    spotify = SpotifyManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    spotify.authenticate()

    await update_playlist(spotify, PLAYLIST_ID_MELON, get_melon_chart, "멜론")
    await update_playlist(spotify, PLAYLIST_ID_TJ, get_tj_song, "TJ노래방")

    print("Finished updating all playlists")

asyncio.run(main())