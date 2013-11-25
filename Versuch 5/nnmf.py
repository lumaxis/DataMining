# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:44:06 2013

@author: Mathis
"""

import pandas as pd


"""
Loads the matrix into a dataframe
"""
def loadMatrix():
    d = pd.read_csv('artikel-wort-matrix.csv', index_col=0)
    return d
    