# -*- coding: utf-8 -*-
'''
Created on Mar 17, 2014

@author: mdonnell

http://www.crummy.com/software/BeautifulSoup/bs4/doc/

# bedrooms
price
contact #
Date available
address
region
utilities
amenities
description

'''

import re
import urllib.request
from bs4 import BeautifulSoup


bedrooms=''
price=''
phone=''
address=''
utilities=''
laundry=''
parking=''
description=''

area=''
dogsAllowed=False
catsAllowed=False
noSmoking=False

html_doc = '<h2 class="postingtitle"><span class="star v"></span>$990 / 3br - 1275ft - Large 3 BR apt off Aberg (1821 Spohn)</h2><div class="mapAndAttrs"><div class="mapbox"><div id="map" data-latitude="43.117073" data-longitude="-89.361200" class="leaflet-container leaflet-fade-anim" tabindex="0"><div class="leaflet-map-pane" style="-webkit-transform: translate3d(0px, 0px, 0px);"><div class="leaflet-tile-pane"><div class="leaflet-layer"><div class="leaflet-tile-container"></div><div class="leaflet-tile-container leaflet-zoom-animated"><img class="leaflet-tile leaflet-tile-loaded" src="//map6.craigslist.org/t06/14/4124/6012.png" style="height: 256px; width: 256px; left: -135px; top: -125px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map7.craigslist.org/t06/14/4125/6012.png" style="height: 256px; width: 256px; left: 121px; top: -125px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map7.craigslist.org/t06/14/4124/6013.png" style="height: 256px; width: 256px; left: -135px; top: 131px;"><img class="leaflet-tile leaflet-tile-loaded" src="//map8.craigslist.org/t06/14/4125/6013.png" style="height: 256px; width: 256px; left: 121px; top: 131px;"></div></div></div><div class="leaflet-objects-pane"><div class="leaflet-shadow-pane"><img src="//www.craigslist.org/images/map/marker-shadow.png" class="leaflet-marker-shadow leaflet-zoom-animated" style="margin-left: -12px; margin-top: -41px; width: 41px; height: 41px; -webkit-transform: translate3d(140px, 130px, 0px);"></div><div class="leaflet-overlay-pane"></div><div class="leaflet-marker-pane"><img src="//www.craigslist.org/images/map/marker-icon.png" class="leaflet-marker-icon leaflet-zoom-animated leaflet-clickable" tabindex="0" style="margin-left: -12px; margin-top: -41px; width: 25px; height: 41px; -webkit-transform: translate3d(140px, 130px, 0px); z-index: 130;"></div><div class="leaflet-popup-pane"></div></div></div><div class="leaflet-control-container"><div class="leaflet-top leaflet-left"><div class="leaflet-control-zoom leaflet-bar leaflet-control"><a class="leaflet-control-fullscreen leaflet-bar-part leaflet-bar-part-top" href="#" title="Toggle Full Screen"></a><a class="leaflet-control-zoom-in leaflet-bar-part " href="#" title="Zoom in"></a><a class="leaflet-control-zoom-out leaflet-bar-part leaflet-bar-part-bottom" href="#" title="Zoom out"></a></div></div><div class="leaflet-top leaflet-right"></div><div class="leaflet-bottom leaflet-left"></div><div class="leaflet-bottom leaflet-right"><div class="leaflet-control-attribution leaflet-control"> craigslist - Map data  <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a></div></div></div></div><div class="mapaddress">1821 Spohn Ave</div><p class="mapaddress"><small>(<a target="_blank" href="https://maps.google.com/?q=loc%3A+%31%38%32%31+Spohn+Ave+Madison+WI+US">google map</a>)(<a target="_blank" href="http://maps.yahoo.com/maps_result?addr=%31%38%32%31+Spohn+Ave&amp;csz=Madison+WI&amp;country=US">yahoo map</a>)</small></p></div><p class="attrgroup"><span><b>3</b>BR / <b>1</b>Ba</span> <span><b>1275</b>ft<sup>2</sup></span> <span>apartment</span><br><span>laundry in bldg</span> <span>off-street parking</span><br><span>cats are OK - purrr</span> <span>dogs are OK - wooof</span></p></div>'

url = 'http://madison.craigslist.org/apa/4358168647.html'
url = 'http://madison.craigslist.org/apa/4379291341.html'
url = 'http://madison.craigslist.org/apa/4376503977.html'
url = 'http://madison.craigslist.org/apa/4360252140.html'
url = 'http://madison.craigslist.org/apa/4368114137.html'
url = 'http://madison.craigslist.org/apa/4354279835.html'
'''url = 'http://madison.craigslist.org/apa/4361869710.html'''
url = 'http://madison.craigslist.org/apa/4368134058.html'
url = 'http://madison.craigslist.org/apa/4358145929.html'
page = urllib.request.urlopen(url)

soup = BeautifulSoup(page)
postingbody = soup.find('section',id='postingbody').get_text()

'''print(soup.prettify())'''


''' Price and # of Bedrooms '''
postingtitle = soup.find('h2','postingtitle').get_text()
price = postingtitle.split()[0]
bedrooms = postingtitle.split()[2]


''' Address '''
try:
    address = soup.find('div','mapaddress').get_text()
except AttributeError:
    pass


''' Contact phone number '''
try:
    phonePattern = re.compile(r'''
                    # don't match beginning of string, number can start anywhere
        (\d{3})     # area code is 3 digits (e.g. '800')
        \D+         # optional separator is any number of non-digits
        (\d{3})     # trunk is 3 digits (e.g. '555')
        \D+         # optional separator
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        ''', re.VERBOSE)
    phone = phonePattern.search(postingbody).group(0).split('\n')[0]
except AttributeError:
    pass

'''print(postingbody)'''

attrgroup = soup.find('p','attrgroup')
for span in attrgroup.find_all('span'):
    attribute = span.get_text()    
    if 'ft2' in attribute: 
        area = attribute 
    elif 'laundry' in attribute or 'w/d' in attribute:
        laundry = attribute
    elif 'parking' in attribute or 'garage' in attribute or 'carport' in attribute:
        parking = attribute
    elif 'purrr' in attribute:
        catsAllowed = True
    elif 'wooof' in attribute:
        dogsAllowed = True
    elif 'no smoking' in attribute:
        noSmoking = True
    elif 'BR' in attribute:
        bedrooms = attribute
    else:
        '''print (attribute)'''




print('#BR,PRICE,CONTACT,DESCRIPTION,ADDRESS') 


amenities = []
if parking:
    amenities.append(parking)
if laundry:
    amenities.append(laundry)
if dogsAllowed:
    amenities.append('dogs allowed')
if catsAllowed:
    amenities.append('cats allowed')

bedrooms = bedrooms.split('BR')[0]
description = "Amenities include: " + '; '.join(amenities)

row = [bedrooms, price, phone, description, address]
print(",".join(row))


'''print("bedrooms:",bedrooms)
print("price:",price)
print("phone:",phone)
print("address: ",address)
print("utilities: ",utilities)
print("laundry: ",laundry)
print("parking: ",parking)

print()
print("area: ",area)
if dogsAllowed:
    amenities.append('dogs allowed')
    print("dogs are allowed")
    
print(amenities)'''