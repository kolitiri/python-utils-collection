# Standard library imports
import os
import hashlib


def get_files(directory):
    """ Recursively yield all the files from a
        directory tree.

        Yields:
            One by one the files under the directory tree
    """

    for root_dir, directories, files in os.walk(directory):

        # Ignore hidden files
        files = [file for file in files if not file[0] == '.']

        for file in files:
            yield os.path.join(os.path.abspath(root_dir), file)

def is_file_empty(file):
    """ A function that checks whether a file is empty.

        Args:
            input_file: The file to process

        Returns:
            True:  If file is empty
            False: If file is not empty
    """

    if os.stat(file).st_size > 0:
        return False
    else:
        return True

def get_md5_hash(filename):
    """ Calculate the MD5 checksum of a file.
        Args:
            filename: The file to be hashed

        Returns:
            The MD5 checksum of the file
    """

    chunk_size = 65536
    hasher = hashlib.md5()

    with open(filename, 'rb') as target_file:

        buffer_ = target_file.read(chunk_size)

        while len(buffer_) > 0:
            hasher.update(buffer_)
            buffer_ = target_file.read(chunk_size)

    return hasher.hexdigest()


# for file in get_files('../file_operations'):
#     print(file)

# print(is_file_empty('file_operations.py'))

# hash_ = get_md5_hash('file_operations.py')
# print(hash_)
