from peewee import *
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
db = MySQLDatabase('ttm', user=DB_USER, password=DB_PASSWORD, host=DB_ENDPOINT, port=3306)

class BaseModel(Model):
  class Meta:
    database = db

class Trade(BaseModel):
  timestamp = TimestampField()
  side = TextField()
  size = IntegerField()
  price = DecimalField()
  tick_direction = TextField()
  trade_id = TextField()

db.connect()

# THIS SCRIPT WILL DROP TABLE

db.drop_tables([Trade])
db.create_tables([Trade])
