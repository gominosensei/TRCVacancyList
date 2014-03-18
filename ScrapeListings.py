'''
Created on Mar 17, 2014
@author: michael donnelly
'''

import urllib.request
import xlsxwriter
from bs4 import BeautifulSoup
from ParseListing import parseListing
from ExcelFile import createSpreadsheet, addRow, saveSpreadsheet

# Constants
apa = 'http://madison.craigslist.org/apa/'
urlbase = 'http://madison.craigslist.org'
filename = 'vacancy_list.xlsx'

# Setup Excel worksheet
workbook = xlsxwriter.Workbook(filename)
worksheet = createSpreadsheet(workbook)

# Get the list of craigslist posts
page = urllib.request.urlopen(apa)
soup = BeautifulSoup(page)

# Loop over listings and add each one to the sheet
rowNumber=0
for row in soup.find_all('p','row'):
    link = row.find('a')
    url = urlbase + link['href']
    rowNumber += 1
    if rowNumber>9:
        break
    row = parseListing(url)
    addRow(workbook, worksheet, rowNumber, row)
    print("adding listing at",url)
    #print(",".join(row))

saveSpreadsheet(workbook)
print('done')