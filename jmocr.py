""" This is the core script for the document reader """
# pylint: disable=E1101 no-member
# this pylint disable is needed due to poor behaviour inside cv2
import cv2
import numpy as np
import pytesseract

# import our helpers
from ocrcode import ocr

# set up constants to help with openCV's magic numbers
WAIT_UNTIL_PRESSED = 0
# set up constants for parameterising the OCR process
# resizing
PROCESSING_SIZE = 1024
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
BRIGHTNESS = 10
# pytesseract path (for interoperability)
# May be set to set None if PATH variable is set on system
# see https://stackoverflow.com/questions/50655738/
TESSERACT_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

if __name__ == "__main__":

    # point pytesseract at its install location if required
    if TESSERACT_PATH is not None:
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
    # get our list of paths
    paths = ocr.get_paths("data\\jmbusinesscard.jpg", "data\\business card.jpg")
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
        cv2.imshow("preprocessed_image", preprocessed_image)
        contour_check = np.copy(scaled_image)
        # get our largest quadrilateral contour
        paper_contour = ocr.get_contour_from_mask(
            mask=preprocessed_image,
            min_area=MIN_AREA,
            epsilon=EPSILON,
            contour_check=contour_check,
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
        # improve contrast (keep seperate as we could save this out to disc)
        # see https://stackoverflow.com/questions/39308030
        levelled_image = cv2.addWeighted(
            unwarped_paper,
            alpha=CONTRAST,
            src2=unwarped_paper,
            beta=0,
            gamma=BRIGHTNESS,
        )
        cv2.imshow("test_image", levelled_image)
        # COULD SAVE IMAGE TO DISC HERE

        clean_paper = ocr.improve_image_quality(image=levelled_image)

        # TBD text detection (fast and avoids trying to detect non existent text)

        # pass to tesseract for OCR
        ocr_text = pytesseract.image_to_string(clean_paper, lang="eng")

        # TBD QR code detect and read

        # output OCRed text

        # TEMP display codes
        print(ocr_text)
        print(preprocessed_image.shape)
        print(type(preprocessed_image))

        cv2.waitKey(WAIT_UNTIL_PRESSED)
        # cv2.destroyAllWindows()
