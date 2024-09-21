import pytest
from disk_usage import FileFilter
from disk_usage import FileInfo


@pytest.fixture
def mock_file_info(mocker):
    return [
        mocker.Mock(spec=FileInfo, size=100, extension='.txt', owner='user1', level=2),
        mocker.Mock(spec=FileInfo, size=200, extension='.jpg', owner='user2', level=3),
        mocker.Mock(spec=FileInfo, size=150, extension='.txt', owner='user1', level=1),
        mocker.Mock(spec=FileInfo, size=250, extension='.png', owner='user3', level=2),
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
