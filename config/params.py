KLINES_BEFORE = 672 # 7 days
KLINES_AFTER = 48 # half day
# set will span over 7 and a half days.
TOTAL_KLINES = KLINES_BEFORE + KLINES_AFTER

PERCENT_MOVEMENT_THRESHOLD = 0.01
KLINES_INTERVAL = 900
SET_INTERVAL = 604800
# SET_INTERVAL = 648000 # SET_INTERVAL is the total seconds of the time frame we're looking at..
START_TIMESTAMP = 1569973500

# earliest trade recorded for btcusd is 1569973531.07181
# lets use first kline as 1569973500
