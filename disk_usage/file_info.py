import os
import time
from pathlib import Path


class FileInfo:
    def __init__(self, path: Path, root: Path = None):
        self.path = path
        self.size = path.stat().st_size
        self.mtime = time.ctime(path.stat().st_mtime)
        self.extension = path.suffix
        self.level = len(path.parts) - (len(root.parts) if root else 0)

        if os.name == 'posix':
            self.owner = path.owner()
        else:
            self.owner = 'N/A'