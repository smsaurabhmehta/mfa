import pandas as pd
import time
import os
import pickle
from ticker_resolver import resolve_tickers
from extractor import get_fund_data
from analyzer import calculate_similarity, calculate_membership_grid
from formatter import apply_visuals

CACHE_FILE = "raw_fund_data.pkl"

def run_analyzer():
    # 1. User Choice for Refresh
    user_input = input("Force refresh from Yahoo? (y/n) [Default: n]: ").lower()
    FORCE_REFRESH = True if user_input == 'y' else False
    
    print("--- STARTING MODULAR MF ANALYZER ---")
    
    # --- STEP 1: LOAD OR FETCH DATA ---
    if os.path.exists(CACHE_FILE) and not FORCE_REFRESH:
        print(f"Loading data from cache: {CACHE_FILE} (Yahoo skipped)")
        with open(CACHE_FILE, 'rb') as f:
            cache_data = pickle.load(f)
            master_dashboard_data = cache_data['dashboard']
            all_fund_holdings = cache_data['holdings']
            holdings_output = cache_data['output_list']
    else:
        print("Fetching fresh data from Yahoo...")
        ticker_map = resolve_tickers()
        master_dashboard_data = {} 
        holdings_output = []
        all_fund_holdings = {} 
        
        fund_items = list(ticker_map.items())
        for idx, (fund_name, tickers) in enumerate(fund_items, 1):
            print(f"[{idx}/{len(fund_items)}] Querying Yahoo: {fund_name}")
            for ticker in tickers:
                sectors, holdings, performance = get_fund_data(ticker)
                if sectors is not None or performance:
                    row = performance if performance else {}
                    if sectors is not None:
                        row.update(sectors['Weightage'].to_dict())
                    master_dashboard_data[fund_name] = row
                    
                    if holdings is not None:
                        all_fund_holdings[fund_name] = holdings
                        # Prepare vertical list for standard 'Fund_Holdings' sheet
                        holdings_output.append([f"--- {fund_name.upper()} ---", None])
                        for _, h_row in holdings.iterrows():
                            holdings_output.append([h_row['holdingName'], h_row['holdingPercent']])
                        holdings_output.append([None, None])
                    break
            time.sleep(2.0)

        # SAVE THE CACHE IMMEDIATELY AFTER FETCHING
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump({
                'dashboard': master_dashboard_data,
                'holdings': all_fund_holdings,
                'output_list': holdings_output
            }, f)

    # --- STEP 2: RUN ANALYTICS ---
    print("--- RUNNING ANALYTICS SPECIALISTS ---")
    df_dashboard = pd.DataFrame.from_dict(master_dashboard_data, orient='index').fillna(0)
    df_holdings_list = pd.DataFrame(holdings_output, columns=['Stock Name', 'Weight %'])
    
    # Correctly Unpack the two matrices returned by analyzer.py
    similarity_df, count_df = calculate_similarity(all_fund_holdings)
    exposure_grid = calculate_membership_grid(all_fund_holdings)

    # --- STEP 3: SAVE EXCEL ---
    filename = "Mutual_Fund_Comparison.xlsx"
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        # Sheet 1: Dashboard
        df_dashboard.to_excel(writer, sheet_name="Dashboard")
        
        # Sheet 2: Standard Vertical List
        df_holdings_list.to_excel(writer, sheet_name="Fund_Holdings", index=False)
        
        # Sheet 3: Similarity Matrices (Two tables on one sheet)
        # Matrix A: Weighted Overlap %
        similarity_df.to_excel(writer, sheet_name="Similarity_Matrix", startrow=1)
        writer.sheets['Similarity_Matrix'].write(0, 0, "WEIGHTED OVERLAP (%)")
        
        # Matrix B: Common Stock Count (Placed below Matrix A)
        start_row_count = len(similarity_df) + 5
        count_df.to_excel(writer, sheet_name="Similarity_Matrix", startrow=start_row_count + 1)
        writer.sheets['Similarity_Matrix'].write(start_row_count, 0, "COMMON TOP 10 STOCK COUNT")
        
        # Sheet 4: The 1/N Scaled Exposure Grid
        exposure_grid.to_excel(writer, sheet_name="Stock_Exposure_Grid")
        
        # Apply visual heatmaps and data bars
        apply_visuals(writer, list(all_fund_holdings.keys()))

    # --- STEP 4: TERMINAL SUMMARY (LLM READY) ---
    print("\n" + "="*20 + " TOP 10 PORTFOLIO WEIGHTS " + "="*20)
    if not exposure_grid.empty:
        # Total Portfolio Exposure (%) is the scaled 1/N column
        top_stocks = exposure_grid['Total Portfolio Exposure (%)'].head(10)
        for stock, weight in top_stocks.items():
            print(f"{stock:<40} | {weight:.2f}%")

    print(f"\nSUCCESS: Analysis updated using { 'CACHE' if not FORCE_REFRESH else 'YAHOO' }")

if __name__ == "__main__":
    run_analyzer()

# --- NEW: AGENTIC REPORTING SECTION ---
from agent_manager import PortfolioAgent
from agent_bridge import get_full_portfolio_context # We'll define this below

try:
    print("\n" + "="*30)
    print("🤖 STARTING AGENTIC AI AUDIT")
    print("="*30)

    # 1. Package the 4-tab context from the Excel we just saved
    excel_file = 'Mutual_Fund_Comparison.xlsx'
    data_context = get_full_portfolio_context(excel_file)

    # 2. Initialize the Agent and Generate the Report
    user_choice = input("Select Model: [g] Gemini / [a] Anthropic: ").lower()
    provider = "gemini" if user_choice == 'g' else "claude"
    agent = PortfolioAgent(provider=provider) # Passes your choice to the manager
    html_report = agent.generate_report(data_context)
    
    # 3. Save the "Brilliant" HTML Dashboard
    output_html = "Portfolio_XRay_Interactive.html"
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_report)

    print(f"\n✅ SUCCESS: Interactive Dashboard created: {output_html}")
    print("Open this file in your browser to see the X-Ray.")

except Exception as e:
    print(f"\n❌ Agentic Audit Failed: {e}")