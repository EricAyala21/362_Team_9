# clear_bad_timestamps.py
# Deletes any logs in the database with improperly formatted timestamps
# Helps prevent app crashes due to date parsing

import sqlite3
import datetime

# Define the correct format used throughout the app
EXPECTED_FORMAT = "%m/%d/%Y %H:%M"

# Connect to the temp database (update if your filename is different)
conn = sqlite3.connect("temp.db")
cur = conn.cursor()

# Grab all timestamps from the logs table
cur.execute("SELECT timestamp FROM logs")
rows = cur.fetchall()

bad_rows = []

# Check each timestamp format
for r in rows:
    ts = r[0]
    try:
        datetime.datetime.strptime(ts, EXPECTED_FORMAT)
    except ValueError:
        bad_rows.append((ts,))

# Delete rows with bad timestamps
if bad_rows:
    cur.executemany("DELETE FROM logs WHERE timestamp = ?", bad_rows)
    conn.commit()
    print(f"Deleted {len(bad_rows)} bad log(s) with incorrect timestamp format.")
else:
    print("No formatting issues found. Database is clean.")

conn.close()
