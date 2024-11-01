import requests
from bs4 import BeautifulSoup

async def get_tj_song():
    url = 'https://www.tjmedia.com/tjsong/song_monthPopular.asp?strType=1&SYY=2024&SMM=10&EYY=2024&EMM=11'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select('#BoardType1 > table > tbody > tr > td')
    song_lists = []
    for i in range(2, len(titles), 4):
        song_lists.append([titles[i].text, titles[i + 1].text])
    return song_lists

