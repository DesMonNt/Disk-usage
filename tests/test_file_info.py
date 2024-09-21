import pytest
import time
from pathlib import Path
from disk_usage import FileInfo

def test_file_info_initialization(mocker):
    mock_path = mocker.Mock(spec=Path)
    mock_path.stat.return_value.st_size = 1024
    mock_path.stat.return_value.st_mtime = time.time()
    mock_path.suffix = '.txt'
    mock_path.parts = ('folder', 'subfolder', 'file.txt')

    mocker.patch('os.name', 'posix')
    mock_path.owner = mocker.Mock(return_value='user123')

    file_info = FileInfo(mock_path)

    assert file_info.size == 1024
    assert file_info.mtime == time.ctime(mock_path.stat.return_value.st_mtime)
    assert file_info.extension == '.txt'
    assert file_info.level == 3
    assert file_info.owner == 'user123'


def test_file_info_windows_owner(mocker):
    mock_path = mocker.Mock(spec=Path)
    mock_path.stat.return_value.st_size = 2048
    mock_path.stat.return_value.st_mtime = time.time()
    mock_path.suffix = '.jpg'
    mock_path.parts = ('folder', 'image.jpg')

    mocker.patch('os.name', 'nt')

    file_info = FileInfo(mock_path)

    assert file_info.size == 2048
    assert file_info.extension == '.jpg'
    assert file_info.level == 2
    assert file_info.owner == 'N/A'


def test_file_info_empty_path(mocker):
    mock_path = mocker.Mock(spec=Path)
    mock_path.stat.side_effect = FileNotFoundError
    mock_path.parts = []

    with pytest.raises(FileNotFoundError):
        FileInfo(mock_path)