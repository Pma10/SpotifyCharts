import aiohttp
from bs4 import BeautifulSoup

async def get_melon_chart():
    url = 'https://www.melon.com/chart/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
            titles = soup.select('div.ellipsis.rank01 > span > a')
            artists = soup.select('div.ellipsis.rank02 > span')
            melon_chart = []
            for i in range(min(100, len(titles), len(artists))):
                melon_chart.append([titles[i].text, artists[i].text])
            return melon_chart