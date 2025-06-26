from fastapi import FastAPI, Request
from . import weather_utils as wu
import re

app = FastAPI()

def extract_city(text):
    match = re.findall(r"in\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    if match:
        return match[-1]
    words = text.split()
    cities = [w for w in words if w.istitle()]
    return cities[-1] if cities else "Delhi"

@app.post("/mcp")
async def weather_mcp(req: Request):
    body = await req.json()
    context = body.get("context", "")

    lower_context = context.lower()

    if "forecast" in lower_context or "next days" in lower_context:
        city = extract_city(context)
        result = await wu.get_forecast(city)
        return {"response": result}
    
    if "temperature" in lower_context or "weather" in lower_context or "rain" in lower_context:
        city = extract_city(context)
        result = await wu.get_weather(city)
        return {"response": result}
    
    return {"response": "I didn't understand your weather query."}

@app.get("/metadata")
async def metadata(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "name": "Weather Tool",
        "description": "Provides current weather and forecast by city.",
        "endpoint": f"{base_url}/mcp"
    }