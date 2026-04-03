# IDP Dashboard

Dashboard with managerial and analytical metrics. Calculations in Python, visualizations with Plotly + Dash.

## Structure

```
idp-dashboard/
├── app.py                 # Entry point, Dash app creation
├── callbacks/
│   ├── __init__.py        # Callbacks module export
│   └── main.py            # All Dash callbacks
├── components/
│   ├── __init__.py        # Components export
│   ├── charts.py          # Reusable chart functions (Plotly)
│   └── kpi.py             # KPI formatting and badges
├── config/
│   └── theme.py           # Colors and chart styling
├── data/
│   ├── sample_data.py     # Data loading and calculation functions
│   ├── gigasearch.json    # GigaSearch data
│   ├── summarization.json # Summarization data
│   ├── gigaquery.json     # GigaQuery data
│   └── initiatives.json   # Initiatives data
├── layout/
│   ├── __init__.py        # Layout export
│   └── dashboard.py       # Dashboard layout structure
├── assets/
│   └── custom.css         # Responsive styles
└── requirements.txt
```

## Quick Start

```bash
cd idp-dashboard
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open in browser: http://localhost:8050

## Current Charts

1. **Services Carousel** — Line chart with area fill, switchable between:
   - GigaSearch (filters: common-wo-sbol, common-sbol, alpha, sigma, alpha-sbol)
   - Summarization (filters: alpha, sigma, common)
   - GigaQuery (filters: alpha, sigma, common)

2. **Initiatives** — Multi-line chart showing initiatives count over time

3. **RAG Sources** — Donut chart showing RAG source distribution (Alpha/Sigma)

## Architecture

### Separation of Concerns

| Layer | Directory | Responsibility |
|-------|-----------|----------------|
| **Entry Point** | `app.py` | App creation, server config |
| **Callbacks** | `callbacks/` | Dash callback functions |
| **UI Components** | `components/` | Reusable charts, KPI widgets |
| **Layout** | `layout/` | Dashboard structure, grid |
| **Data** | `data/` | Data loading, transformations |
| **Config** | `config/` | Theme, colors, constants |

### Adding New Metrics

1. **Data**: Add function in `data/sample_data.py` (or new module) returning `pd.DataFrame`
2. **Chart**: Add function in `components/charts.py` using `config/theme.py`
3. **Layout**: Add block in `layout/dashboard.py`
4. **Callbacks**: Add callback in `callbacks/main.py`

## Key Improvements (Refactored)

- **Consolidated chart functions**: Single `line_chart()` and `multi_line_chart()` instead of 5 duplicate functions
- **Separated callbacks**: All callbacks moved to `callbacks/` module
- **Type hints**: Added throughout the codebase
- **Removed unused code**: Cleaned up dead functions and imports
- **Better exports**: `__init__.py` files provide clean public APIs
