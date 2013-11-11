# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:45:11 2013

@author: Mathis
"""

import os, sys
lib_path = os.path.abspath('.')
sys.path.append(lib_path)
import pandas as pd

import pylast
import recommendations as rec

# fetches the top 20 artists for every user in group and creates a dataframe
# whith users as index and all fetched artists as columns
# each value (x,y) indicates weather the user x is has y in its top 20 artists
# (1) or not (0)
def createLastfmUserDict(group):
    userTopArtists = {}
    allBands = []
    for u in group:
        topArtists = [a.item.get_name() for a in u.get_top_artists()[0:20]]
        allBands.extend(topArtists)
        userTopArtists[u.get_name()] = topArtists
    userDict = pd.DataFrame(index = [u.get_name() for u in group], columns = allBands)
    
    #
    # TODO: can we do this more efficient??
    for u in group:
        for a in allBands:
            userDict.loc[u.get_name(),a] = 1 if (a in userTopArtists[u.get_name()]) else 0
    return userDict

# connect to lastfm network
net = pylast.get_lastfm_network()

# get artist
artist = net.get_artist('Milow')

# get 10 top fans
fans = artist.get_top_fans(10)
group = [a.item for a in fans]

# create the data-matrix and persist to csv (for performance reasons)
#d = createLastfmUserDict(group)
#d.to_csv('lastfm-data.csv')

# retrieve data from csv instead of fetching from lastfm every time
d = pd.read_csv('lastfm-data.csv', index_col=0)

print rec.topMatches(d.T.to_dict(), 'marriett', 'sim_euclid')

print rec.getRecommendations(d.T.to_dict(), 'marriett', 'sim_euclid')