"""
Data loading for dashboard charts.

Reads data from JSON files in the data/ directory:
  - gigasearch.json   — IDP GigaSearch chart
  - summarization.json — Summarization chart
  - gigaquery.json     — GigaQuery chart
  - initiatives.json   — Initiatives chart

Arrays can contain any number of values (12, 13, 14, ...).
Charts always display the last 12 months. Just append new months to arrays.
"""
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent

# Cache for loaded JSON files
_cached: dict[str, Any] = {}

# Number of months to display on charts
MONTHS_DISPLAY = 12

# Y-axis ranges for GigaSearch filters
GIGASEARCH_Y_RANGES: dict[str, tuple[float, float]] = {
    "common-wo-sbol": (0, 3_000_000),
    "common-sbol": (20_000_000, 50_000_000),
    "alpha": (0, 3_000_000),
    "sigma": (0, 1_000_000),
    "alpha-sbol": (0, 1_000_000),
}

# Y-axis ranges for Alpha/Sigma filters
ALPHA_SIGMA_Y_RANGES: dict[str, tuple[float, float]] = {
    "alpha": (0, 2_000_000),
    "sigma": (0, 1_000_000),
    "common": (0, 1_000_000),
}

# RAG Sources data for donut chart
RAG_SOURCES: dict[str, dict[str, int]] = {
    "alpha": {"SberHelp": 12, "ECM": 25, "KA": 8, "Custom": 18},
    "sigma": {"ECM": 22, "M-App": 15, "K+": 31, "Custom": 7},
}

# Service display names and colors
SERVICE_CONFIG = {
    "gigasearch": {"name": "GigaSearch", "base_calls": 2_500_000, "volatility": 0.15},
    "gigaquery": {"name": "GigaQuery", "base_calls": 800_000, "volatility": 0.20},
    "summarization": {"name": "Summarization", "base_calls": 1_200_000, "volatility": 0.18},
}


def _load_json(name: str) -> dict | list:
    """Load JSON from data/{name}.json with caching."""
    if name not in _cached:
        path = _DATA_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        # Ignore keys starting with underscore (comments, etc.)
        if isinstance(data, dict):
            _cached[name] = {k: v for k, v in data.items() if not k.startswith("_")}
        else:
            _cached[name] = data
    return _cached[name]


def _generate_monthly_index(months_back: int = 12) -> pd.DatetimeIndex:
    """Generate DatetimeIndex for last N months (oldest to newest)."""
    idx = pd.date_range(end=datetime.now(), periods=months_back + 1, freq="ME")
    return idx[:months_back]


def _last_n(values: list | tuple, n: int = MONTHS_DISPLAY) -> list:
    """Get last n values (or all if fewer). Always returns list."""
    seq = list(values)
    return seq[-n:] if len(seq) >= n else seq


def _generate_synthetic_data(
    service: str,
    months: int = 24,
    growth_rate: float = 0.03,
    seasonality: bool = True,
) -> list[int]:
    """
    Generate synthetic monthly call data for a service.
    
    Args:
        service: Service key (gigasearch, gigaquery, summarization)
        months: Number of months to generate
        growth_rate: Monthly growth rate (0.03 = 3%)
        seasonality: Add seasonal variation
        
    Returns:
        List of call counts
    """
    config = SERVICE_CONFIG[service]
    base = config["base_calls"]
    volatility = config["volatility"]
    
    data = []
    for i in range(months):
        # Base with growth
        value = base * (1 + growth_rate) ** i
        
        # Seasonality (higher in winter, lower in summer)
        if seasonality:
            month_idx = i % 12
            seasonal_factor = 1 + 0.15 * (1 if month_idx in [0, 1, 11] else -0.1 if month_idx in [5, 6, 7] else 0)
            value *= seasonal_factor
        
        # Random noise
        noise = random.uniform(1 - volatility, 1 + volatility)
        value *= noise
        
        data.append(int(value))
    
    return data


# Cache for synthetic data
_synthetic_cache: dict[str, list[int]] = {}


def _get_or_generate_synthetic(service: str, months: int = 24) -> list[int]:
    """Get cached or generate synthetic data for service."""
    cache_key = f"{service}_{months}"
    if cache_key not in _synthetic_cache:
        random.seed(hash(service) % 2**32)  # Reproducible per service
        _synthetic_cache[cache_key] = _generate_synthetic_data(service, months)
    return _synthetic_cache[cache_key]


# Time period filters
TIME_PERIODS = {
    "all": {"label": "All", "months": 24},
    "last_3": {"label": "Last 3 months", "months": 3},
    "last_6": {"label": "Last 6 months", "months": 6},
}

# Service filter options
SERVICE_FILTER_OPTIONS = [
    {"label": "GigaSearch", "value": "gigasearch"},
    {"label": "GigaQuery", "value": "gigaquery"},
    {"label": "Summarization", "value": "summarization"},
]


def get_service_calls_data(
    service: str = "gigasearch",
    period: str = "all",
) -> pd.DataFrame:
    """
    Get service calls data for specified service and time period.
    
    Args:
        service: Service key (gigasearch, gigaquery, summarization)
        period: Time period (all, last_3, last_6)
        
    Returns:
        DataFrame with 'calls' column indexed by month
    """
    months_count = TIME_PERIODS.get(period, TIME_PERIODS["all"])["months"]
    values = _get_or_generate_synthetic(service, months=24)
    
    # Take only the last N months based on period
    values = values[-months_count:]
    n = len(values)
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df


def get_service_kpi(service: str = "gigasearch") -> dict:
    """
    Get KPI metrics for a service.
    
    Args:
        service: Service key (gigasearch, gigaquery, summarization)
        
    Returns:
        Dict with current_calls, delta_calls, delta_pct, total_calls
    """
    values = _get_or_generate_synthetic(service, months=24)
    
    current = values[-1]
    previous = values[-2] if len(values) >= 2 else current
    
    delta = current - previous
    delta_pct = ((current - previous) / previous * 100) if previous > 0 else 0
    
    # Total calls in millions (sum of all months)
    total = sum(values)
    
    return {
        "current": current,
        "delta": delta,
        "delta_pct": delta_pct,
        "total": total,
    }


def get_gigasearch_data(filter_key: str) -> tuple[pd.DataFrame, float, float]:
    """
    Get GigaSearch data for specified filter.
    
    Args:
        filter_key: One of common-wo-sbol, common-sbol, alpha, sigma, alpha-sbol
        
    Returns:
        Tuple of (DataFrame with 'calls' column, y_min, y_max)
    """
    data = _load_json("gigasearch")
    if filter_key not in data:
        raise KeyError(
            f"Filter '{filter_key}' not found in gigasearch.json. Available: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = GIGASEARCH_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_summarization_data(filter_key: str) -> tuple[pd.DataFrame, float, float]:
    """
    Get Summarization data for specified filter.
    
    Args:
        filter_key: One of alpha, sigma, common
        
    Returns:
        Tuple of (DataFrame with 'calls' column, y_min, y_max)
    """
    data = _load_json("summarization")
    if filter_key not in data:
        raise KeyError(
            f"Filter '{filter_key}' not found in summarization.json. Available: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = ALPHA_SIGMA_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_gigaquery_data(filter_key: str) -> tuple[pd.DataFrame, float, float]:
    """
    Get GigaQuery data for specified filter.
    
    Args:
        filter_key: One of alpha, sigma, common
        
    Returns:
        Tuple of (DataFrame with 'calls' column, y_min, y_max)
    """
    data = _load_json("gigaquery")
    if filter_key not in data:
        raise KeyError(
            f"Filter '{filter_key}' not found in gigaquery.json. Available: {list(data.keys())}"
        )
    values = _last_n(data[filter_key])
    n = len(values)
    y_min, y_max = ALPHA_SIGMA_Y_RANGES[filter_key]
    months = _generate_monthly_index(n)
    df = pd.DataFrame({"calls": values}, index=months)
    return df, y_min, y_max


def get_initiatives_data() -> pd.DataFrame:
    """
    Get initiatives data by month.
    
    Returns:
        DataFrame with columns: gigasearch, gigaquery, summarization
    """
    data = _load_json("initiatives")
    if not isinstance(data, dict):
        raise ValueError("initiatives.json must be an object with 'months' array or gigasearch/gigaquery/summarization keys")

    if "months" in data:
        raw = _last_n(list(data["months"]))
        if not raw:
            raise ValueError("initiatives.json: months array cannot be empty")
        rows = [[int(r[0]), int(r[1]), int(r[2])] for r in raw]
    else:
        for key in ("gigasearch", "gigaquery", "summarization"):
            if key not in data:
                raise KeyError(
                    f"initiatives.json: needs 'months' array or gigasearch, gigaquery, summarization keys; missing '{key}'"
                )
        gs = _last_n(list(data["gigasearch"]))
        gq = _last_n(list(data["gigaquery"]))
        su = _last_n(list(data["summarization"]))
        n = min(len(gs), len(gq), len(su))
        if n == 0:
            raise ValueError("initiatives.json: arrays cannot be empty")
        rows = [[int(a), int(b), int(c)] for a, b, c in zip(gs[-n:], gq[-n:], su[-n:])]

    n = len(rows)
    months = _generate_monthly_index(n)
    records = [{"gigasearch": r[0], "gigaquery": r[1], "summarization": r[2]} for r in rows]
    df = pd.DataFrame(records)
    df.index = months
    return df


def get_rag_sources_data(filter_key: str) -> list[dict[str, str | int]]:
    """
    Get RAG sources data for donut chart.
    
    Args:
        filter_key: "alpha" or "sigma"
        
    Returns:
        List of dicts: [{"label": str, "value": int}, ...]
    """
    if filter_key not in RAG_SOURCES:
        filter_key = "alpha"
    raw = RAG_SOURCES[filter_key]
    return [{"label": k, "value": v} for k, v in raw.items()]
