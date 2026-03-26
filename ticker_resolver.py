from yahooquery import search
from config import FUNDS_TO_TRACK

def resolve_tickers():
    ticker_map = {}
    print("--- Resolving ISINs to Yahoo Tickers (Cleaning Results) ---")
    
    for name, isin_list in FUNDS_TO_TRACK.items():
        found_tickers = []
        print(f"Processing: {name}...")
        
        for isin in isin_list:
            try:
                data = search(isin)
                # Logic: Only take the FIRST quote for each ISIN search
                if 'quotes' in data and len(data['quotes']) > 0:
                    best_match = data['quotes'][0]['symbol']
                    # Use 'if best_match not in found_tickers' to avoid duplicates
                    if best_match not in found_tickers:
                        found_tickers.append(best_match)
            except Exception as e:
                print(f"  ! Error for ISIN {isin}: {e}")
        
        ticker_map[name] = found_tickers
        print(f"  > Cleaned results: {found_tickers}\n")
            
    return ticker_map

if __name__ == "__main__":
    results = resolve_tickers()
    print("\n--- Final Cleaned Ticker Map ---")
    print(results)