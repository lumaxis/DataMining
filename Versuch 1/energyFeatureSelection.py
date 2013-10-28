# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 12:13:04 2013

@author: lukas
"""

import pandas as pd
from sklearn import feature_selection as fs
#from matplotlib import pyplot as plt

#read csv file
df = pd.read_csv("C:\Users\lukas\Desktop\EnergyMix.csv", index_col=0)

att = df.drop(['CO2Emm','Total2009'],1)
target = df['CO2Emm']
print att.values
ch2 = fs.SelectKBest(fs.chi2)
ch2.fit(att.values,target.values)