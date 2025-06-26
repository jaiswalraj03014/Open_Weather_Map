import os
from dotenv import load_dotenv
import httpx

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"

async def get_weather(city):
    url = f"{BASE_URL}/weather?q={city}&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            data = res.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The current temperature in {city} is {temp}°C with {desc}."
        else:
            return f"Could not fetch weather for {city}."

async def get_forecast(city):
    url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        if res.status_code == 200:
            forecast_data = res.json()["list"][:5]
            result = []
            for f in forecast_data:
                result.append(f"{f['dt_txt']}: {f['main']['temp']}°C, {f['weather'][0]['description']}")
            return "\n".join(result)
        else:
            return f"Could not fetch forecast for {city}."