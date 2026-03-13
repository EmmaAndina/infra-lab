import requests
import os
import json
from dotenv import load_dotenv

load_dotenv("/root/.env")

COOLIFY_URL = os.getenv("COOLIFY_URL")
COOLIFY_TOKEN = os.getenv("COOLIFY_TOKEN")
HEADERS = {"Authorization": f"Bearer {COOLIFY_TOKEN}", "Content-Type": "application/json"}
API_BASE = f"{COOLIFY_URL}/api/v1"

def cleanup():
    print("Obteniendo todos los proyectos...")
    res = requests.get(f"{API_BASE}/projects", headers=HEADERS)
    if res.status_code != 200:
        print("Error obteniendo proyectos:", res.text)
        return

    projects = res.json()
    print(f"[{len(projects)}] proyectos encontrados.")

    # Guardar uno que se llame infra-lab, o el default
    project_to_keep = None
    for p in projects:
        if p.get("name") == "infra-lab":
            project_to_keep = p
            break
            
    if not project_to_keep and projects:
        project_to_keep = projects[0]

    if not project_to_keep:
        print("No hay proyectos.")
        return

    kept_id = project_to_keep.get("uuid")
    print(f"Vamos a MANTENER el proyecto: {project_to_keep.get('name')} ({kept_id})")

    # Borrar el resto
    for p in projects:
        uuid = p.get("uuid")
        if uuid != kept_id and p.get("name") != "default" and p.get("name") != project_to_keep.get("name"):
            print(f"Borrando proyecto duplicado: {p.get('name')} ({uuid})")
            d_res = requests.delete(f"{API_BASE}/projects/{uuid}", headers=HEADERS)
            if d_res.status_code != 200:
                print(f"Error borrando {uuid}: {d_res.text}")

    print("Limpieza de proyectos terminada.")

    # Borrar las configuraciones repetidas si existieran
    print("\nRevisando aplicaciones en el proyecto principal...")
    env_uuid = project_to_keep.get("environments", [{}])[0].get("uuid")
    
    if env_uuid:
        # Obteniendo aplicaciones (probablemente no existan por lo de la UI)
        try:
            apps_res = requests.get(f"{API_BASE}/applications", headers=HEADERS)
            apps = apps_res.json()
            # Delete apps that failed if there are any
            for app in apps:
               print(f"App encontrada: {app.get('name')} ({app.get('uuid')}) Status: {app.get('status')}")
               if app.get("status") == "failed" or app.get("status") == "exited":
                   print(f"Borrando app fallida: {app.get('uuid')}")
                   requests.delete(f"{API_BASE}/applications/{app.get('uuid')}", headers=HEADERS)
        except Exception as e:
            print("Error buscando apps:", e)

cleanup()
