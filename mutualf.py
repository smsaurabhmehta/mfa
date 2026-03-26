import os
os.system('cls')

from yahooquery import Ticker
import pandas as pd

# The ticker for HDFC Top 100 Fund (Direct)
symbol = '0P00009J3K.BO'
fund = Ticker(symbol)

# 1. Get Top 10 Holdings
# This returns a DataFrame containing the company name and its percentage in the fund
holdings = fund.fund_top_holdings
print("Top 10 Holdings:")
print(holdings)

# 2. Get Sector Weightages
# This provides the breakdown across industries like Financial Services, Technology, etc.
sectors = fund.fund_sector_weightings
print("\nSector Weightages:")
print(sectors)

clean_sectors = (sectors * 100).round(2)
print("Sector Breakdown (%):")
print(clean_sectors)

# Sort sectors by concentration (descending)
sorted_sectors = clean_sectors.sort_values(by=clean_sectors.columns[0], ascending=False)
print("\nSectors Ordered by Concentration:")
print(sorted_sectors)