import argparse
import os

def argument_parser():
    ''' Use argparse to allow for the processing of input paths, a save location
    and adjusting the verbosity of the program
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
    parsed = parser.parse_args()
    paths = parsed.paths
    print(paths)
    save_path = parsed.save
    print(save_path)
    verbose = parsed.verbose
    print(verbose)
    return paths, save_path, verbose

def paths_to_files(paths):
    ''' Convert our list of files and folders into a pure list of files
    '''
    files = []
    for path in paths:
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
        if file.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')):
            valid_files.append(file)
    return valid_files

def validate_save(save_path: str):
    ''' validate that a save path is a valid folder'''
    if save_path is not None and os.path.isdir(save_path):
        return save_path
    else:
        return None
    

if __name__ == "__main__":
    # we don't expect to call this library direct, but just in case
    paths, save_path, verbose = argument_parser()
    print(f'paths: {paths}, save_path {save_path}, verbose, {verbose}')
    valid_files = paths_to_files(paths)
    print(f'valid_files: {valid_files}')
    save_path = validate_save(save_path)
    print(f'validated save path: {save_path}')

