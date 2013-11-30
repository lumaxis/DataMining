# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:44:06 2013

@author: Mathis
"""

import pandas as pd
import numpy as np
import math

"""
Loads the matrix into a dataframe
"""
def loadMatrix():
    #d = pd.read_csv('artikel-wort-matrix.csv', index_col=0)
    d = pd.read_csv('test.csv', index_col=0)
    return d

"""
Calculates the difference between A and B defined as ||A-B||^2
"""
def cost(A,B):
    cost = 0.0
    for n in np.nditer(A-B):
        p = math.pow(n,2)
        if not math.isnan(p):
            cost = cost + p
    return cost

"""
Calculate W and H for m features and it iterations
"""
def nnmf(A,m,it):
    
    # find number of words and articles
    numarticles = A.shape[0]
    numwords = A.shape[1]
    
    # create H and W with random values
    H = np.random.rand(m,numwords)
    W = np.random.rand(numarticles,m)
    
    for i in range(it):
        
        # calculate current costs
        c = cost(A,np.dot(W,H))
        
        # exit if current costs lower than 5        
        if (c<5):
            break        
        
        # W^T*A
        WtA = np.dot(np.transpose(W),A)        
        # W^T*W*H
        WtWH = np.dot(np.dot(np.transpose(W),W),H)             
        
        # calculate new H
        H = (WtA/WtWH)*H
        
        # A*H^T
        AHt = np.dot(A,np.transpose(H))        
        # W*H*H^T
        WHHt = np.dot(np.dot(W,H),np.transpose(H))          
        
        # calculate new W
        W = (AHt/WHHt)*W
         
    return W,H
            
"""
Expects W, H, the article-titles in a list and all words in a list and prints
the result
numWordsPerFeature and numFeaturesPerItem are customization-options that allow
the user to set the number of words that form a feature and the number of features
that should be displayed for every article
"""
def showfeatures(W,H,titlevec,wordvec,numWordsPerFeature=6,numFeaturesPerItem=3):
    
    # find words that form a feature (6 per feature)
    tmp = [[(v,w)for w,v in zip(wordvec,f)] for f in H]
    for f in tmp:
        f.sort()
        f.reverse()
    # features contains a list per feature that lists all words that
    # form the feature
    features = [[v[1] for v in f[:numWordsPerFeature]] for f in tmp]
    
    # find features that are most present in each article
    tmp = [[(v,f)for f,v in zip(range(len(features)),a)] for a in W]
    for a in tmp:
        a.sort()
        a.reverse()
    # articleFeatures contains a list per article that lists the best matching
    # 3 features for each article
    articleFeatures = [[v[1] for v in a[:numFeaturesPerItem]] for a in tmp]
    
    # print result
    print "Es lassen sich folgende %d Merkmale definierten:" % len(features)
    for i,f in zip(range(len(features)),features):
        print "Merkmal %d: %s" % (i, f)
    print "\n"
    print "Den Artikeln lassen sich diese Merkmale wie folgt zuordnen:"
    for a,f in zip(titlevec,articleFeatures):
        print "%s: %s" % (a,f)
    
m = loadMatrix()
W,H = nnmf(m.values,4,3)
showfeatures(W,H,m.index,m.T.index)