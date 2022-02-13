"""Test suite for ocrcode. Note that not all functions are tested.
Tests are implemented where:
    1) The function has a resonable chance of failure on complexity grounds
    2) The function implements logic rather than just chaining library functions
    3) the functionality can be tested with test data of reasonable size
Placeholder test classes exist for untested functions to allow future test
implementation
"""
from cv2 import exp
from mock import patch
import os
import pytest
from ocrcode import arguments

class TestArgumentParser:
    """ Test class for arguments.argument_parser """

    @pytest.mark.parametrize(
        'params_in, expected',
        [
            (['file.jpg'], ['file.jpg']),
            (['file.jpg', '-v'], ['file.jpg']),
            (['file.jpg', '--verbose'], ['file.jpg']),
            (['file.jpg', '-s', 'dir'], ['file.jpg']),
            (['file.jpg', '--save', 'dir'], ['file.jpg']),
            (['file.jpg', '-s', 'dir', '-v'], ['file.jpg']),
            (['file.jpg', 'file2.jpg'], ['file.jpg', 'file2.jpg']),
            ([], []),
            (['-v'], []),
            (['-s', 'dir', '-v'], []),
        ]
    )
    def test_files_to_process_added_to_list(self, params_in, expected):
        files, _, _ = arguments.argument_parser(params_in)
        assert files == expected

    @pytest.mark.parametrize(
        'params_in, expected',
        [
            (['file.jpg', '-v'], None),
            (['file.jpg', '--verbose'], None),
            (['file.jpg', '-s', 'dir', '-v'], 'dir'),
            (['file.jpg', '-s', 'dir', '--verbose'], 'dir'),
            (['file.jpg', '--save', 'dir'], 'dir'),
            (['file.jpg'], None),
        ]
    )
    def test_verbose_flag_returns_save_path_if_given(self, params_in, expected):
        _, save_path, _ = arguments.argument_parser(params_in)
        if save_path is None:
            assert save_path is expected
        else:
            assert save_path == expected

    @pytest.mark.parametrize(
        'params_in, expected',
        [
            (['file.jpg', '-v'], True),
            (['file.jpg', '--verbose'], True),
            (['file.jpg', '-s', 'dir', '-v'], True),
            (['file.jpg', '-s', 'dir', '--verbose'], True),
            (['file.jpg', '-s', 'dir'], False),
            (['file.jpg'], False),
        ]

    )
    def test_verbose_flag_returns_verbose_true(self, params_in, expected):
        _, _, verbose = arguments.argument_parser(params_in)
        assert verbose == expected


class TestPathsToFiles:
    """ Test class for arguments.argument_parser """

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_returns_empty_list_for_invalid_file(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = False
        assert arguments.paths_to_files(['invalid']) == []

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_returns_empty_list_if_not_image(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        assert arguments.paths_to_files(['valid.txt']) == []

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_returns_list_if_valid_image(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        assert arguments.paths_to_files(['valid.jpg']) == ['valid.jpg']

    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_returns_list_if_valid_dir(
        self, 
        mock_isfile, 
        mock_isdir,
        mock_listdir,
    ):
        mock_isdir.return_value = True
        mock_isfile.return_value = True
        mock_listdir.return_value = ['valid.jpg', 'other.txt']
        assert arguments.paths_to_files(['dir/']) == ['dir/valid.jpg']

    @patch('os.listdir')
    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_returns_list_if_valid_dir_but_not_image(
        self, 
        mock_isfile, 
        mock_isdir,
        mock_listdir,
    ):
        mock_isdir.return_value = True
        mock_isfile.return_value = True
        mock_listdir.return_value = ['valid.txt']
        assert arguments.paths_to_files(['dir/']) == []

class TestValidateSave:
    """ Test class for arguments.argument_parser """

    @patch('os.path.isdir')
    def test_returns_valid_path(self, mock_isdir):
        mock_isdir.return_value = True
        assert arguments.validate_save(save_path = 'valid') == 'valid'

    @patch('os.path.isdir')
    def test_returns_none_for_invalid_path(self, mock_isdir):
        mock_isdir.return_value = False
        assert arguments.validate_save(save_path = 'invalid') is None