import argparse
import os
import sys

def argument_parser(args):
    ''' Use argparse to allow for the processing of input paths, a save location
    and adjusting the verbosity of the program. we pass args explicitly to
    simplify testing

    Args:
        args (list(str)): list of sys.argv arguments excluding the program name 

    Returns:
        image_paths (list(str)): List of image paths
        save_path (str): Directory path to save outputs to
        verbose (bool): whether or not to provide verbose output
    '''
    parser = argparse.ArgumentParser(
        description = 'Process images to straighten images and extract text',
    )
    parser.add_argument(
        'paths',
        metavar='N',
        type=str,
        nargs='*', # ? is zero or one, * is zero or more, + is one or more
        help='File or folder paths. If not specified, will read files from /data',
    )
    parser.add_argument(
        '-s',
        '--save',
        required = False,
        type = str,
        nargs='?',
        default = None,
        help='Save data to specified folder',
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Display intermediate steps in processing',
    )
    parsed = parser.parse_args(args)
    image_paths = parsed.paths
    print(image_paths)
    save_path = parsed.save
    print(save_path)
    verbose = parsed.verbose
    print(verbose)
    return image_paths, save_path, verbose

def paths_to_files(paths):
    ''' Convert our list of files and folders into a pure list of files. Folders
    are expanded to their constituent files (non-recursively) and all files are
    validated as image files by examining files extensions. Only valid files are
    returned

    Args:
        paths (list(str)): a list of paths to convert
    
    Returns
        (list(str)): a list of image file locations
    '''
    files = []
    for path in paths:
        # only explore the specified directory, this is not a recursive search
        if os.path.isdir(path):
            _files = [
                os.path.join(path, file) for file in os.listdir(path) if
                os.path.isfile(os.path.join(path, file))
            ]
            files.extend(_files)
        else:
            if os.path.isfile(path):
                files.append(path)
    print(files)
    # take only image files we can read
    valid_files = []
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            valid_files.append(file)
    return valid_files

def validate_save(save_path: str):
    ''' validate that a save path is a valid folder else return None
    
    Args:
        path: Directory path to be validated

    Returns:
        (str or None): directory path if valid else None
    '''
    if save_path is not None and os.path.isdir(save_path):
        return save_path
    else:
        return None
    
if __name__ == "__main__":
    # we don't expect to call this library direct, but just in case
    paths, save_path, verbose = argument_parser(sys.argv[1:])
    print(f'paths: {paths}, save_path {save_path}, verbose, {verbose}')
    valid_files = paths_to_files(paths)
    print(f'valid_files: {valid_files}')
    save_path = validate_save(save_path)
    print(f'validated save path: {save_path}')

