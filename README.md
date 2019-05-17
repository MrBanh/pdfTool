# pdfTool

pdfTool is a command-line tool that utilizes the PyPDF4 pip package to extract pages from a pdf, combine 2 pdf files, combine all pdf files in a directory, rotate the orientation of a pdf, rotate all pdf files in a directory, encrypting and decrypting a pdf file, or encrypting and decrypting all pdf files in a directory.

## Getting Started

### Prerequisites
 
 Python version: Python 3.7.3
 
 Install package dependency:
 
    python3 -m pip install PyPDF4

Clone this project using git:

    git clone https://github.com/MrBanh/pdfTool.git .

## Test if it works

Using the terminal, cd to the pdfTool folder. Test if it works by using:

    python pdfTool.py

### Command Line Options

      pdfTool extract <pdf file>
      pdfTool combine <pdf file> <pdf file> ...
      pdfTool combineAll <directory of pdf files>
      pdfTool rotate <pdf file>
      pdfTool rotateAll <directory of pdf files>
      pdfTool encrypt <pdf file>
      pdfTool encryptAll <directory of pdf files>
      pdfTool decrypt <pdf file>
      pdfTool decryptAll <directory of pdf files>
