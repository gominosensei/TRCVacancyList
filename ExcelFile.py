'''
Generate an excel spreadsheet of the TRC Vacancy List
Created on Mar 18, 2014
@author: michael donnelly
'''

import xlsxwriter  # docs at http://xlsxwriter.readthedocs.org/contents.html

def createSpreadsheet(workbook):
    worksheet = workbook.add_worksheet()
    
    worksheet.freeze_panes(1, 0) # # Freeze the first row.
    
    # Column widths
    worksheet.set_column('A:A', 4)  # # bedrooms
    worksheet.set_column('B:B', 7)  # price
    worksheet.set_column('C:C', 12) # contact phone #    
    worksheet.set_column('D:D', 48) # description
    worksheet.set_column('E:E', 14) # available 
    worksheet.set_column('F:F', 35) # address
    worksheet.set_column('G:G', 10) # region 
    worksheet.set_column('H:H', 5) # type
    worksheet.set_column('I:I', 70) # listing
    
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
    worksheet.write('H1', 'Type', italics)
    worksheet.write('I1', 'Listing', italics)
    worksheet.write('J1', 'URL', italics)
            
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
    
    # bedrooms, price, contact, description, available, address, region, type, listing, url
    formats = [top, top, top, wrap, top, top, None, top, wrap, None]
        
    # Add columns to sheet
    rowData.insert(4, '')   # blank column for availability
    for column in range (0,10):
        worksheet.write(rowNumber, column, rowData[column], formats[column])
            