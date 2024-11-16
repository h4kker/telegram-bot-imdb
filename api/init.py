import aiohttp

API_URL = "https://imdb-top-100-movies1.p.rapidapi.com/"
HEADERS = {
    "X-RapidAPI-Key": "8e908df381msh3445741ab9cf3cap1d60c6jsnda8602f5a917",
    "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com",
}


async def fetch_movies():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return {"error": f"Ошибка запроса: {response.status}"}
