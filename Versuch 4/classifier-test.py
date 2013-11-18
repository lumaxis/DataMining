# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 11:33:13 2013

@author: Mathis
"""

import os, sys
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import docclass as d

# test-data
data = {
    'nobody owns the water': 'good',
    'the quick rabbit jumps fences': 'good',
    'buy pharmaceuticals now': 'bad',
    'make quick money at the online casino': 'bad',
    'the quick brown fox jumps': 'good',
    'next meeting is at night': 'good',
    'meeting with your superstar': 'bad',
    'money like water': 'bad'
}

cl = d.Classifier()
for t, c in data.iteritems():
    cl.train(t,c)
    
print cl.prob('the money jumps', 'good')
print cl.prob('the money jumps', 'bad')