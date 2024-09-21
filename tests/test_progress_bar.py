import pytest
from disk_usage import ProgressBar

def test_initial_progress():
    bar = ProgressBar(100)
    assert bar.current_progress == 0


def test_progress_update():
    bar = ProgressBar(100)
    bar.update(25)
    assert bar.current_progress == 25

    bar.update(25)
    assert bar.current_progress == 50


def test_progress_over_total():
    bar = ProgressBar(100)
    bar.update(150)
    assert bar.current_progress == 150


def test_progress_with_zero_total():
    bar = ProgressBar(0)
    with pytest.raises(ZeroDivisionError):
        bar.current_progress