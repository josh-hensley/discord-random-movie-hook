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

genres = [
		{
			"id": "28%7C12",
			"name": "Action/ Adventure"
		},
		{
			"id": 35,
			"name": "Comedy"
		},
		{
			"id": 99,
			"name": "Documentary"
		},
		{
			"id": "18%7C9648",
			"name": "Drama/ Mystery"
		},
		{
            "id": 10749,
			"name": "Romance"
		},
		{
            "id": 878,
			"name": "Science Fiction"
		},
        {
            "id": "27%7C53",
            "name": "Horror/ Thriller"
        }
	]
    
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

randomEntry = random.randrange(0, json['total_results'] - 1)
pageItem = randomEntry % 20
page = math.floor(randomEntry / 20) + 1
print(f"random entry: {randomEntry}\npage: {page}\nitem: {pageItem}")

url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=vote_average.desc&vote_average.gte=5&vote_count.gte=500&with_genres={genre["id"]}&page={page}'

response = requests.get(url, headers=headers)

json = response.json()
movie = json['results'][pageItem]
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

 