'''
Generate an excel spreadsheet of the TRC Vacancy List
Created on Mar 18, 2014
@author: michael donnelly
'''

import xlsxwriter  # docs at http://xlsxwriter.readthedocs.org/contents.html

def openFile(filename):
    workbook = xlsxwriter.Workbook(filename)
    try:
        workbook.close()
        workbook = xlsxwriter.Workbook(filename)
        return workbook 
    except PermissionError:
        print('Someone has',filename,'open. Close it and run the script again.')
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
    worksheet.set_column('G:G', 10) # region 
    worksheet.set_column('H:H', 9)  # county
    worksheet.set_column('I:I', 6)  # ZIP code
    worksheet.set_column('J:J', 17) # neighborhood
    worksheet.set_column('K:K', 70) # listing
    # listing URL
    
    # Headers
    bold = workbook.add_format({'bold': True})
    italics = workbook.add_format({'italic': True})
    
    worksheet.write('A1', '# BR', bold)
    worksheet.write('B1', 'Price', bold)
    worksheet.write('C1', 'Contact', bold)
    worksheet.write('D1', 'Description', bold)
    worksheet.write('E1', 'Available', bold)
    worksheet.write('F1', 'Address', bold)
    worksheet.write('G1', 'Region', bold)
    worksheet.write('H1', 'County', italics)
    worksheet.write('I1', 'ZIP', italics)
    worksheet.write('J1', 'Neighborhood', italics)
    worksheet.write('K1', 'Listing', italics)
    worksheet.write('L1', 'URL', italics)
            
    return worksheet

def saveSpreadsheet(workbook):
    workbook.close()

def addRow(workbook, worksheet, rowNumber, rowData):
    # Formatting
    top = workbook.add_format()
    top.set_align('top')
    
    wrap = workbook.add_format()
    wrap.set_text_wrap()
    wrap.set_align('top')
    
    # bedrooms, price, contact, description, available, address, region, county, zip, neighborhood, listing, url
    formats = [top, top, top, wrap, top, top, None, top, top, top, wrap, None]
        
    # Add columns to sheet
    rowData.insert(4, '')   # blank column for availability
    for column in range (0,12):
        worksheet.write(rowNumber, column, rowData[column], formats[column])
            
