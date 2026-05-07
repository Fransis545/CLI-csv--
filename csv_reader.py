import csv
from pathlib import Path
from typing import List, Dict, Any

def read_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Читает несколько CSV-файлов и объединяет их содержимое.
    Ожидает, что в файлах есть колонки: title, ctr, retention_rate.
    """
    data = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Преобразуем числовые значения
                try:
                    row['ctr'] = float(row['ctr'])
                    row['retention_rate'] = float(row['retention_rate'])
                except (KeyError, ValueError):
                    # Если данных нет или они некорректны – пропускаем строку
                    continue
                data.append(row)
    return data