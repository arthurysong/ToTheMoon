# websockets subscribe to trades and klines
# once we get 7 days worth of trades and klines
# we can start capturing a set of features
# and use our nn to predict ? 

# so each time we want to test we need to wait 7 days.. that's pretty shit.
# i need to train nn to be able to accept a smaller time frame?
# so even if 4042 features we can just feed like 100
import os
import asyncio
import websockets
# print(os.environ['BYBIT_API_KEY'])
BYBIT_API_KEY = os.environ['BYBIT_API_KEY']
BYBIT_SECRET = os.environ['BYBIT_SECRET']

async def connect():
  uri = "wss://stream.bybit.com/realtime"
  expires = time.