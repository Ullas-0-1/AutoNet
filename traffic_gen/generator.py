import requests
import time
import random
import sys

# The Nginx Gateway URL (Internal Docker DNS)
TARGET_URL = "http://gateway:80"

# Simulated IPs (We will block the 'Malicious' ones later)
FAKE_IPS = [
    "192.168.1.5",   # Normal User
    "10.0.0.2",      # Normal User
    "203.55.11.22",  # ATTACKER (SQL Injector)
    "172.16.0.99"    # ATTACKER (Bot)
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "AutoNet-Bot/1.0",
    "Python-urllib/3.9",
    "Evil-Scanner-v2"
]

ENDPOINTS = ["/", "/balance", "/admin"]

def run_traffic():
    print("--- Starting Traffic Generator ---")
    
    while True:
        try:
            # Pick a random Identity
            fake_ip = random.choice(FAKE_IPS)
            user_agent = random.choice(USER_AGENTS)
            endpoint = random.choice(ENDPOINTS)
            
            headers = {
                "X-Forwarded-For": fake_ip,  # Inject Fake IP
                "User-Agent": user_agent
            }
            
            # Send the request
            full_url = f"{TARGET_URL}{endpoint}"
            resp = requests.get(full_url, headers=headers, timeout=2)
            
            print(f"[{fake_ip}] accessed {endpoint} | Status: {resp.status_code}")

        except Exception as e:
            print(f"Connection Error: {e}")
        
        # Fast loop to generate logs quickly (0.5s delay)
        time.sleep(0.5)

if __name__ == "__main__":
    # Wait for Nginx to boot up
    time.sleep(5)
    run_traffic()