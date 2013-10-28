# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 11:11:40 2013

@author: mathis
"""

import pandas
import matplotlib.pyplot as plt

# import and ignore 'Total2009'-column
data = pandas.read_csv('EnergyMix.csv')
data = data.drop('Total2009',1)
data = data.drop('CO2Emm',1)

# drop china because of immense coal usage
data =  data.drop(data.index[[52,53]])

# calc mean-value for each energy resource and print the results
mean = data.mean(0)
print mean

# plot data
data.boxplot()
plt.show()