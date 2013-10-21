# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:10:04 2013

@author: mathis
"""

import pandas
import sklearn.preprocessing as sk
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as sd
import scipy.cluster.hierarchy as ch

# import and ignore 'Total2009'-column
data = pandas.read_csv('EnergyMix.csv', index_col=0)
data = data.drop('Total2009',1)
data = data.drop('CO2Emm',1)
values = data.values

# standardize each attribute
values = sk.scale(values, with_mean=0)

# compute distance matrix
dist = sd.pdist(values, metric='correlation')

# compute clusters
cluster = ch.linkage(dist)

ch.dendrogram(cluster)
plt.show()