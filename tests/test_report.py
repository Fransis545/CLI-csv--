import pytest
from report import ClickbaitReport, get_report

def test_clickbait_filtering():
    report = ClickbaitReport()
    data = [
        {"title": "A", "ctr": 20, "retention_rate": 30},
        {"title": "B", "ctr": 10, "retention_rate": 20},   # ctr low
        {"title": "C", "ctr": 25, "retention_rate": 45},   # retention high
        {"title": "D", "ctr": 18, "retention_rate": 35},
    ]
    result = report.generate(data)
    assert len(result) == 2
    assert result[0]["title"] == "C"  # 25 > 20, sorted desc
    assert result[1]["title"] == "A"

def test_clickbait_sorting():
    report = ClickbaitReport()
    data = [
        {"title": "X", "ctr": 30, "retention_rate": 20},
        {"title": "Y", "ctr": 25, "retention_rate": 25},
        {"title": "Z", "ctr": 28, "retention_rate": 22},
    ]
    result = report.generate(data)
    titles = [r["title"] for r in result]
    assert titles == ["X", "Z", "Y"]

def test_get_report_known():
    report = get_report("clickbait")
    assert isinstance(report, ClickbaitReport)

def test_get_report_unknown():
    with pytest.raises(ValueError, match="Неизвестный отчёт: unknown"):
        get_report("unknown")