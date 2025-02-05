# perp-arb-bot

A Python-based **Perpetual Funding Rate Arbitrage Bot** designed to exploit differences in funding rates across decentralized (DEX) and centralized (CEX) exchanges. The bot runs delta-neutral strategies, automating position management for consistent profits.

## Features

- **Delta-Neutral Trading**: Simultaneously long and short positions to minimize market risk.
- **Cross-Exchange Arbitrage**: Monitors funding rates on platforms like dYdX, GMX, and Binance.
- **Configurable Thresholds**: Set custom profit and risk parameters.
- **Automation**: Fully automated trading, including opening, monitoring, and closing positions.
- **API Integration**: Fetches live data from DEX and CEX APIs for accurate execution.
- **Error Handling**: Resilient to API failures and edge cases like position flips.

---

## Project Structure


---

## How It Works

1. **Monitor Funding Rates**:
   The bot continuously fetches funding rate data from supported exchanges.
   
2. **Identify Opportunities**:
   When a funding rate difference exceeds the defined threshold, the bot triggers a delta-neutral trade.

3. **Execute Trades**:
   - Long on the exchange with a lower funding rate.
   - Short on the exchange with a higher funding rate.

4. **Manage Positions**:
   The bot monitors positions to avoid liquidation, handles funding flips, and closes trades when the opportunity diminishes.

5. **Profit**:
   Gains from funding rate discrepancies are automatically tracked.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/DylanLi6905/perp-arb-bot.git
   cd perp-arb-bot
