import pytest
from csv_reader import read_csv_files
from unittest.mock import mock_open, patch

def test_read_csv_files_success(tmp_path):
    content = """title,ctr,retention_rate
Video1,20.5,30
Video2,10.0,50
"""
    file1 = tmp_path / "data.csv"
    file1.write_text(content, encoding="utf-8")
    data = read_csv_files([str(file1)])
    assert len(data) == 2
    assert data[0]["title"] == "Video1"
    assert data[0]["ctr"] == 20.5
    assert data[0]["retention_rate"] == 30.0

def test_read_csv_files_not_found():
    with pytest.raises(FileNotFoundError, match="Файл не найден: missing.csv"):
        read_csv_files(["missing.csv"])

def test_read_csv_files_empty(capsys, tmp_path):
    file1 = tmp_path / "empty.csv"
    file1.write_text("title,ctr,retention_rate\n", encoding="utf-8")
    data = read_csv_files([str(file1)])
    assert data == []