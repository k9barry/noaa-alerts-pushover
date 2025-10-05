import os
import sqlite3

# Try Docker path first, fallback to local path
docker_db_path = '/app/data/alerts.db'
local_db_path = os.path.join(os.path.dirname(__file__), 'data', 'alerts.db')
db_path = docker_db_path if os.path.exists('/app/data') else local_db_path

conn = sqlite3.connect(db_path)
conn.execute("VACUUM")
conn.close()

print(f"Database vacuumed successfully: {db_path}")
