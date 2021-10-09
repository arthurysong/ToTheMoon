from peewee import *
from dotenv import load_dotenv
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from models.kline import Kline

load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
db = MySQLDatabase('ttm', user=DB_USER, password=DB_PASSWORD, host=DB_ENDPOINT, port=3306)

db.connect()

db.create_tables([Kline])