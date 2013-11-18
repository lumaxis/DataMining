# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:13:25 2013

@author: Mathis
"""

def getwords():
    return []

class Classifier:
    
    '''
    a dictionary like this:
    {
        'wort1': {'good': x, 'bad': y}
        'wort2': {'good': z, 'bad': a}
        ...
        'wortn': {'good': b, 'bad': c}
    }
    '''
    fc = {}
    
    '''
    a dictionary that counts the number documents in both categories
    '''
    cc = {}
    getfeatures = getwords
    
    def __init__ (self):
        self.fc = {}
        self.cc = {'good':0, 'bad':0}


    def incf(self,f,cat):
        if self.fc.has_key(f) == False:
    
    '''
    calculates the probability that a given word f belongs to category cat
    '''
            self.fc[f] = {'good':0, 'bad':0}
        self.fc[f][cat] =+ 1

    def incc(self,cat):
        self.cc[cat] =+ 1
    def fprob(self,f,cat):
        return self.fc[f][cat]/self.cc[cat]

    def fcount(self,f,cat):
        return self.fc[f][cat]
    
    '''

    def catcount(self, cat):
    calculates the same propability as fprob but corrects extrem values that
    may occur if a word does not occur often in training data
        return self.cc[cat]

    def totalcount(self):
    '''
        return sum(self.cc.values())

    def train(self,item,cat):
        features = self.getfeatures(item)
    def weightedprob(self,f,cat):
        # the probability to return if f did not occur yet in training-data
        for word in features:
            self.incf(self,word,cat)
        initprob = 0.5
        self.incc(self,cat)
        
        cnt = self.fc[f]['good']+self.fc[f]['bad']
        return (initprob+cnt*self.fprob(f,cat))/(1+cnt)

