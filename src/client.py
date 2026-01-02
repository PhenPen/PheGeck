import requests, os
from dotenv import load_dotenv
import config

# Loading API Key stored in env
load_dotenv() #Load every environmental variable found in any .env file in project
test_api_key = os.getenv("API_KEY")
test_debug = os.getenv("DEBUG")
base_url = config.DEFAULT_BASE_URL






class CoinGeckoClient : #() Only add parenthesis if inheriting from another class
    def __init__(self,API_Key = None) -> None:
        self.base_url = base_url
        self.API_Key = API_Key
        self.query_params = {}
        self.custom_headers = {}
        self.endpoint = None

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
    
        Args : The API endpoint string (e.g., "/simple/price").
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

    def run(self):
        try :
            response = requests.get(f"{self.base_url}{self.endpoint}", headers=self.all_headers(), params=self.query_params)
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
    def __init__(self, client):
        self.client = client

    # ENDPOINT_COINS
    @property
    def ping(self):
        self.client.endpoint = '/ping'
        return self.client

    @property
    def simple_price(self):
        self.client.endpoint = '/simple/price'
        return self.client

    def simple_token_price(self, id):
        self.client.endpoint = f'/simple/token_price/{id}'
        return self.client

    @property
    def simple_supported_vs_currencies(self):
        self.client.endpoint = '/simple/supported_vs_currencies'
        return self.client

    @property
    def coins_list(self):
        self.client.endpoint = '/coins/list'
        return self.client

    @property
    def coins_markets(self):
        self.client.endpoint = '/coins/markets'
        return self.client

    def coins(self, id):
        self.client.endpoint = f'/coins/{id}'
        return self.client

    def coins_tickers(self, id):
        self.client.endpoint = f'/coins/{id}/tickers'
        return self.client

    def coins_history(self, id):
        self.client.endpoint = f'/coins/{id}/history'
        return self.client

    def coins_market_chart(self, id):
        self.client.endpoint = f'/coins/{id}/market_chart'
        return self.client

    def coins_market_chart_range(self, id):
        self.client.endpoint = f'/coins/{id}/market_chart/range'
        return self.client

    @property
    def coins_ohlc(self):
        self.client.endpoint = '/coins-id-ohlc'
        return self.client

    @property
    def coins_categories_list(self):
        self.client.endpoint = '/coins/categories/list'
        return self.client

    @property
    def coins_categories(self):
        self.client.endpoint = '/coins/categories'
        return self.client

    # ENDPOINT_NFTS
    @property
    def nfts_list(self):
        self.client.endpoint = '/nfts/list'
        return self.client

    def nfts(self, id):
        self.client.endpoint = f'/nfts/{id}'
        return self.client

    # ENDPOINT_EXCHANGES_SPOT
    @property
    def exchanges(self):
        self.client.endpoint = '/exchanges'
        return self.client

    @property
    def exchanges_list(self):
        self.client.endpoint = '/exchanges/list'
        return self.client

    def exchanges_id(self, id):
        self.client.endpoint = f'/exchanges/{id}'
        return self.client

    def exchanges_tickers(self, id):
        self.client.endpoint = f'/exchanges/{id}/tickers'
        return self.client

    def exchanges_volume_chart(self, id):
        self.client.endpoint = f'/exchanges/{id}/volume_chart'
        return self.client

    # ENDPOINT_EXCHANGES_DERIVATIVES
    @property
    def derivatives(self):
        self.client.endpoint = '/derivatives'
        return self.client

    @property
    def derivatives_exchanges(self):
        self.client.endpoint = '/derivatives/exchanges'
        return self.client

    def derivatives_exchanges_id(self, id):
        self.client.endpoint = f'/derivatives/exchanges/{id}'
        return self.client

    @property
    def derivatives_exchanges_list(self):
        self.client.endpoint = '/derivatives/exchanges/list'
        return self.client

    # ENDPOINT_TREASURY
    @property
    def entities_list(self):
        self.client.endpoint = '/entities/list'
        return self.client

    def public_treasury_entity_coin(self, entity, coin_id):
        self.client.endpoint = f'/{entity}/public_treasury/{coin_id}'
        return self.client

    def public_treasury_entity(self, entity_id):
        self.client.endpoint = f'/public_treasury/{entity_id}'
        return self.client

    def public_treasury_holding_chart(self, entity_id, coin_id):
        self.client.endpoint = f'/public_treasury/{entity_id}/{coin_id}/holding_chart'
        return self.client

    def public_treasury_transaction_history(self, entity_id):
        self.client.endpoint = f'/public_treasury/{entity_id}/transaction_history'
        return self.client

    # ENDPOINT_SEARCH
    @property
    def search(self):
        self.client.endpoint = '/search'
        return self.client

    @property
    def search_trending(self):
        self.client.endpoint = '/search/trending'
        return self.client

    @property
    def asset_platforms(self):
        self.client.endpoint = '/asset_platforms'
        return self.client

    def token_lists(self, asset_platform_id):
        self.client.endpoint = f'/token_lists/{asset_platform_id}/all.json'
        return self.client

    # ENDPOINT_ONCHAIN
    @property
    def onchain_networks(self):
        self.client.endpoint = '/onchain/networks'
        return self.client

    def onchain_networks_dexes(self, network):
        self.client.endpoint = f'/onchain/networks/{network}/dexes'
        return self.client

    def onchain_networks_token_info(self, network, token_address):
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}/info'
        return self.client

    def onchain_networks_pools(self, network, pool_address):
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}'
        return self.client

    def onchain_networks_pools_multi(self, network, pool_addresses):
        self.client.endpoint = f'/onchain/networks/{network}/pools/multi/{pool_addresses}'
        return self.client

    @property
    def onchain_trending_pools(self):
        self.client.endpoint = '/onchain/networks/trending_pools'
        return self.client

    def onchain_networks_trending_pools(self, network):
        self.client.endpoint = f'/onchain/networks/{network}/trending_pools'
        return self.client

    def onchain_networks_top_pools(self, network):
        self.client.endpoint = f'/onchain/networks/{network}/pools'
        return self.client

    def onchain_networks_dex_pools(self, network, dex):
        self.client.endpoint = f'/onchain/networks/{network}/dexes/{dex}/pools'
        return self.client

    @property
    def onchain_new_pools(self):
        self.client.endpoint = '/onchain/networks/new_pools'
        return self.client

    def onchain_networks_new_pools(self, network):
        self.client.endpoint = f'/onchain/networks/{network}/new_pools'
        return self.client

    @property
    def onchain_search_pools(self):
        self.client.endpoint = '/onchain/search/pools'
        return self.client

    def onchain_networks_pools_info(self, network, pool_address):
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/info'
        return self.client

    def onchain_simple_token_price(self, network, token_addresses):
        self.client.endpoint = f'/onchain/simple/networks/{network}/token_price/{token_addresses}'
        return self.client

    def onchain_networks_token_pools(self, network, token_address):
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}/pools'
        return self.client

    def onchain_networks_token(self, network, token_address):
        self.client.endpoint = f'/onchain/networks/{network}/tokens/{token_address}'
        return self.client

    @property
    def onchain_tokens_recently_updated(self):
        self.client.endpoint = '/onchain/tokens/info_recently_updated'
        return self.client

    def onchain_networks_pools_ohlcv(self, network, pool_address, timeframe):
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}'
        return self.client

    def onchain_networks_pools_trades(self, network, pool_address):
        self.client.endpoint = f'/onchain/networks/{network}/pools/{pool_address}/trades'
        return self.client

#cg = CoinGeckoClient(test_api_key)
#parameters = {
#    "ids": "bitcoin,ethereum",
#    "vs_currencies": "usd"
#}

 
 
#result = cg.endpoints.simple_price.params(parameters).run()
#print(result)