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
PROCESSING_SIZE = 1024
# preprocessing
PROCESSING_BLUR = 5
THRESHOLD_HIGH = 200
THRESHOLD_LOW = 200
KERNEL_SIZE = 7
# contour extraction
MIN_AREA = 10000
EPSILON = 0.02


# def get_parallelogram_dimensions(quad:np.array)->'tuple[int,int]':
#     """gets the width and height of a parallelogram whose corner coordinates
#     are defined in a np.array((4,2))

#     Args:
#         quad (np.array): 4x2 array defining the corners of a parallelogram

#     Returns:
#         tuple[int,int]: width, height
#     """
#     # define our points
#     a = quad[0]
#     b = quad[1]
#     c = quad[2]
#     # L2 norm is the euclidian distance between two points
#     # https://stackoverflow.com/questions/1401712
#     width = int(abs(np.linalg.norm(b-a)))
#     height = int(abs(np.linalg.norm(c-a)))
#     return width, height

# def unwarp_quadrilateral(
#     image:np.array,
#     quad:np.array,
#     margin=1,
# )->np.array:
#     """extracts a quadrilateral segment of an image and unwarps into a rectangle
#     trimming off a margin round the edge as desired

#     Args:
#         image (np.array): image to be unwarped
#         quad (np.array): 4x2 array designating the quadrilateral to be unwwarped
#         margin (int, optional): margin to trim from unwarped image. Defined in
#             pixels. Defaults to 1

#     Returns:
#         np.array: [description]
#     """
#     # drop uneeded axis if present
#     quad_2d = quad.reshape((4,2))
#     # calculate width and height of our quadrilateral (approx parallelogram)
#     width, height = get_parallelogram_dimensions(quad_2d)
#     # get our source quad in float 32
#     area_view = np.float32(quad_2d)
#     # define our target rectangle
#     area_target = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
#     # define a transform between the quad and the rectangle
#     transform = cv2.getPerspectiveTransform(area_view,area_target)
#     # apply that transform to our image
#     transformed_image = cv2.warpPerspective(image, transform, (width, height))
#     # edges tend to be untidy so crop in to aid OCR
#     cropped_image = transformed_image[margin:-margin,margin:-margin]
#     # imgCropped = cv2.resize(imgCropped,(widthImg,heightImg))

#     return cropped_image


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

        # clean_paper = ocr.

        # WE COULD OPTIONALLY SAVE THE CLEANED UP IMAGE HERE

        # greyscale rectified image

        # denoise

        # blur rectified image

        # threshhold rectified image

        # text detection (fast and avoids trying to detect non existent text)

        # get contours

        # pass to tesseract for OCR

        # output OCRed text

        # TEMP display codes

        # cv2.imshow("input_image", raw_image)
        print(preprocessed_image.shape)
        print(type(preprocessed_image))
        cv2.imshow("processed_image", preprocessed_image)
        cv2.imshow("unwarped_image", unwarped_paper)
        cv2.waitKey(WAIT_UNTIL_PRESSED)
        # cv2.destroyAllWindows()
