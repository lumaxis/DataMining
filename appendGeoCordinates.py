# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:23:25 2013

@author: mathis
"""
import urllib
import json

def geocode(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    data = urllib.urlopen(url).read()
    info = json.loads(data).get("results")[0].get("geometry").get("location")  
    #A little ugly I concede, but I am open to all advices :) '''
    return info


res = geocode("Deutschland")
print res['lat']
print res['lng']