# ðŸŒªï¸ Vortex Order Book (LOB)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![High Performance](https://img.shields.io/badge/performance-high-green.svg)](#)

A high-performance, memory-optimized **Limit Order Book (LOB)** implementation in Python. Designed for low-latency simulations, backtesting, and algorithmic trading.

## ðŸš€ Features
- **O(log N) Price Access:** Uses `SortedDict` for efficient price level management.
- **O(1) FIFO Priority:** Employs `collections.deque` for constant-time order matching within a price level.
- **Memory Optimized:** Uses `__slots__` to minimize memory footprint for millions of orders.
- **Full L2 Snapshots:** Easily generate depth snapshots for visualization or analysis.

## ðŸ› ï¸ Installation
```bash
pip install sortedcontainers
```

## ðŸ’» Quick Start
```python
from vortex_order_book import OrderBook

# Initialize book for BTC/USD
book = OrderBook("BTC-USD")

# Add a limit buy order
fills = book.limit_order(side="BUY", price=45000, qty=1.5, order_id="order_1")

# Add a crossing limit sell order
fills = book.limit_order(side="SELL", price=44900, qty=0.5, order_id="order_2")

# Get Top 5 Bid/Ask Levels
print(book.get_l2_snapshot(depth=5))
```

## ðŸ“Š Performance Benchmarks
Designed to handle thousands of updates per second in pure Python. For production HFT environments, this architecture provides a clean baseline that can be easily ported to Cython or C++.

## ðŸ¤ Contributing
Contributions are welcome! If you find a bug or have a feature request, please open an issue or submit a pull request.

## ðŸ“„ License
MIT License. See [LICENSE](LICENSE) for details.

---
Built with âš¡ by [David Selorm Walker](https://github.com/selormwalker)
