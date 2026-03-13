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
        
    servers = requests.get(f"{API_BASE}/servers", headers=HEADERS).json()
    s_uuid = servers[0].get("uuid")
    
    envs = requests.get(f"{API_BASE}/projects/{p_uuid}", headers=HEADERS).json()
    env_name = envs.get("environments", [{}])[0].get("name", "production")
    
    payload = {
        "project_uuid": p_uuid,
        "server_uuid": s_uuid,
        "environment_name": env_name,
        "git_repository": "https://github.com/EmmaAndina/infra-lab",
        "git_branch": "main",
        "build_pack": "dockerfile",
        "ports_exposes": "80",
        "base_directory": "/agents/operator-agent",
        "dockerfile_location": "/agents/operator-agent/Dockerfile"
    }

    print("POST /applications/public")
    a_res = requests.post(f"{API_BASE}/applications/public", headers=HEADERS, json=payload)
    if a_res.status_code != 201:
        print("Error creando app:", a_res.text)
        return
        
    app_uuid = a_res.json().get("uuid")
    print(f"App creada correctamente: {app_uuid}")
    
    print("Iniciando deploy...")
    d_res = requests.post(f"{API_BASE}/applications/{app_uuid}/deploy", headers=HEADERS)
    print("Deploy res:", d_res.status_code, d_res.text)

deploy()
