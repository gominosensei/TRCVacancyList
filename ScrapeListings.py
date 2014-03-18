'''
Created on Mar 17, 2014
@author: michael donnelly
'''

import urllib.request
from bs4 import BeautifulSoup
from ParseListing import parseListing

apa = 'http://madison.craigslist.org/apa/'
urlbase = 'http://madison.craigslist.org'

page = urllib.request.urlopen(apa)
soup = BeautifulSoup(page)

print('#BR,PRICE,CONTACT,DESCRIPTION,ADDRESS,URL')

count=0
for row in soup.find_all('p','row'):
    link = row.find('a')
    url = urlbase + link['href']
    count += 1
    if count>10:
        break
    print(parseListing(url))

'''url = 'http://madison.craigslist.org/apa/4380412363.html'
print(parseListing(url))'''