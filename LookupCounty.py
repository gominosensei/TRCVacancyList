'''
Figure out the county based on the query string in a Google Maps URL
Created on Mar 20, 2014
@author: michael donnelly
'''

from pygeocoder import Geocoder # docs at https://bitbucket.org/xster/pygeocoder/wiki/Home
# Google geocoding API docs at https://developers.google.com/maps/documentation/geocoding/?csw=1#GeocodingRequests

def findCounty(mapUrl):
    # Try to get the query string from the Google Maps URL
    try:
        address = mapUrl.split('?q=')[1]
    except IndexError:
        return ''

    # Geocode the address
    try:        
        geocode = Geocoder.geocode(address)
    except:
        return''

    # In the Google geocoding API, county is in results.administrative_area_level_2
    county = geocode.administrative_area_level_2
    print(geocode.raw)
    return county.split(' ')[0]

    

print(Geocoder.geocode('1141 E Johnson St, Madison WI').raw)
