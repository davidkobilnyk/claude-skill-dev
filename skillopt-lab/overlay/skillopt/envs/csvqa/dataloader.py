"""CSV-backed QA dataloader: columns input, expected_output, scenario."""
from __future__ import annotations

import csv
import os

from skillopt.datasets.base import SplitDataLoader


def load_csv_items(path: str) -> list[dict]:
    items: list[dict] = []
    with open(path, encoding="utf-8", newline="") as f:
        for idx, row in enumerate(csv.DictReader(f)):
            items.append({
                "id": f"r{idx + 1:03d}",
                "question": row.get("input", ""),
                "expected": row.get("expected_output", ""),
                "task_type": (row.get("scenario") or "default").strip(),
            })
    return items


class CsvQADataLoader(SplitDataLoader):
    def load_raw_items(self, data_path: str) -> list[dict]:
        if os.path.isdir(data_path):
            csvs = sorted(p for p in os.listdir(data_path) if p.endswith(".csv"))
            if len(csvs) != 1:
                raise ValueError(f"expected exactly one .csv in {data_path}, found {csvs}")
            data_path = os.path.join(data_path, csvs[0])
        return load_csv_items(data_path)
