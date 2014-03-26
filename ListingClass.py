'''
Download a craigslist housing post and extract data for the Tenant Resource Center Vacancy List
Created on Mar 17, 2014
@author: michael donnelly
'''

import re
import urllib.request
from bs4 import BeautifulSoup  # docs at http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def findPhone(text):
    # RegEx Patterns
    phonePattern = re.compile(r'''
        (\d{3})     # area code is 3 digits (e.g. '800')
        \D{0,2}     # optional 1 or 2 character separator
        (\d{3})     # prefix is 3 digits (e.g. '555')
        \D?         # optional 1 character separator
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        ''', re.VERBOSE)

    phonePatternNoAreaCode = re.compile(r'''
        (\d{3})     # prefix is 3 digits (e.g. '555')
        -           # require literal dash to avoid false positives
        (\d{4})     # rest of number is 4 digits (e.g. '1212')
        ''', re.VERBOSE)

    # Search first with then without area code
    try:
        phone = phonePattern.search(text)
    except AttributeError:
        try:
            phone = phonePatternNoAreaCode.search(text)
        except AttributeError:
            phone = ''
    # Format for display with dashes
    try:
        phone = '-'.join(phone.groups())
    except AttributeError:
        phone = ''
        
    return(phone)

class Listing:
	price = ''
	housingType = ''
	address = ''
	phone = ''
	bedrooms=''
	laundry=''
	parking=''    
	dogsAllowed=False
	catsAllowed=False
	noSmoking=False    
	area = ''
	mapUrl = ''
	listingUrl = ''
		
		
	def description():
		return 'desc'

	def bedroomColumn():
		return 'beds'

	def representation(self):
		return ('Listing(\n     price=%s\n     housingType=%s\n     address=%s\n     phone=%s\n     bedrooms=%s\n     laundry=%s\n     parking=%s\n     dogsAllowed=%s\n     catsAllowed=%s\n     noSmoking=%s\n     area=%s\n     mapUrl=%s\n     listingUrl=%s\n)' % (repr(self.price), repr(self.housingType), repr(self.address), repr(self.phone), repr(self.bedrooms), repr(self.laundry), repr(self.parking), repr(self.dogsAllowed), repr(self.catsAllowed), repr(self.noSmoking), repr(self.area), repr(self.mapUrl), repr(self.listingUrl)))
	
	def __str__(self):
		return(self.representation())
		
	def __repr__(self):
		return(self.representation())

	def __init__(self, url):
		print ('initialized',url)
		self.listingUrl = url
		# Retrieve page and extract contents 
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page)    
			postingtitle = soup.find('h2','postingtitle').get_text()
			postingbody = soup.find('section',id='postingbody').get_text()
			extension = url.split('/')[3]
		except AttributeError:
			print('whoops')
			self = None
			

def parseListing(url):
    # Retrieve page and extract contents 
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)    
        postingtitle = soup.find('h2','postingtitle').get_text()
        postingbody = soup.find('section',id='postingbody').get_text()
        extension = url.split('/')[3]
    except AttributeError:
        return ''
    
    # Price 
    price = postingtitle.split()[0]
    try:
        price.split('$')[1]
    except IndexError:
        price='' 

    # Address 
    try:
        address = soup.find('div','mapaddress').get_text()
        address = address.replace(',', ' ')
    except AttributeError:
        address = ''
    
    # Contact phone number
    try:
        replylink = url.replace(extension, 'reply').replace('.html','')
        replypage = str(urllib.request.urlopen(replylink).read())
        phone = findPhone(replypage)
    except AttributeError:
        try:
            phone = findPhone(postingbody)
        except AttributeError:
            phone = ''    
    
    # Go through block of discrete attributes        
    bedrooms=''
    laundry=''
    parking=''
    
    dogsAllowed=False
    catsAllowed=False
    noSmoking=False    
    
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
            bedrooms = attribute.split('BR')[0]
        else:
            '''print (attribute)'''
    
    # Make amenities from#parking, laundry, pets, and smoking 
    amenities = []
    if parking:
        amenities.append(parking)
    if laundry:
        amenities.append(laundry)
    if dogsAllowed and catsAllowed:
        amenities.append('cats & dogs allowed')
    elif dogsAllowed: 
        amenities.append('dogs allowed')
    elif catsAllowed:
        amenities.append('cats allowed')
    if noSmoking:
        amenities.append('no smoking')
                
    if len(amenities)>0:
        description = "Amenities include: " + '; '.join(amenities)
        description = description.replace(',', ' ')
    else:
        description = ''
        
    # Region
    try:
        mapaddress = soup.find('p','mapaddress')
        mapLink = mapaddress.find('a')['href']
    except AttributeError:
        mapLink = ''
        
    # Type of housing
    if extension == 'roo':
        bedrooms = 'shared(0)'
    elif extension == 'sub':
        bedrooms = 'sublet(' + bedrooms + ')'
    
    # Return discrete data from the listing       
    row = [bedrooms, price, phone, description, address, mapLink, postingbody, url]
    return row

	
print('hello')
url = 'http://madison.craigslist.org/apa/4393689706.html'
mylisting = Listing(url)
print(mylisting.price)
mylisting.bedrooms = 2
print(mylisting)