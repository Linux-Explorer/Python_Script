import psutil
import time
import os

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def clear_screen():
    # Clear screen command for Windows is 'cls', for Linux/Mac is 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def show_system_load():
    print("="*40)
    print("      SYSTEM LOAD MONITOR (Ctrl+C to stop)")
    print("="*40)
    
    try:
        while True:
            # --- CPU Information ---
            # interval=1 means it waits 1 second to calculate the average usage
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            
            # --- Memory (RAM) Information ---
            svmem = psutil.virtual_memory()
            
            # --- Swap (Pagefile) Information ---
            swap = psutil.swap_memory()

            # Clear previous output to create a "dashboard" feel
            clear_screen()
            
            print("="*40)
            print(f"Time: {time.strftime('%H:%M:%S')}")
            print("="*40)

            # CPU Output
            print(f"CPU Usage:      {cpu_usage}%")
            if cpu_freq:
                print(f"CPU Frequency:  {cpu_freq.current:.2f}Mhz")
            print("-" * 40)

            # RAM Output
            print(f"Total RAM:      {get_size(svmem.total)}")
            print(f"Available RAM:  {get_size(svmem.available)}")
            print(f"Used RAM:       {get_size(svmem.used)}")
            print(f"RAM Usage:      {svmem.percent}%")
            
            # Visual Bar for RAM
            # Creates a bar like [||||||    ]
            bar_length = 20
            filled_length = int(bar_length * svmem.percent // 100)
            bar = '|' * filled_length + '-' * (bar_length - filled_length)
            print(f"[{bar}]")
            
            print("-" * 40)
            
            # Optional: Swap/Pagefile memory (Virtual memory on disk)
            print(f"Swap Used:      {get_size(swap.used)} ({swap.percent}%)")

            # The loop is already delayed by cpu_percent(interval=1), 
            # so we don't need an extra time.sleep()
            
    except KeyboardInterrupt:
        print("\nStopped by user.")

if __name__ == "__main__":
    show_system_load()