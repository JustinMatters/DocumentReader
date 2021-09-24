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
PROCESSING_SIZE = 2048
# preprocessing
PROCESSING_BLUR = 5
THRESHOLD_HIGH = 200
THRESHOLD_LOW = 200
KERNEL_SIZE = 7
# contour extraction
MIN_AREA = 10000
EPSILON = 0.02
# contrast and brightness controls
CONTRAST = 1.3
BRIGHTNESS =  10

if __name__ == "__main__":

    # get our list of paths
    paths = ocr.get_paths("data/jmbusinesscard.jpg")  # , 'data/business card.jpg')
    # cycle through our paths
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
            mask=preprocessed_image, min_area=MIN_AREA, epsilon=EPSILON,
        )
        print(paper_contour)

        # make sure we have our points in the correct order for the transformation
        ordered_paper_contour = ocr.order_quadrilateral(quad=paper_contour)
        print(ordered_paper_contour)
        # apply transformation to image
        unwarped_paper = ocr.unwarp_quadrilateral(
            image=scaled_image,
            quad=ordered_paper_contour,
            # trim the edge 2% off to cope with imperfect transforms
            margin=int(PROCESSING_SIZE * 0.02),
        )
        # improve contrast (keep sepearate as we could save this out to disc)
        # see https://stackoverflow.com/questions/39308030
        levelled_image = cv2.addWeighted(
            unwarped_paper,
            alpha=CONTRAST,
            src2= unwarped_paper,
            beta=0,
            gamma=BRIGHTNESS
        )
        cv2.imshow("test_image", levelled_image)
        # COULD SAVE IMAGE TO DISC HERE

        clean_paper = ocr.improve_image_quality(image=levelled_image)

        # text detection (fast and avoids trying to detect non existent text)

        # get contours

        # pass to tesseract for OCR

        # output OCRed text

        # TEMP display codes

        # cv2.imshow("input_image", raw_image)
        #cv2.imshow("scaled_image",scaled_image)
        print(preprocessed_image.shape)
        print(type(preprocessed_image))
        #cv2.imshow("processed_image", preprocessed_image)
        cv2.imshow("unwarped_image", unwarped_paper)
        #cv2.imshow("clean_image", clean_paper)
        cv2.waitKey(WAIT_UNTIL_PRESSED)
        # cv2.destroyAllWindows()
