import cv2
import numpy as np
import os
import sys

def get_paths(*file_names : str):
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
        file_name = 'data/business card.jpg'
        full_path = os.path.abspath(file_name)
        return [full_path]

def scale_longest_axis(image: np.ndarray, new_size = 512):
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
        new_dimensions = (new_size, int(height*new_size//width))
    else:
        # weirldy though image.shape is h*w*d resize is w*h !!
        new_dimensions = (int(width*new_size//height), new_size)
    print(new_dimensions)
    # are we growing or shrinking - we need appropriate interpolation
    if width > new_size or height > new_size:
        # shrinking 
        interpolation = cv2.INTER_AREA
    else:
        # growing
        interpolation = cv2.INTER_CUBIC
    # rescale
    return cv2.resize(image, new_dimensions, interpolation = interpolation)

if __name__ == '__main__':
    # we have no cause to run this file directly currently
    pass