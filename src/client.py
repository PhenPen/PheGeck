import requests, os, config
from dotenv import load_dotenv

# Loading API Key stored in env
load_dotenv() #Load every environmental variable found in any .env file in project
test_api_key = os.getenv("API_KEY")
test_debug = os.getenv("DEBUG")


base_url = config.DEFAULT_BASE_URL
default_timeout = config.TIMEOUT
default_retries = config.RETRY_ATTEMPT






class CoinGeckoClient : #() Only add parenthesis if inheriting from another class
    def __init__(self,API_Key = None) -> None:
        self.base_url = config.DEFAULT_BASE_URL
        self.API_Key = API_Key
        self.query_params = {}
        self.custom_headers = {}
        self.endpoint = None
        self.custom_timeout = config.TIMEOUT
        self.custom_retry_attempt = config.RETRY_ATTEMPT
        self.custom_retry_delay = config.RETRY_DELAY

    def api_key(self):
        '''
        Returns the API Key or None if no API Key is set.
        
        Example:
            >>> client = CoinGeckoClient("your_api_key")
            >>> print(client.api_key())
            'your_api_key'
        '''
        return self.API_Key

    def headerAPI_Key(self) -> dict:
        API_Key_Header = {'x-cg-demo-api-key' : self.API_Key}
        return API_Key_Header

    def __str__(self) -> str:
        ''' Returns a user-friendly string representation of the CoinGeckoClient instance. '''
        return f'{self.__class__.__name__}'
    
    def __repr__(self) -> str:
        ''' Returns a detailed string representation of the CoinGeckoClient instance, including the API Key for developers. '''
        return f'{self.__class__.__name__} with API Key  {self.API_Key}'
    
    @property
    def endpoints(self) :
        '''
        Uses the provided endpoint string to set the API endpoint for the request.

        Clears the previous endpoint and query parameters if an endpoint was already set 
    
        Returns: CoinGeckoClient :Self for chaining.
        '''
        self.query_params = {}
        return Endpoints(self)
    
    def params(self,params : dict) -> "CoinGeckoClient":
        ''' Uses the provided dictionary to set query parameters for the request.
        
        Args : A dictionary of query parameters (e.g., {"ids": "bitcoin", "vs_currencies": "usd"}).
        Returns: CoinGeckoClient :Self for chaining.'''
        self.query_params.update(params)
        return self
    
    
    def headers(self,headers : dict) -> "CoinGeckoClient":
        ''' Uses the provided dictionary to set custom headers for the request.
        
        Args : A dictionary of custom headers (e.g., {"Authorization": "Bearer token"}).
        Returns: CoinGeckoClient :Self for chaining.'''
        self.custom_headers.update(headers)
        return self
    
    def all_headers(self) -> dict:
        headers = {**self.headerAPI_Key(),**self.custom_headers}
        return headers
    
    @property
    def timeout(self) :
        '''
    Gets the current timeout value.
    
    Returns:
        int: The timeout in seconds
    '''
        return self.custom_timeout
    
    @timeout.setter
    def timeout(self, value):
        ''' Sets the timeout value.
    
    Args:
        value (int): The timeout in seconds
    '''
        self.custom_timeout = value
        print(f'Timeout Changed to {value} seconds') 
        

    def run(self):
        try :
            response = requests.get(f"{self.base_url}{self.endpoint}", headers=self.all_headers(), params=self.query_params, timeout=config.TIMEOUT)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json() # will change this to return response object later for more flexibility
        except AttributeError as error:
            if test_debug :
                print(f"An error occurred: {error}")
            else:
                print("Please ensure that endpoint, params, and headers are set before making a request.")
            return None
        except requests.exceptions.HTTPError as error: # Handles HTTP errors eg 4xx and 5xx status codes
            if test_debug :
                if error.response.status_code == 429:
                    print(f"Error {error.response.status_code}, Rate limit exceeded. Please try again later.")
                elif error.response.status_code == 401:
                    print(f"Error {error.response.status_code}, Unauthorized access. Please check your API key.")
                elif error.response.status_code == 404:
                    print(f"Error {error.response.status_code}, Endpoint not found. Please check the endpoint URL.")
                elif error.response.status_code == 403:
                    print(f"Error {error.response.status_code}, Forbidden access. You do not have permission to access this resource.")
                else:
                    print(f"HTTP error occurred: {error}")
            else:
                if error.response.status_code == 429:
                    print("Rate limit exceeded. Please try again later.")
                elif error.response.status_code == 401:
                    print("Unauthorized access. Please check if you have a valid API key.") 
                elif error.response.status_code == 404:
                    print("Endpoint not found. Please enter a valid endpoint URL.")
                elif error.response.status_code == 403:
                    print("Forbidden access. You are restricted from accessing this resource.")
                else:
                    print("An error occurred while processing your request.")
            return None
        except requests.exceptions.RequestException as error: # Handles other requests exceptions eg connection errors, timeouts, etc
            if test_debug :
                print(f"An error occurred while making the request: {error}")
            else:
                print("An error occurred while making the request. Please check your network connection and try again.")
            return None


class Endpoints:
    def __init__(self, client): # initializes to take in the original client and return something back
        self.client = client

    # ENDPOINT_COINS
    @property # Property decorator makes it so that, it can be called with brackets at the end
    def ping(self):
        '''
        Check the API server status.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/ping' # Changes the self.endpoint that is in the coin gecko client class from None to the new endpoint
        return self.client # Returns the client back to coin gecko client class

    @property
    def simple_price(self):
        '''
        Query the prices of one or more coins by using their unique Coin API IDs.
        
        Args:
            None
        
        Params:
            ids: Comma-separated coin IDs to query (e.g., bitcoin,ethereum)
            names: Comma-separated coin names to query (e.g., Bitcoin,Ethereum)
            symbols: Comma-separated coin symbols to query (e.g., btc,eth)
            vs_currencies: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            include_tokens: For symbol lookups - top (top-ranked tokens only) or all (all matching tokens)
            include_market_cap: Boolean flag to include market capitalization in response
            include_24hr_vol: Boolean flag to include 24-hour trading volume in response
            include_24hr_change: Boolean flag to include 24-hour price change percentage in response
            include_last_updated_at: Boolean flag to include last updated timestamp (UNIX) in response
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/simple/price'
        return self.client

    def simple_token_price(self, id):  #Does not include property decorator so it has brackets and can take in arguments 
        '''
        Query the prices of one or more coins by using their unique Coin API IDs.
        
        Args:
            id: Token contract platform address (e.g., ethereum)
        
        Params:
            contract_addresses: Comma-separated token contract addresses for querying token prices by address
            vs_currencies: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            include_market_cap: Boolean flag to include market capitalization in response
            include_24hr_vol: Boolean flag to include 24-hour trading volume in response
            include_24hr_change: Boolean flag to include 24-hour price change percentage in response
            include_last_updated_at: Boolean flag to include last updated timestamp (UNIX) in response
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/simple/token_price/{id}'
        return self.client

    @property
    def simple_supported_vs_currencies(self):
        '''
        Query all the supported currencies on CoinGecko.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/simple/supported_vs_currencies'
        return self.client

    @property
    def coins_list(self):
        '''
        Query all the supported coins on CoinGecko with coins ID, name and symbol.
        
        Args:
            None
        
        Params:
            include_platform: Boolean flag to include platform and token contract addresses in coins list
            status: Filter by status - active (listed) or inactive (delisted) coins/exchanges
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/coins/list'
        return self.client

    @property
    def coins_markets(self):
        '''
        Query all the supported coins with price, market cap, volume and market related data.
        
        Args:
            None
        
        Params:
            vs_currency: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            ids: Comma-separated coin IDs to query (e.g., bitcoin,ethereum)
            names: Comma-separated coin names to query (e.g., Bitcoin,Ethereum)
            symbols: Comma-separated coin symbols to query (e.g., btc,eth)
            include_tokens: For symbol lookups - top (top-ranked tokens only) or all (all matching tokens)
            category: Filter coins by category (e.g., layer-1, defi, gaming)
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            per_page: Number of results per page (1-250, default varies by endpoint)
            page: Page number for pagination (starting from 1)
            sparkline: Boolean flag to include 7-day sparkline chart data
            price_change_percentage: Include price change percentages for specific timeframes (1h, 24h, 7d, 14d, 30d, 200d, 1y)
            locale: Language/localization code for response (en, es, fr, ja, zh, etc.)
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/coins/markets'
        return self.client

    def coins(self, id):
        '''
        Query all the metadata (image, websites, socials, description, contract address, etc.) from the CoinGecko coin page based on a particular coin ID.
        
        Args:
            id: Coin ID (e.g., bitcoin)
        
        Params:
            localization: Boolean flag to include localized coin names in all supported languages
            tickers: Boolean flag to include exchange tickers data in coin response
            market_data: Boolean flag to include market data (price, market cap, volume, ATH, ATL, etc.)
            community_data: Boolean flag to include community data (Reddit, Telegram followers, etc.) in response
            developer_data: Boolean flag to include developer data (GitHub stats, commits, etc.) in response
            sparkline: Boolean flag to include 7-day sparkline chart data
            include_categories_details: Boolean flag to include detailed category information with metadata
            dex_pair_format: Display format for DEX pairs - contract_address or symbol (e.g., WETH, USDC)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/coins/{id}'
        return self.client

    def coins_tickers(self, id):
        '''
        Query the coin tickers on both centralized exchange (CEX) and decentralized exchange (DEX) based on a particular coin ID.
        
        Args:
            id: Coin ID (e.g., bitcoin)
        
        Params:
            exchange_ids: Comma-separated exchange IDs to filter tickers by specific exchanges
            include_exchange_logo: Boolean flag to include exchange logo URL in response
            page: Page number for pagination (starting from 1)
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            depth: Boolean flag to include 2% orderbook depth (cost_to_move_up_usd and cost_to_move_down_usd)
            dex_pair_format: Display format for DEX pairs - contract_address or symbol (e.g., WETH, USDC)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/coins/{id}/tickers'
        return self.client

    def coins_history(self, id):
        '''
        Query the historical data (price, market cap, 24hr volume, …) at a given date for a coin based on a particular coin ID.
        
        Args:
            id: Coin ID (e.g., bitcoin)
        
        Params:
            date: Historical data snapshot date in ISO format (YYYY-MM-DD)
            localization: Boolean flag to include localized coin names in all supported languages
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/coins/{id}/history'
        return self.client

    def coins_market_chart(self, id):
        '''
        Get the historical chart data of a coin including time in UNIX, price, market cap and 24hr volume based on particular coin ID.
        
        Args:
            id: Coin ID (e.g., bitcoin)
        
        Params:
            vs_currency: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or max for all available data)
            interval: Data interval granularity - 5m (5-minute), hourly, or daily (Enterprise plans support 5m and hourly)
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/coins/{id}/market_chart'
        return self.client

    def coins_market_chart_range(self, id):
        '''
        Get the historical chart data of a coin within certain time range in UNIX along with price, market cap and 24hr volume based on particular coin ID.
        
        Args:
            id: Coin ID (e.g., bitcoin)
        
        Params:
            vs_currency: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            from: Starting date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)
            to: Ending date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)
            interval: Data interval granularity - 5m (5-minute), hourly, or daily (Enterprise plans support 5m and hourly)
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/coins/{id}/market_chart/range'
        return self.client

    @property
    def coins_ohlc(self):
        '''
        Get the OHLC chart (Open, High, Low, Close) of a coin based on particular coin ID.
        
        Args:
            None
        
        Params:
            vs_currency: Target currencies for price data (e.g., usd, eur, gbp, jpy, etc.)
            days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or max for all available data)
            interval: Data interval granularity - 5m (5-minute), hourly, or daily (Enterprise plans support 5m and hourly)
            precision: Decimal places for price values (full or 0-18 digits)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/coins-id-ohlc'
        return self.client

    @property
    def coins_categories_list(self):
        '''
        Query all the coins categories on CoinGecko.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/coins/categories/list'
        return self.client

    @property
    def coins_categories(self):
        '''
        Query all the coins categories with market data (market cap, volume, …) on CoinGecko.
        
        Args:
            None
        
        Params:
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            per_page: Number of results per page (1-250, default varies by endpoint)
            page: Page number for pagination (starting from 1)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/coins/categories'
        return self.client

    # ENDPOINT_NFTS
    @property
    def nfts_list(self):
        '''
        Query all supported NFTs with ID, contract address, name, asset platform ID and symbol on CoinGecko.
        
        Args:
            None
        
        Params:
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            per_page: Number of results per page (1-250, default varies by endpoint)
            page: Page number for pagination (starting from 1)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/nfts/list'
        return self.client

    def nfts(self, id):
        '''
        Query all the NFT data (name, floor price, 24hr volume, …) based on the NFT collection ID.
        
        Args:
            id: NFT collection ID
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/nfts/{id}'
        return self.client

    # ENDPOINT_EXCHANGES_SPOT
    @property
    def exchanges(self):
        '''
        Query all the supported exchanges with exchanges' data (ID, name, country, …) that have active trading volumes on CoinGecko.
        
        Args:
            None
        
        Params:
            per_page: Number of results per page (1-250, default varies by endpoint)
            page: Page number for pagination (starting from 1)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/exchanges'
        return self.client

    @property
    def exchanges_list(self):
        '''
        Query all the exchanges with ID and name.
        
        Args:
            None
        
        Params:
            status: Filter by status - active (listed) or inactive (delisted) coins/exchanges
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/exchanges/list'
        return self.client

    def exchanges_id(self, id):
        '''
        Query exchange's data (name, year established, country, …), exchange volume in BTC and tickers based on exchange's ID.
        
        Args:
            id: Exchange ID
        
        Params:
            dex_pair_format: Display format for DEX pairs - contract_address or symbol (e.g., WETH, USDC)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/exchanges/{id}'
        return self.client

    def exchanges_tickers(self, id):
        '''
        Query exchange's tickers based on exchange's ID.
        
        Args:
            id: Exchange ID
        
        Params:
            coin_ids: Comma-separated coin IDs to filter exchange tickers
            include_exchange_logo: Boolean flag to include exchange logo URL in response
            page: Page number for pagination (starting from 1)
            depth: Boolean flag to include 2% orderbook depth (cost_to_move_up_usd and cost_to_move_down_usd)
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            dex_pair_format: Display format for DEX pairs - contract_address or symbol (e.g., WETH, USDC)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/exchanges/{id}/tickers'
        return self.client

    def exchanges_volume_chart(self, id):
        '''
        Query the historical volume chart data with time in UNIX and trading volume data in BTC based on exchange's ID.
        
        Args:
            id: Exchange ID
        
        Params:
            days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or max for all available data)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/exchanges/{id}/volume_chart'
        return self.client

    # ENDPOINT_EXCHANGES_DERIVATIVES
    @property
    def derivatives(self):
        '''
        Query all the tickers from derivatives exchanges on CoinGecko.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/derivatives'
        return self.client

    @property
    def derivatives_exchanges(self):
        '''
        Query all the derivatives exchanges with related data (ID, name, open interest, …) on CoinGecko.
        
        Args:
            None
        
        Params:
            order: Sort results by field (market_cap_desc, volume_asc, trust_score_desc, etc.)
            per_page: Number of results per page (1-250, default varies by endpoint)
            page: Page number for pagination (starting from 1)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/derivatives/exchanges'
        return self.client

    def derivatives_exchanges_id(self, id):
        '''
        Query the derivatives exchange's related data (ID, name, open interest, …) based on the exchanges' ID.
        
        Args:
            id: Exchange ID
        
        Params:
            include_tickers: Include tickers data - all (all tickers), unexpired (non-expired only), or empty to omit
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/derivatives/exchanges/{id}'
        return self.client

    @property
    def derivatives_exchanges_list(self):
        '''
        Query all the derivatives exchanges with ID and name on CoinGecko.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/derivatives/exchanges/list'
        return self.client

    # ENDPOINT_TREASURY
    @property
    def entities_list(self):
        '''
        Query all the supported entities (companies/governments) with their ID, name, symbol, and country.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/entities/list'
        return self.client

    def public_treasury_entity_coin(self, entity, coin_id):
        '''
        Query the holdings of a specific coin (e.g., bitcoin) by a specific group (e.g., public_companies).
        
        Args:
            entity: Entity name (e.g., public_companies)
            coin_id: Coin ID (e.g., bitcoin)
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/{entity}/public_treasury/{coin_id}'
        return self.client

    def public_treasury_entity(self, entity_id):
        '''
        Query the full cryptocurrency holdings and profile of a specific organization by its ID.
        
        Args:
            entity_id: Entity ID
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/public_treasury/{entity_id}'
        return self.client

    def public_treasury_holding_chart(self, entity_id, coin_id):
        '''
        Query historical chart data of an organization's holdings for a specific coin over time.
        
        Args:
            entity_id: Entity ID
            coin_id: Coin ID (e.g., bitcoin)
        
        Params:
            days: Number of days of historical data (1, 7, 14, 30, 90, 180, 365, or max for all available data)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/public_treasury/{entity_id}/{coin_id}/holding_chart'
        return self.client

    def public_treasury_transaction_history(self, entity_id):
        '''
        Query the specific buy/sell history and transaction links for an organization.
        
        Args:
            entity_id: Entity ID
        
        Params:
            asset_id: Filter by asset ID (used in treasury endpoints to query specific coin holdings)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/public_treasury/{entity_id}/transaction_history'
        return self.client

    # ENDPOINT_SEARCH
    @property
    def search(self):
        '''
        Search for specific coins, categories, or markets by name or keyword.
        
        Args:
            None
        
        Params:
            query: Search query string to find coins, categories, exchanges, or NFTs
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/search'
        return self.client

    @property
    def search_trending(self):
        '''
        Query the top trending coins, NFTs, and categories from the last 24 hours.
        
        Args:
            None
        
        Params:
            show_max: Show maximum results available - coins, nfts, categories (comma-separated for multiple)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/search/trending'
        return self.client

    @property
    def asset_platforms(self):
        '''
        Query all blockchain networks (Ethereum, Solana, etc.) supported by CoinGecko.
        
        Args:
            None
        
        Params:
            filter: Apply filters to results (e.g., nft to get NFT-supporting asset platforms)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/asset_platforms'
        return self.client

    def token_lists(self, asset_platform_id):
        '''
        Get a full list of tokens for a specific blockchain network.
        
        Args:
            asset_platform_id: Asset platform ID (e.g., ethereum, solana)
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/token_lists/{asset_platform_id}/all.json'
        return self.client

    # ENDPOINT_ONCHAIN
    @property
    def onchain_networks(self):
        '''
        Query all supported blockchain networks on GeckoTerminal.
        
        Args:
            None
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/onchain/networks'
        return self.client

    def onchain_networks_dexes(self, network):
        '''
        Query all supported decentralized exchanges (DEXs) on a specific network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/dexes'
        return self.client

    def onchain_networks_token_info(self, network, token_address):
        '''
        Query token metadata (socials, description, image) via contract address.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            token_address: Token contract address
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}/info'
        return self.client

    def onchain_networks_pools(self, network, pool_address):
        '''
        Query a specific liquidity pool's data.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            pool_address: Pool contract address
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}'
        return self.client

    def onchain_networks_pools_multi(self, network, pool_addresses):
        '''
        Query multiple pools at once.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            pool_addresses: Comma-separated pool contract addresses
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools/multi/{pool_addresses}'
        return self.client

    @property
    def onchain_trending_pools(self):
        '''
        Query trending pools across all networks.
        
        Args:
            None
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/onchain/networks/trending_pools'
        return self.client

    def onchain_networks_trending_pools(self, network):
        '''
        Query trending pools on a specific network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/trending_pools'
        return self.client

    def onchain_networks_top_pools(self, network):
        '''
        Query top-performing pools on a specific network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools'
        return self.client

    def onchain_networks_dex_pools(self, network, dex):
        '''
        Query top pools for a specific DEX (e.g., Uniswap) on a specific network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            dex: DEX name (e.g., uniswap, sushiswap)
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/dexes/{dex}/pools'
        return self.client

    @property
    def onchain_new_pools(self):
        '''
        Query the newest pools created across all networks.
        
        Args:
            None
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/onchain/networks/new_pools'
        return self.client

    def onchain_networks_new_pools(self, network):
        '''
        Query the latest pools on a specific network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/new_pools'
        return self.client

    @property
    def onchain_search_pools(self):
        '''
        Search for pools by name or address.
        
        Args:
            None
        
        Params:
            query: Search query string to find coins, categories, exchanges, or NFTs
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/onchain/search/pools'
        return self.client

    def onchain_networks_pools_info(self, network, pool_address):
        '''
        Query pool metadata (base/quote token details, socials).
        
        Args:
            network: Network name (e.g., ethereum, solana)
            pool_address: Pool contract address
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/info'
        return self.client

    def onchain_simple_token_price(self, network, token_addresses):
        '''
        Get real-time token price based on contract address.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            token_addresses: Comma-separated token contract addresses
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/simple/networks/{network}/token_price/{token_addresses}'
        return self.client

    def onchain_networks_token_pools(self, network, token_address):
        '''
        Query all pools that contain a specific token.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            token_address: Token contract address
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}/pools'
        return self.client

    def onchain_networks_token(self, network, token_address):
        '''
        Query specific data for a token on a network.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            token_address: Token contract address
        
        Params:
            None
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}'
        return self.client

    @property
    def onchain_tokens_recently_updated(self):
        '''
        Query the 100 most recently updated tokens across all networks.
        
        Args:
            None
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = '/onchain/tokens/info_recently_updated'
        return self.client

    def onchain_networks_pools_ohlcv(self, network, pool_address, timeframe):
        '''
        Get OHLCV chart data (Open, High, Low, Close, Volume) for a pool.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            pool_address: Pool contract address
            timeframe: Time interval for OHLCV data (e.g., 1h, 4h, 1d)
        
        Params:
            from: Starting date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)
            to: Ending date/timestamp for historical data range (ISO date YYYY-MM-DD or UNIX timestamp)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}'
        return self.client

    def onchain_networks_pools_trades(self, network, pool_address):
        '''
        Query the last 300 trades in the past 24 hours for a pool.
        
        Args:
            network: Network name (e.g., ethereum, solana)
            pool_address: Pool contract address
        
        Params:
            page: Page number for pagination (starting from 1)
            per_page: Number of results per page (1-250, default varies by endpoint)
        
        Returns: CoinGeckoClient
        '''
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/trades'
        return self.client

#cg = CoinGeckoClient(test_api_key)
#parameters = {
#    "ids": "bitcoin,ethereum",
#    "vs_currencies": "usd"
#}

 
 
#result = cg.endpoints.simple_price.params(parameters).run()
#print(result)


#print(cg.timeout)



