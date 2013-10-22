# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\lukas\.spyder2\.temp.py
"""
import time
import urllib, json
import pandas as pd
import numpy as np
randn = np.random.randn

df = pd.read_csv("C:\Users\lukas\Desktop\EnergyMix.csv", index_col=0)
df.plot()

#Simplified graph
#graph = df[0:4]
#graph.plot()

#Random example data instead of Google Maps
gmaps = pd.DataFrame(randn(len(df.index),2), columns=('Lat','Long'), index=df.index)
def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")  
    return info
        
df['Lat']= pd.Series(0.0, index=df.index)
df['Long']= pd.Series(0.0, index=df.index)

for row_index, row in df.iterrows():
    res = (geocode(str(row_index)))
    df.loc[row_index, ['Lat']] = res['lat']
    df.loc[row_index, ['Long']] = res['lng']
    time.sleep(1)

#Append geodata to dataframe
df.to_csv("C:\Users\lukas\Desktop\EnergyMixGeo.csv")