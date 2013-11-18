# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:13:25 2013

@author: Mathis
"""

def getwords():
    return []

class Classifier:
    
    fc = {}
    cc = {}
    getfeatures = getwords
    
    def __init__ (self):
        fc = {}
        cc = {'good':0, 'bad':0}


    def incf(self,f,cat):
        if self.fc.has_key(f) == False:
            self.fc[f] = {'good':0, 'bad':0}
        self.fc[f][cat] =+ 1

    def incc(self,cat):
        self.cc[cat] =+ 1

    def fcount(self,f,cat):
        return self.fc[f][cat]

    def catcount(self, cat):
        return self.cc[cat]

    def totalcount(self):
        return sum(self.cc.values())

    def train(self,item,cat):
        features = self.getfeatures(item)
        for word in features:
            self.incf(self,word,)

