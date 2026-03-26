import pandas as pd

def calculate_similarity(all_fund_holdings):
    """Calculates the weighted overlap between every pair of funds."""
    fund_names = list(all_fund_holdings.keys())
    # We will create two matrices: one for % weight overlap, one for common stock count
    similarity_df = pd.DataFrame(index=fund_names, columns=fund_names)
    count_df = pd.DataFrame(index=fund_names, columns=fund_names)

    for f1 in fund_names:
        for f2 in fund_names:
            if f1 == f2:
                similarity_df.loc[f1, f2] = 100.0
                count_df.loc[f1, f2] = 10 # Total stocks in top 10
            else:
                h1 = all_fund_holdings[f1]
                h2 = all_fund_holdings[f2]
                
                # Merge on stock names to find intersections
                common = pd.merge(h1, h2, on='holdingName', suffixes=('_1', '_2'))
                
                if not common.empty:
                    # 1. Weighted Overlap (%)
                    overlap = common[['holdingPercent_1', 'holdingPercent_2']].min(axis=1).sum()
                    similarity_df.loc[f1, f2] = round(overlap, 2)
                    
                    # 2. Common Stock Count (How many names match?)
                    count_df.loc[f1, f2] = len(common)
                else:
                    similarity_df.loc[f1, f2] = 0.0
                    count_df.loc[f1, f2] = 0
                    
    return similarity_df, count_df

def calculate_membership_grid(all_fund_holdings):
    """Creates a weighted grid where each fund is 1/N of the portfolio."""
    num_funds = len(all_fund_holdings)
    if num_funds == 0: return pd.DataFrame()
    
    # Each fund's weight in your total portfolio (e.g., 0.04 for 25 funds)
    fund_weight_in_portfolio = 1.0 / num_funds
    
    flat_data = []
    for fund_name, df_holdings in all_fund_holdings.items():
        if df_holdings is not None:
            for _, row in df_holdings.iterrows():
                # SCALE DOWN: Individual Stock Weight * Fund's Portfolio Weight
                weighted_contribution = row['holdingPercent'] * fund_weight_in_portfolio
                
                flat_data.append({
                    'Fund': fund_name,
                    'Stock': row['holdingName'],
                    'Actual_Weight': row['holdingPercent'], # For the cell value
                    'Portfolio_Contribution': weighted_contribution # For the total sum
                })
    
    df = pd.DataFrame(flat_data)
    
    # Pivot for the grid view (showing actual % in each fund for readability)
    grid = df.pivot(index='Stock', columns='Fund', values='Actual_Weight').fillna(0)
    
    # Calculate Total Portfolio Exposure using the scaled values
    total_exposure = df.groupby('Stock')['Portfolio_Contribution'].sum()
    grid['Total Portfolio Exposure (%)'] = total_exposure
    
    # Sort by the most impactful stocks in your total portfolio
    return grid.sort_values(by='Total Portfolio Exposure (%)', ascending=False)