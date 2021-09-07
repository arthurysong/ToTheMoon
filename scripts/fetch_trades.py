
from typing import ByteString
import requests
from pprintpp import pprint
import pandas as pd
from datetime import date, timedelta
import pyarrow.feather as feather
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "../data/trades").resolve()

sdate = date(2021, 8, 11) #start date
edate = date.today()
delta = edate - sdate

for i in range(delta.days + 1):
  day = sdate + timedelta(days=i)
  
  print(day)

  url = f"https://public.bybit.com/trading/BTCUSD/BTCUSD{day}.csv.gz"
  file_path = (base_path / f"../data/trades/{day}").resolve()
  df = pd.read_csv(url)
  df.reset_index().to_feather(file_path)


