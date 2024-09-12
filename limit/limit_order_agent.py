import trading_framework
from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from trading_framework.execution_client import ExecutionException

class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders = []

    def on_price_tick(self, product_id: str, price: float):
        """
        Monitors price changes and executes orders when the conditions are met.
        Buys 1000 shares of IBM when the price drops below $100.
        Executes any other limit orders added via add_order.
        """
        if product_id == 'IBM' and price < 100:
            try:
                self.execution_client.buy(product_id, 1000)
                print(f"Bought 1000 shares of {product_id} at {price}")
            except ExecutionException:
                print(f"Failed to buy {product_id} at {price}")

        for order in self.orders:
            if (order['buy'] and price <= order['limit']) or (not order['buy'] and price >= order['limit']):
                try:
                    if order['buy']:
                        self.execution_client.buy(order['product_id'], order['amount'])
                        print(f"Executed buy order for {order['amount']} shares of {order['product_id']} at {price}")
                    else:
                        self.execution_client.sell(order['product_id'], order['amount'])
                        print(f"Executed sell order for {order['amount']} shares of {order['product_id']} at {price}")
                    self.orders.remove(order)
                except ExecutionException:
                    print(f"Failed to execute order for {order['product_id']} at {price}")

    def add_order(self, buy: bool, product_id: str, amount: int, limit: float):
        """
        Adds a new order to be executed when the price matches or exceeds the limit.
        :param buy: True if the order is a buy, False if it is a sell
        :param product_id: The product ID to buy/sell
        :param amount: The number of shares to buy/sell
        :param limit: The price limit for executing the order
        """
        self.orders.append({'buy': buy, 'product_id': product_id, 'amount': amount, 'limit': limit})
        print(f"Order added: {'Buy' if buy else 'Sell'} {amount} shares of {product_id} at limit {limit}")
