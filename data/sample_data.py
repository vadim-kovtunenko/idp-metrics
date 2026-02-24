"""
Загрузка данных для графиков дашборда.

Данные читаются из JSON-файлов в папке data/:
  - gigasearch.json   — график IDP GigaSearch
  - summarization.json — график Summarization
  - gigaquery.json     — график GigaQuery
  - initiatives.json   — график «Количество заведенных инициатив»

В массивах может быть любое количество значений (12, 13, 14, …). На графиках всегда
отображаются последние 12. Просто дополняйте массивы новыми месяцами — старые не трогайте.
"""
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent

# Кэш загруженных JSON (чтобы не читать файл при каждом вызове)
_cached = {}


def _load_json(name: str) -> dict | list:
    """Загрузить JSON из data/{name}.json."""
    if name not in _cached:
        path = _DATA_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Файл данных не найден: {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # Игнорируем служебные ключи с подчёркиванием (_comment и т.п.)
        if isinstance(data, dict):
            _cached[name] = {k: v for k, v in data.items() if not k.startswith("_")}
        else:
            _cached[name] = data
    return _cached[name]


# Сколько последних месяцев показывать на графиках
MONTHS_DISPLAY = 12


def _generate_monthly_index(months_back: int = 12) -> pd.DatetimeIndex:
    """Индекс месяцев: последние N месяцев (от старого к новому). Ровно months_back дат."""
    # В части версий pandas date_range(end=..., periods=N, freq='ME') возвращает N-1 дат
    idx = pd.date_range(
        end=datetime.now(),
        periods=months_back + 1,
        freq="ME",
    )
    return idx[:months_back]


def _last_n(values, n: int = MONTHS_DISPLAY) -> list:
    """Взять последние n значений (если меньше — вернуть все). Всегда возвращает list."""
    seq = list(values)
    return seq[-n:] if len(seq) >= n else seq


# Диапазоны оси Y для отображения (не из данных)
GIGASEARCH_Y_RANGES = {
    "common-wo-sbol": (0, 3_000_000),
    "common-sbol": (20_000_000, 50_000_000),
    "alpha": (0, 3_000_000),
    "sigma": (0, 1_000_000),
    "alpha-sbol": (0, 1_000_000),
}

ALPHA_SIGMA_Y_RANGES = {
    "alpha": (0, 2_000_000),
    "sigma": (0, 1_000_000),
    "common": (0, 1_000_000),
}


def get_gigasearch_data(filter_key: str) -> tuple:
    """
    Возвращает (df, y_min, y_max) для выбранного фильтра GigaSearch.
    Данные из data/gigasearch.json.
    """
    data = _load_json("gigasearch")
    if filter_key not in data:
        raise KeyError(
            f"Фильтр '{filter_key}' не найден в gigasearch.json. Доступны: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = GIGASEARCH_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_summarization_data(filter_key: str) -> tuple:
    """
    Возвращает (df, y_min, y_max) для выбранного фильтра Summarization.
    Данные из data/summarization.json.
    """
    data = _load_json("summarization")
    if filter_key not in data:
        raise KeyError(
            f"Фильтр '{filter_key}' не найден в summarization.json. Доступны: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = ALPHA_SIGMA_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_gigaquery_data(filter_key: str) -> tuple:
    """
    Возвращает (df, y_min, y_max) для выбранного фильтра GigaQuery.
    Данные из data/gigaquery.json.
    """
    data = _load_json("gigaquery")
    if filter_key not in data:
        raise KeyError(
            f"Фильтр '{filter_key}' не найден в gigaquery.json. Доступны: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = ALPHA_SIGMA_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_initiatives_data() -> pd.DataFrame:
    """
    Возвращает помесячные данные по инициативам.
    Данные из data/initiatives.json. Колонки: gigasearch, gigaquery, summarization.
    Поддерживаются форматы: "months": [[g,gq,s],...] или отдельные ключи "gigasearch", "gigaquery", "summarization".
    """
    data = _load_json("initiatives")
    if not isinstance(data, dict):
        raise ValueError("initiatives.json должен быть объектом с полем months или gigasearch/gigaquery/summarization")

    if "months" in data:
        raw = data["months"]
        rows = _last_n(list(raw))
        if not rows:
            raise ValueError("initiatives.json: массив months не может быть пустым")
        # Строка = [gigasearch, gigaquery, summarization]; приводим к int
        rows = [[int(r[0]), int(r[1]), int(r[2])] for r in rows]
    else:
        for key in ("gigasearch", "gigaquery", "summarization"):
            if key not in data:
                raise KeyError(f"initiatives.json: нужен массив 'months' или ключи gigasearch, gigaquery, summarization; нет '{key}'")
        gs = _last_n(list(data["gigasearch"]))
        gq = _last_n(list(data["gigaquery"]))
        su = _last_n(list(data["summarization"]))
        n = min(len(gs), len(gq), len(su))
        if n == 0:
            raise ValueError("initiatives.json: массивы не могут быть пустыми")
        rows = [[int(a), int(b), int(c)] for a, b, c in zip(gs[-n:], gq[-n:], su[-n:])]

    n = len(rows)
    months = _generate_monthly_index(n)
    # Собираем DataFrame из списка строк — так длины не разъедутся
    records = [{"gigasearch": r[0], "gigaquery": r[1], "summarization": r[2]} for r in rows]
    df = pd.DataFrame(records)
    df.index = months
    return df


# Источники RAG: Alpha (SberHelp, ECM, KA, Custom) и Sigma (ECM, M-App, K+, Custom).
# Значения в диапазоне 3–40 для отображения на круговой диаграмме.
RAG_SOURCES = {
    "alpha": {"SberHelp": 12, "ECM": 25, "KA": 8, "Custom": 18},
    "sigma": {"ECM": 22, "M-App": 15, "K+": 31, "Custom": 7},
}


def get_rag_sources_data(filter_key: str) -> list[dict]:
    """
    Возвращает данные для графика «Источники RAG» по выбранному фильтру.
    filter_key: "alpha" | "sigma".
    Возвращает список словарей [{"label": str, "value": int}, ...].
    """
    if filter_key not in RAG_SOURCES:
        filter_key = "alpha"
    raw = RAG_SOURCES[filter_key]
    return [{"label": k, "value": v} for k, v in raw.items()]


def get_rag_common_sbol_monthly_calls() -> pd.DataFrame:
    """RAG Common & SBOL — при необходимости добавьте data/rag_common_sbol.json."""
    months = _generate_monthly_index(12)
    return pd.DataFrame({"calls": [0] * 12}, index=months)


def get_rag_common_monthly_calls() -> pd.DataFrame:
    """RAG Common — при необходимости добавьте data/rag_common.json."""
    months = _generate_monthly_index(12)
    return pd.DataFrame({"calls": [0] * 12}, index=months)
