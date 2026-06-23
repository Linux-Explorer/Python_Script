import os
import shutil
import sqlite3
from datetime import datetime, timedelta
from urllib.parse import urlparse
from collections import defaultdict

def chrome_time_to_datetime(chrome_time):
    # Chrome timestamp = microseconds since 1601-01-01
    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)

def get_chrome_history_db():
    user = os.environ.get("USERNAME")
    history_path = fr"C:\Users\{user}\AppData\Local\Google\Chrome\User Data\Default\History"
    if not os.path.exists(history_path):
        raise FileNotFoundError("Chrome History file not found. Are you using Chrome 'Default' profile?")
    return history_path

def safe_copy_history_db(src_path):
    temp_path = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "ChromeHistory_copy")
    shutil.copy2(src_path, temp_path)
    return temp_path

def estimate_time_spent(visits, max_gap_seconds=300):
    """
    Estimate time on a site by looking at time gaps between consecutive page visits.
    We cap each gap at 5 minutes (default) to avoid huge overestimation.
    """
    visits = sorted(visits, key=lambda x: x["time"])
    domain_seconds = defaultdict(int)

    for i in range(len(visits) - 1):
        cur = visits[i]
        nxt = visits[i + 1]
        gap = (nxt["time"] - cur["time"]).total_seconds()

        # ignore negative/zero gaps
        if gap <= 0:
            continue

        # cap large gaps (user may be away)
        gap = min(gap, max_gap_seconds)

        domain_seconds[cur["domain"]] += int(gap)

    return domain_seconds

def main():
    # Today range (local time)
    now = datetime.now()
    start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    src_db = get_chrome_history_db()
    db_copy = safe_copy_history_db(src_db)

    conn = sqlite3.connect(db_copy)
    cur = conn.cursor()

    # Pull url + visit_time from visits + urls
    query = """
    SELECT urls.url, urls.title, visits.visit_time
    FROM visits
    JOIN urls ON visits.url = urls.id
    WHERE visits.visit_time > ?
    ORDER BY visits.visit_time ASC
    """

    # Convert "start_today" to Chrome epoch
    chrome_epoch = datetime(1601, 1, 1)
    start_chrome = int((start_today - chrome_epoch).total_seconds() * 1_000_000)

    cur.execute(query, (start_chrome,))
    rows = cur.fetchall()
    conn.close()

    visits = []
    for url, title, visit_time in rows:
        try:
            dt = chrome_time_to_datetime(visit_time)
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            if domain:
                visits.append({"time": dt, "domain": domain, "url": url, "title": title or ""})
        except Exception:
            pass

    if not visits:
        print("No Chrome history found for today.")
        return

    # Count visits per domain
    domain_visits = defaultdict(int)
    for v in visits:
        domain_visits[v["domain"]] += 1

    # Estimate time spent per domain (approx)
    domain_seconds = estimate_time_spent(visits, max_gap_seconds=300)

    # Combine + sort
    report = []
    for d in domain_visits:
        seconds = domain_seconds.get(d, 0)
        report.append((d, domain_visits[d], seconds))

    report.sort(key=lambda x: (x[2], x[1]), reverse=True)

    print("\n==== CHROME DAILY USAGE (TODAY) ====")
    print(f"Date: {start_today.strftime('%Y-%m-%d')}")
    print("Note: 'Time spent' is an estimate based on gaps between page visits (capped at 5 min).")
    print("\nTop sites:\n")

    print(f"{'Domain':40} {'Visits':>8} {'Est. Time':>12}")
    print("-" * 65)

    total_seconds = 0
    for domain, visits_count, sec in report[:30]:
        total_seconds += sec
        hrs = sec // 3600
        mins = (sec % 3600) // 60
        time_str = f"{hrs}h {mins}m" if hrs else f"{mins}m"
        print(f"{domain:40} {visits_count:>8} {time_str:>12}")

    th = total_seconds // 3600
    tm = (total_seconds % 3600) // 60
    print("\n---------------------------------")
    print(f"Estimated tracked browsing time: {th}h {tm}m (approx)")

if __name__ == "__main__":
    main()
