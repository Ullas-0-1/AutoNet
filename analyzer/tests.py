import unittest
import pandas as pd

# Try to import just the feature extractor.
# We skip importing SIGNATURES/ATTACK_PATTERNS to avoid errors if they are missing.
try:
    from main import extract_features
except ImportError:
    # Dummy fallback to allow tests to run (and fail gracefully) if import breaks
    print("⚠️ Could not import extract_features from main.py")
    def extract_features(url): return pd.DataFrame()

class TestAnalyzerLogic(unittest.TestCase):

    def test_feature_extraction_returns_dataframe(self):
        """Test if the feature extractor returns a valid Pandas DataFrame"""
        url = "/search?q=apple"
        df = extract_features(url)
        self.assertIsInstance(df, pd.DataFrame, "Function should return a Pandas DataFrame")
        self.assertFalse(df.empty, "Returned DataFrame should not be empty")

    def test_feature_dimensions(self):
        """Test if we extract the expected number of features (7 for the ML model)"""
        url = "/api/login"
        df = extract_features(url)
        # We expect 1 row (for 1 URL) and 7 columns/features
        self.assertEqual(df.shape[0], 1, "Should return 1 row")
        self.assertEqual(df.shape[1], 7, "Should return 7 feature columns")

    def test_feature_math_accuracy(self):
        """Test if features like Length are calculated correctly"""
        # URL: "abc" (Length 3)
        url = "abc" 
        df = extract_features(url)
        
        # The first feature is 'len'. Check if it equals 3.
        # Using iloc[0,0] to get the first feature of the first row
        calculated_len = df.iloc[0, 0]
        self.assertEqual(calculated_len, 3, "First feature (Length) should be 3 for input 'abc'")

    def test_special_character_counting(self):
        """Test if the extractor counts special characters correctly"""
        # URL has 1 single quote: '
        url = "/search?q='"
        df = extract_features(url)
        
        # The second feature is typically SQLi char count in our logic
        # Check if it detected at least one special char count > 0
        sqli_count = df.iloc[0, 1] 
        self.assertGreaterEqual(sqli_count, 1, "Should detect the single quote in the SQLi feature column")

if __name__ == '__main__':
    unittest.main()