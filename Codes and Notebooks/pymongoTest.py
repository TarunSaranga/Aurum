# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 18:31:58 2020

@author: Tharun Saranga
"""

from pymongo import MongoClient

try:
   conn = MongoClient()
   print("Connected successfully!!!")
except:
   print("Could not connect to MongoDB")

db = conn.kiteconnect
print("Database created")
collection = db.tick_data



ticks=[{'tradable': True, 'mode': 'full', 'instrument_token': 895745, 'last_price': 431.4, 'last_quantity': 25, 'average_price': 426.77, 'volume': 11502423, 'buy_quantity': 7772, 'sell_quantity': 0, 'ohlc': {'open': 434.0, 'high': 435.15, 'low': 421.3, 'close': 436.85}, 'change': -1.2475678150394975, 'last_trade_time': 'datetime.datetime(2020, 2, 18, 5, 29, 45)', 'oi': 0, 'oi_day_high': 0, 'oi_day_low': 0, 'timestamp': 'datetime.datetime(2020, 2, 18, 6, 35, 15)', 'depth': {'buy': [{'quantity': 7772, 'price': 431.4, 'orders': 27}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}], 'sell': [{'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}, {'quantity': 0, 'price': 0.0, 'orders': 0}]}}]

x=collection.insert_many(ticks)
print(x.inserted_ids)