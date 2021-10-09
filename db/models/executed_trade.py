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

# we can kind of think about how we want to record for now, bybit will always have our trade records.
class ExecutedTrade(BaseModel):
#   open_time = TimestampField()
#   open = DecimalField()
#   high = DecimalField()
#   low = DecimalField()
#   close = DecimalField()
#   volume = IntegerField()
#   turnover = DecimalField()