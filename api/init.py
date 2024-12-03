import aiohttp
import config
from typing import Dict, Any

API_URL = "https://imdb-top-100-movies1.p.rapidapi.com/"
HEADERS = {
    "X-RapidAPI-Key": config.rapid_API_KEY,
    "X-RapidAPI-Host": "imdb-top-100-movies.p.rapidapi.com",
}


async def fetch_movies() -> Dict[str, Any]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    raise Exception(f"Ошибка при запросе: HTTP {response.status}")
    except aiohttp.ClientError as e:
        return {"error": f"Сетевое исключение: {str(e)}"}
    except Exception as e:
        return {"error": f"Неизвестная ошибка: {str(e)}"}
