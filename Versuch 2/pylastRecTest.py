# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:27:42 2013

@author: Mathis
"""

import os, sys
lib_path = os.path.abspath('.')
sys.path.append(lib_path)

import pylast

# connect to lastfm network
net = pylast.get_lastfm_network()

# get artist
artist = net.get_artist('Milow')

# get top fans
fans = artist.get_top_fans(10)
group = [a.item for a in fans]
print group