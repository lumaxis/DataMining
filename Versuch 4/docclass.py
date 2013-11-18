# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:13:25 2013

@author: Mathis
"""

'''
splits the given doc into lowercase words
'''
def getwords(doc):
    # maximum an minimum length of words that should be handled
    maxlength = 25
    minlength = 3    
    
    sep = ['.',',','?','!',';','"','\'',':']
    res = {}
    for s in sep:
        doc = doc.replace(s, ' ')
    doc = doc.split(' ')
    for w in doc:
        if len(w) in range(minlength,maxlength+1):
            res[w.lower()] = 1
    return res
    

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
        self.getfeatures = getwords


    def incf(self,f,cat):
        if self.fc.has_key(f) == False:
            self.fc[f] = {'good':0, 'bad':0}
        self.fc[f][cat] =+ 1

    def incc(self,cat):
        self.cc[cat] =+ 1

    '''
    calculates the probability that a given word f belongs to category cat
    '''
    def fprob(self,f,cat):
        return self.fc[f][cat]/self.cc[cat]

    def fcount(self,f,cat):
        return self.fc[f][cat]


    def catcount(self, cat):
        return self.cc[cat]

    def totalcount(self):
        return sum(self.cc.values())

    def train(self,item,cat):
        features = self.getfeatures(item)
        for word in features:
            self.incf(self,word,cat)
        self.incc(self,cat)


    '''
    calculates the same propability as fprob but corrects extrem values that
    may occur if a word does not occur often in training data'''
    def weightedprob(self,f,cat):
        # the probability to return if f did not occur yet in training-data

        initprob = 0.5
        cnt = self.fc[f]['good']+self.fc[f]['bad']
        return (initprob+cnt*self.fprob(f,cat))/(1+cnt)

    def prob(self,item,cat):
        result = 1
        for w in item:
            result = result * self.weightedprob(self,w,cat)


        return result * self.catcount(self,cat) / self.totalcount()
