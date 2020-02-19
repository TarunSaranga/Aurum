# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 17:57:14 2020

@author: SathvikE
"""

import logging
from kiteconnect import KiteConnect
logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="9rdztbl29kf1atay")
#%%
print(kite.login_url())
import urllib

#%%
data = kite.generate_session("0XKq1cTyYJ0fc6nJe7jWVA2tVD75dPWK", api_secret="qju1lmjj868frnnn7ym883iq8yamvua9")
kite.set_access_token(data["access_token"])
#%%
import pandas as pd
instruments = pd.read_csv('D:/Sathvik/Data/instruments_nse.csv')
token = pd.Series(instruments.instrument_token.values, index = instruments.tradingsymbol).to_dict()

#%%
import datetime
import json

days_limit = 60

def data_gen(value = '', interval = ''):
    from_date = datetime.date(2017,1,1)
    to_date = from_date + datetime.timedelta(days=days_limit)
    temp = pd.DataFrame()
    temp = temp.append(kite.historical_data(token[value],from_date, to_date, interval, continuous= 0, oi = 0))
    f_name = value + '_' + interval + '.csv'
    # with open(f_name, 'w') as json_file:
    #     json.dump(temp, json_file, indent=4, sort_keys=True,default=str)
    while to_date <= datetime.date.today()-datetime.timedelta(days=days_limit):
        
        to_date = to_date + datetime.timedelta(days=days_limit)
        from_date = from_date + datetime.timedelta(days=days_limit)
        temp = temp.append(kite.historical_data(token[value],from_date, to_date, interval, continuous= 0, oi =0))
    temp['date'] = pd.to_datetime(temp.date)
    temp = temp.sort_values(by='date')
    temp = temp.set_index("date")
    temp.to_csv(f_name)
#%%
from itertools import product
interval_lst = ['minute','3minute', '5minute', '10minute', 'day']
stock_lst = ['WIPRO', 'INFY','HCLTECH','TECHM','GAIL','JSWSTEEL','TATASTEEL','BHARTIARTL','INFRATEL','SUNPHARMA','CIPLA','NTPC','ONGC','COALINDIA','POWERGRID','BPCL','SBIN','AXISBANK','HDFCBANK','ICICIBANK','TATAMOTORS','M&M']
for val, inter in product(stock_lst, interval_lst):
    data_gen(val, inter)