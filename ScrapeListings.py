'''
Created on Mar 17, 2014
Scrape Madison housing posts from craigslist and compile data for the TRC Housing Vacancy List
@author: michael donnelly
'''

import urllib.request
import time
import xlsxwriter
from bs4 import BeautifulSoup
from ExcelFile import openFile, createSpreadsheet, addRow, saveSpreadsheet
from ListingClass import Listing
  
# Constants
urlbase = 'http://madison.craigslist.org'
extension = ['apa', 'roo', 'sub']
maximumPages = [20, 5, 3]
filename = 'vacancy_list.xlsx'
maximumRows = 10 #3000

def scrapeRow(row, urlbase, rowNumber, workbook, worksheet):
	link = row.find('a')
	url = urlbase + link['href']
	thisListing = Listing(url)
	# Only add listings that are known to be in Dane County or where we can't tell.
	if thisListing.county == "Dane" or thisListing.county == "":
		print(rowNumber,"adding listing",url)
		addRow(workbook, worksheet, rowNumber, thisListing)

def scrapePage(listUrl, urlbase, rowNumber, workbook, worksheet):
    print('\nscraping',listUrl)

    # Get the list of craigslist posts
    page = urllib.request.urlopen(listUrl)
    soup = BeautifulSoup(page)
    
    # Loop over listings and add each one to the sheet
    rowsOnThisPage = 1
    for row in soup.find_all('p','row'):
        rowNumber += 1
        if rowNumber > maximumRows:
            break
        scrapeRow(row, urlbase, rowNumber, workbook, worksheet)

        rowsOnThisPage += 1
        if rowsOnThisPage > 101:   # for testing
            break
        
    return rowNumber    

def scrapeCategory(categoryUrl, pages, urlbase, rowNumber, workbook, worksheet):
    for pagesback in range(0, pages):
        if pagesback > 0:
            index = 'index' + str(pagesback) + '00.html'
        else:
            index = ''
        listUrl = categoryUrl + index
        
        rowNumber = scrapePage(listUrl, urlbase, rowNumber, workbook, worksheet)
        if rowNumber > maximumRows:
            break
    
    return rowNumber       

# Setup
start = time.time()
workbook = openFile(filename)
worksheet = createSpreadsheet(workbook)
rowNumber = 0

# Loop over categories: normal, rooms, sublets
for category in range(0,3):
    categoryUrl = urlbase + '/' + extension[category] + '/'
    pages = maximumPages[category]
    
    rowNumber = scrapeCategory(categoryUrl, pages, urlbase, rowNumber, workbook, worksheet)
    if rowNumber > maximumRows:
        break
   
saveSpreadsheet(workbook)
end = time.time()
print('done in',end-start,'seconds')
input("Press Enter to continue...")
