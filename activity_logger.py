import os
import time
import csv
import datetime
import threading
import psutil

# Requires: pip install pywin32
import win32gui
import win32process

# Requires: pip install watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


LOG_FILE = os.path.abspath("activity_log.csv")
POLL_SECONDS = 3  # change to 1-5 seconds as you like
WATCH_PATH = r"D:\\"  # <-- change to C:\\ or any folder you want


def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_foreground_window_info():
    """
    Returns (window_title, process_name, pid) for the current foreground window.
    """
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd) or ""
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        proc_name = ""
        try:
            proc_name = psutil.Process(pid).name()
        except Exception:
            proc_name = ""
        return title.strip(), proc_name, pid
    except Exception:
        return "", "", 0


def ensure_log_header():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            # Added columns: path + details
            w.writerow(["timestamp", "event", "process_name", "pid", "window_title", "path", "details"])


def log_row(event, process_name="", pid="", window_title="", path="", details=""):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([now_str(), event, process_name, pid, window_title, path, details])


class FSHandler(FileSystemEventHandler):
    """
    Logs folder/file create/delete/rename events.
    """
    def on_created(self, event):
        if event.is_directory:
            folder_name = os.path.basename(event.src_path.rstrip("\\/"))
            log_row("DIR_CREATED", path=event.src_path, details=f"name={folder_name}")
            print(f"[{now_str()}] DIR_CREATED | {folder_name} | {event.src_path}")
        else:
            file_name = os.path.basename(event.src_path)
            log_row("FILE_CREATED", path=event.src_path, details=f"name={file_name}")
            print(f"[{now_str()}] FILE_CREATED | {file_name} | {event.src_path}")

    def on_deleted(self, event):
        # NOTE: when deleted, src_path still contains the deleted item's path (name included)
        if event.is_directory:
            folder_name = os.path.basename(event.src_path.rstrip("\\/"))
            log_row("DIR_DELETED", path=event.src_path, details=f"name={folder_name}")
            print(f"[{now_str()}] DIR_DELETED | {folder_name} | {event.src_path}")
        else:
            file_name = os.path.basename(event.src_path)
            log_row("FILE_DELETED", path=event.src_path, details=f"name={file_name}")
            print(f"[{now_str()}] FILE_DELETED | {file_name} | {event.src_path}")

    def on_moved(self, event):
        # Rename/move: event.src_path -> event.dest_path
        if event.is_directory:
            old_name = os.path.basename(event.src_path.rstrip("\\/"))
            new_name = os.path.basename(event.dest_path.rstrip("\\/"))
            details = f"{old_name} -> {new_name}"
            log_row("DIR_RENAMED", path=event.dest_path, details=details)
            print(f"[{now_str()}] DIR_RENAMED | {details} | {event.src_path} -> {event.dest_path}")
        else:
            old_name = os.path.basename(event.src_path)
            new_name = os.path.basename(event.dest_path)
            details = f"{old_name} -> {new_name}"
            log_row("FILE_RENAMED", path=event.dest_path, details=details)
            print(f"[{now_str()}] FILE_RENAMED | {details} | {event.src_path} -> {event.dest_path}")

    def on_modified(self, event):
        # Modified events can be noisy; keep if you want
        # If you don't want modified logs, comment this function.
        if event.is_directory:
            return
        file_name = os.path.basename(event.src_path)
        log_row("FILE_MODIFIED", path=event.src_path, details=f"name={file_name}")
        print(f"[{now_str()}] FILE_MODIFIED | {file_name} | {event.src_path}")


def start_filesystem_watcher(stop_event: threading.Event):
    if not os.path.exists(WATCH_PATH):
        print(f"❌ WATCH_PATH not found: {WATCH_PATH}")
        return

    observer = Observer()
    observer.schedule(FSHandler(), WATCH_PATH, recursive=True)
    observer.start()

    print(f"Filesystem watcher started ✅ (watching: {WATCH_PATH})")

    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    finally:
        observer.stop()
        observer.join()


def main():
    print("Activity Logger started ✅")
    print(f"Logging to: {LOG_FILE}")
    print(f"Watching file/folder activity in: {WATCH_PATH}")
    print("Press Ctrl+C to stop.\n")

    ensure_log_header()

    stop_event = threading.Event()
    fs_thread = threading.Thread(target=start_filesystem_watcher, args=(stop_event,), daemon=True)
    fs_thread.start()

    # Track processes to detect newly started apps
    known_pids = set(psutil.pids())

    last_title = None
    last_pid = None

    # First entry
    title, pname, pid = get_foreground_window_info()
    log_row("FOREGROUND", pname, pid, title)
    print(f"[{now_str()}] FOREGROUND | {pname} ({pid}) | {title}")

    try:
        while True:
            # 1) Detect new processes (apps you opened)
            current_pids = set(psutil.pids())
            new_pids = current_pids - known_pids
            known_pids = current_pids

            for npid in list(new_pids)[:200]:  # safety cap
                try:
                    p = psutil.Process(npid)
                    pname = p.name()
                    log_row("PROCESS_START", pname, npid, "")
                    print(f"[{now_str()}] PROCESS_START | {pname} ({npid})")
                except Exception:
                    continue

            # 2) Track foreground window changes (what you’re actively doing)
            title, pname, pid = get_foreground_window_info()
            if title and (title != last_title or pid != last_pid):
                log_row("FOREGROUND", pname, pid, title)
                print(f"[{now_str()}] FOREGROUND | {pname} ({pid}) | {title}")
                last_title, last_pid = title, pid

            time.sleep(POLL_SECONDS)

    except KeyboardInterrupt:
        stop_event.set()
        print("\nStopped. Log saved ✅")


if __name__ == "__main__":
    main()
