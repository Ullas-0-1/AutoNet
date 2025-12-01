# import requests
# import time
# import random
# import string
# import uuid

# # The Nginx Gateway URL
# TARGET_URL = "http://gateway:80"

# # --- 1. DYNAMIC ACTORS ---
# # We use a pool of IPs to simulate a distributed botnet vs real users
# NORMAL_IPS = [f"192.168.1.{x}" for x in range(5, 20)]  # 15 Normal Users
# ATTACKER_IPS = ["203.55.11.22", "66.77.88.99", "185.20.30.40"] # 3 Bad Guys

# # --- 2. REALISTIC USER AGENTS ---
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/89.0",
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
# ]

# # --- 3. DYNAMIC NORMAL TRAFFIC GENERATION ---
# def get_normal_request():
#     """Generates a valid, harmless request to Juice Shop"""
    
#     # Resource types common in Juice Shop
#     endpoints = [
#         "/rest/products/search",
#         "/api/Feedbacks",
#         "/api/BasketItems",
#         "/api/Complaints",
#         "/rest/user/login",
#         "/i18n/en.json"
#     ]
    
#     base = random.choice(endpoints)
    
#     # 1. Search Queries (Random strings)
#     if "search" in base:
#         search_term = random.choice(["apple", "orange", "juice", "ticket", "green", "smoothie"])
#         return f"{base}?q={search_term}"
    
#     # 2. Basket/Items (Random IDs)
#     elif "Basket" in base:
#         # Juice shop uses numeric IDs
#         return f"{base}/{random.randint(1, 20)}"
    
#     # 3. Login (Just probing the endpoint)
#     elif "login" in base:
#         return base
        
#     # 4. Static Assets (Images/JSON)
#     else:
#         return base

# # --- 4. DYNAMIC ATTACK GENERATION ---
# def get_attack_request():
#     """Generates a malicious request by injecting payloads into valid paths"""
    
#     # Attack Payloads (The 'Bazookas')
#     sqli_payloads = [
#         "' OR 1=1 --",
#         "' UNION SELECT 1,2,3,4,5,6,7,8,9 FROM users --",
#         "'; DROP TABLE users; --",
#         "' OR '1'='1",
#         "admin' --"
#     ]
    
#     xss_payloads = [
#         "<script>alert('XSS')</script>",
#         "<img src=x onerror=alert(1)>",
#         "javascript:alert(1)"
#     ]
    
#     traversal_payloads = [
#         "../../../../etc/passwd",
#         "..%2F..%2F..%2Fwindows%2Fwin.ini",
#         "/ftp/package.json.bak%2500.md"
#     ]

#     attack_type = random.choice(["SQLi", "XSS", "TRAVERSAL"])
#     base = "/rest/products/search" # Search is the easiest place to inject
    
#     path = ""
#     if attack_type == "SQLi":
#         payload = random.choice(sqli_payloads)
#         # Inject into query param
#         path = f"{base}?q={payload}"
        
#     elif attack_type == "XSS":
#         payload = random.choice(xss_payloads)
#         # Inject into Feedback or Search
#         path = f"/api/Feedbacks?comment={payload}"
        
#     elif attack_type == "TRAVERSAL":
#         payload = random.choice(traversal_payloads)
#         # Try to access public assets
#         path = f"/public/images/{payload}"

#     return path, attack_type

# def run():
#     print("--- 🚀 Enterprise Traffic Generator Started ---")
#     print("Generating dynamic, randomized traffic patterns...")
    
#     while True:
#         try:
#             # 60% Normal, 40% Attack
#             if random.random() < 0.6:
#                 path = get_normal_request()
#                 ip = random.choice(NORMAL_IPS)
#                 label = "NORMAL"
#             else:
#                 path, attack_type = get_attack_request()
#                 ip = random.choice(ATTACKER_IPS)
#                 label = f"ATTACK ({attack_type})"

#             headers = {
#                 "X-Forwarded-For": ip,
#                 "User-Agent": random.choice(USER_AGENTS)
#             }

#             # Send Request
#             # We use a custom User-Agent to make it look real
#             full_url = f"{TARGET_URL}{path}"
            
#             # Use a short timeout so we don't get stuck if Nginx drops packets
#             resp = requests.get(full_url, headers=headers, timeout=1)
            
#             # Logs
#             status_icon = "✅" if label == "NORMAL" else "❌"
#             print(f"{status_icon} [{label}] {ip} -> {path[:40]}... | Code: {resp.status_code}")

#         except Exception:
#             pass # Connection errors are expected when Firewall blocks us
            
#         # Realistic User Jitter (0.2s to 1.0s)
#         time.sleep(random.uniform(0.2, 1.0))

# if __name__ == "__main__":
#     time.sleep(5) 
#     run()


import requests
import time
import random
import string

TARGET_URL = "http://gateway:80"

# ... (Keep IP lists and User Agents from previous version) ...
NORMAL_IPS = [f"192.168.1.{x}" for x in range(5, 20)]
ATTACKER_IPS = ["203.55.11.22", "66.77.88.99", "185.20.30.40"]

USER_AGENTS = ["Mozilla/5.0", "Chrome/91.0", "Safari/537.36"] # Simplified for brevity

def get_normal_request():
    # ... (Keep previous normal logic) ...
    return "/rest/products/search?q=apple" # Simplified example

def get_attack_request():
    # ... (Keep SQLi/XSS payloads) ...
    
    # ADD HONEYPOT PROBE
    payloads = [
        "/rest/products/search?q=' OR 1=1 --",
        "/api/Feedbacks?comment=<script>alert(1)</script>",
        "/honeypot" # <--- THIS TRIGGERS THE HONEYPOT CONTAINER
    ]
    
    path = random.choice(payloads)
    
    if "OR" in path: return path, "SQLi"
    if "script" in path: return path, "XSS"
    if "honeypot" in path: return path, "PROBE"
    return path, "ATTACK"

def run():
    print("--- 🚀 Traffic Gen (Honeypot Enabled) ---")
    while True:
        try:
            if random.random() < 0.6:
                path = get_normal_request()
                ip = random.choice(NORMAL_IPS)
                label = "NORMAL"
            else:
                path, label = get_attack_request()
                ip = random.choice(ATTACKER_IPS)

            headers = {"X-Forwarded-For": ip, "User-Agent": random.choice(USER_AGENTS)}
            
            # Request
            resp = requests.get(f"{TARGET_URL}{path}", headers=headers, timeout=1)
            
            status_icon = "✅" if label == "NORMAL" else "❌"
            print(f"{status_icon} [{label}] {ip} -> {path[:25]}... | Code: {resp.status_code}")

        except:
            pass
            
        # SLOWER SPEED to prevent Rate Limit Bans on Good Users
        time.sleep(random.uniform(0.8, 2.0)) 

if __name__ == "__main__":
    time.sleep(5) 
    run()