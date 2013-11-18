# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:13:25 2013

@author: Mathis
"""

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
    
    def __init__ (self):
        self.fc = {}
        self.cc = {'good':0, 'bad':0}
    
    '''
    calculates the probability that a given word f belongs to category cat
    '''
    def fprob(self,f,cat):
        return self.fc[f][cat]/self.cc[cat]
    
    '''
    calculates the same propability as fprob but corrects extrem values that
    may occur if a word does not occur often in training data
    '''
    def weightedprob(self,f,cat):
        # the probability to return if f did not occur yet in training-data
        initprob = 0.5
        
        cnt = self.fc[f]['good']+self.fc[f]['bad']
        return (initprob+cnt*self.fprob(f,cat))/(1+cnt)