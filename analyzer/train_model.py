# import pandas as pd
# import numpy as np
# from sklearn.ensemble import IsolationForest
# import joblib
# import random
# import string
# import math
# from collections import Counter

# print("🏗️  MLOPS: Starting Model Training Pipeline...")

# # --- MATH HELPER FUNCTIONS ---
# def calculate_entropy(text):
#     """Calculates Shannon Entropy (Randomness level of the string)"""
#     if not text: return 0
#     entropy = 0
#     for x in Counter(text).values():
#         p_x = x / len(text)
#         entropy -= p_x * math.log2(p_x)
#     return entropy

# # --- STEP 1: GENERATE COMPLEX BUT BENIGN TRAFFIC ---
# def generate_complex_normal_url():
#     # Same logic as before, ensuring we cover realistic web patterns
#     bases = ["/api/v1", "/rest", "/graphql", "/app", "/static", "/assets", "/images", "/socket.io"]
#     resources = ["user", "product", "order", "cart", "auth", "search", "feed", "notification"]
#     extensions = [".json", ".xml", ".html", ".jpg", ".png", ".js", ""]
    
#     path = random.choice(bases)
#     for _ in range(random.randint(1, 3)):
#         path += "/" + random.choice(resources)
    
#     if random.random() > 0.5:
#         slug = ''.join(random.choices(string.ascii_letters + string.digits + "-", k=random.randint(5, 20)))
#         path += "/" + slug
    
#     path += random.choice(extensions)

#     # Add query params (Normal looking ones)
#     if random.random() > 0.3:
#         path += "?"
#         num_params = random.randint(1, 4)
#         for i in range(num_params):
#             key = ''.join(random.choices(string.ascii_lowercase, k=4))
#             val = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
#             path += f"{key}={val}"
#             if i < num_params - 1:
#                 path += "&"
#     return path

# print("Generating 15,000 complex normal samples...")
# data = []
# for _ in range(15000):
#     url = generate_complex_normal_url()
    
#     # --- ADVANCED FEATURE ENGINEERING ---
#     entropy = calculate_entropy(url)
#     special_chars = sum(not c.isalnum() for c in url)
#     punctuation_ratio = special_chars / len(url) if len(url) > 0 else 0
    
#     features = [
#         len(url),                     # 1. Length
#         url.count("'") + url.count("%27"), # 2. SQLi chars
#         url.count("<") + url.count("%3C"), # 3. XSS chars
#         url.count("."),               # 4. Dots
#         special_chars,                # 5. Total Special Chars
#         entropy,                      # 6. Randomness (New!)
#         punctuation_ratio             # 7. Density (New!)
#     ]
#     data.append(features)

# df = pd.DataFrame(data, columns=['len', 'sqli', 'xss', 'dots', 'specials', 'entropy', 'density'])

# # --- STEP 2: TRAIN ---
# print(f"🧠 Training Isolation Forest with Entropy...")
# # contamination=0.01: We are very confident our training data is clean
# model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
# model.fit(df)

# # --- STEP 3: SAVE ---
# print("💾 Saving model to 'brain.pkl'...")
# joblib.dump(model, 'brain.pkl')
# print("✅ MLOps Pipeline Complete.")


import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import random
import string
import math
from collections import Counter

print("🏗️  MLOPS: Starting Model Training Pipeline...")

# --- HELPER: CALCULATE ENTROPY ---
def calculate_entropy(text):
    if not text: return 0
    entropy = 0
    for x in Counter(text).values():
        p_x = x / len(text)
        entropy -= p_x * math.log2(p_x)
    return entropy

# --- STEP 1: GENERATE HYBRID TRAINING DATA ---
def generate_training_data():
    data = []
    
    # A. KNOWN SAFE PATHS (The "Cheat Sheet" for Juice Shop)
    # This ensures the model explicitly trusts these patterns.
    safe_patterns = [
        "/", "/#/search", "/#/login", "/#/register", "/#/photo-wall",
        "/api/Challenges", "/api/Feedbacks", "/api/Quantitys",
        "/rest/products/search?q=apple", "/rest/products/search?q=orange",
        "/assets/public/images/products/juice.jpg", 
        "/assets/public/images/products/apple_juice.jpg",
        "/socket.io/?EIO=3&transport=polling", 
        "/socket.io/?EIO=3&transport=polling&t=O_123",
        "/ftp/legal.md", "/rest/user/login", "/api/BasketItems",
        "/api/Complaints"
    ]
    
    # B. SYNTHETIC COMPLEX PATHS (General Web Traffic)
    bases = ["/api/v1", "/rest", "/graphql", "/app", "/static", "/assets"]
    
    # Generate 15,000 samples
    for _ in range(15000):
        # 30% Chance to pick a known safe path (Reinforcement)
        if random.random() < 0.3:
            url = random.choice(safe_patterns)
        else:
            # 70% Chance to generate a random benign URL
            path = random.choice(bases)
            slug = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
            url = f"{path}/{slug}.json"
            
            if random.random() > 0.5:
                url += f"?id={random.randint(1,999)}"

        # EXTRACT FEATURES
        entropy = calculate_entropy(url)
        special_chars = sum(not c.isalnum() for c in url)
        density = special_chars / len(url) if len(url) > 0 else 0
        
        features = [
            len(url),
            url.count("'") + url.count("%27"), # SQLi
            url.count("<") + url.count("%3C"), # XSS
            url.count("."),
            special_chars,
            entropy,
            density
        ]
        data.append(features)
        
    return pd.DataFrame(data, columns=['len', 'sqli', 'xss', 'dots', 'specials', 'entropy', 'density'])

# --- STEP 2: TRAIN ---
df = generate_training_data()
print(f"🧠 Training Isolation Forest on {len(df)} samples...")

# increased contamination slightly to reduce false positives
model = IsolationForest(n_estimators=100, contamination=0.02, random_state=42) 
model.fit(df)

print("💾 Saving model to 'brain.pkl'...")
joblib.dump(model, 'brain.pkl')
print("✅ MLOps Pipeline Complete.")


