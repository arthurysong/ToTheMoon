# ======= sibling imports =======
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# ======= sibling imports =======

from db.models.kline import Kline
from db.models.trade import Trade
from config.params import SET_INTERVAL
import time
# alright do some thinking here..
# 1. executed_trades need model
# so we can record all executed trades
# 2. Need ByBit APi info so we can execute trade
# - how do we execute trade @ 100% balance
# 3. deposit 500 into ByBit. 


# 3. this will be a script that gets run every 10 min? by a cron job script
# 4. get all relevant klines
# 5. get all relevant trades
# 6. get aggregates
# 7. create nn input
# 8. predict hold buy or sell using nn model
# 9. execute trade

# get klines
# do we just get last 672 klines? or get timestamps. 
# i like figuring out the timestamps of the start and end.
# and then querying klines between the two timestamps
# and also querying trade between the two timestamps
print(f'current timestamp {int(time.time())}')
print(f'7 days before timetsamp {int(time.time()) - SET_INTERVAL}')

end_timestamp = int(time.time())
start_timestamp = end_timestamp - SET_INTERVAL

klines = Kline.select().where(Kline.open_time >= start_timestamp, Kline.open_time <= end_timestamp)
print(f'length of klines = {len(klines)}')

# map each kline to ['open' 'high', 'low', 'close', 'volume', 'turnover']
# then flatten evertying
# so we should get 672 * 6


# what is the format of the input of model? 
# is it just list of values?
