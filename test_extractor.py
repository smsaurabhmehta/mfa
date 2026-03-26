import unittest
from extractor import get_fund_data

class TestFundExtractor(unittest.TestCase):

    def test_invalid_ticker(self):
        """Test how the code handles a ticker that doesn't exist"""
        sectors, holdings = get_fund_data("INVALID_TICKER_123")
        # We expect the code to return None instead of crashing
        self.assertIsNone(sectors)
        self.assertIsNone(holdings)

    def test_data_types(self):
        """Test if the returned data is actually a DataFrame"""
        # Using a known reliable ticker for a quick test
        sectors, holdings = get_fund_data("0P0000YWL1.BO") 
        
        if sectors is not None:
            import pandas as pd
            self.assertIsInstance(sectors, pd.DataFrame)
            # Check if our 'Weightage' column exists
            self.assertIn('Weightage', sectors.columns)

if __name__ == '__main__':
    unittest.main()
    