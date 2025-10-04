import datetime
import os
import peewee

# Try Docker path first, fallback to local path
docker_db_path = '/app/data/alerts.db'
local_db_path = os.path.join(os.path.dirname(__file__), 'data', 'alerts.db')
db_path = docker_db_path if os.path.exists('/app/data') else local_db_path

data_dir = os.path.dirname(db_path)
os.makedirs(data_dir, exist_ok=True)

db = peewee.SqliteDatabase(db_path, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64  # 64MB page-cache.
})

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Alert(BaseModel):
    alert_id = peewee.CharField()
    title = peewee.CharField()
    event = peewee.CharField()
    details = peewee.CharField(null=True)
    expires = peewee.DateTimeField()
    expires_utc_ts = peewee.DoubleField()
    url = peewee.CharField()
    api_url = peewee.CharField()
    fips_codes = peewee.TextField(null=True)
    ugc_codes = peewee.TextField(null=True)
    created = peewee.DateTimeField()

    def __repr__(self):
        return self.title

if __name__ == "__main__":
    if db.is_closed():
        db.connect()
    db.create_tables([Alert,])
