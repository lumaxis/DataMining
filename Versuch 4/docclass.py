# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 10:13:25 2013

@author: Mathis
"""
import operator

'''
splits the given doc into lowercase words
'''
def getwords(doc):
    # maximum an minimum length of words that should be handled
    maxlength = 25
    minlength = 4
    
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

    # a dictionary that counts the number documents in both categories
    cc = {}
    

    def __init__ (self, cats):
        self.cats = cats
        self.fc = {}
        self.cc = {k:0 for k in cats}
        self.getfeatures = getwords


    def incf(self,f,cat):
        if self.fc.has_key(f) == False:
            self.fc[f] = {k:0 for k in self.cc.iterkeys()}
        self.fc[f][cat] =+ 1

    def incc(self,cat):
        self.cc[cat] =+ 1

    # calculates the probability that a given word f belongs to category cat
    def fprob(self,f,cat):
        return self.fc[f][cat]/self.cc[cat] if self.fc.has_key(f) & self.cc[cat] != 0 else 0

    def fcount(self,f,cat):
        return self.fc[f][cat]


    def catcount(self, cat):
        return self.cc[cat]

    def totalcount(self):
        return sum(self.cc.values())

    def train(self,item,cat):
        features = self.getfeatures(item)
        for word in features:
            self.incf(word,cat)
        self.incc(cat)


    '''
    calculates the same propability as fprob but corrects extrem values that
    may occur if a word does not occur often in training data'''
    def weightedprob(self,f,cat):
        # the probability to return if f did not occur yet in training-data

        initprob = 0.5
        cnt = self.fc[f][self.cats[0]]+self.fc[f][self.cats[1]] if self.fc.has_key(f) else 0
        return (initprob+cnt*self.fprob(f,cat))/(1+cnt)

    def prob(self,item,cat):
        result = 1
        item = self.getfeatures(item)
        for w in item:
            result = result * self.weightedprob(w,cat)

        return result * self.catcount(cat) / self.totalcount()

    def classify(self, item):
        catProbs = {}
        for cat in self.cats:
            catProbs[cat] = self.prob(item, cat)

        sumCatProbs = sum(catProbs.values())
        for cat in catProbs:
            catProbs[cat] = catProbs[cat]/sumCatProbs

        return max(catProbs.iteritems(), key=operator.itemgetter(1))[0]

