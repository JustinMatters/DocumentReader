# DocumentReader

## Overview
Python OCR document reader using OpenCV and Tesseract

## Requirements

You will need to install Tesseract 5. Details can be found here https://tesseract-ocr.github.io/tessdoc/Home.html. The Python library is just a wrapper and not sufficient on its own.

Beyond the usual libraries installed with Conda you will also require:
pip install opencv-python
pip install tesseract5

Testing makes use of pytest, linting is done with pylint and formatting was handled with black. All are available via pypi.org.

requirements.txt details sufficient but most likely excessive libraries

## Structure

The main script is jmocr.py in the root directory. 
Helper functions are in `ocrcode`.
Tests are in `test`.
Example and development images are in `data`.

## Usage

This tool can be used to isolate pages of text from their background in an image, straighten them to give a clean full frame image. and then convert to text them using Tesseract OCR. The cleaned image and text can be saved if required.

To run the jmocr from the command line:
python jmocr.py [N [N ...]] [-h] [-s [SAVE]] [-v] [-t TESSERACT]

positional arguments:
  N                     File or folder paths. Files must be jpg, png or gif

optional arguments:
  -h, --help            show this help message and exit
  -s [SAVE], --save [SAVE]
                        Save data to current working directory or a specified folder
  -v, --verbose         Display intermediate steps in processing
  -t TESSERACT, --tesseract TESSERACT
                        Specify location of tesseract.exe

eg:
python jmocr.py data\jmbusinesscard.jpg  -s  -t "C:\Program Files\Tesseract-OCR\tesseract.exe" 

## License
Code in this repo is licensed under Apache 2.0 for consistency with the two libraries on which it principally relies
https://www.apache.org/licenses/LICENSE-2.0

OpenCV2 is licensed under Apache 2.0
https://opencv.org/license/

Note that Tesseract OCR on which this project relies is licensed under Apache 2.0
https://github.com/tesseract-ocr/tesseract

