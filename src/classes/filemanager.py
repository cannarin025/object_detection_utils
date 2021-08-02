import os
from typing import Dict, List

# class File():

#     def __init__(self, dirpath, filepath) -> None:
        

class FileManager():

    dir_opened: bool = False
    dirpath: str = None # the directory currently opened
    filepaths: List[str] # list of separate, "non-dir files"

    def __init__(self) -> None:
        pass