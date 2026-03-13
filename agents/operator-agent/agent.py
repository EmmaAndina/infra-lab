import os
import subprocess
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode()
    except Exception as e:
        return str(e)

def perform_check():
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/server_checks.log"
    with open(log_file, "a") as f:
        f.write(f"\n--- Check at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write("Server status:\n")
        f.write(run("uptime") + "\n")
        f.write("\nDisk usage:\n")
        f.write(run("df -h") + "\n")

class SimpleAgentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        perform_check()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        uptime = run("uptime")
        html = f"<html><body><h1>Operator Agent Active</h1><pre>{uptime}</pre></body></html>"
        self.wfile.write(html.encode("utf-8"))

def main():
    # Initial check
    perform_check()
    
    port = int(os.environ.get("PORT", 80))
    server = HTTPServer(("0.0.0.0", port), SimpleAgentHandler)
    print(f"Agent running on port {port}...")
    server.serve_forever()

if __name__ == "__main__":
    main()
