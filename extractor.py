from yahooquery import Ticker
import pandas as pd
import time

def get_fund_data(ticker_symbol):
    fund = Ticker(ticker_symbol)
    
    # 1. INITIALIZE EVERYTHING (This prevents NameErrors)
    sectors = None
    holdings = None
    performance = {}
    
    # --- PART 1: Sector Weightings ---
    try:
        raw_sectors = fund.fund_sector_weightings
        if isinstance(raw_sectors, dict) and ticker_symbol in raw_sectors:
            sectors = raw_sectors[ticker_symbol]
        elif isinstance(raw_sectors, pd.DataFrame):
            sectors = raw_sectors

        if sectors is not None and not sectors.empty:
            sectors.columns = ['Weightage']
            sectors = sectors.sort_values(by='Weightage', ascending=False)
        else:
            sectors = None
    except Exception:
        sectors = None

    # --- PART 2: Top 10 Holdings ---
    try:
        raw_holdings = fund.fund_top_holdings
        if isinstance(raw_holdings, dict) and ticker_symbol in raw_holdings:
            holdings = raw_holdings[ticker_symbol]
        elif isinstance(raw_holdings, pd.DataFrame):
            holdings = raw_holdings

        if holdings is not None and not holdings.empty:
            holdings = holdings.sort_values(by='holdingPercent', ascending=False).head(10)
            holdings = holdings[['holdingName', 'holdingPercent']].reset_index(drop=True)
        else:
            holdings = None
    except Exception:
        holdings = None

    # --- PART 3: Performance Data ---
    try:
        perf_data = fund.fund_performance
        if isinstance(perf_data, dict) and ticker_symbol in perf_data:
            trailing = perf_data[ticker_symbol].get('trailingReturns', {})
            # Mapping Yahoo's keys to the clean labels you want in Excel
            performance = {
                '1 Month': trailing.get('oneMonth'),
                '3 Month': trailing.get('threeMonth'),
                '6 Month': trailing.get('sixMonth'),
                '1 Year': trailing.get('oneYear'),
                '3 Year': trailing.get('threeYear'),
                '5 Year': trailing.get('fiveYear')
            }
    except Exception:
        performance = {}

    # 2. RETURN ALL THREE (main.py is expecting this order)
    return sectors, holdings, performance