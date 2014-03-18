'''
Download a craigslist housing post and extract data for the Tenant Resource Center Vacancy List
Created on Mar 17, 2014
@author: michael donnelly
'''

def parseListing(url):
    import re
    import urllib.request
    from bs4 import BeautifulSoup
      
    ''' Retrieve page and extract contents '''
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page)    
        postingtitle = soup.find('h2','postingtitle').get_text()
        postingbody = soup.find('section',id='postingbody').get_text()
    except AttributeError:
        return ''
    
    ''' Price '''
    price = postingtitle.split()[0]
    try:
        price.split('$')[1]
    except IndexError:
        price='' 

    ''' Address '''
    try:
        address = soup.find('div','mapaddress').get_text()
        address = address.replace(',', ' ')
    except AttributeError:
        address = ''
    
    ''' Contact phone number '''
    try:
        phonePattern = re.compile(r'''
                        # don't match beginning of string, number can start anywhere
            (\d{3})     # area code is 3 digits (e.g. '800')
            \D          # separator
            (\d{3})     # trunk is 3 digits (e.g. '555')
            \D          # separator
            (\d{4})     # rest of number is 4 digits (e.g. '1212')
            ''', re.VERBOSE)
        phone = '-'.join(phonePattern.search(postingbody).groups())
    except AttributeError:
        phone = ''
    
    ''' Go through block of discrete attributes '''
       
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
    
    ''' Make amenities from parking, laundry, pets, and smoking '''
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
        
    row = [bedrooms, price, phone, description, address, url]
    return ",".join(row)
    
    