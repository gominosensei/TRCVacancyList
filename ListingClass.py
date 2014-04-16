'''
Class to represent a craigslist housing post
Created on Mar 17, 2014
@author: michael donnelly
'''

import re
import logging
import urllib.request
from bs4 import BeautifulSoup  # docs at http://www.crummy.com/software/BeautifulSoup/bs4/doc/
from pygeocoder import Geocoder # docs at https://bitbucket.org/xster/pygeocoder/wiki/Home
# Google geocoding API docs at https://developers.google.com/maps/documentation/geocoding/?csw=1#GeocodingRequests

def formatPhoneNumber(phone):
	try:
		phone = '-'.join(phone.groups())
	except AttributeError:
		logging.error('Error formatting phone number: %s', phone)
		pass
	return (phone)

def findPhone(text, strict = False):
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
		
	phonePatternStrict = re.compile(r'''
		(\d{3})     # area code is 3 digits (e.g. '800')
		-     		# literal dash
		(\d{3})     # prefix is 3 digits (e.g. '555')
		-           # literal dash
		(\d{4})     # rest of number is 4 digits (e.g. '1212')
		''', re.VERBOSE)

	# First look for a number with area code separated by dashes
	try:
		phone = phonePatternStrict.search(text)
	except AttributeError:
		pass
		
	if (phone):
		return(formatPhoneNumber(phone))

	# If matching is strict, give up if that didn't work. 
	if (strict):
		return('')
		
	# Otherwise search for any number with an area code with looser rules on the dividers
	try:
		phone = phonePattern.search(text)
	except AttributeError:
		try:
			phone = phonePatternNoAreaCode.search(text)
		except AttributeError:
			phone = ''
			
	return(formatPhoneNumber(phone))
	
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
	county = ''
	neighborhood = ''
	zip = ''
		
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
			return 'Shared(0)'
		if self.housingType == 'sub':
			return 'Sublet(' + self.bedrooms + ')'
		return self.bedrooms

	def addressWithNeighborhood(self):
		if self.neighborhood == '':
			return self.address
		if self.address == '':
			return self.neighborhood
		return '%s (%s)' % (self.address, self.neighborhood)

	def representation(self):
		return ('Listing(\n     price=%s\n     housingType=%s\n     address=%s\n     phone=%s\n     bedrooms=%s\n     laundry=%s\n     parking=%s\n     dogsAllowed=%s\n     catsAllowed=%s\n     noSmoking=%s\n     area=%s\n     zip=%s\n     county=%s\n     neighborhood=%s\n     mapUrl=%s\n     listingUrl=%s\n)' % (repr(self.price), repr(self.housingType), repr(self.address), repr(self.phone), repr(self.bedrooms), repr(self.laundry), repr(self.parking), repr(self.dogsAllowed), repr(self.catsAllowed), repr(self.noSmoking), repr(self.area), repr(self.zip), repr(self.county), repr(self.neighborhood), repr(self.mapUrl), repr(self.listingUrl)))
		
	def __str__(self):
		return(self.representation())
		
	def __repr__(self):
		return(self.representation())

	# Instantiate the class and populate attributes based on data from the URL provided
	def __init__(self, url):	
		# Retrieve page and extract contents 
		try:
			page = urllib.request.urlopen(url)
			soup = BeautifulSoup(page)    
			postingtitle = soup.find('h2','postingtitle').get_text()
			postingbody = soup.find('section',id='postingbody').get_text()
			extension = url.split('/')[3]
		except AttributeError:
			logging.error('Failed to download listing %s', url)
			self = None
			return
			
		self.listingBody = postingbody
		
		# Price 
		self.price = postingtitle.split()[0]
		try:
			self.price.split('$')[1]
		except IndexError:
			logging.debug('Non-$ price %s,', self.price)
			self.price='' 

		# Address 
		try:
			address = soup.find('div','mapaddress').get_text()
			self.address = address.replace(',', ' ')
		except AttributeError:
			pass
		
		# Type of housing
		self.housingType = extension
		
		# Contact phone number
		try:
			replylink = url.replace(extension, 'reply').replace('.html','')
			replypage = str(urllib.request.urlopen(replylink).read())
			self.phone = findPhone(replypage, True)
		except (AttributeError, HTTPError):
			logging.debug('No phone from reply page')
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
			else:
				logging.debug('Mystery attribute: %s', attribute)
    
		# URLs
		self.listingUrl = url
		try:
			mapaddress = soup.find('p','mapaddress')
			self.mapUrl = mapaddress.find('a')['href']
		except AttributeError:
			pass
        
		# Geocode based on the Maps URL
		try:
			mapQueryString = self.mapUrl.split('?q=')[1]
			geocode = Geocoder.geocode(mapQueryString)
			county = geocode.administrative_area_level_2
			self.county = county.split(' ')[0]
			self.neighborhood = geocode.neighborhood
			self.zip = geocode.postal_code
		except:
			logging.debug('Geocoding error')
			pass
