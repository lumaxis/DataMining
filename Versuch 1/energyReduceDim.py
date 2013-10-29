# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 10:25:59 2013

@author: lukas
"""

import pandas as pd
from sklearn.manifold import Isomap
from matplotlib import pyplot as plt

#read csv file
df = pd.read_csv("EnergyMix.csv", index_col=0)

#create list with dataframe indices
df_indices = df.index.tolist()

#create array only with energy values
array = df.values[:,0:5]

#create isomap and use it on array
imap = Isomap()
X = imap.fit_transform(array)

#plot data
plt.plot(X[:,0],X[:,1],'.')
for z in range(len(df_indices)):
    plt.text(X[z,0], X[z,1], str(df_indices[z]))
plt.show()
