from client import CoinGeckoClient, test_api_key


cg = CoinGeckoClient(test_api_key)

# Test 1: AttributeError (endpoint not set)
print("Test 1: No endpoint set")
result = cg.run()  # Should error: endpoint is None
print(f"Result: {result}\n")

# Test 2: HTTPError 404 (endpoint doesn't exist)
print("Test 2: Invalid endpoint (404)")
result = cg.endpoints.ping.params({}).run()  # Valid
result = cg.endpoints.coins('invalid_coin_xyz').run()  # 404 error
print(f"Result: {result}\n")

# Test 3: HTTPError 401 (bad API key)
print("Test 3: Unauthorized (401)")
bad_client = CoinGeckoClient()
result = bad_client.endpoints.simple_price.params({"ids": "bitcoin", "vs_currencies": "usd"}).run()
print(f"Result: {result}\n")

# Test 4: Valid request (success)
print("Test 4: Valid request")
result = cg.endpoints.ping.run()
print(f"Result: {result}\n")

# Test 5: Valid request with params
print("Test 5: Valid request with params")
result = cg.endpoints.simple_price.params({"ids": "bitcoin,ethereum", "vs_currencies": "usd"}).run()
print(f"Result: {result}\n")