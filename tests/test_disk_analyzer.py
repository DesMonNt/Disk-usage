import pytest
from pathlib import Path
from disk_usage.disk_analyzer import DiskAnalyzer
from disk_usage.file_info import FileInfo


@pytest.fixture
def mock_path(mocker):
    return mocker.Mock(spec=Path)


@pytest.fixture
def mock_file_info(mocker):
    return mocker.Mock(spec=FileInfo)


@pytest.mark.asyncio
async def test_disk_usage(mocker):
    mock_usage = mocker.Mock()
    mock_usage.used = 500 * (10**9)
    mock_usage.total = 1000 * (10**9)

    mocker.patch('psutil.disk_usage', return_value=mock_usage)

    analyzer = DiskAnalyzer(mock_path)
    used, total = await analyzer.disk_usage()

    assert used == 500 * (10**9)
    assert total == 1000 * (10**9)
