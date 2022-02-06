# DocumentReader

## Overview
Python OCR document reader using OpenCV and Tesseract

## Requirements

You will need to install Tesseract 5. Details can be found here https://tesseract-ocr.github.io/tessdoc/Home.html. The Python library is just a wrapper and not sufficient on its own.

Beyond the usual libraries installed with Conda you will also require:
pip install opencv-python
pip install tesseract5

Testing makes use of pytest, linting is done with pylint and formatting was handled with black. All are available via pypi.org.

## Structure

The main script is jmocr.py in the root directory. 
Helper functions are in `ocrcode`.
Tests are in `test`.
Example and development images are in `data`.

## License
TBD

