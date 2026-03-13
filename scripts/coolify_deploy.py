import os
import requests
import time
from dotenv import load_dotenv

print("Cargando variables...")
load_dotenv()

COOLIFY_URL = os.getenv("COOLIFY_URL")
COOLIFY_TOKEN = os.getenv("COOLIFY_TOKEN")
HEADERS = {"Authorization": f"Bearer {COOLIFY_TOKEN}", "Content-Type": "application/json"}
API_BASE = f"{COOLIFY_URL}/api/v1"

def create_project():
    res = requests.post(f"{API_BASE}/projects", headers=HEADERS, json={"name": "infra-lab"})
    if res.status_code == 201: return res.json().get("uuid")
    for p in requests.get(f"{API_BASE}/projects", headers=HEADERS).json():
        if p.get("name") == "infra-lab": return p.get("uuid")
    return requests.get(f"{API_BASE}/projects", headers=HEADERS).json()[0].get("uuid")

def get_server_uuid():
    return requests.get(f"{API_BASE}/servers", headers=HEADERS).json()[0].get("uuid")

def create_app(project_uuid, server_uuid):
    envs = requests.get(f"{API_BASE}/projects/{project_uuid}", headers=HEADERS).json()
    env_name = envs.get("environments", [{}])[0].get("name", "production")
    
    payload = {
        "project_uuid": project_uuid,
        "server_uuid": server_uuid,
        "environment_name": env_name,
        "git_repository": "https://github.com/EmmaAndina/infra-lab",
        "git_branch": "main",
        "build_pack": "dockerfile",
        "ports_exposes": "80",
        "base_directory": "/agents/operator-agent",
        "dockerfile_location": "/agents/operator-agent/Dockerfile"
    }

    print(f"POST {API_BASE}/applications/public")
    res = requests.post(f"{API_BASE}/applications/public", headers=HEADERS, json=payload)
    if res.status_code == 201: return res.json().get("uuid")
    print(res.text)
    return None

def deploy(app_uuid):
    print("Deploying...")
    res = requests.post(f"{API_BASE}/applications/{app_uuid}/deploy", headers=HEADERS)
    print(res.status_code)

server = get_server_uuid()
proj = create_project()
app = create_app(proj, server)
if app: deploy(app)
