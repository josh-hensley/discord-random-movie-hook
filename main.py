import requests
import random
import math
import datetime
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()

TMDB_API_KEY = getenv('TMDB_API_KEY')
DISCORD_WEB_HOOK = getenv('DISCORD_WEB_HOOK')
TEST_HOOK = getenv('TEST_HOOK')

with open('genres.json') as file:
    data = json.load(file)
    genres = data["genres"]
    
date = datetime.datetime.now()
day = date.weekday()

genre = genres[day]

headers = {
    "accept": "application/json",
    "Authorization" : f"Bearer {TMDB_API_KEY}"
}

url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=vote_average.desc&vote_average.gte=5&vote_count.gte=1000&with_genres={genre["id"]}&page=1"


response = requests.get(url, headers=headers)

json = response.json()

randomEntry = random.randrange(1, json['total_results'])
pageItem = randomEntry % 19
page = math.floor(randomEntry / 19) + 1
print(f"random entry: {randomEntry}\npage: {page}\nitem: {pageItem}")

url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=vote_average.desc&vote_average.gte=5&vote_count.gte=1000&with_genres={genre["id"]}&page={page}'

response = requests.get(url, headers=headers)

json = response.json()
movie = json['results'][pageItem] if json['results'][pageItem] else json['results'][0]
title = movie['title']
releaseDate = movie['release_date'].split('-')[0]
plot = movie['overview']
image = f"https://image.tmdb.org/t/p/original{movie['poster_path']}"

postbody = {
    "content" : f"Random {genre["name"]} Movie of the Week:",
    "embeds" : [
        {
            "title" : title,
            "description" : f"Released {releaseDate}. {plot}",
            "image" : {
                "url" : image
                }
        }
    ]
    }

requests.post(DISCORD_WEB_HOOK, json = postbody)

 