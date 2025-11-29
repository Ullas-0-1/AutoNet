from fastapi import FastAPI, Request
import socket
import random

#currently i have this basic , model, will implement all the features properly later

app = FastAPI(title="AutoNet Secure Bank API")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to AutoNet Bank",
        "node": socket.gethostname(),
        "status": "Operational"
    }

@app.get("/balance")
def get_balance():
    # Simulate a sensitive endpoint
    return {
        "account": "123-456-789",
        "balance": random.randint(1000, 50000),
        "currency": "USD"
    }

@app.post("/login")
def login_user(data: dict):
    # Simulate a login action
    return {"message": f"Login processed for user: {data.get('username', 'guest')}"}

@app.get("/admin")
def admin_panel():
    return {"message": "ADMIN AREA - RESTRICTED ACCESS"}