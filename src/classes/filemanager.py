import os
from typing import Dict, List

# class File():

#     def __init__(self, dirpath, filepath) -> None:
        

class FileManager():
    """
    root_dir: path to the root folder of the dataset
    filepaths: A list of separate images not contained within the root dir
    """

    root_dir: str = None # path to the dataset directory
    filepaths: List[str] # list of separate, "non-dir files"

    def set_root_dir(self, new_dir_path):
        self.rootdirpath = new_dir_path