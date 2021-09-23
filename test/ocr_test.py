import pytest
from ocrcode import ocr
import cv2
import numpy as np

class TestScaleLongestAxis:
    """Test Class for ocr.scale_longest_axis"""

    @pytest.mark.parametrize(
        # remember numpy arrays are h*w*d or y*x*d
        'y_in, x_in, scale, y_out, x_out',
        [
            # scale down
            (1024,1024,512,512,512),
            #scale up
            (10,10,512,512,512),
            # scale on non default scale
            (10,10,40,40,40),
            # scale on x
            (1200,600,512,512,256),
            # scale on y
            (300,600,512,256,512),
        ]
    )
    def test_correct_scaling(self, x_in, y_in, scale, x_out, y_out):
        # create a pseudo input image
        image_in = np.ones((x_in,y_in,3))
        # create the expected output image
        expected_out = np.ones((x_out,y_out,3))
        function_out = ocr.scale_longest_axis(
            image = image_in, 
            new_size = scale
        )
        # check the output shapes are correct
        assert expected_out.shape  == function_out.shape