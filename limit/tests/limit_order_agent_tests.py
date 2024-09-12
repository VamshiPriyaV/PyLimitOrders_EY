import unittest
from limit.limit_order_agent import LimitOrderAgent 
from trading_framework.execution_client import ExecutionClient


# Mock class to simulate the ExecutionClient behavior
class MockExecutionClient(ExecutionClient):

    def __init__(self):
        self.buys = []
        self.sells = []

    def buy(self, product_id: str, amount: int):
        self.buys.append((product_id, amount))

    def sell(self, product_id: str, amount: int):
        self.sells.append((product_id, amount))


class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        # Initialize the mock execution client and the agent before each test
        self.execution_client = MockExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_buy_ibm_when_price_below_100(self):
        # Check if 1000 shares of IBM are bought when the price drops below $100
        self.agent.on_price_tick('IBM', 99)
        self.assertIn(('IBM', 1000), self.execution_client.buys)

    def test_add_and_execute_buy_order(self):
        # Test if a custom buy order is executed at or below the limit price
        self.agent.add_order(True, 'AAPL', 500, 150)
        self.agent.on_price_tick('AAPL', 149)
        self.assertIn(('AAPL', 500), self.execution_client.buys)

    def test_add_and_execute_sell_order(self):
        # Test if a custom sell order is executed at or above the limit price
        self.agent.add_order(False, 'AAPL', 500, 155)
        self.agent.on_price_tick('AAPL', 156)
        self.assertIn(('AAPL', 500), self.execution_client.sells)

    def test_no_action_when_price_does_not_meet_limit(self):
        # Ensure no action is taken when the price doesn't meet the order limit
        self.agent.add_order(True, 'AAPL', 500, 150)
        self.agent.on_price_tick('AAPL', 151)
        self.assertNotIn(('AAPL', 500), self.execution_client.buys)


if __name__ == '__main__':
    unittest.main()
