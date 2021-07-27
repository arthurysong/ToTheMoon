from config.params import KLINES_AFTER, KLINES_BEFORE, PERCENT_MOVEMENT_THRESHOLD

def raw_to_nn_data(str):
  klines_arr = str.split('\n')
  
  def without_open_time(str):
    kline_arr = str.split(' ')
    kline_arr = kline_arr[1:]
    return ' '.join(kline_arr)

  klines_arr_without_open_times = list(map(without_open_time, klines_arr))

  nn_str = "\n".join(grouped_sets_to_labeled_data(sets_to_grouped_sets(klines_arr_without_open_times)))

  return nn_str

def grouped_sets_to_labeled_data(unlabled_kline_sets):
  """take n sets of X klines (array) and return labeled sets (array)"""

  labeled_sets = []
  for set in unlabled_kline_sets:

    last_length = KLINES_AFTER * 6
    last_klines = set.split(" ")[-last_length:] 

    # get open from first and close from last 
    # get total price movement
    # and it should be > 1%
    first_open = float(last_klines[0])
    last_close = float(last_klines[-3])
    price_movement = (last_close - first_open) / first_open

    buy_sell_or_hold = None
    if price_movement > PERCENT_MOVEMENT_THRESHOLD:
      buy_sell_or_hold = "1" # buy
    elif price_movement < -PERCENT_MOVEMENT_THRESHOLD:
      buy_sell_or_hold = "0" # sell
    else:
      buy_sell_or_hold = "2" # hold

    all_but_last_klines = set.split(" ")[0:-last_length]
    all_but_last_klines.extend([str(first_open), buy_sell_or_hold])

    labeled_sets.append(" ".join(all_but_last_klines))
  
  return labeled_sets


# def to_grouped_sets_no_timestamps(klines):
#   list(map(lambda x: x[1:-1], klines))

def sets_to_grouped_sets(klines):
  """accept x amount of klines and return sets of X points
  
  klines is an array of kline strings
  return is an array of string (which rep X sets)"""

  num_of_klines_for_set = KLINES_BEFORE + KLINES_AFTER
  # 720 klines
  # 672 (7 days) before
  # 48 (.5 day) ahead
  sum_list = []


  # we're going to have list
  # start at i = 0 
  # get groups of num_of_klines_for_set
  # 

  # if array = [1 2 3 4 5]
  # and we want groups of 2
  # we start at 0 and go to length - 2


  # groups of 3
  # i = 0 to length - 3


  i = 0
  while i < len(klines) - num_of_klines_for_set:
    sum_list.append(' '.join(klines[i:i+num_of_klines_for_set]))
    i += 1

  return sum_list
  # i = 1
  # while i < num_of_klines_for_set - 1:
  #   print(f'grouping day + {i}')
  #   list2 = klines[i:]

  #   for (item1, item2) in zip(list1, list2):
  #     sum_list.append(item1 + " " + item2)

  #   # update for next iteration
  #   list1 = sum_list
  #   sum_list = []
  #   i += 1
  # print('bubbles')
  # print(len(klines))
  # list2 = klines[1:]

  # for (item1, item2) in zip(list1, list2):
  #   sum_list.append(item1 + " " + item2)

  # update for next iteration
  # list1 = sum_list

  # return sum_list
