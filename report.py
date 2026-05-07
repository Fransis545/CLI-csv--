from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Report(ABC):
    """Базовый класс для всех отчётов."""

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Возвращает список записей, отфильтрованных и отсортированных по правилам отчёта."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя отчёта, используемое в параметре --report."""
        pass

class ClickbaitReport(Report):
    """
    Отчёт "clickbait": выбирает видео с ctr > 15 и retention_rate < 40,
    сортирует по убыванию ctr.
    """

    @property
    def name(self) -> str:
        return "clickbait"

    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = [
            row for row in data
            if row.get('ctr', 0) > 15 and row.get('retention_rate', 100) < 40
        ]
        # Сортировка по убыванию CTR
        sorted_data = sorted(filtered, key=lambda x: x['ctr'], reverse=True)
        # Возвращаем только нужные колонки
        return [
            {'title': row['title'], 'ctr': row['ctr'], 'retention_rate': row['retention_rate']}
            for row in sorted_data
        ]

# Фабрика отчётов
REPORTS = {cls().name: cls() for cls in [ClickbaitReport]}

def get_report(report_name: str) -> Report:
    """Возвращает экземпляр отчёта по имени или выбрасывает исключение."""
    if report_name not in REPORTS:
        raise ValueError(f"Неизвестный отчёт: {report_name}. Доступные: {list(REPORTS.keys())}")
    return REPORTS[report_name]