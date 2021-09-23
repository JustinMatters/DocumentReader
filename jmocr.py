""" This is the core script for the document reader """
# pylint: disable=E1101 no-member
# this pylint disable is needed due to poor behaviour inside cv2
import cv2
import numpy as np
from ocrcode import ocr

# set up constants to help with openCV's magic numbers
WAIT_UNTIL_PRESSED = 0

# set up constants for parameterising the OCR process
PROCESSING_SIZE = 512
PROCESSING_BLUR = 5
THRESHOLD_HIGH = 200
THRESHOLD_LOW = 200
KERNEL_SIZE = 7


def preprocess_image(
    image: np.array,
    size: int,
    blur: int,
    threshold_high: int,
    threshold_low: int,
    kernel_size: int,
):
    """ Given an image and some processing parameters returns an image which
    is black and white lineart ready for edge detection

    Args:
        image (np.array): the input image as a numpy array
        size (int): resize the maximum dimension to this many pixels
        blur (int): size of gaussian blur to apply
        threshold_high (int): upper edge detection threshold
        threshold_low (int): lower edge detection threshold
        kernel_size (int): kernel size for dilation and erosion

    Returns:
        np.array: the preprocessed image as a numpy array
    """
    # scale file to something manageable
    processed_image = ocr.scale_longest_axis(image, new_size=size)
    # greyscale
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    # blur
    processed_image = cv2.GaussianBlur(processed_image, (blur, blur), 0)
    # edge detect
    processed_image = cv2.Canny(processed_image, threshold_high, threshold_low)
    # dilate and erode our edge detections
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    processed_image = cv2.dilate(processed_image, kernel, iterations=2)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)
    return processed_image


if __name__ == "__main__":
    print("main")
    # ## Broad plan overview

    paths = ocr.get_paths("data/jmbusinesscard.jpg")  # , 'data/business card.jpg')
    print(paths)
    for full_path in paths:

        # open file
        raw_image = cv2.imread(full_path, cv2.IMREAD_COLOR)

        preprocessed_image = preprocess_image(
            image=raw_image,
            size=PROCESSING_SIZE,
            blur=PROCESSING_BLUR,
            threshold_high=THRESHOLD_HIGH,
            threshold_low=THRESHOLD_LOW,
            kernel_size=KERNEL_SIZE,
        )

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

        cv2.imshow("input_image", raw_image)
        print(preprocessed_image.shape)
        print(type(preprocessed_image))
        cv2.imshow("processed_image", preprocessed_image)
        cv2.waitKey(WAIT_UNTIL_PRESSED)
        # cv2.destroyAllWindows()
