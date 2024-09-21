import asyncio
import os
from pathlib import Path
from typing import List

import psutil

from disk_usage.file_info import FileInfo
from disk_usage.progress_bar import ProgressBar


class DiskAnalyzer:
    def __init__(self, root: Path):
        self._root = root
        self._files = list()
        self._progress_bar = None

    @property
    def files(self) -> List[FileInfo]:
        return self._files

    @property
    def current_progress(self) -> float:
        return 0 if self._progress_bar is None else self._progress_bar.current_progress

    async def disk_usage(self):
        return await asyncio.to_thread(self._disk_usage_sync)

    async def analyze(self):
        total_files = sum(len(files) for _, _, files in os.walk(self._root))
        self._progress_bar = ProgressBar(total_files)

        await asyncio.to_thread(self._analyze_sync)

    def _disk_usage_sync(self):
        usage = psutil.disk_usage(str(self._root))
        return usage.used, usage.total

    def _analyze_sync(self):
        for directory, _, filenames in os.walk(self._root):
            for filename in filenames:
                filepath = Path(directory) / filename
                file_info = FileInfo(filepath)

                self._files.append(file_info)
                self._progress_bar.update()
