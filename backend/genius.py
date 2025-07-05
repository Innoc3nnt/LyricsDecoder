import os
import re
import httpx
from bs4 import BeautifulSoup

GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')
HEADERS = {"Authorization": f"Bearer {GENIUS_TOKEN}"} if GENIUS_TOKEN else {}
API_URL = "https://api.genius.com"

async def search_song(query: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/search", params={"q": query}, headers=HEADERS)
        r.raise_for_status()
        return r.json()['response']['hits']

async def get_song(song_id: int):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{API_URL}/songs/{song_id}", headers=HEADERS)
        r.raise_for_status()
        return r.json()['response']['song']

async def parse_referents(song_id: int):
    url = f"https://genius.com/songs/{song_id}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        html = r.text
    soup = BeautifulSoup(html, 'lxml')
    nodes = []
    edges = []
    lyric_lines = soup.select('.referent')
    for ref in lyric_lines:
        line = ref.get_text(strip=True)
        annotation_links = ref.select('a')
        for a in annotation_links:
            href = a.get('href', '')
            if 'genius.com' in href:
                m = re.search(r'/songs/(\d+)', href)
                if m:
                    target = f"song_{m.group(1)}"
                    edges.append({
                        'data': {
                            'source': f'song_{song_id}',
                            'target': target,
                            'relation': 'refers to',
                            'line': line
                        }
                    })
    return nodes, edges
