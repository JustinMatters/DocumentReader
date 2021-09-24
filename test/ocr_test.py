"""Test suite for ocrcode. Note that not all functions are tested.
Tests are implemented where:
    1) The function has a resonable chance of failure on complexity grounds
    2) The function implements logic rather than just chaining library functions
    3) the functionality can be tested with test data of reasonable size
Placeholder test classes exist for untested functions to allow future test
implementation
"""
import pytest
from ocrcode import ocr
import cv2
import numpy as np


class TestGetPaths:
    """Test class for ocr.get_paths (no tests for reason 2 above)"""

    pass


class TestScaleLongestAxis:
    """Test class for ocr.scale_longest_axis"""

    @pytest.mark.parametrize(
        # remember numpy arrays are h*w*d or y*x*d
        "y_in, x_in, scale, y_out, x_out",
        [
            # scale down
            (1024, 1024, 512, 512, 512),
            # scale up
            (10, 10, 512, 512, 512),
            # scale on non default scale
            (10, 10, 40, 40, 40),
            # scale on x
            (1200, 600, 512, 512, 256),
            # scale on y
            (300, 600, 512, 256, 512),
        ],
    )
    def test_correct_scaling(self, x_in, y_in, scale, x_out, y_out):
        # create a pseudo input image
        image_in = np.ones((x_in, y_in, 3))
        # create the expected output image
        expected_out = np.ones((x_out, y_out, 3))
        function_out = ocr.scale_longest_axis(image=image_in, new_size=scale)
        # check the output shapes are correct
        assert expected_out.shape == function_out.shape


class TestPreprocessImage:
    """Test class for ocr.preprocess_image (no tests for reason 2 above)"""

    pass


class TestGetContourFromMask:
    """Test class for ocr.get_contour_from_mask (no tests for reason 3 above)"""

    pass


class TestOrderQuadrilateral:
    """"Test class for ocr.order_quadrilateral"""

    @pytest.mark.parametrize(
        "quad_in,expected_quad",
        [
            (
                # trivial values already ordered
                np.array([[[0, 0]], [[1, 0]], [[0, 1]], [[1, 1]]]),
                np.array([[[0, 0]], [[1, 0]], [[0, 1]], [[1, 1]]]),
            ),
            (
                # trivial values
                np.array([[[0, 1]], [[1, 0]], [[1, 1]], [[0, 0]]]),
                np.array([[[0, 0]], [[1, 0]], [[0, 1]], [[1, 1]]]),
            ),
            (
                # non-trivial values
                np.array([[[241, 105]], [[62, 149]], [[126, 429]], [[308, 388]]]),
                np.array([[[62, 149]], [[241, 105]], [[126, 429]], [[308, 388]]]),
            ),
        ],
    )
    def test_correct_reordering(self, quad_in, expected_quad):
        # comparing np.arrays with == you get an array returned so use .all()
        assert (expected_quad == ocr.order_quadrilateral(quad=quad_in)).all()


class TestGetParallelogramDimensions:
    """Test class for ocr.get_parallelogram_dimensions"""

    @pytest.mark.parametrize(
        "quad_in,expected_width,expected_height",
        [
            (
                # trivial values, remember opencv goes height, width!
                np.array([[[0, 0]], [[1, 0]], [[0, 2]], [[1, 2]]]),
                1,
                2,
            ),
            (
                # offset trivial values, remember opencv goes height, width!
                np.array([[[10, 10]], [[11, 10]], [[10, 12]], [[11, 12]]]),
                1,
                2,
            ),
            (
                # pythagorean triangle test, remember opencv goes height, width!
                np.array([[[5, 10]], [[2,14 ]], [[9,13]], [[6,17]]]),
                5,
                5,
            )
        ],
    )
    def test_correct_measurement(self, quad_in, expected_width, expected_height):
        height, width = ocr.get_parallelogram_dimensions(quad=quad_in)
        assert expected_width == width and expected_height == height


class TestUnwarpQuadrilateral:
    """Test class for ocr.unwarp_quadrilateral (no tests for reason 2 above)"""

    pass
