'''
Generate an excel spreadsheet of the TRC Vacancy List
Created on Mar 18, 2014
@author: michael donnelly
'''

import sys
import logging
import xlsxwriter  # docs at http://xlsxwriter.readthedocs.org/contents.html
import ListingClass

def openFile(filename):
    workbook = xlsxwriter.Workbook(filename)
    try:
        workbook.close()
        workbook = xlsxwriter.Workbook(filename)
        return workbook 
    except PermissionError:
        print('Someone has',filename,'open. Close it and run the script again.\n')
        logging.critical('File cannot be locked: %s', filename)
        input('Press Enter to continue...')
        sys.exit()
        return 

def createSpreadsheet(workbook):
    worksheet = workbook.add_worksheet()
    
    worksheet.freeze_panes(1, 0) # # Freeze the first row.
    
    # Column widths
    worksheet.set_column('A:A', 9)  # # bedrooms
    worksheet.set_column('B:B', 7)  # price
    worksheet.set_column('C:C', 12) # contact phone #    
    worksheet.set_column('D:D', 48) # description
    worksheet.set_column('E:E', 14) # available 
    worksheet.set_column('F:F', 35) # address
    worksheet.set_column('G:G', 6)  # ZIP code
    worksheet.set_column('H:H', 9)  # county
    worksheet.set_column('I:I', 70) # listing
    # L listing URL
    
    # Headers
    bold = workbook.add_format({'bold': True})
    italics = workbook.add_format({'italic': True})
    
    worksheet.write('A1', '# BR', bold)
    worksheet.write('B1', 'Price', bold)
    worksheet.write('C1', 'Contact', bold)
    worksheet.write('D1', 'Description', bold)
    worksheet.write('E1', 'Available', bold)
    worksheet.write('F1', 'Address', bold)
    worksheet.write('G1', 'ZIP', bold)
    worksheet.write('H1', 'County', italics)
    worksheet.write('I1', 'Listing', italics)
    worksheet.write('J1', 'URL', italics)
            
    return worksheet

def saveSpreadsheet(workbook):
    workbook.close()

def addRow(workbook, worksheet, rowNumber, listing):
	# Formatting
	top = workbook.add_format()
	top.set_align('top')

	wrap = workbook.add_format()
	wrap.set_text_wrap()
	wrap.set_align('top')
	
	link = workbook.add_format({'color': 'blue', 'underline': 1})
	link.set_align('top')

	# Add rows
	worksheet.write(rowNumber, 0, listing.bedroomsField(), top)
	worksheet.write(rowNumber, 1, listing.price, top)
	worksheet.write(rowNumber, 2, listing.phone, top)
	worksheet.write(rowNumber, 3, listing.descriptionField(), wrap)
	# availability
	worksheet.write(rowNumber, 5, listing.addressWithNeighborhood(), top)
	worksheet.write(rowNumber, 6, listing.zip, top)
	# If there isn't a county, include the link to Google Maps 
	if listing.county == '':
		worksheet.write_url(rowNumber, 7, listing.mapUrl, link, 'unknown')
	else:	
		worksheet.write(rowNumber, 7, listing.county, top)
	worksheet.write(rowNumber, 8, listing.listingBody, wrap)
	worksheet.write_url(rowNumber, 9, listing.listingUrl, link)

