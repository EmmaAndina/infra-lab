import os
import requests
import time
from dotenv import load_dotenv

load_dotenv("/root/.env")

COOLIFY_URL = os.getenv("COOLIFY_URL")
COOLIFY_TOKEN = os.getenv("COOLIFY_TOKEN")
HEADERS = {"Authorization": f"Bearer {COOLIFY_TOKEN}", "Content-Type": "application/json"}
API_BASE = f"{COOLIFY_URL}/api/v1"

def deploy():
    # Encontrar proyecto infra-lab
    projects = requests.get(f"{API_BASE}/projects", headers=HEADERS).json()
    p_uuid = None
    for p in projects:
        if p.get("name") == "infra-lab":
            p_uuid = p.get("uuid")
            break
            
    if not p_uuid:
        print("Error: No se encontró el proyecto infra-lab")
        return
        
    envs = requests.get(f"{API_BASE}/projects/{p_uuid}", headers=HEADERS).json()
    if not envs or not envs.get("environments"):
        print("No se encontraron entornos")
        return
        
    env_uuid = envs.get("environments", [{}])[0].get("uuid")
    
    apps_res = requests.get(f"{API_BASE}/environments/{env_uuid}/applications", headers=HEADERS)
    if apps_res.status_code == 200 and apps_res.json():
        app_uuid = apps_res.json()[0].get("uuid")
        print(f"App encontrada correctamente: {app_uuid}")
        
        print(f"Iniciando deploy para uuid={app_uuid}...")
        # Using the correct Coolify v4 deploy endpoint for a specific resource
        d_res = requests.post(f"{API_BASE}/deploy?uuid={app_uuid}", headers=HEADERS)
        print("Deploy res:", d_res.status_code, d_res.text)
    else:
        print("App not found in env", apps_res.status_code, apps_res.text)

deploy()
