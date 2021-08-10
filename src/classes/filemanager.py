import os
from typing import Dict, List
from src.classes.labelled_img import Labelled_Img


# class File():

#     def __init__(self, dirpath, filepath) -> None:


class FileManager():
    dirpath: str = None  # the directory currently opened
    filepaths: List[str]  # list of filepaths

    def __init__(self) -> None:
        pass

    def open_dir(self, dirpath):
        self.dirpath = dirpath
        self.filepaths = [x for x in os.listdir(dirpath) if x.endswith((".jpg", ".png"))]

