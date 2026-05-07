#!/usr/bin/env python3
import argparse
import sys
from tabulate import tabulate

from csv_reader import read_csv_files
from report import get_report

def main():
    parser = argparse.ArgumentParser(description="Обработка CSV с метриками видео YouTube")
    parser.add_argument("--files", nargs="+", required=True, help="Пути к CSV-файлам")
    parser.add_argument("--report", required=True, help="Название отчёта (например, clickbait)")
    args = parser.parse_args()

    # Чтение данных из файлов
    try:
        data = read_csv_files(args.files)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    if not data:
        print("Нет данных для обработки.", file=sys.stderr)
        sys.exit(1)

    # Получение отчёта
    try:
        report = get_report(args.report)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

    # Генерация отчёта
    result = report.generate(data)

    # Вывод таблицы
    if result:
        headers = ["title", "ctr", "retention_rate"]
        table = [[row["title"], row["ctr"], row["retention_rate"]] for row in result]
        print(tabulate(table, headers=headers, tablefmt="grid", floatfmt=".1f"))
    else:
        print("Нет видео, удовлетворяющих условиям отчёта.")

if __name__ == "__main__":
    main()