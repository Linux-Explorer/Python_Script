import psutil
import platform
import socket
import time

def get_system_info():
    print("\n=== SYSTEM INFO ===")
    print("OS:", platform.system(), platform.release())
    print("Machine:", platform.machine())
    print("Hostname:", socket.gethostname())


def get_cpu():
    print("\n=== CPU USAGE ===")
    print("CPU Usage:", psutil.cpu_percent(interval=1), "%")
    print("CPU Cores:", psutil.cpu_count(logical=True))


def get_memory():
    mem = psutil.virtual_memory()
    print("\n=== MEMORY ===")
    print(f"Total: {mem.total / (1024**3):.2f} GB")
    print(f"Available: {mem.available / (1024**3):.2f} GB")
    print(f"Usage: {mem.percent}%")


def get_disk():
    disk = psutil.disk_usage('/')
    print("\n=== DISK ===")
    print(f"Total: {disk.total / (1024**3):.2f} GB")
    print(f"Used: {disk.used / (1024**3):.2f} GB")
    print(f"Free: {disk.free / (1024**3):.2f} GB")
    print(f"Usage: {disk.percent}%")


def get_uptime():
    boot_time = psutil.boot_time()
    uptime = time.time() - boot_time
    print("\n=== UPTIME ===")
    print(f"System Uptime: {uptime / 3600:.2f} hours")


if __name__ == "__main__":
    while True:
        print("\n==============================")
        get_system_info()
        get_cpu()
        get_memory()
        get_disk()
        get_uptime()
        print("\nRefreshing in 20 second...\n")
        time.sleep(20)