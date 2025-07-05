from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from genius import search_song, get_song, parse_referents

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/api/search')
async def search(q: str):
    hits = await search_song(q)
    return {'hits': [h['result'] for h in hits]}

@app.get('/api/song/{song_id}')
async def song(song_id: int):
    s = await get_song(song_id)
    return s

@app.get('/api/graph/{song_id}')
async def graph(song_id: int):
    song_data = await get_song(song_id)
    nodes = [{
        'data': {
            'id': f'song_{song_id}',
            'label': song_data['title'],
            'artist': song_data['primary_artist']['name'],
            'image': song_data.get('song_art_image_thumbnail_url')
        }
    }]
    ref_nodes, edges = await parse_referents(song_id)
    nodes.extend(ref_nodes)
    return {'nodes': nodes, 'edges': edges}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
