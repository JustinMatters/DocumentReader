""" This is the core script for the document reader """
# pylint: disable=E1101 no-member
# this pylint disable is needed due to poor behaviour inside cv2
import cv2
import numpy as np
from ocrcode import ocr

# set up constants to help with openCV's magic numbers
WAIT_UNTIL_PRESSED = 0

# set up constants for parameterising the OCR process
# resizing
PROCESSING_SIZE = 512
# preprocessing
PROCESSING_BLUR = 5
THRESHOLD_HIGH = 200
THRESHOLD_LOW = 200
KERNEL_SIZE = 7
# contour extraction
MIN_AREA = 10000
EPSILON = 0.02

if __name__ == "__main__":
    print("main")
    # ## Broad plan overview

    paths = ocr.get_paths("data/jmbusinesscard.jpg")  # , 'data/business card.jpg')
    print(paths)
    for full_path in paths:

        # open file
        raw_image = cv2.imread(full_path, cv2.IMREAD_COLOR)
        # scale file to something manageable
        scaled_image = ocr.scale_longest_axis(raw_image, new_size=PROCESSING_SIZE)
        # perform our preprocessing
        preprocessed_image = ocr.preprocess_image(
            image=scaled_image,
            blur=PROCESSING_BLUR,
            threshold_high=THRESHOLD_HIGH,
            threshold_low=THRESHOLD_LOW,
            kernel_size=KERNEL_SIZE,
        )

        paper_contour = ocr.get_contour_from_mask(
            mask=preprocessed_image,
            min_area=MIN_AREA,
            epsilon=EPSILON,
        )
        print(paper_contour)

        # make sure we have our points in the correct order for the transformation
        ordered_paper_contour = ocr.order_quadrilateral(quad=paper_contour)
        print(ordered_paper_contour)
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

        cv2.imshow("input_image", raw_image)
        print(preprocessed_image.shape)
        print(type(preprocessed_image))
        cv2.imshow("processed_image", preprocessed_image)
        cv2.waitKey(WAIT_UNTIL_PRESSED)
        # cv2.destroyAllWindows()
