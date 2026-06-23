import subprocess
import platform

# List your servers here (IP or domain)
servers = [
    "192.168.0.2",
    "192.168.0.5",
    "192.168.0.3"
    
]

# Detect OS
param = "-n" if platform.system().lower() == "windows" else "-c"

def ping_server(server):
    try:
        command = ["ping", param, "1", server]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            return "UP"
        else:
            return "DOWN"
    except Exception as e:
        return f"ERROR: {e}"

print("Server Status Check\n" + "-"*25)

for server in servers:
    status = ping_server(server)
    print(f"{server} : {status}")