from itertools import groupby
from typing import Optional, List, Iterator
from disk_usage.file_info import FileInfo

class FileFilter:
    def __init__(self, files: List[FileInfo]):
        self.files = files

    def filter_by_extension(self, extension: str) -> List[FileInfo]:
        return list(filter(lambda file: file.extension == extension, self.files))

    def filter_by_owner(self, owner: str) -> List[FileInfo]:
        return list(filter(lambda file: file.owner == owner, self.files))

    def filter_by_size(self, min_size: Optional[int] = None, max_size: Optional[int] = None) -> List[FileInfo]:
        return list(filter(lambda file: (min_size is None or file.size >= min_size) and
                                      (max_size is None or file.size <= max_size), self.files))

    def filter_by_level(self, level):
        return list(filter(lambda file: file.level == level, self.files))

    def group_by_extension(self) -> Iterator:
        self.files.sort(key=lambda file: file.extension)
        return groupby(self.files, lambda file: file.extension)

    def group_by_owner(self) -> Iterator:
        self.files.sort(key=lambda file: file.owner)
        return groupby(self.files, lambda file: file.owner)

    def group_by_level(self) -> Iterator:
        self.files.sort(key=lambda file: file.level)
        return groupby(self.files, lambda file: file.level)
