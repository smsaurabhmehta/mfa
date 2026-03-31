from yahooquery import search
import pandas as pd
import time

# 1. Your list of fund names
funds = [
    "Motilal Oswal Large and Midcap Fund",
    "Invesco India Large & Mid Cap Fund",
    "Invesco India Smallcap Fund",
    "Bandhan Small Cap Fund",
    "Parag Parikh Flexi Cap Fund",
    "ICICI Prudential Pharma Healthcare & Diagnostics (P.H.D) Fund",
    "HDFC Focused Fund",
    "Kotak Midcap Fund",
    "Motilal Oswal Flexi Cap Fund",
    "Motilal Oswal Small Cap Fund",
    "Edelweiss Mid Cap Fund",
    "Nippon India Growth Mid Cap Fund",
    "Invesco India Focused Fund",
    "JM Midcap Fund",
    "Kotak Large Cap Fund",
    "ICICI Prudential Nifty Next 50 Index Fund"
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