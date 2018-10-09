#! python3

# pdfTool.py - 

import PyPDF4 as pdf
import re
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s : %(message)s ')
logging.disable(logging.CRITICAL)
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop\\')
os.chdir(desktop)   # by default, the script searches for the pdf file on the uesr's desktop

def determinePages(pages: list) -> list:
    pageRegex = re.compile(r'(\d+)')    # Pattern: obtain only the numbers
    pagesList = re.split(r'\s*,\s*', pages) # Split the given page(s) and page range by removing any commas and spaces around the commas

    logging.info(pagesList)

    completedPagesList = []
    for pageRange in pagesList:
        tempList = [int(i) for i in pageRegex.findall(pageRange)] # Page ranges are returned as a list with 2 elements, a single page is returned as a list with 1 element; converted to int

        if len(tempList) == 2 and tempList[0] >= tempList[1]:
            print(f'{tempList[0]}-{tempList[1]} is not a valid range.\n')
            continue    # Skips invalid ranges (e.g. don't include pages 18 - 15, but 15 - 18 works)

        elif len(tempList) >= 3:
            print(f'\n{"-".join(str(i) for i in tempList)} is not a valid range\n')
            continue    # Skips invalid ranges (e.g. 12-13-16 would not be valid)

        else:
            completedPagesList.append(tempList) # if valid, append to the completed list

    logging.info(completedPagesList)
    return completedPagesList

# pdfTool extract <pdf file>    --> ask user for page(s) to extract
def extractPages(pdfFile):

    # Open the pdf file
    openPdf = open(pdfFile, 'rb')
    pdfReader = pdf.PdfFileReader(openPdf)
    pdfWriter = pdf.PdfFileWriter() # Instantiates PdfFileWriter class

    # Get the pages to extract from user
    pagesToExtract = input('Enter the page(s) to extract: ')
    listOfPages = determinePages(pagesToExtract)    # Obtain the page(s) in a list format

    # Add the pages to the PdfFileWriter object
    for pageRange in listOfPages:
        # if a page range (e.g. 3 - 5, add pages 3, 4, and 5)
        if len(pageRange) == 2:
            for page in range(pageRange[0] - 1, pageRange[1]):
                pageObj = pdfReader.getPage(page)
                pdfWriter.addPage(pageObj)

        # If only a single page
        elif len(pageRange) == 1:
            pageObj = pdfReader.getPage(pageRange)
            pdfWriter.addPage(pageObj)

        else:
            print('Something went wrong. Closing program...')
            exit()

    # Get the name of the new pdf file with the extracted page
    newPdfName = input('Enter the name of the new pdf file with extracted page: ')

    # Write the pages to the pdf output file as .pdf
    if newPdfName.endswith('.pdf'):
        pdfOutputFile = open(newPdfName, 'wb')
    else:
        pdfOutputFile = open(f'{newPdfName}.pdf', 'wb')
    
    pdfWriter.write(pdfOutputFile)  # Creates the pdf file on the desktop by default
    openPdf.close()
    pdfOutputFile.close()


# TODO: pdfTool combine <pdf file> <pdf file> ...
def combinePDFs(pdfFiles):
    pass

# TODO: pdfTool combineAll <directory of pdf files> --> ask for order to combine, calls the combine function, passes in each pdf file as arg
def combineAllPDFs(pdfFiles):
    pass

# TODO: pdfTool rotateRight <pdf file>
def rotateRight(pdfFile):
    pass

# TODO: pdfTool rotateLeft <pdf file>
def rotateLeft(pdfFile):
    pass

# TODO: pdfTool rotateAll <directory of pdf files> --> ask for right or left, calls rotateLeft or rotateRight, passes in each pdf file
def rotateAll(pdfFiles):
    pass

# TODO: pdfTool rotatePages <pdf file> --> ask user for page(s) to rotate
def rotatePages(pdfFile):
    pass

# TODO: pdfTool encrypt <pdf file> --> ask user for password
def encryptPDF(pdfFile):
    pass

# TODO: pdfTool encryptAll <directory of pdf files> --> calls encrypt function for each pdf
def encryptAllPDFs(pdfFiles):
    pass

# TODO: pdfTool decrypt <pdf file>
def decryptPDF(pdfFile):
    pass

# TODO: pdfTool decryptAll <directory of pdf files> --> calls decrypt function for each pdf
def decryptAllPDFs(pdfFiles):
    pass

# TODO: pdfTool deletePages <pdf file> --> ask user for page(s) to delete
def deletePages(pdfFile):
    pass

if sys.argv[1] == 'extract':
    extractPages(sys.argv[2])

elif sys.argv[1] == 'combine':
    pass
elif sys.argv[1] == 'combineAll':
    pass
elif sys.argv[1] == 'rotateRight':
    pass
elif sys.argv[1] == 'rotateLeft':
    pass
elif sys.argv[1] == 'rotateAll':
    pass
elif sys.argv[1] == 'rotatePages':
    pass
elif sys.argv[1] == 'encrypt':
    pass
elif sys.argv[1] == 'encryptAll':
    pass
elif sys.argv[1] == 'decrypt':
    pass
elif sys.argv[1] == 'decryptAll':
    pass
elif sys.argv[1] == 'deletePages':
    pass