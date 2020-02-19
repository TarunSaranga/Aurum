# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:59:42 2020

@author: esath
"""
import os
import glob
import pandas as pd
import talib
from tkinter import *
from tkinter import filedialog
from scipy.signal import find_peaks
import numpy as np


root = Tk()
main_dir =  filedialog.askdirectory(title =" Select Directory Containing CSV's ")
root.withdraw()

Dir_list = [item_name for item_name in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir,item_name))]
for dirs in Dir_list:
  files_dirs = os.path.join(main_dir,dirs,'*.csv')
  file_list = glob.glob(files_dirs)
  for files in file_list:
      
      df = pd.read_csv(files,index_col='date')
      #=====================================================================================================
      #Indicators
      #=====================================================================================================
      df["sma5"] = talib.SMA(df.close.values, timeperiod=5)
      df["sma10"] = talib.SMA(df.close.values, timeperiod=10)
      df["sma20"] = talib.SMA(df.close.values, timeperiod=20)
      df["emadiff"] = talib.EMA(df.close.values, timeperiod=12) - talib.EMA(df.close.values, timeperiod=26)
      u,m,l = talib.BBANDS(df.close.values,timeperiod = 14)
      df["BB"] = (u-l)/m
      fastk, fastd = talib.STOCHRSI(df.close.values, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
      df["stochrsifastk"] = fastk
      df["stochrsifastd"] = fastd
      df["ROC"] = talib.ROC(df.close.values, timeperiod=14)
      df["TrueRange"] = talib.TRANGE(df.high.values, df.low.values, df.close.values)
      df["MOM6"] = talib.MOM(df.close.values, timeperiod=6)
      df["MOM12"] = talib.MOM(df.close.values, timeperiod=12)
      df["WilliamR10"] = talib.WILLR(df.high.values, df.low.values, df.close.values, timeperiod=10)
      df["WilliamR16"] = talib.WILLR(df.high.values, df.low.values, df.close.values, timeperiod=16)
      df["ULOSC"] = talib.ULTOSC(df.high.values, df.low.values, df.close.values, timeperiod1=7, timeperiod2=14, timeperiod3=28)
      df["RSI6"] = talib.RSI(df.close.values, timeperiod=6)
      df["RSI12"] = talib.RSI(df.close.values, timeperiod=12)
      df["stochfastkdiff"] = df["stochrsifastk"] - df["stochrsifastk"].shift(1)
      df["stochfastddiff"] = df["stochrsifastd"] - df["stochrsifastd"].shift(1)
      df["avgPrice"] = (df.close - df.close.shift(1))/df.close.shift(1)
      #df["normPrice"] = (df.close - df.close[0])/df.close[0]
      df["pricediff"] = (df.close - df.low)/(df.high-df.low)
      df["sma5diff"] = (df.sma5 - df.sma5.shift(1))/df.sma5.shift(1)
      df["sma20diff"] = (df.sma20 - df.sma20.shift(1))/df.sma20.shift(1)
      df["smadiff"] = (df.sma5 - df.sma20.shift(1))/df.sma20.shift(1)
      df["pricemadiff"] = (df.close - df.sma20)/df.sma20
      
      #====================================================================================================
      #Peaks and Troughs
      #====================================================================================================
      pk = []
      tr = []
      pt = []
      peekidx,_ = find_peaks(df.close.values, prominence = 1.5)#, distance = 5 )
      troughidx,_ = find_peaks( - df.close.values, prominence = 1.5)#, distance = 5 )
      for i in range(0,len(df)):
          if(i in peekidx):
            pt.append(1)
            pk.append(1)
            tr.append(np.nan)
          elif(i in troughidx):
            pt.append(-1)
            tr.append(1)
            pk.append(np.nan)
          else:
            pt.append(0)
            tr.append(np.nan)
            pk.append(np.nan)
      df["peaks"] = pt
      
      #=====================================================================================================
      #Normalizations
      #=====================================================================================================
      df["sig_norm"] = 1/((np.exp(df.close))+1)
      df["median_norm"] = df.close/df.close.median()
      df["tanh_norm"] = 0.5 * (np.tanh(0.01 * ((df.close - df.close.mean()) / df.close.std())) + 1)
      
      #=====================================================================================================
      #Peek Future
      #=====================================================================================================
      
      peeks = [5,8,13,21,34]
      for peek in peeks:
          col_name = 'peek_'+str(peek)
          df[col_name] = df.close < (df.close.shift(-peek))
          df[col_name].replace(True, 1, inplace = True)
          df[col_name].replace(False, 0, inplace = True)
      
      #=====================================================================================================
      #Saving
      #=====================================================================================================
          
      fol = os.path.join(main_dir, dirs,'with_indicators')
      if not os.path.exists(fol):
          os.mkdir(fol)
          
      fl_name = os.path.basename(files)
      df.to_csv(os.path.join(fol,fl_name))
  