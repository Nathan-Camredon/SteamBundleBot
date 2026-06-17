# Architecture & Business Logic

## Domain
**SteamBundleBot** is designed to identify profitable Steam bundles by comparing bundle prices against the market value of individual trading cards or items.

## Core Modules
- **storeFetcher**: Fetches bundle and game data from the Steam Store API/Scraping.
- **marketFetcher**: Fetches item prices from the Steam Community Market.
- **profitCalculator**: Calculates the potential profit based on bundle cost vs. market value of drops.
- **databaseManager**: Manages local data persistence to cache prices and prevent redundant requests.

## Workflow
1. Fetch available bundles.
2. For each bundle, extract games.
3. For each game, check if it has trading cards or market items.
4. Calculate the total estimated market value.
5. Compare bundle price with potential market value to flag profitable opportunities.


## UML class Mermaid code 
classDiagram
    class SteamScannerBot {
        - StoreFetcher store_fetcher
        - GameDetailsFetcher details_fetcher
        - MarketFetcher market_fetcher
        - DatabaseManager db
        - ProfitCalculator calculator
        + run_daily_batch() void
    }

    class StoreFetcher {
        - str target_url
        - dict headers
        + fetch_cheap_promos() tuple~list, list~
    }

    class GameDetailsFetcher {
        - str base_url
        - dict headers
        + has_trading_cards(app_id: int) bool
    }

    class MarketFetcher {
        - str base_url
        + get_average_card_price(app_id: int, card_name: str) float
        - _sleep_to_prevent_ban() void
    }

    class DatabaseManager {
        - Connection conn
        + setup_tables() void
        + is_item_already_scanned(item_id: str) bool
        + save_profitable_item(item_id: str, profit: float) void
        + clean_old_entries(days: int) void
    }

    class Game {
        + int app_id
        + str title
        + float final_price
        + int total_card_set
        + drops_available() int
    }

    class Bundle {
        + int bundle_id
        + str name
        + float final_price
        + list~Game~ games
        + get_valid_games() list~Game~
    }

    class ProfitCalculator {
        + calculate_net_fee(gross_price: float) float
        - _calculate_game_ev(game: Game, avg_card_price: float) float
        + is_solo_game_profitable(game: Game, avg_card_price: float) float
        + is_bundle_profitable(bundle: Bundle, dict_card_prices: dict) float
    }

    SteamScannerBot --> StoreFetcher : utilise
    SteamScannerBot --> GameDetailsFetcher : utilise
    SteamScannerBot --> MarketFetcher : utilise
    SteamScannerBot --> DatabaseManager : utilise
    SteamScannerBot --> ProfitCalculator : utilise
    
    StoreFetcher ..> Game : instancie (Type 0)
    StoreFetcher ..> Bundle : instancie (Type 1)
    Bundle "1" *-- "1..*" Game : contient
    ProfitCalculator ..> Game : évalue
    ProfitCalculator ..> Bundle : évalue