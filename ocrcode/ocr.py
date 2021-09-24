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
        # TBD for now default to returning our test image
        file_name = "data/business card.jpg"
        full_path = os.path.abspath(file_name)
        return [full_path]


def scale_longest_axis(image: np.ndarray, new_size=512):
    """resize an image so its longest axis (height or width) equals the 
    specified new size. Choose appropriate interpolation depending on whether 
    we are growing or shrinking

    Args:
        image (np.ndarray): input image
        new_size (int, optional): size of new maximum dimension. Defaults to 512

    Returns:
        (np.ndarray): resized image
    """
    # get current dimensions
    height, width = image.shape[0], image.shape[1]
    print(width, height)
    # find long axis then calculate new shape
    if width > height:
        # weirldy though image.shape is h*w*d resize is w*h !!
        new_dimensions = (new_size, int(height * new_size // width))
    else:
        # weirldy though image.shape is h*w*d resize is w*h !!
        new_dimensions = (int(width * new_size // height), new_size)
    print(new_dimensions)
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
    mask:np.array,
    min_area: int,
    epsilon:int,
):
    # get only external contours from the group
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    largest_quadrilateral = np.array([])
    largest_area = min_area
    # pick the largest quadrilateral contour we are assuming that will be the target
    for contour in contours:
        area = cv2.contourArea(contour)
        # check if contour is the largest we have found
        if area > largest_area:
            perimeter = cv2.arcLength(contour,closed=True)
            # simplify to a polygon
            # https://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
            simplified = cv2.approxPolyDP(contour,epsilon=(epsilon*perimeter),closed=True)
            # check if the polygon is quadrilateral and update our candidate if so
            if len(simplified) ==4:
                largest_quadrilateral = simplified
                largest_area = area           
    return largest_quadrilateral

def order_quadrilateral(quad:np.array):
    # reshape to drop the excess axis from cv2.findContours
    quad = quad.reshape((4,2))
    # gut our finished quad will need that axis for the next step
    ordered_quad = np.zeros((4,1,2), np.int32)
    # get top left and bottom right from max and min of sum of dimensions
    quad_sum = np.sum(quad, axis=1)
    ordered_quad[0] = quad[np.argmin(quad_sum)]
    ordered_quad[3] = quad[np.argmax(quad_sum)]
    # get bottom left and top right from max and min of dimension difference
    quad_diff = np.diff(quad, axis=1)
    ordered_quad[1] = quad[np.argmin(quad_diff)]
    ordered_quad[2] = quad[np.argmax(quad_diff)]
    return ordered_quad


if __name__ == "__main__":
    # we have no cause to run this file directly currently
    pass
