from yahooquery import search
import pandas as pd
import time

# 1. Your list of fund names
funds = [
    "Parag Parikh Flexi Cap Fund",
    "HDFC Flexi Cap Fund",
    "Kotak Flexicap Fund",
    "SBI Focused Fund",
    "Aditya Birla Sun Life Flexi Cap Fund",
    "ICICI Prudential Flexicap Fund",
    "ICICI Prudential Focused Equity Fund",
    "Aditya Birla Sun Life Focused Fund",
    "Kotak Focused Fund",
    "Tata Flexi Cap Fund",
    "Edelweiss Flexi Cap Fund",
    "ICICI Prudential Large Cap Fund",
    "DSP Nifty 50 Equal Weight Index Fund",
    "Nippon India Multi Cap Fund",
    "Kotak Multicap Fund"
]

results = []

print("Starting ticker lookup...")

# 2. Loop through each fund name to query the API
for fund in funds:
    # We add "Direct Growth" to get the most common professional plan
    query = f"{fund} Direct Growth"
    
    # The 'india' country code helps the API prioritize local results
    search_data = search(query, country='india')
    
    # Check if 'quotes' exists in the response and has at least one result
    if 'quotes' in search_data and len(search_data['quotes']) > 0:
        # We take the first result as the "best match"
        match = search_data['quotes'][0]
        
        ticker = match.get('symbol')
        full_name = match.get('longname')
        
        results.append({
            "Original Name": fund,
            "Yahoo Ticker": ticker,
            "Found Name": full_name
        })
        print(f"Done: {fund} -> {ticker}")
    else:
        results.append({
            "Original Name": fund,
            "Yahoo Ticker": "NOT_FOUND",
            "Found Name": "N/A"
        })
        print(f"Failed: Could not find {fund}")
    
    # Small pause to be polite to the API servers
    time.sleep(0.5)

# 3. Use Pandas to display the results in a clean table
df = pd.DataFrame(results)

print("\n--- FINAL TICKER LIST ---")
print(df)

# Optional: Save this to a CSV so you don't have to run it again
# df.to_csv("my_fund_tickers.csv", index=False)


from yahooquery import search

# Try a broader search term
query = "Parag Parikh Flexi Cap"
data = search(query, country='india')

# Look at everything the API found
if 'quotes' in data:
    for result in data['quotes']:
        print(f"Ticker: {result.get('symbol')} | Name: {result.get('longname')}")