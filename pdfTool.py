#! python3

# pdfTool.py - 

import PyPDF4 as pdf
import re
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s : %(message)s ')
desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop\\')
os.chdir(desktop)

def determinePages(pages: list) -> list:
    pageRegex = re.compile(r'(\d+)')    # Pattern: obtain only the numbers
    pagesList = re.split(r'\s*,\s*', pages) # Split the given page(s) and page range by removing any commas and spaces around the commas

    logging.info(pagesList)

    completedPagesList = []
    for pageRange in pagesList:
        tempList = [int(i) for i in pageRegex.findall(pageRange)] # Page ranges are returned as a list with 2 elements, a single page is returned as a list with 1 element; converted to int
        if len(tempList) == 2 and tempList[0] >= tempList[1]:
            continue    # Skips invalid ranges (e.g. don't include pages 18 - 15, but 15 - 18 works)
        else:
            completedPagesList.append(tempList) # if valid, append to the completed list

    logging.info(completedPagesList)
    return completedPagesList

# pdfTool extract <pdf file>    --> ask user for page(s) to extract
def extractPages(pdfFile):

    logging.info(pdfFile)
    pagesToExtract = input('Enter the page(s) to extract: ')
    listOfPages = determinePages(pagesToExtract)
    for pageOrPages in listOfPages:
        pass

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