import unittest
import pandas as pd
import re
from main import extract_features, SIGNATURES

class TestAnalyzerLogic(unittest.TestCase):

    def test_feature_extraction_shape(self):
        """Test if the math engine returns the correct table format"""
        # We expect 7 features (len, sqli, xss, dots, specials, entropy, density)
        url = "/search?q=apple"
        df = extract_features(url)
        self.assertEqual(df.shape[1], 7, "Feature extractor must return exactly 7 columns")

    def test_feature_calculation(self):
        """Test if feature calculation logic works"""
        # URL with 1 special char (dot)
        url = "test.jpg"
        df = extract_features(url)
        
        # Column 0 is Length (8)
        self.assertEqual(df.iloc[0, 0], 8)
        # Column 3 is Dots (1)
        self.assertEqual(df.iloc[0, 3], 1)

    def test_sqli_signature(self):
        """Test if our Regex catches standard SQL Injection"""
        payload = "/product?id=' OR 1=1"
        detected = False
        for pattern in SIGNATURES:
            if re.search(pattern, payload, re.IGNORECASE):
                detected = True
                break
        self.assertTrue(detected, "Regex should catch SQL Injection pattern")

    def test_xss_signature(self):
        """Test if our Regex catches XSS"""
        payload = "/feedback?msg=<script>alert(1)</script>"
        detected = False
        for pattern in SIGNATURES:
            if re.search(pattern, payload, re.IGNORECASE):
                detected = True
                break
        self.assertTrue(detected, "Regex should catch Script tags")

    def test_normal_traffic_safe(self):
        """Test that a normal URL does NOT trigger Regex"""
        payload = "/api/user/login"
        detected = False
        for pattern in SIGNATURES:
            if re.search(pattern, payload, re.IGNORECASE):
                detected = True
                break
        self.assertFalse(detected, "Normal URL should pass Regex check")

if __name__ == '__main__':
    unittest.main()