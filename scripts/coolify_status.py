import os
import requests
import json
from dotenv import load_dotenv

load_dotenv("/root/.env")

COOLIFY_URL = os.getenv("COOLIFY_URL")
COOLIFY_TOKEN = os.getenv("COOLIFY_TOKEN")
HEADERS = {"Authorization": f"Bearer {COOLIFY_TOKEN}", "Content-Type": "application/json"}
API_BASE = f"{COOLIFY_URL}/api/v1"

def print_logs():
    d_uuid = "g466qgj1o9ar02r0d324ejga"
    res = requests.get(f"{API_BASE}/deployments/{d_uuid}", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        print(f"Status: {data.get('status')}")
        logs = data.get('logs', [])
        
        if isinstance(logs, list):
            for log in logs:
                try:
                    obj = json.loads(log) if isinstance(log, str) else log
                    if 'log' in obj:
                        print(obj['log'].strip())
                    elif 'output' in obj: # coolify uses output sometimes
                        print(obj['output'].strip())
                    else:
                        print(obj)
                except:
                    print(log)
        elif isinstance(logs, str):
            # If logs is just a massive string
            print(logs)
    else:
        print("Error:", res.status_code, res.text)

print_logs()
