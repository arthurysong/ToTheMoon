import pandas as pd
import finplot as fplt
from config.params import KLINES_BEFORE, TOTAL_KLINES

def plot_one_set(set):
  """accept a string set that contains x klines and plot candlesticks for those klines
  
  use to analyze a single set of nn data
  marks entry point and labels growth over last 10 klines"""

  # restructure set
  kline_array = set.split(" ")
  divided_klines = [kline_array[i:i + 7] for i in range(0, len(kline_array), 7)]

  df = pd.DataFrame(map_kline_arr_to_dicts(divided_klines))
  df = df.rename(columns={'open_time': 'time'})

  ax, ax2 = fplt.create_plot('BTCUSD', rows=2)
  candles = df[['time','open','close','high','low']]

  entry_pos = KLINES_BEFORE
  last_pos = TOTAL_KLINES - 1
  # mark our potential entry point
  df['start'] = None
  df.at[entry_pos, 'start'] = df.at[entry_pos, 'open']
  fplt.plot(df['time'], df['start'], ax=ax, color='#5ed', style='^', legend='entry point')
  
  # add line from entry to end of 10 points
  fplt.add_line(df.loc[entry_pos, 'time':'open'], df.loc[[last_pos], ['time', 'close']].loc[last_pos], color="#bbb", style="--")

  # add text that displays growth over last 10 klines
  last_close = df.at[last_pos, 'close']
  first_open = df.at[entry_pos, 'open']
  # print('last_close', last_close)
  # print('last_close', first_open)
  growth_of_last_10 = round(((last_close - first_open) / first_open) * 100, 2)
  fplt.add_text(df.loc[entry_pos, 'time':'open'], f'{growth_of_last_10}%', color="#000")

  # plot
  fplt.candlestick_ochl(candles, ax=ax)
  fplt.show()

def map_kline_arr_to_dicts(klines):
  def to_dict(arr):
    dict = {}
    dict["open_time"] = int(arr[0])
    dict["open"] = float(arr[1])
    dict["high"] = float(arr[2])
    dict["low"] = float(arr[3])
    dict["close"] = float(arr[4])

    return dict

  return list(map(to_dict, klines))


def plot_klines(klines):
  """accept array of kline strs and plot candlestick charts"""

  df = pd.DataFrame(map_kline_strs_to_dicts(klines))
  print("df", df)
  df = df.rename(columns={'open_time': 'time'})

  ax, ax2 = fplt.create_plot('BTCUSD', rows=2)
  candles = df[['time','open','close','high','low']]

  fplt.candlestick_ochl(candles, ax=ax)
  fplt.show()
  

def map_kline_strs_to_dicts(klines):
  def to_dict(str):
    values = str.split(' ')
    dict = {}
    dict["open_time"] = int(values[0])
    dict["open"] = float(values[1])
    dict["high"] = float(values[2])
    dict["low"] = float(values[3])
    dict["close"] = float(values[4])

    return dict

  return list(map(to_dict, klines))
