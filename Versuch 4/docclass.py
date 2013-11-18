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
    calculates the propability that a given word f belongs to category cat
    '''
    def fprob(self,f,cat):
        
        