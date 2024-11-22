# Auto-trader and back-tester

## Overview
This project provides a backtesting and auto-trading framework designed to simulate and run trading strategies on the cryptocurrency exchanges. It is intended for users interested in algorithmic trading, allowing them to develop, test, and refine strategies using historical market data.

## Features
- **Strategy Backtesting**: Simulate various trading strategies.
- **Market and Signal Management**: Manage market data and trading signals.
- **Multi-Exchange Support**: Includes configurations for Kucoin and other exchanges.
- **Data Management**: Downloads, indexes, and organizes data for efficient backtesting.
- **User-Friendly Settings**: Configure accounts, signals, and strategies through JSON files.

## Project Structure
- **accounts/**: Contains configurations for different accounts, including:
  - **settings/**: JSON files for accounts, markets, trades, tasks, and database indexing.
  - **signals/**: JSON files defining different bot signals.
  - **strategies/**: Scripts and configuration files for various strategies.
- **src/**: Core source code for the backtesting framework, organized by functionality:
  - **backTestTask.py**: Main backtesting task execution.
  - **data.py, data_downloader.py**: For handling data retrieval and management.
  - **orderManager.py, portfolioManager.py**: Manages orders and portfolios.
  - **exchanges/**: Handles exchange-specific configurations and functions.
  - **tests/**: Unit tests for different modules.

## Prerequisites
- **Python 3.8+**
- **Kucoin API Credentials** (for live testing)
  
## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sohiyel/Auto-trader-Back-test.git
   cd Auto-trader-Back-test
   pip install -r requirements.txt
