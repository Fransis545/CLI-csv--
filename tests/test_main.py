from unittest.mock import patch, MagicMock
from main import main
import sys

@patch("main.read_csv_files")
@patch("main.get_report")
@patch("main.tabulate")
def test_main_success(mock_tabulate, mock_get_report, mock_read_csv, capsys):
    mock_read_csv.return_value = [{"title": "T", "ctr": 20.5, "retention_rate": 30.0}]
    mock_report = MagicMock()
    mock_report.generate.return_value = [{"title": "T", "ctr": 20.5, "retention_rate": 30.0}]
    mock_get_report.return_value = mock_report
    mock_tabulate.return_value = "formatted table"

    with patch.object(sys, "argv", ["main.py", "--files", "a.csv", "--report", "clickbait"]):
        main()

    mock_read_csv.assert_called_once_with(["a.csv"])
    mock_get_report.assert_called_once_with("clickbait")
    mock_report.generate.assert_called_once()
    captured = capsys.readouterr()
    assert "formatted table" in captured.out

@patch("main.read_csv_files")
def test_main_file_not_found(mock_read_csv, capsys):
    mock_read_csv.side_effect = FileNotFoundError("Файл не найден: missing.csv")
    with patch.object(sys, "argv", ["main.py", "--files", "missing.csv", "--report", "clickbait"]):
        with pytest.raises(SystemExit):
            main()
    captured = capsys.readouterr()
    assert "Файл не найден: missing.csv" in captured.err