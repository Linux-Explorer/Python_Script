import tkinter as tk
from tkinter import ttk
import psutil
import time
from datetime import datetime

# ---------- LOG FILE ----------
LOG_FILE = "system_usage.log"

# ---------- FUNCTIONS ----------

def get_top_processes(limit=5):
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except:
            pass

    procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)
    return procs[:limit]


def format_bytes(bytes_val):
    return bytes_val / (1024 ** 3)


def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hrs = int(uptime_seconds // 3600)
    mins = int((uptime_seconds % 3600) // 60)
    return f"{hrs}h {mins}m"


def log_data(cpu, mem):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | CPU: {cpu}% | RAM: {mem}%\n")


# ---------- UPDATE FUNCTION ----------

prev_net = psutil.net_io_counters()

def update():
    global prev_net

    cpu = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    # Network speed
    sent_speed = (net.bytes_sent - prev_net.bytes_sent) / 1024
    recv_speed = (net.bytes_recv - prev_net.bytes_recv) / 1024
    prev_net = net

    # Update labels
    cpu_label.config(text=f"CPU Usage: {cpu:.1f}%")
    mem_label.config(text=f"RAM Usage: {mem.percent:.1f}%")
    disk_label.config(text=f"Disk Usage: {disk.percent:.1f}%")
    net_label.config(text=f"Net: ↑ {sent_speed:.1f} KB/s ↓ {recv_speed:.1f} KB/s")
    uptime_label.config(text=f"Uptime: {get_uptime()}")

    # Update progress bars
    cpu_bar['value'] = cpu
    mem_bar['value'] = mem.percent
    disk_bar['value'] = disk.percent

    # Alert coloring
    if cpu > 80:
        cpu_label.config(fg="red")
    else:
        cpu_label.config(fg="white")

    if mem.percent > 85:
        mem_label.config(fg="red")
    else:
        mem_label.config(fg="white")

    # Top processes
    for row in tree.get_children():
        tree.delete(row)

    for proc in get_top_processes():
        tree.insert("", "end", values=(
            proc['pid'],
            proc['name'][:20],
            f"{proc['cpu_percent']:.1f}",
            f"{proc['memory_percent']:.1f}"
        ))

    # Logging
    log_data(cpu, mem.percent)

    root.after(2000, update)


# ---------- GUI ----------

root = tk.Tk()
root.title("Advanced System Monitor")
root.geometry("600x500")
root.configure(bg="#1e1e1e")

# ---------- STYLES ----------
style = ttk.Style()
style.theme_use('default')

# ---------- LABELS ----------
cpu_label = tk.Label(root, text="", fg="white", bg="#1e1e1e")
cpu_label.pack()

cpu_bar = ttk.Progressbar(root, length=500, maximum=100)
cpu_bar.pack(pady=5)

mem_label = tk.Label(root, text="", fg="white", bg="#1e1e1e")
mem_label.pack()

mem_bar = ttk.Progressbar(root, length=500, maximum=100)
mem_bar.pack(pady=5)

disk_label = tk.Label(root, text="", fg="white", bg="#1e1e1e")
disk_label.pack()

disk_bar = ttk.Progressbar(root, length=500, maximum=100)
disk_bar.pack(pady=5)

net_label = tk.Label(root, text="", fg="white", bg="#1e1e1e")
net_label.pack(pady=5)

uptime_label = tk.Label(root, text="", fg="white", bg="#1e1e1e")
uptime_label.pack(pady=5)

# ---------- PROCESS TABLE ----------
columns = ("PID", "Name", "CPU %", "MEM %")
tree = ttk.Treeview(root, columns=columns, show='headings', height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(pady=10, fill="x")

# ---------- CLOSE SHORTCUT ----------
root.bind("<Escape>", lambda e: root.destroy())

# ---------- START ----------
update()
root.mainloop()