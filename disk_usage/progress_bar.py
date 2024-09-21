class ProgressBar:
    def __init__(self, total: int):
        self._total = total
        self._current = 0

    @property
    def current_progress(self):
        return (self._current / self._total) * 100

    def update(self, step: int = 1):
        self._current += step