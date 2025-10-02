import datetime
import os
import peewee

# Store database in data directory for better Docker volume management
DB_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'alerts.db')

db = peewee.SqliteDatabase(DB_PATH, pragmas={'journal_mode': 'wal'})

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
    db.connect()
    db.create_tables([Alert,])
