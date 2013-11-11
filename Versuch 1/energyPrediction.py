# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

"""
Created on Fri Nov 08 17:27:14 2013

@author: lukas
"""
import pandas as pd
from sklearn.svm import SVR
from sklearn import metrics
from sklearn import cross_validation
import matplotlib.pyplot as plt

df = pd.read_csv("EnergyMix.csv", index_col=0)

#Extract CO2Emm Values
targets = df.values[0:64,6]

#Extract Energy Values
features = df.values[0:64,0:5]

#Suche nach optimalen Parametern
#==============================================================================
# min_score = 100.0
# opt_varC = 0.0
# opt_varEpsilon = 0.0
# 
# for varC in [float(j) / 10 for j in range(1, 21, 1)]: 
#     for varEpsilon in [float(i) / 100 for i in range(1,21,1)]:    
#         print "Testing with"  
#         print "varC: %2.3f" % (varC)
#         print "varEpsilon: %2.3f" % (varEpsilon)
#         eSVR = SVR(C=varC,epsilon=varEpsilon,kernel='linear')
#         scores = cross_validation.cross_val_score(eSVR,features,targets,cv=10,score_func=metrics.mean_squared_error)
#                 
#         if scores[-1] < min_score:
#             print "Better parameters found!"
#             print "varC: %2.3f" % (varC)
#             print "varEpsilon: %2.3f" % (varEpsilon)            
#             min_score = scores[-1]
#             opt_varC = varC
#             opt_varEpsilon = varEpsilon
#             
#         #print "Cross Validation scores:"
#         #print scores
#     
# print "Optimale Parameter:"
# print "C = %2.3f" % (opt_varC)
#==============================================================================
print "epsilon = %2.3f" % (opt_varEpsilon)

opt_varC = 1.9
opt_varEpsilon = 0.01

#Do cross validation
eSVR = SVR(C=opt_varC,epsilon=opt_varEpsilon,kernel='linear')
scores = cross_validation.cross_val_score(eSVR,features,targets,cv=10,score_func=metrics.mean_squared_error)

#==============================================================================
# mse = 1.0/64*np.sum((prediction-targets)**2)
# print "Mean Square Error %2.3f" % (mse)
#==============================================================================



#KFold
#==============================================================================
# KFcv = cross_validation.KFold(n=64, n_folds=10)
# for train_index, test_index in KFcv:
#     print("TRAIN:", train_index, "TEST:", test_index)
#     X_train, X_test = features[train_index], features[test_index]
#     y_train, y_test = targets[train_index], targets[test_index]
#==============================================================================

#Do epsilon-Support Vector Regression
eSVR.fit(features, targets)
print "SVR coef_:"
print eSVR.coef_
prediction = eSVR.predict(features)

# Print Prediction Error graph
#==============================================================================
# Error = prediction - targets
# plt.stem(np.arange(64),Error)
# plt.title('Prediction Error')
# plt.show()
#==============================================================================

# Calculate Mean Absolute Error
mae = metrics.mean_absolute_error(targets,prediction)
print "Mean Absolute Error %2.3f" % (mae)

#Soll/Ist Diagramm
plt.plot(prediction, prediction, 'ro', targets, targets, 'bo')
plt.show()

# Calculate SVR score
#==============================================================================
# score = eSVR.score(features, targets)
# print "SVR Score%2.3f" % (score)
#==============================================================================
