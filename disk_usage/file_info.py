import os
import time
from pathlib import Path


class FileInfo:
    def __init__(self, path: Path):
        self.path = path
        self.size = path.stat().st_size
        self.mtime = time.ctime(path.stat().st_mtime)
        self.extension = path.suffix
        self.level = len(path.parts)

        if os.name == 'posix':
            self.owner = path.owner()
        else:
            self.owner = 'N/A'