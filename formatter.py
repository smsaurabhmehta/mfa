def apply_visuals(writer, fund_names):
    workbook = writer.book
    num_funds = len(fund_names)
    
    # --- SHEET: Similarity_Matrix ---
    if 'Similarity_Matrix' in writer.sheets:
        sim_sheet = writer.sheets['Similarity_Matrix']
        
        # 1. Top Matrix: Weighted Overlap % (Green to Red Heatmap)
        sim_sheet.conditional_format(1, 1, num_funds, num_funds, {
            'type': '3_color_scale',
            'min_color': "#63BE7B",
            'mid_color': "#FFEB84",
            'max_color': "#F8696B"
        })

        # 2. Bottom Matrix: Common Stock Count (Highlight 5 or more)
        # We calculate the start row (same logic as main.py)
        start_row_count = num_funds + 5 
        
        # Create a "Danger" format (Red fill for high structural overlap)
        danger_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        
        # Apply formatting to the second matrix range
        sim_sheet.conditional_format(
            start_row_count + 1, 1,           # Start Row, Start Col
            start_row_count + num_funds, num_funds, # End Row, End Col
            {
                'type':     'cell',
                'criteria': '>=',
                'value':    5,
                'format':   danger_format
            }
        )

    # --- SHEET: Stock_Exposure_Grid ---
    if 'Stock_Exposure_Grid' in writer.sheets:
        grid_sheet = writer.sheets['Stock_Exposure_Grid']
        grid_sheet.conditional_format(1, 1, 1000, num_funds, {
            'type': 'data_bar',
            'bar_color': '#A6C9EC',
            'bar_solid': True
        })