import psutil
import time
import datetime
import os

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def system_check():
    clear_screen()
    print("=" * 50)
    print(" SYSTEM HEALTH CHECKUP ")
    print(" Time:", datetime.datetime.now())
    print("=" * 50)

    # CPU Information
    print("\nCPU INFORMATION")
    print(f"CPU Usage       : {psutil.cpu_percent(interval=1)} %")
    print(f"CPU Cores       : {psutil.cpu_count(logical=True)}")
    
    # Memory Information
    mem = psutil.virtual_memory()
    print("\nMEMORY INFORMATION")
    print(f"Total Memory    : {round(mem.total / (1024**3), 2)} GB")
    print(f"Used Memory     : {round(mem.used / (1024**3), 2)} GB")
    print(f"Memory Usage    : {mem.percent} %")

    # Disk Information
    disk = psutil.disk_usage('/')
    print("\nDISK INFORMATION")
    print(f"Total Disk      : {round(disk.total / (1024**3), 2)} GB")
    print(f"Used Disk       : {round(disk.used / (1024**3), 2)} GB")
    print(f"Disk Usage      : {disk.percent} %")

    # Network Information
    net = psutil.net_io_counters()
    print("\nNETWORK INFORMATION")
    print(f"Sent Data       : {round(net.bytes_sent / (1024**2), 2)} MB")
    print(f"Received Data   : {round(net.bytes_recv / (1024**2), 2)} MB")

    print("\nPress Ctrl + C to stop monitoring")

# Continuous Monitoring
try:
    while True:
        system_check()
        time.sleep(5)
except KeyboardInterrupt:
    print("\nSystem monitoring stopped.")