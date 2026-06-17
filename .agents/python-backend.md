# Python Backend Rules

## Tech Stack
- **Python 3.10+**
- **Libraries**: `requests` (API calls), `beautifulsoup4` (Scraping), `python-dotenv` (Env vars).

## Coding Standards
- **Type Hints**: Always use `def fetch_data(url: str) -> dict:`
- **Error Handling**: Wrap network calls in `try...except` and handle timeouts/HTTP errors gracefully. Do not let the bot crash on a single failed request.
- **Rate Limiting**: Steam APIs are heavily rate-limited. Always include `time.sleep()` between requests or implement a queue/delay mechanism.
- **Environment Variables**: Never hardcode credentials. Use `os.getenv('STEAM_API_KEY')` and `os.getenv('STEAM_ID')` after loading `.env`.

## Project Structure
- `main.py`: Entry point.
- `src/`: Contains all business logic modules (`bundle.py`, `game.py`, `marketFetcher.py`, etc.).
