import collections
from sortedcontainers import SortedDict

class Order:
    """
    Memory-optimized Order object using __slots__.
    """
    __slots__ = ['order_id', 'price', 'qty', 'side']
    
    def __init__(self, order_id, price, qty, side):
        self.order_id = order_id
        self.price = price
        self.qty = qty
        self.side = side

class OrderBook:
    """
    A high-performance Limit Order Book (LOB) using SortedDict for O(log N) price access
    and deque for O(1) FIFO order priority.
    """
    def __init__(self, symbol):
        self.symbol = symbol
        self.bids = SortedDict(lambda x: -x) # Max-heap behavior: Highest bid first
        self.asks = SortedDict()             # Min-heap behavior: Lowest ask first
        self.orders = {}                     # Global order lookup for O(1) access

    def limit_order(self, side, price, qty, order_id):
        """
        Submits a limit order and matches it against the opposite side of the book.
        """
        if side.upper() == 'BUY':
            return self._match(price, qty, self.asks, 'BUY', order_id)
        else:
            return self._match(price, qty, self.bids, 'SELL', order_id)

    def _match(self, price, qty, counter_side, side, order_id):
        fills = []
        
        # 1. Matching Logic
        while qty > 0 and counter_side:
            best_price, orders_at_level = counter_side.peekitem(0)
            
            # Check for price crossing
            if (side == 'BUY' and price < best_price) or (side == 'SELL' and price > best_price):
                break
            
            while qty > 0 and orders_at_level:
                matching_order = orders_at_level[0]
                fill_qty = min(qty, matching_order.qty)
                
                qty -= fill_qty
                matching_order.qty -= fill_qty
                
                fills.append({
                    'order_id': order_id,
                    'matched_with': matching_order.order_id,
                    'price': best_price,
                    'qty': fill_qty
                })
                
                if matching_order.qty == 0:
                    orders_at_level.popleft()
                    del self.orders[matching_order.order_id]
            
            if not orders_at_level:
                counter_side.popitem(0)

        # 2. Add remaining quantity to book
        if qty > 0:
            book_side = self.bids if side == 'BUY' else self.asks
            if price not in book_side:
                book_side[price] = collections.deque()
            
            new_order = Order(order_id, price, qty, side)
            book_side[price].append(new_order)
            self.orders[order_id] = new_order
            
        return fills

    def cancel_order(self, order_id):
        """
        Cancels an order from the book. Note: deque removal is O(N).
        For production, a custom Doubly Linked List is recommended.
        """
        if order_id in self.orders:
            order = self.orders.pop(order_id)
            side = self.bids if order.side == 'BUY' else self.asks
            side[order.price].remove(order)
            if not side[order.price]:
                del side[order.price]
            return True
        return False

    def get_l2_snapshot(self, depth=5):
        """
        Returns the top levels of the book for visualization.
        """
        return {
            'bids': [(p, sum(o.qty for o in self.bids[p])) for p in self.bids.keys()[:depth]],
            'asks': [(p, sum(o.qty for o in self.asks[p])) for p in self.asks.keys()[:depth]]
        }
