import pandas as pd

def get_full_portfolio_context(excel_path):
    # FIXED: Wrapped these in a 'tabs' dictionary variable
    tabs = {
        "Dashboard": "Dashboard",
        "Holdings": "Fund_Holdings",
        "Overlap": "Similarity_Matrix",
        "Concentration": "Stock_Exposure_Grid" 
    }

    # Tab 1: Dashboard
    df_dash = pd.read_excel(excel_path, sheet_name=tabs["Dashboard"])
    
    # Tab 2: Fund Holdings
    df_holdings = pd.read_excel(excel_path, sheet_name=tabs["Holdings"])
    
    # Tab 3: Similarity Matrix
    df_sim = pd.read_excel(excel_path, sheet_name=tabs["Overlap"], index_col=0)
    
    # Tab 4: Stock Concentration (FIXED: Using the grid name)
    df_conc = pd.read_excel(excel_path, sheet_name=tabs["Concentration"])

    # Build the Markdown String
    context = "# PORTFOLIO RAW DATA SNAPSHOT\n\n"
    context += "## Tab 1: Dashboard (Sectors & Performance)\n" + df_dash.to_markdown(index=False) + "\n\n"
    context += "## Tab 2: Top 10 Holdings per Fund\n" + df_holdings.to_markdown(index=False) + "\n\n"
    context += "## Tab 3: Mutual Fund Overlap Matrix\n" + df_sim.to_markdown(index=True) + "\n\n"
    context += "## Tab 4: Weighted Stock Concentration (Portfolio Level)\n" + df_conc.to_markdown(index=False)
    
    return context