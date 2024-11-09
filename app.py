from flask import Flask, request, jsonify, render_template
import requests
from fuzzywuzzy import fuzz

app = Flask(__name__)

# Ваш токен доступа
access_token = 'm0ReUc39wpBnh5auzZVAvgyMh-7RIHJSVZ0GSt9JrolLCnDocRyScuKYtmWZMQLS'

# Функция для поиска песни по тексту с приближенным поиском
def search_song_by_lyrics(lyrics_snippet, similarity_threshold=0):
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if query:
        results = search_song_by_lyrics(query)
        return jsonify(results)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
