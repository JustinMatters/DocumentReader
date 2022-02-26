import argparse
import os
import sys


def argument_parser(args):
    """ Use argparse to allow for the processing of input paths, a save location
    and adjusting the verbosity of the program. we pass args explicitly to
    simplify testing

    Args:
        args (list(str)): list of sys.argv arguments excluding the program name 

    Returns:
        image_paths (list(str)): List of image paths
        save_path (str): Directory path to save outputs to
        verbose (bool): Whether or not to provide verbose output
        tesseract_path (str): Absolute path to tesseract.exe 
    """
    parser = argparse.ArgumentParser(
        description="Process images to straighten images and extract text",
    )
    parser.add_argument(
        "paths",
        metavar="N",
        type=str,
        nargs="*",  # ? is zero or one, * is zero or more, + is one or more
        help="File or folder paths. Files must be jpg, png or gif",
    )
    parser.add_argument(
        "-s",
        "--save",
        required=False,
        type=str,
        nargs="?",
        default=None,  # returned if argument not used
        const="||cwd||",  # returned if argument has no trailing parameter
        help="Save data to current working directory or a specified folder",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display intermediate steps in processing",
    )
    parser.add_argument(
        "-t",
        "--tesseract",
        required=False,
        type=str,
        default=None,  # returned if argument not used
        help="Specify location of tesseract.exe",
    )
    parsed = parser.parse_args(args)
    image_paths = parsed.paths
    save_path = parsed.save
    verbose = parsed.verbose
    tesseract_path = parsed.tesseract
    return image_paths, save_path, verbose, tesseract_path


def paths_to_files(paths):
    """ Convert our list of files and folders into a pure list of files. Folders
    are expanded to their constituent files (non-recursively) and all files are
    validated as image files by examining files extensions. Only valid files are
    returned. If no valid files are found, a FileNotFoundError error is raised

    Args:
        paths (list(str)): a list of paths to convert
    
    Returns
        (list(str)): a list of image file locations
    """
    files = []
    for path in paths:
        # only explore the specified directory, this is not a recursive search
        if os.path.isdir(path):
            _files = [
                os.path.join(path, file)
                for file in os.listdir(path)
                if os.path.isfile(os.path.join(path, file))
            ]
            files.extend(_files)
        else:
            if os.path.isfile(path):
                files.append(path)
    # take only image files we can read
    valid_files = []
    for file in files:
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            valid_files.append(file)
    if len(valid_files) > 0:
        return valid_files
    else:
        raise FileNotFoundError("No valid input image files specified")


def validate_save(save_path: str):
    """ Validate that a save path is a valid folder. If no save path was 
    specified then the current working directory will be returned. If an invalid
    save path is specified, a NotADirectoryError error is raised.
    
    Args:
        path: Directory path to be validated

    Returns:
        (str or None): None if passed None, otherwise directory path if valid
    """
    if save_path is None:
        return None
    elif save_path == "||cwd||":
        return os.getcwd()
    elif os.path.isdir(save_path):
        return save_path
    else:
        raise NotADirectoryError("invalid save path specified")


def validate_tesseract(tesseract_path: str):
    """ validate that the tesseract path is valid folder else raise an error
    
    Args:
        tesseract_path: Directory path to be validated

    Returns:
        (str or None): None if passed None, otherwise directory path if valid
    """
    if tesseract_path is None:
        return None
    if os.path.isfile(tesseract_path) and tesseract_path[-13:] == "tesseract.exe":
        return tesseract_path
    else:
        raise FileNotFoundError("Location specified is not a tesseract.exe file")


if __name__ == "__main__":
    # we don't expect to call this library direct, but just in case
    paths, save_path, verbose, tesseract = argument_parser(sys.argv[1:])
    print(f"paths: {paths}, -s {save_path}, -v {verbose}, -t, {tesseract}")
    valid_files = paths_to_files(paths)
    print(f"valid_files: {valid_files}")
    save_path = validate_save(save_path)
    print(f"validated save path: {save_path}")
    tesseract = validate_tesseract(tesseract)
    print(f"validated tesseract path: {tesseract}")
