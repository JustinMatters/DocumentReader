"""Test suite for arguments.py"""

from mock import patch
import pytest
from ocrcode import arguments


class TestArgumentParser:
    """ Test class for arguments.argument_parser """

    @pytest.mark.parametrize(
        "params_in, expected",
        [
            (["file.jpg"], ["file.jpg"]),
            (["file.jpg", "-v"], ["file.jpg"]),
            (["file.jpg", "--verbose"], ["file.jpg"]),
            (["file.jpg", "-s", "dir"], ["file.jpg"]),
            (["file.jpg", "--save", "dir"], ["file.jpg"]),
            (["file.jpg", "-s", "dir", "-v"], ["file.jpg"]),
            (["file.jpg", "file2.jpg"], ["file.jpg", "file2.jpg"]),
            ([], []),
            (["-v"], []),
            (["-s", "dir", "-v", "-t", "dir2"], []),
        ],
    )
    def test_files_to_process_added_to_list(self, params_in, expected):
        files, _, _, _ = arguments.argument_parser(params_in)
        assert files == expected

    @pytest.mark.parametrize(
        "params_in, expected",
        [
            (["file.jpg", "-v"], None),
            (["file.jpg", "--verbose"], None),
            (["file.jpg", "-s", "dir", "-v"], "dir"),
            (["file.jpg", "-s", "dir", "--verbose", "-t", "dir2"], "dir"),
            (["file.jpg", "--save", "dir"], "dir"),
            (["file.jpg"], None),
        ],
    )
    def test_save_flag_returns_save_path_if_given(self, params_in, expected):
        _, save_path, _, _ = arguments.argument_parser(params_in)
        if save_path is None:
            assert save_path is expected
        else:
            assert save_path == expected

    @pytest.mark.parametrize(
        "params_in, expected",
        [
            (["file.jpg", "-v"], True),
            (["file.jpg", "--verbose"], True),
            (["file.jpg", "-s", "dir", "-v"], True),
            (["file.jpg", "-s", "dir", "--verbose"], True),
            (["file.jpg", "-s", "dir", "-t", "dir"], False),
            (["file.jpg"], False),
        ],
    )
    def test_verbose_flag_returns_verbose_true(self, params_in, expected):
        _, _, verbose, _ = arguments.argument_parser(params_in)
        assert verbose == expected

    @pytest.mark.parametrize(
        "params_in, expected",
        [
            (["file.jpg", "-v"], None),
            (["file.jpg", "-s", "dir", "--verbose"], None),
            (["file.jpg", "--tesseract", "dir"], "dir"),
            (["file.jpg", "-t", "dir"], "dir"),
            (["file.jpg", "-s", "dir", "--verbose", "-t", "dir"], "dir"),
        ],
    )
    def test_tesseract_flag_returns_tesseract_path(self, params_in, expected):
        _, _, _, tesseract = arguments.argument_parser(params_in)
        assert tesseract == expected


class TestPathsToFiles:
    """ Test class for arguments.argument_parser """

    @patch("os.path.isdir")
    @patch("os.path.isfile")
    def test_returns_empty_list_for_invalid_file(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = False
        with pytest.raises(FileNotFoundError):
            arguments.paths_to_files(["invalid"])

    @patch("os.path.isdir")
    @patch("os.path.isfile")
    def test_raises_error_if_not_image(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        with pytest.raises(FileNotFoundError):
            arguments.paths_to_files(["valid.txt"])

    @patch("os.path.isdir")
    @patch("os.path.isfile")
    def test_returns_list_if_valid_image(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        assert arguments.paths_to_files(["valid.jpg"]) == ["valid.jpg"]

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("os.path.isfile")
    def test_returns_list_if_valid_dir(
        self, mock_isfile, mock_isdir, mock_listdir,
    ):
        mock_isdir.return_value = True
        mock_isfile.return_value = True
        mock_listdir.return_value = ["valid.jpg", "other.txt"]
        assert arguments.paths_to_files(["dir/"]) == ["dir/valid.jpg"]

    @patch("os.listdir")
    @patch("os.path.isdir")
    @patch("os.path.isfile")
    def test_returns_empty_list_if_valid_dir_but_not_image(
        self, mock_isfile, mock_isdir, mock_listdir,
    ):
        mock_isdir.return_value = True
        mock_isfile.return_value = True
        mock_listdir.return_value = ["valid.txt"]
        with pytest.raises(FileNotFoundError):
            arguments.paths_to_files(["dir/"])


class TestValidateSave:
    """ Test class for arguments.argument_parser """

    @patch("os.path.isdir")
    @patch("os.getcwd")
    def test_returns_none_when_no_save(self, mock_getcwd, mock_isdir):
        mock_getcwd.return_value = "cwd"
        mock_isdir.return_value = False
        assert arguments.validate_save(save_path=None) is None

    @patch("os.path.isdir")
    @patch("os.getcwd")
    def test_returns_cwd_when_no_parameter(self, mock_getcwd, mock_isdir):
        mock_getcwd.return_value = "cwd"
        mock_isdir.return_value = False
        assert arguments.validate_save(save_path="||cwd||") == "cwd"

    @patch("os.path.isdir")
    @patch("os.getcwd")
    def test_returns_valid_path(self, mock_getcwd, mock_isdir):
        mock_getcwd.return_value = "cwd"
        mock_isdir.return_value = True
        assert arguments.validate_save(save_path="valid") == "valid"

    @patch("os.path.isdir")
    @patch("os.getcwd")
    def test_raises_exception_for_invalid_path(self, mock_getcwd, mock_isdir):
        mock_getcwd.return_value = "cwd"
        mock_isdir.return_value = False
        with pytest.raises(Exception):
            arguments.validate_save(save_path="invalid")


class TestValidateTesseract:
    @patch("os.path.isfile")
    def test_returns_none_when_passed_none(self, mock_isfile):
        mock_isfile.return_value = False
        assert arguments.validate_tesseract(None) is None

    @patch("os.path.isfile")
    def test_returns_valid_tesseract_path(self, mock_isfile):
        mock_isfile.return_value = True
        input = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        expected = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        assert arguments.validate_tesseract(input) == expected

    @patch("os.path.isfile")
    def test_raises_error_for_invalid_path(self, mock_isfile):
        mock_isfile.return_value = False
        with pytest.raises(FileNotFoundError):
            arguments.validate_tesseract("invalid")

    @patch("os.path.isfile")
    def test_raises_error_for_non_tesseract_path(self, mock_isfile):
        mock_isfile.return_value = True
        with pytest.raises(FileNotFoundError):
            arguments.validate_tesseract("C:\\Program Files\\other.exe")
