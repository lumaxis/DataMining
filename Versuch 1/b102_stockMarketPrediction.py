# -*- coding: utf-8 -*-
"""
Created on Wed Nov 06 11:21:47 2013

@author: Mathis
"""

import pandas as pd
from sklearn import svm
import numpy as np

# config
# num values to use for fitting the classifier
PRED_TIME_DELAY = 24
# num values to predict
PRED_COUNT = 50
# num training-sets
PRED_TRAINING_SETS = 650
# num days to display  before prediction
DISPLAY_BEFORE_PRED = 30

# import data
data = pd.read_csv('effectiveRates.csv', index_col=0)

# plot 5 stock rates
dataToPlot = data.drop(['PEP','NAV','GSK','MSFT','KMB','R','SAP','GS','CL','WAG','WMT','GE','SNE','PFE','AMZN','MAR','NVS','KO','MMM','CMCSA','SNY','IBM','CVX','WFC','DD','CVS','TOT','CAT','CAJ','BAC','AIG','TWX','HD','TXN','KFT','VLO','F','CVC','TM','PG','LMT','K','HMC','GD','HPQ','DELL','MTU','XRX','YHOO','XOM','JPM','MCD','CSCO','NOC','UN'],1)
#dataToPlot.plot()

# generate cylic data where predData[dataset][0..23] is the training-data
# and predData[dataset][24] is the value to be trained
trainData = np.zeros((PRED_TRAINING_SETS,(PRED_TIME_DELAY+1)))
for i in range(PRED_TRAINING_SETS):
    t = data['YHOO']
    trainData[i]=t[range(i,i+PRED_TIME_DELAY+1)]

# train svr using the generated data
clf = svm.SVR()
clf.fit(trainData[:,0:PRED_TIME_DELAY], trainData[:,PRED_TIME_DELAY:25].ravel())
svm.SVR(C=600, epsilon=0.6)

# index of first value to predict
predIndex = PRED_TRAINING_SETS+PRED_TIME_DELAY-1

# gen array with PRED_TIME_DELAY elements before predIndex
predData = data['YHOO'][predIndex-PRED_TIME_DELAY:predIndex].values

# predict PRED_COUNT values
for it in range(PRED_COUNT):
    res = clf.predict(predData[len(predData)-PRED_TIME_DELAY:len(predData)])
    predData = np.append(predData,[res])
    
# extract the predicted values and associate them with dates
prediction = pd.DataFrame(data=predData[len(predData)-PRED_COUNT:len(predData)], columns=['YHOO_PRED'], index=data.index[predIndex:predIndex+PRED_COUNT])

# merge and plot results
dataYahoo = pd.DataFrame(data=data['YHOO'],columns=['YHOO'],index=data.index)
dataYahoo = dataYahoo.join(prediction, how='outer')
dataYahoo[predIndex-DISPLAY_BEFORE_PRED:len(dataYahoo.index)].plot()