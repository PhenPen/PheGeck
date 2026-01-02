''' Coin Gecko API Parameters Documentation '''

# Note: Path parameters (e.g., {id}) are NOT included here - only query parameters
# Path parameters are part of the URL path, not query string

PARAMS_COINS = {
    '/ping': [],
    '/simple/price': ['ids', 'names', 'symbols', 'vs_currencies', 'include_tokens', 'include_market_cap', 'include_24hr_vol', 'include_24hr_change', 'include_last_updated_at', 'precision'],
    '/simple/token_price/{id}': ['contract_addresses', 'vs_currencies', 'include_market_cap', 'include_24hr_vol', 'include_24hr_change', 'include_last_updated_at', 'precision'],
    '/simple/supported_vs_currencies': [],
    '/coins/list': ['include_platform', 'status'],
    '/coins/markets': ['vs_currency', 'ids', 'names', 'symbols', 'include_tokens', 'category', 'order', 'per_page', 'page', 'sparkline', 'price_change_percentage', 'locale', 'precision'],
    '/coins/{id}': ['localization', 'tickers', 'market_data', 'community_data', 'developer_data', 'sparkline', 'include_categories_details', 'dex_pair_format'],
    '/coins/{id}/tickers': ['exchange_ids', 'include_exchange_logo', 'page', 'order', 'depth', 'dex_pair_format'],
    '/coins/{id}/history': ['date', 'localization'],
    '/coins/{id}/market_chart': ['vs_currency', 'days', 'interval', 'precision'],
    '/coins/{id}/market_chart/range': ['vs_currency', 'from', 'to', 'interval', 'precision'],
    '/coins/{id}/ohlc': ['vs_currency', 'days', 'interval', 'precision'],
    '/coins/categories/list': [],
    '/coins/categories': ['order', 'per_page', 'page']
}

PARAMS_NFTS = {
    '/nfts/list': ['order', 'per_page', 'page'],
    '/nfts/{id}': [],
    '/nfts/{asset_platform_id}/contract/{contract_address}': []
}

PARAMS_EXCHANGES_SPOT = {
    '/exchanges': ['per_page', 'page'],
    '/exchanges/list': ['status'],
    '/exchanges/{id}': ['dex_pair_format'],
    '/exchanges/{id}/tickers': ['coin_ids', 'include_exchange_logo', 'page', 'depth', 'order', 'dex_pair_format'],
    '/exchanges/{id}/volume_chart': ['days']
}

PARAMS_EXCHANGES_DERIVATIVES = {
    '/derivatives': [],
    '/derivatives/exchanges': ['order', 'per_page', 'page'],
    '/derivatives/exchanges/{id}': ['include_tickers'],
    '/derivatives/exchanges/list': []
}

PARAMS_TREASURY = {
    '/entities/list': [],
    '/{entity}/public_treasury/{coin_id}': [],
    '/public_treasury/{entity_id}': [],
    '/public_treasury/{entity_id}/{coin_id}/holding_chart': ['days'],
    '/public_treasury/{entity_id}/transaction_history': ['asset_id']
}

PARAMS_SEARCH = {
    '/search': ['query'],
    '/search/trending': ['show_max'],
    '/asset_platforms': ['filter'],
    '/token_lists/{asset_platform_id}/all.json': []
}

PARAMS_ONCHAIN = {
    '/onchain/networks': [],
    '/onchain/networks/{network}/dexes': [],
    '/onchain/networks/{network}/tokens/{token_address}/info': [],
    '/onchain/networks/{network}/pools/{pool_address}': [],
    '/onchain/networks/{network}/pools/multi/{pool_addresses}': [],
    '/onchain/networks/trending_pools': ['page', 'per_page'],
    '/onchain/networks/{network}/trending_pools': ['page', 'per_page'],
    '/onchain/networks/{network}/pools': ['page', 'per_page'],
    '/onchain/networks/{network}/dexes/{dex}/pools': ['page', 'per_page'],
    '/onchain/networks/new_pools': ['page', 'per_page'],
    '/onchain/networks/{network}/new_pools': ['page', 'per_page'],
    '/onchain/search/pools': ['query', 'page', 'per_page'],
    '/onchain/networks/{network}/pools/{pool_address}/info': [],
    '/onchain/simple/networks/{network}/token_price/{token_addresses}': [],
    '/onchain/networks/{network}/tokens/{token_address}/pools': ['page', 'per_page'],
    '/onchain/networks/{network}/tokens/{token_address}': [],
    '/onchain/tokens/info_recently_updated': ['page', 'per_page'],
    '/onchain/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}': ['from', 'to'],
    '/onchain/networks/{network}/pools/{pool_address}/trades': ['page', 'per_page']
}

PARAMS_ALL = {**PARAMS_COINS, **PARAMS_NFTS, **PARAMS_EXCHANGES_SPOT, **PARAMS_EXCHANGES_DERIVATIVES, **PARAMS_TREASURY, **PARAMS_SEARCH, **PARAMS_ONCHAIN}

# Params details/descriptions
PARAMS_ALL_DETAILS = {
    'asset_id': 'Filter by asset ID (used in treasury endpoints to query specific coin holdings)',
    'category': 'Filter coins by category (e.g., layer-1, defi, gaming)',
    'coin_ids': 'Comma-separated coin IDs to filter exchange tickers',
    'community_data': 'Boolean flag to include community data (Reddit, Telegram followers, etc.) in response',
    'contract_addresses': 'Comma-separated token contract addresses for querying token prices by address',
    'date': 'Historical data snapshot date in ISO format (YYYY-MM-DD)',
    'days': 'Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or max for all available data)',
    'depth': 'Boolean flag to include 2% orderbook depth (cost_to_move_up_usd and cost_to_move_down_usd)',
    'developer_data': 'Boolean flag to include developer data (GitHub stats, commits, etc.) in response',
    'dex_pair_format': 'Display format for DEX pairs - contract_address or symbol (e.g., WETH, USDC)',
    'exchange_ids': 'Comma-separated exchange IDs to filter tickers by specific exchanges',
    'filter': 'Apply filters to results (e.g., nft to get NFT-supporting asset platforms)',
    'from': 'Starting date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)',
    'ids': 'Comma-separated coin IDs to query (e.g., bitcoin,ethereum)',
    'include_24hr_change': 'Boolean flag to include 24-hour price change percentage in response',
    'include_24hr_vol': 'Boolean flag to include 24-hour trading volume in response',
    'include_categories_details': 'Boolean flag to include detailed category information with metadata',
    'include_exchange_logo': 'Boolean flag to include exchange logo URL in response',
    'include_last_updated_at': 'Boolean flag to include last updated timestamp (UNIX) in response',
    'include_market_cap': 'Boolean flag to include market capitalization in response',
    'include_platform': 'Boolean flag to include platform and token contract addresses in coins list',
    'include_tickers': 'Include tickers data - all (all tickers), unexpired (non-expired only), or empty to omit',
    'include_tokens': 'For symbol lookups - top (top-ranked tokens only) or all (all matching tokens)',
    'interval': 'Data interval granularity - 5m (5-minute), hourly, or daily (Enterprise plans support 5m and hourly)',
    'locale': 'Language/localization code for response (en, es, fr, ja, zh, etc.)',
    'localization': 'Boolean flag to include localized coin names in all supported languages',
    'market_data': 'Boolean flag to include market data (price, market cap, volume, ATH, ATL, etc.)',
    'names': 'Comma-separated coin names to query (e.g., Bitcoin,Ethereum)',
    'order': 'Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)',
    'page': 'Page number for pagination (starting from 1)',
    'per_page': 'Number of results per page (1-250, default varies by endpoint)',
    'precision': 'Decimal places for price values (full or 0-18 digits)',
    'price_change_percentage': 'Include price change percentages for specific timeframes (1h, 24h, 7d, 14d, 30d, 200d, 1y)',
    'query': 'Search query string to find coins, categories, exchanges, or NFTs',
    'show_max': 'Show maximum results available - coins, nfts, categories (comma-separated for multiple)',
    'sparkline': 'Boolean flag to include 7-day sparkline chart data',
    'status': 'Filter by status - active (listed) or inactive (delisted) coins/exchanges',
    'symbols': 'Comma-separated coin symbols to query (e.g., btc,eth)',
    'tickers': 'Boolean flag to include exchange tickers data in coin response',
    'to': 'Ending date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)',
    'vs_currencies': 'Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)'
}




