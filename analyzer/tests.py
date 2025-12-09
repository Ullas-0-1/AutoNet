import unittest
import pandas as pd
from main import extract_features, ATTACK_PATTERNS
import re

class TestAnalyzerLogic(unittest.TestCase):

    def test_feature_extraction_count(self):
        """Test if we extract exactly 7 features as expected by the model"""
        url = "/search?q=apple"
        df = extract_features(url)
        self.assertEqual(df.shape[1], 7, "Should extract exactly 7 features")

    def test_sqli_signature_detection(self):
        """Test if our Regex catches standard SQL Injection"""
        sqli_payload = "/product?id=' OR 1=1"
        detected = False
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, sqli_payload, re.IGNORECASE):
                detected = True
                break
        self.assertTrue(detected, "SQL Injection should be detected by Regex")

    def test_xss_signature_detection(self):
        """Test if our Regex catches Script tags"""
        xss_payload = "/feedback?msg=<script>alert(1)</script>"
        detected = False
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, xss_payload, re.IGNORECASE):
                detected = True
                break
        self.assertTrue(detected, "XSS should be detected by Regex")

    def test_normal_traffic_safe(self):
        """Test that a normal URL does NOT trigger a regex match"""
        normal_url = "/api/v1/login"
        detected = False
        for pattern in ATTACK_PATTERNS:
            if re.search(pattern, normal_url, re.IGNORECASE):
                detected = True
                break
        self.assertFalse(detected, "Normal URL should NOT trigger Regex")

if __name__ == '__main__':
    unittest.main()