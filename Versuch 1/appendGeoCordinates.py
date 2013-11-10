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

df_energy= df.iloc[0:,0:5]
df_energy.plot()

oil = df[['Oil']]
oil.plot()

gas = df[['Gas']]
gas.plot()

coal = df[['Coal']]
coal.plot()

nuclear = df[['Nuclear']]
nuclear.plot()

hydro = df[['Hydro']]
hydro.plot()


max_idx = 7
#Simplified graphs for every energy sort
df_sort = df.sort(['Oil'], ascending=False)
graph_oil = df_sort.iloc[0:max_idx,0:1]
graph_oil.plot()

df_sort = df.sort(['Gas'], ascending=False)
df_gas = df_sort.iloc[0:max_idx,1:2]
df_gas.plot()

df_sort = df.sort(['Coal'], ascending=False)
graph_coal = df_sort.iloc[0:max_idx,2:3]
graph_coal.plot()

df_sort = df.sort(['Nuclear'], ascending=False)
graph_nuclear = df_sort.iloc[0:max_idx,3:4]
graph_nuclear.plot()
 
df_sort = df.sort(['Hydro'], ascending=False)
graph_hydro = df_sort.iloc[0:max_idx,4:5]
graph_hydro.plot()


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
