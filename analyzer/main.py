import time
import subprocess
import os
import re
import joblib
import pandas as pd
import math
from collections import defaultdict, deque, Counter

LOG_FILE = "/shared_data/access.log"
ANSIBLE_PLAYBOOK = "update_firewall.yml"
MODEL_PATH = "brain.pkl"

# --- CONFIG ---
RATE_LIMIT_MAX = 500 
RATE_LIMIT_WINDOW = 60 

THREAT_FEED = {"192.168.100.100"}

SIGNATURES = [
    r"('|\"|%27|%22)\s*(OR|UNION|SELECT|INSERT|DROP)", 
    r"(<script>|%3Cscript%3E|alert\()",               
    r"(\.\./|\.\.%2f)",                                                                  
]

# --- HELPERS ---
def calculate_entropy(text):
    if not text: return 0
    entropy = 0
    for x in Counter(text).values():
        p_x = x / len(text)
        entropy -= p_x * math.log2(p_x)
    return entropy

class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.history = defaultdict(deque)

    def is_allowed(self, ip):
        now = time.time()
        timestamps = self.history[ip]
        while timestamps and timestamps[0] < now - self.window:
            timestamps.popleft()
        timestamps.append(now)
        return len(timestamps) <= self.limit

print("--- 🔄 Initializing AutoNet AI ---")
try:
    ml_model = joblib.load(MODEL_PATH)
    print("✅ AI Brain Loaded.")
except:
    print("❌ CRITICAL: No brain.pkl found.")
    exit(1)

BANNED_IPS = set()
rate_limiter = RateLimiter(limit=RATE_LIMIT_MAX, window=RATE_LIMIT_WINDOW)

def extract_features(url):
    # MUST MATCH train_model.py EXACTLY
    entropy = calculate_entropy(url)
    special_chars = sum(not c.isalnum() for c in url)
    punctuation_ratio = special_chars / len(url) if len(url) > 0 else 0

    return pd.DataFrame([[
        len(url),
        url.count("'") + url.count("%27"),
        url.count("<") + url.count("%3C"),
        url.count("."),
        special_chars,
        entropy,
        punctuation_ratio
    ]], columns=['len', 'sqli', 'xss', 'dots', 'specials', 'entropy', 'density'])

def trigger_response(ip, reason):
    if ip in BANNED_IPS: return
    print(f"🚨 BLOCKING {ip} | Reason: {reason}")
    cmd = f"ansible-playbook {ANSIBLE_PLAYBOOK} --extra-vars 'banned_ip={ip}'"
    try:
        subprocess.run(cmd, shell=True, check=True)
        BANNED_IPS.add(ip)
    except:
        pass

def follow(thefile):
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def start_surveillance():
    print("--- 🛡️  IPS Active. Monitoring... ---")
    while not os.path.exists(LOG_FILE): time.sleep(2)
    logfile = open(LOG_FILE, "r")

    for line in follow(logfile):
        try:
            parts = line.split(" ")
            if len(parts) < 7: continue
            ip = parts[0]
            
            try:
                url = line.split('"')[1].split(" ")[1]
            except:
                continue

            # 1. THREAT INTEL
            if ip in THREAT_FEED:
                trigger_response(ip, "Threat_Intel")
                continue

            # 2. RATE LIMIT
            if not rate_limiter.is_allowed(ip):
                trigger_response(ip, "DDoS_Behavior_RateLimit")
                continue

            # 3. SIGNATURES
            sig_matched = False
            for pattern in SIGNATURES:
                if re.search(pattern, url, re.IGNORECASE):
                    print(f"⚠️  Signature Match: {url}")
                    trigger_response(ip, "Signature_Detection")
                    sig_matched = True
                    break
            if sig_matched: continue

            # 4. ML ANOMALY
            features = extract_features(url)
            if ml_model.predict(features)[0] == -1:
                print(f"🤖 AI Anomaly Detected (High Entropy): {url}")
                trigger_response(ip, "ML_Anomaly")

        except Exception:
            pass

if __name__ == "__main__":
    start_surveillance()