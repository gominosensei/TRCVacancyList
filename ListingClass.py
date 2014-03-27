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
	# Attributes
	price = ''
	housingType = ''
	address = ''
	phone = ''
	bedrooms = ''
	laundry = ''
	parking = ''    
	dogsAllowed = False
	catsAllowed = False
	noSmoking = False    
	area = ''
	mapUrl = ''
	listingUrl = ''
	listingBody = ''		
		
	# Combined output of several attributes for the description column
	def descriptionField(self):			
		# Make amenities from parking, laundry, pets, and smoking 
		amenities = []
		if self.parking:
			amenities.append(self.parking)
		if self.laundry:
			amenities.append(self.laundry)
		if self.dogsAllowed and self.catsAllowed:
			amenities.append('cats & dogs allowed')
		elif self.dogsAllowed: 
			amenities.append('dogs allowed')
		elif self.catsAllowed:
			amenities.append('cats allowed')
		if self.noSmoking:
			amenities.append('no smoking')
					
		if len(amenities)>0:
			description = "Amenities include: " + '; '.join(amenities)
			description = description.replace(',', ' ')
		else:
			description = ''
			
		return description
			
	# Combined output for the bedrooms column with the # of rooms plus the type of rental
	def bedroomsField(self):
		if self.housingType == 'roo':
			return 'shared(0)'
		if self.housingType == 'sub':
			return 'sublet(' + self.bedrooms + ')'
		return self.bedrooms

	# Legacy support - spit out the row with all the fields in order
	def row(self):				
		# Return discrete data from the listing       
		row = [self.bedroomsField(), self.price, self.phone, self.descriptionField(), self.address, self.mapUrl, self.listingBody, self.listingUrl]
		return row

	def representation(self):
		return ('Listing(\n     price=%s\n     housingType=%s\n     address=%s\n     phone=%s\n     bedrooms=%s\n     laundry=%s\n     parking=%s\n     dogsAllowed=%s\n     catsAllowed=%s\n     noSmoking=%s\n     area=%s\n     mapUrl=%s\n     listingUrl=%s\n)' % (repr(self.price), repr(self.housingType), repr(self.address), repr(self.phone), repr(self.bedrooms), repr(self.laundry), repr(self.parking), repr(self.dogsAllowed), repr(self.catsAllowed), repr(self.noSmoking), repr(self.area), repr(self.mapUrl), repr(self.listingUrl)))
		
	def __str__(self):
		return(self.representation())
		
	def __repr__(self):
		return(self.representation())

	# Instantiate the class and populate attributes based on data from the URL provided
	def __init__(self, url):
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
			
		self.listingBody = postingbody
		
		# Price 
		self.price = postingtitle.split()[0]
		try:
			self.price.split('$')[1]
		except IndexError:
			self.price='' 

		# Address 
		try:
			address = soup.find('div','mapaddress').get_text()
			self.address = address.replace(',', ' ')
		except AttributeError:
			pass
		
		# Contact phone number
		try:
			replylink = url.replace(extension, 'reply').replace('.html','')
			replypage = str(urllib.request.urlopen(replylink).read())
			self.phone = findPhone(replypage)
		except AttributeError:
			try:
				self.phone = findPhone(postingbody)
			except AttributeError:
				pass
		
		# Go through block of discrete attributes        
		attrgroup = soup.find('p','attrgroup')
		for span in attrgroup.find_all('span'):
			attribute = span.get_text()    
			if 'ft2' in attribute: 
				self.area = attribute 
			elif 'laundry' in attribute or 'w/d' in attribute:
				self.laundry = attribute
			elif 'parking' in attribute or 'garage' in attribute or 'carport' in attribute:
				self.parking = attribute
			elif 'purrr' in attribute:
				self.catsAllowed = True
			elif 'wooof' in attribute:
				self.dogsAllowed = True
			elif 'no smoking' in attribute:
				self.noSmoking = True
			elif 'BR' in attribute:
				self.bedrooms = attribute.split('BR')[0]
    
		# Region
		try:
			mapaddress = soup.find('p','mapaddress')
			self.mapUrl = mapaddress.find('a')['href']
		except AttributeError:
			pass
        
		# Type of housing
		self.housingType = extension
