from limit import LimitOrderAgent
from trading_framework import ExecutionClient

# Mock execution client to simulate buying and selling
class MockExecutionClient(ExecutionClient):

    def buy(self, product_id: str, amount: int):
        print(f"Buying {amount} of {product_id}")

    def sell(self, product_id: str, amount: int):
        print(f"Selling {amount} of {product_id}")

# Instantiate the agent with the mock client
execution_client = MockExecutionClient()
agent = LimitOrderAgent(execution_client)

# Simulate a price tick
agent.on_price_tick('IBM', 99)  # Should buy 1000 shares of IBM
agent.add_order(True, 'AAPL', 500, 150)
agent.on_price_tick('AAPL', 149)  # Should buy 500 shares of AAPL
agent.add_order(False, 'AAPL', 500, 155)
agent.on_price_tick('AAPL', 156)  # Should sell 500 shares of AAPL
