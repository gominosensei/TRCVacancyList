'''
Try to find the county where an address is
Created on Mar 20, 2014
@author: michael donnelly
'''

#from pygeocoder import Geocoder
import Geocoder

results = Geocoder.geocode('1141 E Johnson St, Madison WI')
print(results[0].coordinates)
print(results[0])
