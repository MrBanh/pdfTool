#! python3

# pdfTool.py - a command line tool used to extract pages, combine, rotate,
# encrypt, and decrypt pdf files

import PyPDF4 as pdf
import re
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s : %(message)s ')

# logging.disable(logging.CRITICAL)

desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop\\')
os.chdir(desktop)   # by default, searches for the pdf file on user's desktop


def clear():
    os.system('cls')


def determinePages(pages: list) -> list:
    pageRegex = re.compile(r'(\d+)')    # Pattern: obtain only the numbers

    # Split the given page(s) and page range by removing
    # any commas and spaces around the commas

    pagesList = re.split(r'\s*,\s*', pages)

    logging.info(pagesList)

    completedPagesList = []
    for pageRange in pagesList:

        # Page ranges are returned as a list with 2 elements,
        # a single page is returned as a list with 1 element; converted to int

        tempList = [int(i) for i in pageRegex.findall(pageRange)]

        if len(tempList) == 2 and tempList[0] >= tempList[1]:
            print(f'{tempList[0]}-{tempList[1]} is not a valid range.\n')
            # Skip invalid ranges (e.g. 18 - 15 doesn't work, but 15 - 18 work)
            continue

        elif len(tempList) >= 3:
            print(f'\n{"-".join(str(i) for i in tempList)}'
                  f'is not a valid range\n')
            # Skip invalid ranges (e.g. 12-13-16 would not be valid)
            continue

        else:
            # if valid, append to the completed list
            completedPagesList.append(tempList)

    logging.info(completedPagesList)
    return completedPagesList


def getOutputFileName(dir: str = desktop) -> str:
    # Get the name of the new pdf file
    newPdfName = input('Enter name for the new pdf file: ')

    # Returns the specified pdf file name
    if newPdfName.endswith('.pdf'):
        return os.path.join(dir, newPdfName)
    else:
        return os.path.join(dir, f'{newPdfName}.pdf')


def printPdfList(oldList: list, newList: list, listLen: int):
    # Print out current list of available pdf files and the new order list
    print()
    print('------------------------- PDF LIST -------------------------')
    print(f'| {"OLD LIST":^26} || {"NEW ORDERED LIST":^26} |')
    print('------------------------------------------------------------')
    for i in range(listLen):
        if i < len(oldList):
            print(f'| {i + 1}. {os.path.basename(oldList[i]):<23} |', end='')
        else:
            print(f'| {" ":<26} |', end='')

        if i < len(newList):
            print(f'| {i + 1}. {os.path.basename(newList[i]):<23} |', end='')
        else:
            print(f'| {" ":<26} |', end='')
        print()
    print('------------------------------------------------------------')
    print()


def newOrder(pdfList: list) -> list:

    newList = []
    tempList = pdfList[:]
    listLen = len(tempList)

    print('\nCurrent order of pdf files: \n')
    for i in range(len(tempList)):
        print(f'{i + 1}. {os.path.basename(tempList[i])}')

    toReorder = input('\nWould you like to re-order? (y/n): ')
    if toReorder.lower() == 'y':
        while tempList:
            # Get user input index of pdf file to append to new list
            try:
                if len(tempList) == 1:
                    newList.append(tempList.pop())
                    clear()
                    printPdfList(tempList, newList, listLen)
                    break
                reorderIndex = int(input('Please enter a number from above: '))

                # Make sure the pdf file is within range (No IndexError)
                if reorderIndex > len(tempList):
                    raise Exception

            except Exception:
                print('Invalid input.')
                continue
            else:
                # Append the file to new list and delete from tempList
                newList.append(tempList.pop(reorderIndex - 1))
                logging.info(tempList)
                printPdfList(tempList, newList, listLen)

        logging.info(f'Original List: {tempList}')
        logging.info(f'New ordered list: {newList}')

        # return newList
        return newList

    elif toReorder.lower() == 'n':
        return tempList
    else:
        print('Invalid input.')


# pdfTool extract <pdf file>    --> ask user for page(s) to extract
def extractPages(pdfFile: str, dir=desktop):

    # Open the pdf file
    openPdf = open(pdfFile, 'rb')
    pdfReader = pdf.PdfFileReader(openPdf)
    pdfWriter = pdf.PdfFileWriter()     # Instantiates PdfFileWriter class

    # Get the pages to extract from user
    pagesToExtract = input('Enter the page(s) to extract: ')

    # Obtain the page(s) in a list format
    listOfPages = determinePages(pagesToExtract)

    # Add the pages to the PdfFileWriter object
    for pageRange in listOfPages:
        # if a page range (e.g. 3 - 5, add pages 3, 4, and 5)
        if len(pageRange) == 2:
            for page in range(pageRange[0] - 1, pageRange[1]):
                pageObj = pdfReader.getPage(page)
                pdfWriter.addPage(pageObj)

        # If only a single page
        elif len(pageRange) == 1:
            pageObj = pdfReader.getPage(pageRange[0] - 1)
            pdfWriter.addPage(pageObj)

        else:
            print('Something went wrong.')
            return

    # Write the pages to the pdf output file as .pdf
    newFileLocation = getOutputFileName(dir)
    pdfOutputFile = open(newFileLocation, 'wb')

    # Creates the pdf file on the desktop by default
    pdfWriter.write(pdfOutputFile)
    print(f'\nDone!\n\nNew File Located at: {newFileLocation}\n')
    openPdf.close()
    pdfOutputFile.close()


# pdfTool combine <pdf file> <pdf file> ...
def combinePDFs(pdfFiles: list, dir: str = desktop):
    # Instantiate PdfFileWriter class
    pdfWriter = pdf.PdfFileWriter()

    for file in pdfFiles:
        # Opens each pdf file
        openPdf = open(file, 'rb')
        pdfReader = pdf.PdfFileReader(openPdf)

        # Goes through each page of each pdf, adds it to the PdfFileWriter obj
        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

    # Outputs the PdfFileWriter object for all pages from each specified pdf
    newFileLocation = getOutputFileName(dir)
    pdfOutputFile = open(newFileLocation, 'wb')
    pdfWriter.write(pdfOutputFile)

    print(f'\nDone!\n\nNew File Located at: {newFileLocation}\n')

    openPdf.close()
    pdfOutputFile.close()


# pdfTool combineAll <directory of pdf files> --> ask for order to combine,
# calls the combine function, passes in each pdf file as arg
def combineAll(dir: str = desktop):
    logging.info(os.path.isdir(os.path.abspath(dir)))

    pdfList = []

    # Validate directory and that it exists
    if os.path.isdir(os.path.abspath(dir)):
        # Goes through the list of filename strings from os.listdir(<path>)
        for filename in os.listdir(dir):
            # Only combine pdf files
            if filename.endswith('.pdf'):
                logging.info(filename)
                pdfList.append(os.path.abspath(os.path.join(dir, filename)))

    else:
        print('Invalid directory. Please try again...')

    logging.info(pdfList)

    # Allow user to change the order of how the pdf files are combined
    pdfList = newOrder(pdfList)

    # combines all pdf files in the directory
    combinePDFs(pdfList, dir)


# pdfTool rotate <pdf file>
def rotate(pdfFile: str):
    # Make sure we get the pdf file
    if not pdfFile.endswith('.pdf'):
        pdfFile = pdfFile + '.pdf'

    # Make sure the file actually exists
    if not os.path.exists(pdfFile):
        print(f'\n{pdfFile} does not exist...\n')
        return

    openFile = open(pdfFile, 'rb')
    pdfReader = pdf.PdfFileReader(openFile)

    while True:
        rotateOption = input(f"""
            Please enter the direction to rotate {os.path.basename(pdfFile)}:
                1. Rotate Clockwise (right)
                2. Rotate CounterClockwise (left)
                3. Rotate Upside Down

            -> """)

        try:
            # Default is rotate right
            rotateTo = 90
            if int(rotateOption) == 1:
                break
            elif int(rotateOption) == 2:
                rotateTo = 270  # Rotate left
                break
            elif int(rotateOption) == 3:
                rotateTo = 180  # Rotate upside down
                break
            else:
                continue
        except ValueError:
            print('\nInvalid input')

    # Create PdfFileWriter object
    pdfWriter = pdf.PdfFileWriter()

    # Loop through each page, rotate the page, then add to PdfFileWriter object
    for pageNum in range(pdfReader.numPages):

        # Obtain a page from the pdf file
        page = pdfReader.getPage(pageNum)

        # Rotate that page
        page.rotateClockwise(rotateTo)

        # Add the page to the PdfFileWriter object
        pdfWriter.addPage(page)

    # Create pdf file based on the original pdf file name
    fileName = os.path.splitext(pdfFile)[0] + '_rotated.pdf'
    resultPdfFile = open(fileName, 'wb')

    # Write to the new pdf file
    pdfWriter.write(resultPdfFile)

    resultPdfFile.close()
    openFile.close()


# pdfTool rotateAll <directory of pdf files> --> ask for right or left,
# calls rotate function, passes in each pdf file
def rotateAll(dir: str = desktop):
    pdfList = []

    # Validate directory and that it exists
    if os.path.isdir(os.path.abspath(dir)):
        # Goes through the list of filename strings from os.listdir(<path>)
        for filename in os.listdir(dir):
            # Only combine pdf files
            if filename.endswith('.pdf'):
                logging.info(filename)
                pdfList.append(os.path.abspath(os.path.join(dir, filename)))

    else:
        print('Invalid directory. Please try again...')

    # Pass each pdf in the pdfList to the rotate() function
    for pdfFile in pdfList:
        rotate(pdfFile)

    print('Done!')


# pdfTool encrypt <pdf file> --> ask user for password
def encrypt(pdfFile: str):
    # Make sure we get the pdf file
    if not pdfFile.endswith('.pdf'):
        pdfFile = pdfFile + '.pdf'

    # Make sure the file actually exists
    if not os.path.exists(pdfFile):
        print(f'\n{pdfFile} does not exist...\n')
        return

    openFile = open(pdfFile, 'rb')
    pdfReader = pdf.PdfFileReader(openFile)

    # Make sure the file isn't encrypted
    if pdfReader.isEncrypted:
        print(f'{os.path.basename(pdfFile)} is already encrypted.')
        return

    else:   # Encrypt the file
        pdfWriter = pdf.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            page = pdfReader.getPage(pageNum)
            pdfWriter.addPage(page)

        # Add password for encryption
        pdfWriter.encrypt(input(f'Enter a password to encrypt '
                                f'{os.path.basename(pdfFile)}: '))

        # Create pdf file based on the original pdf file name
        fileName = os.path.splitext(pdfFile)[0] + '_encrypted.pdf'
        resultPdfFile = open(fileName, 'wb')

        # Write to the new pdf file
        pdfWriter.write(resultPdfFile)

        resultPdfFile.close()
        openFile.close()


# pdfTool encryptAll <directory of pdf files> --> calls encrypt function
# for each pdf file in a directory
def encryptAll(dir: str = desktop):
    pdfList = []

    # Validate directory and that it exists
    if os.path.isdir(os.path.abspath(dir)):
        # Goes through the list of filename strings from os.listdir(<path>)
        for filename in os.listdir(dir):
            # Only combine pdf files
            if filename.endswith('.pdf'):
                logging.info(filename)
                pdfList.append(os.path.abspath(os.path.join(dir, filename)))

    else:
        print('Invalid directory. Please try again...')

    # Pass each pdf in the pdfList to the rotate() function
    for pdfFile in pdfList:
        encrypt(pdfFile)

    print('Done!')


# pdfTool decrypt <pdf file>
def decrypt(pdfFile: str):
    # Make sure we get the pdf file
    if not pdfFile.endswith('.pdf'):
        pdfFile = pdfFile + '.pdf'

    # Make sure the file actually exists
    if not os.path.exists(pdfFile):
        print(f'\n{pdfFile} does not exist...\n')
        return

    openFile = open(pdfFile, 'rb')
    pdfReader = pdf.PdfFileReader(openFile)

    # Make sure the file is encrypted
    if not pdfReader.isEncrypted:
        print(f'{os.path.basename(pdfFile)} is not encrypted.')
        return

    else:   # Decrypt it
        while True:
            isDecrypted = pdfReader.decrypt(
                                        input(f'Enter decryption password'
                                              f' {os.path.basename(pdfFile)}:'
                                              f' '))

            # Handles an incorrect password
            if isDecrypted == 0:
                print('\n>> File was not decrypted with provided password.')
                print('>> Try again or press <CTRL + C + Return> to quit.\n')

            else:
                break

        # Create a new pdf file for the decrypted file
        pdfWriter = pdf.PdfFileWriter()
        for pageNum in range(pdfReader.numPages):
            page = pdfReader.getPage(pageNum)
            pdfWriter.addPage(page)

        # Create pdf file based on the original pdf file name
        fileName = os.path.splitext(pdfFile)[0] + '_decrypted.pdf'
        resultPdfFile = open(fileName, 'wb')

        # Write to the new pdf file
        pdfWriter.write(resultPdfFile)

        resultPdfFile.close()
        openFile.close()


# pdfTool decryptAll <directory of pdf files> --> calls decrypt function
# for each pdf file in a directory
def decryptAll(dir: str = desktop):
    pdfList = []

    # Validate directory and that it exists
    if os.path.isdir(os.path.abspath(dir)):
        # Goes through the list of filename strings from os.listdir(<path>)
        for filename in os.listdir(dir):
            # Only combine pdf files
            if filename.endswith('.pdf'):
                logging.info(filename)
                pdfList.append(os.path.abspath(os.path.join(dir, filename)))

    else:
        print('Invalid directory. Please try again...')

    # Pass each pdf in the pdfList to the rotate() function
    for pdfFile in pdfList:
        decrypt(pdfFile)

    print('Done!')


# TODO: Handles user provide pdfs that have spaces in the pdf file name
# def PdfWithSpaces(pdfStr: str) -> list:
#     logging.info(pdfStr)

#     tempStr = ''
#     allPdfsListed = []
#     for letterIndex in range(len(pdfStr)):

#         if pdfStr[letterIndex:letterIndex + 4] == '.pdf':
#             allPdfsListed.append(tempStr)
#             tempStr = ''
#         else:
#             tempStr += pdfStr[letterIndex]

#     logging.info(allPdfsListed)


try:
    if sys.argv[1] == 'extract':
        extractPages(sys.argv[2])
        # PdfWithSpaces(' '.join(sys.argv[2:]))

    elif sys.argv[1] == 'combine':
        combinePDFs(sys.argv[2:])

    elif sys.argv[1] == 'combineAll':
        combineAll(sys.argv[2])

    elif sys.argv[1] == 'rotate':
        rotate(sys.argv[2])

    elif sys.argv[1] == 'rotateAll':
        rotateAll(sys.argv[2])

    elif sys.argv[1] == 'encrypt':
        encrypt(sys.argv[2])

    elif sys.argv[1] == 'encryptAll':
        encryptAll(sys.argv[2])

    elif sys.argv[1] == 'decrypt':
        decrypt(sys.argv[2])

    elif sys.argv[1] == 'decryptAll':
        decryptAll(sys.argv[2])
    else:
        raise IndexError

except IndexError:
    print('\n!!!! PLEASE PROVIDE THE APPROPRIATE ARGUMENTS !!!!')
    print("""
        pdfTool extract <pdf file>
        pdfTool combine <pdf file> <pdf file> ...
        pdfTool combineAll <directory of pdf files>
        pdfTool rotate <pdf file>
        pdfTool rotateAll <directory of pdf files>
        pdfTool encrypt <pdf file>
        pdfTool encryptAll <directory of pdf files>
        pdfTool decrypt <pdf file>
        pdfTool decryptAll <directory of pdf files>
        """)