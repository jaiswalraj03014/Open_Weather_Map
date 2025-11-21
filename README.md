# Weather MCP Server

A FastAPI-based Model Context Protocol (MCP) server that provides current weather and forecast information for cities worldwide using the OpenWeatherMap API.

## Features

- **Current Weather**: Get real-time temperature and weather conditions for any city
- **5-Day Forecast**: Retrieve weather forecast for the next 5 days
- **Smart City Detection**: Automatically extracts city names from natural language queries
- **Async Implementation**: Built with async/await for better performance

## Installation

1. Clone or download the project files
2. Install required dependencies:
```bash
pip install fastapi uvicorn httpx python-dotenv
```

3. Set up your OpenWeatherMap API key:
   - Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Create a `.env` file in the project root:
```env
OPENWEATHER_API_KEY=your_api_key_here
```

## Project Structure

```
weather-mcp/
├── main.py              # FastAPI application with MCP endpoints
├── weather_utils.py     # Weather API utilities
├── .env                 # Environment variables (create this)
└── README.md
```

## Usage

### Running the Server

```bash
uvicorn main:app --reload --port 8000
```

The server will start at `http://localhost:8000`

### API Endpoints

#### POST `/mcp`
Main endpoint for weather queries. Accepts natural language requests.

**Request Body:**
```json
{
  "context": "What's the weather in London?"
}
```

**Example Responses:**
```json
{
  "response": "The current temperature in London is 15°C with scattered clouds."
}
```

```json
{
  "response": "2024-01-15 12:00:00: 16°C, light rain\n2024-01-15 15:00:00: 17°C, overcast clouds\n..."
}
```

#### GET `/metadata`
Returns server metadata and endpoint information.

**Response:**
```json
{
  "name": "Weather Tool",
  "description": "Provides current weather and forecast by city.",
  "endpoint": "http://localhost:8000/mcp"
}
```

### Supported Query Types

The server understands natural language queries like:

- "What's the temperature in Paris?"
- "Show me the weather forecast for New York"
- "Will it rain in Tokyo tomorrow?"
- "How's the weather in Berlin?"

## Example Usage

### Using curl

```bash
# Current weather
curl -X POST "http://localhost:8000/mcp" \
  -H "Content-Type: application/json" \
  -d '{"context": "What is the weather in Tokyo?"}'

# Forecast
curl -X POST "http://localhost:8000/mcp" \
  -H "Content-Type: application/json" \
  -d '{"context": "Show me the forecast for London"}'
```

### Using Python

```python
import httpx
import asyncio

async def test_weather():
    async with httpx.AsyncClient() as client:
        # Current weather
        response = await client.post(
            "http://localhost:8000/mcp",
            json={"context": "What's the temperature in Paris?"}
        )
        print(response.json())
        
        # Forecast
        response = await client.post(
            "http://localhost:8000/mcp",
            json={"context": "Forecast for New York next days"}
        )
        print(response.json())

asyncio.run(test_weather())
```

## Error Handling

- Returns user-friendly error messages when city is not found
- Handles API key authentication errors
- Provides fallback responses for unrecognized queries

## Dependencies

- `fastapi`: Web framework for building APIs
- `httpx`: Async HTTP client for API requests
- `python-dotenv`: Environment variable management
- `uvicorn`: ASGI server for running the application

## Configuration

- Default port: 8000
- Temperature units: Metric (°C)
- Forecast: 5 days with 3-hour intervals

## Notes

- Requires a valid OpenWeatherMap API key
- City names are automatically extracted from queries
- Default fallback city: Delhi (when no city is detected)

## License

This project is open source and available under the [MIT License](LICENSE).
