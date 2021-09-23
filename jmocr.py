import cv2
import numpy as np
from ocrcode import ocr
import os
import sys

# set up variables to help with openCV's magic numbers
wait_until_pressed = 0

if __name__ == '__main__':
    print('main')
    # ## Broad plan overview
    
    paths = ocr.get_paths('data/jmbusinesscard.jpg', 'data/business card.jpg')
    print(paths)
    for full_path in paths:

        # open file
        image = cv2.imread(full_path, cv2.IMREAD_UNCHANGED)
        # scale file to something manageable
        image = ocr.scale_longest_axis(image, new_size = 512)

        # greyscale

        # blur

        # threshold

        # get contour

        # apply transformation too original image

        # greyscale rectified image

        # denoise

        # blur rectified image

        # threshhold rectified image

        # text detection (fast and avoids trying to detect non existent text)

        # get contours

        # pass to tesseract for OCR

        # output OCRed text

        # TEMP display codes
        print(image.shape)
        print(type(image))
        cv2.imshow('input_image', image)
        cv2.waitKey(wait_until_pressed)
        #cv2.destroyAllWindows()