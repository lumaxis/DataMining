# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 19:16:07 2013

@author: mathis
"""

import pandas
from pymaps import Map, PyMap, Icon

# import data
data = pandas.read_csv('EnergyMixGeoClustered.csv', index_col=0)

# prepare map
tmap = Map()
tmap.zoom = 2

# prepare icons
iconRed = Icon('iconRed')
iconRed.image = "http://labs.google.com/ridefinder/images/mm_20_red.png"
iconRed.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png"
iconBlue = Icon('iconBlue')
iconBlue.image = "http://labs.google.com/ridefinder/images/mm_20_blue.png"
iconBlue.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png"
iconGreen = Icon('iconGreen')
iconGreen.image = "http://labs.google.com/ridefinder/images/mm_20_green.png"
iconGreen.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png"
iconYellow = Icon('iconYellow')
iconYellow.image = "http://labs.google.com/ridefinder/images/mm_20_yellow.png"
iconYellow.shadow = "http://labs.google.com/ridefinder/images/mm_20_shadow.png"

# create points
for x, row in data.T.iteritems():
    text = 'Oil: %.1f<br>Gas: %.1f<br>Coal: %.1f<br>Nuclear: %.1f<br>Hydro: %.1f<br>Total2009: %.1f<br>CO2Emm: %.1f'
    text = text % (row['Oil'], row['Gas'], row['Coal'], row['Nuclear'], row['Hydro'], row['Total2009'], row['CO2Emm'])
    if (row['Cluster']==1):
        icon = iconRed.id
    if (row['Cluster']==2):
        icon = iconBlue.id
    if (row['Cluster']==3):
        icon = iconGreen.id
    if (row['Cluster']==4):
        icon = iconYellow.id
    point = (row['Lat'], row['Long'], text, icon)
    tmap.setpoint(point)


# create googlemap
gmap = PyMap(key='AIzaSyDuqqx9gOVezHby8srNZJBWY3WGgonBKvw', maplist=[tmap])
gmap.addicon(iconGreen)
gmap.addicon(iconYellow)
gmap.addicon(iconBlue)
gmap.addicon(iconRed)

# output
open('EnergyCluster.html','wb').write(gmap.showhtml())