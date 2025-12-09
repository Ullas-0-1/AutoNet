import unittest
import re
import pandas as pd

# Try to import the specific variables we need. 
# We use a try/except block to handle different versions of your main.py (Old vs New)
try:
    from main import extract_features, SIGNATURES as ATTACK_PATTERNS
except ImportError:
    try:
        from main import extract_features, ATTACK_PATTERNS
    except ImportError:
        # Fallback if the file structure is completely different
        print("⚠️ Could not import logic from main.py. Tests might fail.")
        ATTACK_PATTERNS = []
        def extract_features(url): return pd.DataFrame()

class TestAnalyzerLogic(unittest.TestCase):

    def test_feature_extraction_shape(self):
        """Test if the feature extractor returns the correct table shape (1 row, 7 columns)"""
        url = "/search?q=apple"
        df = extract_features(url)
        # We expect 1 row and 7 columns (len, sqli, xss, dots, digits, specials, depth)
        self.assertEqual(df.shape, (1, 7), "Feature extraction should return 1 row with 7 features")

    def test_sqli_signature_detection(self):
        """Test if the Regex list correctly catches a standard SQL Injection"""
        sqli_payload = "/product?id=' OR 1=1"
        detected = False
        
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, sqli_payload, re.IGNORECASE):
                detected = True
                break
        
        self.assertTrue(detected, "The Attack Patterns list should catch basic SQL Injection")

    def test_xss_signature_detection(self):
        """Test if the Regex list correctly catches a Script tag"""
        xss_payload = "/feedback?msg=<script>alert(1)</script>"
        detected = False
        
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, xss_payload, re.IGNORECASE):
                detected = True
                break
        
        self.assertTrue(detected, "The Attack Patterns list should catch XSS script tags")

    def test_normal_url_is_safe(self):
        """Test that a standard normal URL does NOT trigger the regex"""
        normal_url = "/api/user/login"
        detected = False
        
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, normal_url, re.IGNORECASE):
                detected = True
                break
        
        self.assertFalse(detected, "Normal URLs should not trigger signature detection")

if __name__ == '__main__':
    unittest.main()