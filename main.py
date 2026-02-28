import requests
import random
from dotenv import load_dotenv
from os import getenv

load_dotenv()

TMDB_API_KEY = getenv('TMDB_API_KEY')
DISCORD_WEB_HOOK = getenv('DISCORD_WEB_HOOK')

headers = {
    "accept": "application/json",
    "Authorization" : f"Bearer {TMDB_API_KEY}"
}

url = 'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=vote_average.desc&vote_average.gte=5&vote_count.gte=1000&with_genres=27&page=1'


response = requests.get(url, headers=headers)

json = response.json()

randomPage = random.randrange(1, json['total_pages'])
print(f"random page: {randomPage}")
randomEntry = random.randrange(0,19)
print(f"random entry = {randomEntry}")

url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=vote_average.desc&vote_average.gte=5&vote_count.gte=1000&with_genres=27&page={randomPage}'

response = requests.get(url, headers=headers)

json = response.json()
movie = json['results'][randomEntry] if json['results'][randomEntry] else json['results'][0]
title = movie['title']
releaseDate = movie['release_date'].split('-')[0]

postbody = {
    "content": f"Random Horror Movie of the Week: {title}, Released {releaseDate}.\nhttps://image.tmdb.org/t/p/original{movie['poster_path']}"
}

requests.post(DISCORD_WEB_HOOK, json = postbody)

