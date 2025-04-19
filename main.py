from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from fuzzywuzzy import fuzz

app = FastAPI()

# Подключаем папку для шаблонов и статики
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Токен доступа к Genius API
access_token = 'm0ReUc39wpBnh5auzZVAvgyMh-7RIHJSVZ0GSt9JrolLCnDocRyScuKYtmWZMQLS'

# Функция для поиска
def search_song_by_lyrics(lyrics_snippet: str, similarity_threshold: int = 0):
    search_url = 'https://api.genius.com/search'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {'q': lyrics_snippet}

    response = requests.get(search_url, headers=headers, params=params)
    results = []
    if response.status_code == 200:
        data = response.json()
        hits = data['response']['hits']
        if hits:
            for hit in hits:
                song = hit['result']
                similarity = fuzz.partial_ratio(lyrics_snippet.lower(), song['title'].lower())
                if similarity >= similarity_threshold:
                    results.append({
                        'title': song['full_title'],
                        'url': song['url']
                    })
    return results

# Главная страница
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Обработка поиска
@app.get("/search")
async def search(q: str = ""):
    if q:
        results = search_song_by_lyrics(q)
        return JSONResponse(content=results)
    return JSONResponse(content=[])
