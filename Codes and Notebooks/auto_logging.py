# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 20:34:20 2020

@author: esath
"""
from kiteconnect import KiteConnect
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import re
import datetime
import pandas as pd
import time
from pymongo import MongoClient
from kiteconnect import KiteTicker
import logging


# print(driver.title)
kite = KiteConnect(api_key="9rdztbl29kf1atay")

url = kite.login_url()
driver = webdriver.Firefox()
driver.get(url)
print(driver.title)
if driver.title == "Kite - Zerodha's fast and elegant flagship trading platform":

    # username = driver.find_element(By.XPATH, '//*[@id="container"]/div/div/div[2]/form/div[1]/input')
    # password = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/input[@placeholder = 'Password']")
    # login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[4]/button")
    # username.clear()
    # password.clear()
    time.sleep(5)
    actions = ActionChains(driver)
    # username.send_keys('XK0732')
    # password.send_keys("Sathvik_Niks89")
    # login_button.click()
    actions.send_keys('XK0732')
    actions.send_keys(Keys.TAB)
    actions.send_keys("Sathvik_Niks89")
    actions.send_keys(Keys.ENTER)
    actions.perform()
    # print(driver.current_url)

    # pin = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[2]/div/input")
    # continue_button = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/form/div[3]/button")

    # pin.clear()
    # pin.send_keys('456987')
    # continue_button.click()
    # driver.implicitly_wait(5)
    time.sleep(5)
    actions = ActionChains(driver)
    actions.send_keys('456987')
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(5)
    # driver.implicitly_wait(5)
    curr_url = driver.current_url
    driver.quit()

request_token = re.search('request_token=(.*)&',curr_url)
request_token = request_token.group(1)
request_token = request_token.split('&')

data = kite.generate_session(str(request_token[0]), api_secret="qju1lmjj868frnnn7ym883iq8yamvua9")
kite.set_access_token(data["access_token"])

## Connecting to MongoDB Server
try:
   client = MongoClient()
   print("Connected to Mongo Server successfully!!!")
except:
   print("Could not connect to MongoDB")

db = client.kiteconnect
print("Database connected")
collection = db.tick_data

# df=pd.DataFrame()

logging.basicConfig(level=logging.DEBUG)

kws = KiteTicker("9rdztbl29kf1atay", data["access_token"])

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    logging.debug("Ticks: {}".format(ticks))
    ids = collection.insert_many(ticks).inserted_ids
    print(ids)
    # for tick in ticks:
    #     print(tick)
    #     collection.insert_one(tick)
    #     # df.append(tick, ignore_index=True)
    #     # df.to_csv("test.csv")

def on_connect(ws, response):
    # Callback on successful connect.

    ws.subscribe([895745])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [895745])

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

kws.connect()



#%%
