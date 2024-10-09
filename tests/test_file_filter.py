from datetime import datetime

import pytest
from disk_usage import FileFilter
from disk_usage import FileInfo


@pytest.fixture
def mock_file_info(mocker):
    return [
        mocker.Mock(spec=FileInfo, size=100, extension='.txt', owner='user1', level=2,
                    mtime='Mon Jan 02 10:00:00 2023'),
        mocker.Mock(spec=FileInfo, size=200, extension='.jpg', owner='user2', level=3,
                    mtime='Wed Feb 15 15:00:00 2023'),
        mocker.Mock(spec=FileInfo, size=150, extension='.txt', owner='user1', level=1,
                    mtime='Tue Mar 28 12:00:00 2023'),
        mocker.Mock(spec=FileInfo, size=250, extension='.png', owner='user3', level=2,
                    mtime='Fri Jul 21 18:00:00 2023'),
    ]


def test_filter_by_extension(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    result = file_filter.filter_by_extension('.txt')
    assert len(result) == 2
    assert all(file.extension == '.txt' for file in result)


def test_filter_by_owner(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    result = file_filter.filter_by_owner('user1')
    assert len(result) == 2
    assert all(file.owner == 'user1' for file in result)


def test_filter_by_size(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    result = file_filter.filter_by_size(min_size=150)
    assert len(result) == 3
    assert all(file.size >= 150 for file in result)

    result = file_filter.filter_by_size(max_size=150)
    assert len(result) == 2
    assert all(file.size <= 150 for file in result)

def test_filter_by_time_min_date(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    min_date = datetime.strptime("01.03.2023", "%d.%m.%Y")
    max_date = datetime.strptime("01.03.2024", "%d.%m.%Y")
    result = file_filter.filter_by_time(min_date="01.03.2023")
    assert len(result) == 2
    assert all(datetime.strptime(file.mtime, "%a %b %d %H:%M:%S %Y") >= min_date for file in result)
    assert all(datetime.strptime(file.mtime, "%a %b %d %H:%M:%S %Y") <= max_date for file in result)

def test_filter_by_level(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    result = file_filter.filter_by_level(2)
    assert len(result) == 2
    assert all(file.level == 2 for file in result)

def test_group_by_extension(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    grouped = list(file_filter.group_by_extension())
    assert len(grouped) == 3
    assert grouped[0][0] == '.jpg'
    assert len(list(grouped[0][1])) == 0


def test_group_by_owner(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    grouped = list(file_filter.group_by_owner())
    assert len(grouped) == 3
    assert grouped[0][0] == 'user1'
    assert len(list(grouped[0][1])) == 0


def test_group_by_level(mock_file_info):
    file_filter = FileFilter(mock_file_info)
    grouped = list(file_filter.group_by_level())
    assert len(grouped) == 3
    assert grouped[0][0] == 1
    assert len(list(grouped[0][1])) == 0
