# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 12:10:04 2013

@author: mathis
"""

import pandas
import sklearn.preprocessing as sk
import scipy.spatial.distance as sd
import scipy.cluster.hierarchy as ch
import matplotlib.pyplot as plt

# CONFIG
NUM_CLUSTER = 4

# import and ignore 'Total2009' and 'CO2Emm'-columns
data = pandas.read_csv('EnergyMixGeo.csv', index_col=0)
dataCopy = data
data = data.drop('Total2009',1)
data = data.drop('CO2Emm',1)
data = data.drop(['Lat', 'Long'],1)
index = data.index
values = data.values

# standardize each attribute
values = sk.scale(values, with_mean=0)

# compute distance matrix
dist = sd.pdist(values, metric='correlation')

# compute clustering
clustering = ch.linkage(dist, method='average')

# show dendrogram
ch.dendrogram(clustering, labels=index, orientation='left', leaf_font_size=6)

# select 4 clusters
cluster = ch.fcluster(clustering, t=NUM_CLUSTER, criterion='maxclust')

# add clusters to df and group by clusters
data['Cluster'] = cluster
dataGrouped = data.groupby('Cluster')

# print clusters and show statistics per cluster
plt.figure()
numplt = 411
for name, group in dataGrouped:
    group = group.drop('Cluster',1)
    plt.subplot(numplt)
    plt.plot(group.T)
    plt.xticks(range(5), group.T.index)
    numplt += 1
    print 'Cluster %d:' % (name)
    for country in group.index:
        print country
    print '\n'
plt.show()

# fix round errors in lat and long
for x, row in dataCopy.T.iteritems():
    row['Lat'] = round(row['Lat'], 6)
    row['Long'] = round(row['Long'], 6)

# append clusters and write in csv
dataCopy['Cluster'] = cluster
dataCopy.to_csv('EnergyMixGeoClustered.csv')