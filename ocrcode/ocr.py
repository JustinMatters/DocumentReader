import cv2
import numpy as np
import os
import sys


def get_paths(*file_names: str):
    """given a file string or list of file strings, returns a list of full paths
    to images

    Args:
        file_names (string, optional, *arg): file location string or strings

    Returns:
        list(str): List of absolute paths
    """
    # check if we were passed any file names
    if len(file_names) > 0:
        files_list = []
        for file_name in file_names:
            full_path = os.path.abspath(file_name)
            files_list.append(full_path)
        return files_list
    else:
        raise FileNotFoundError("No valid input image files specified")


def scale_longest_axis(image: np.array, new_size=512) -> np.array:
    """resize an image so its longest axis (height or width) equals the 
    specified new size. Choose appropriate interpolation depending on whether 
    we are growing or shrinking

    Args:
        image (np.array): input image
        new_size (int, optional): size of new maximum dimension. Defaults to 512

    Returns:
        np.array: resized image
    """
    # get current dimensions
    height, width = image.shape[0], image.shape[1]
    # find long axis then calculate new shape
    if width > height:
        # weirldy though image.shape is h*w*d resize is w*h !!
        new_dimensions = (new_size, int(height * new_size // width))
    else:
        # weirldy though image.shape is h*w*d resize is w*h !!
        new_dimensions = (int(width * new_size // height), new_size)
    # are we growing or shrinking - we need appropriate interpolation
    if width > new_size or height > new_size:
        # shrinking
        interpolation = cv2.INTER_AREA
    else:
        # growing
        interpolation = cv2.INTER_CUBIC
    # rescale
    return cv2.resize(image, new_dimensions, interpolation=interpolation)


def preprocess_image(
    image: np.array,
    blur: int,
    threshold_high: int,
    threshold_low: int,
    kernel_size: int,
) -> np.array:
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
    # greyscale
    processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blur
    processed_image = cv2.GaussianBlur(processed_image, (blur, blur), 0)
    # edge detect
    processed_image = cv2.Canny(processed_image, threshold_high, threshold_low)
    # dilate and erode our edge detections
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    processed_image = cv2.dilate(processed_image, kernel, iterations=2)
    processed_image = cv2.erode(processed_image, kernel, iterations=1)
    return processed_image


def get_contour_from_mask(
    mask: np.array, min_area: int, epsilon: int, contour_check: np.array, verbose=True,
) -> np.array:
    """takes a black and white input image and returns the largest continuous
    quadrilateral contour found

    Args:
        mask (np.array): monochrome image (white are areas to be contoured)
        min_area (int): minimum area of quads to be allowed in pixels
        epsilon (int): tuning parameter for cv2.approxPolyDP
            See https://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
        contour_check (numpy.array): image to allow visual investigation 
            of contouring

    Returns:
        np.array: [description]
    """
    # get only external contours from the group
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest_quadrilateral = np.array([[[0, 0]], [[10, 0]], [[0, 10]], [[10, 10]]])
    largest_area = min_area
    # pick the largest quadrilateral contour we are assuming that will be the target
    for contour in contours:
        area = cv2.contourArea(contour)
        cv2.drawContours(contour_check, contour, -1, (255, 0, 0), 3)  ###
        # check if contour is the largest we have found
        if area > largest_area:
            perimeter = cv2.arcLength(contour, closed=True)
            # simplify to a polygon
            # https://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
            simplified = cv2.approxPolyDP(
                contour, epsilon=(epsilon * perimeter), closed=True
            )
            # check if the polygon is quadrilateral and update our candidate if so
            if len(simplified) == 4:
                largest_quadrilateral = simplified
                largest_area = area
    if verbose:
        cv2.imshow("contours", contour_check)  ###
    return largest_quadrilateral


def order_quadrilateral(quad: np.array) -> np.array:
    """reorganise 4 points expressed as a numpy array to the correct order

    Args:
        quad (np.array): 4x2 array defining the corners of a quadrilateral

    Returns:
        np.array: correctly ordered 4x2 array defining the corners of a 
            quadrilateral
    """
    # reshape to drop the excess axis from cv2.findContours if present
    quad = quad.reshape((4, 2))
    # gut our finished quad will need that axis for the next step
    ordered_quad = np.zeros((4, 1, 2), np.int32)
    # get top left and bottom right from max and min of sum of dimensions
    quad_sum = np.sum(quad, axis=1)
    ordered_quad[0] = quad[np.argmin(quad_sum)]
    ordered_quad[3] = quad[np.argmax(quad_sum)]
    # get bottom left and top right from max and min of dimension difference
    quad_diff = np.diff(quad, axis=1)
    ordered_quad[1] = quad[np.argmin(quad_diff)]
    ordered_quad[2] = quad[np.argmax(quad_diff)]
    return ordered_quad


def get_parallelogram_dimensions(quad: np.array) -> "tuple[int,int]":
    """gets the width and height of a parallelogram whose corner coordinates
    are defined in a np.array((4,2)) 

    Args:
        quad (np.array): 4x2 array defining the corners of a parallelogram

    Returns:
        tuple[int,int]: width, height
    """
    # define our points
    top_left = quad[0]
    top_right = quad[1]
    bottom_left = quad[2]
    # L2 norm is the euclidian distance between two points
    # https://stackoverflow.com/questions/1401712
    width = int(abs(np.linalg.norm(top_right - top_left)))
    height = int(abs(np.linalg.norm(bottom_left - top_left)))
    return height, width


def unwarp_quadrilateral(image: np.array, quad: np.array, margin=1,) -> np.array:
    """extracts a quadrilateral segment of an image and unwarps into a rectangle
    trimming off a margin round the edge as desired

    Args:
        image (np.array): image to be unwarped
        quad (np.array): 4x2 array designating the quadrilateral to be unwwarped
        margin (int, optional): margin to trim from unwarped image. Defined in
            pixels. Defaults to 1

    Returns:
        np.array: [description]
    """
    # drop uneeded axis if present
    quad_2d = quad.reshape((4, 2))
    # calculate height and width of our quadrilateral (approx parallelogram)
    height, width = get_parallelogram_dimensions(quad_2d)
    # get our source quad in float 32
    area_view = np.float32(quad_2d)
    # define our target rectangle
    area_target = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # define a transform between the quad and the rectangle
    transform = cv2.getPerspectiveTransform(area_view, area_target)
    # apply that transform to our image
    transformed_image = cv2.warpPerspective(image, transform, (width, height))
    # edges tend to be untidy so crop in to aid OCR
    cropped_image = transformed_image[margin:-margin, margin:-margin]
    # imgCropped = cv2.resize(imgCropped,(widthImg,heightImg))
    return cropped_image


def improve_image_quality(
    image: np.array, threshold: str = "simple", verbose=True
) -> np.array:
    """ improve the image quality for processing by OCR

    Args:
        image (np.array): input image containing text
        threshold (str, optional): threshold method, uses a string to 
            pick to avoid invalid methods being passed. Options are:
            "simple": generally prefered for simple images
            "adaptive": may help with local shodowing
            "otsu": useful for bimodal images eg poor exposure
            Defaults to "simple".

    Returns:
        np.array: image optimised for OCR
    """
    # greyscale rectified image
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # magnify thie image before processing
    large_image = cv2.resize(
        grey_image, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC
    )
    # denoise with a median blur
    median_image = cv2.medianBlur(large_image, ksize=3)
    if verbose:
        cv2.imshow("medianblur", median_image)
    # threshhold image see https://stackoverflow.com/questions/28763419/
    if threshold == "adaptive":
        threshold_image = cv2.adaptiveThreshold(
            median_image,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=31,
            C=2,
        )
    elif threshold == "otsu":
        threshold_image = cv2.threshold(
            median_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]
    else:
        threshold_image = cv2.threshold(median_image, 127, 255, cv2.THRESH_BINARY)[1]
    if verbose:
        cv2.imshow("threshold", threshold_image)
    return threshold_image


if __name__ == "__main__":
    # we have no cause to run this file directly currently
    pass
