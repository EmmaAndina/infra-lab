import os
import subprocess
import datetime

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode()
    except Exception as e:
        return str(e)

def main():
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    log_file = "logs/server_checks.log"
    
    with open(log_file, "a") as f:
        f.write(f"\n--- Check at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        f.write("Server status:\n")
        f.write(run("uptime") + "\n")
        f.write("\nDisk usage:\n")
        f.write(run("df -h") + "\n")
        
    print(f"Agent finished. System checked and logged to {log_file}.")

if __name__ == "__main__":
    main()
