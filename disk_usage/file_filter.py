from datetime import datetime
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

    def filter_by_time(self, min_date: str = None, max_date: str = None) -> List[FileInfo]:
        def date(file: FileInfo) -> bool:
            file_mtime = datetime.strptime(file.mtime, "%a %b %d %H:%M:%S %Y")
            min_dt = datetime.strptime(min_date, '%d.%m.%Y') if min_date else None
            max_dt = datetime.strptime(max_date, '%d.%m.%Y') if max_date else None

            return ((min_dt is None or file_mtime >= min_dt) and
                    (max_dt is None or file_mtime <= max_dt))

        return list(filter(date, self.files))

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
