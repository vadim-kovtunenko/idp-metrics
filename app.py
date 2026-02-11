"""
IDP Dashboard — entry point.
Run from repository root: python app.py
"""
import sys
from pathlib import Path

# Ensure project root is on path (fixes imports when run from any CWD or when layout/dashboard.py is run directly)
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import threading
import webbrowser

import dash
from dash.dependencies import Input, Output

from components.charts import line_chart_gigasearch
from components.kpi import format_kpi_value, kpi_badge_children
from config.theme import COLORS
from data.sample_data import get_gigaquery_data, get_gigasearch_data, get_summarization_data
from layout.dashboard import _pct_change_current_vs_previous, build_layout

# Create Dash app; assets (e.g. assets/custom.css) are loaded automatically
app = dash.Dash(
    __name__,
    title="IDP Dashboard",
    suppress_callback_exceptions=True,
)
app.layout = build_layout


@app.callback(
    [
        Output("chart-gigasearch", "figure"),
        Output("gigasearch-kpi-value", "children"),
        Output("gigasearch-kpi-badge", "children"),
    ],
    Input("gigasearch-filter", "value"),
)
def update_gigasearch(filter_value):
    df, y_min, y_max = get_gigasearch_data(filter_value)
    fig = line_chart_gigasearch(df, y_min, y_max)
    current = df["calls"].iloc[-1]
    pct = _pct_change_current_vs_previous(df["calls"])
    return fig, format_kpi_value(current), kpi_badge_children(pct)


@app.callback(
    [
        Output("chart-summarization", "figure"),
        Output("summarization-kpi-value", "children"),
        Output("summarization-kpi-badge", "children"),
    ],
    Input("summarization-filter", "value"),
)
def update_summarization(filter_value):
    df, y_min, y_max = get_summarization_data(filter_value)
    fig = line_chart_gigasearch(df, y_min, y_max)
    current = df["calls"].iloc[-1]
    pct = _pct_change_current_vs_previous(df["calls"])
    return fig, format_kpi_value(current), kpi_badge_children(pct)


@app.callback(
    [
        Output("chart-gigaquery", "figure"),
        Output("gigaquery-kpi-value", "children"),
        Output("gigaquery-kpi-badge", "children"),
    ],
    Input("gigaquery-filter", "value"),
)
def update_gigaquery(filter_value):
    df, y_min, y_max = get_gigaquery_data(filter_value)
    fig = line_chart_gigasearch(df, y_min, y_max)
    current = df["calls"].iloc[-1]
    pct = _pct_change_current_vs_previous(df["calls"])
    return fig, format_kpi_value(current), kpi_badge_children(pct)

# Apply dashboard background to the outer page
app.index_string = """<!DOCTYPE html>
<html style="overflow-x: hidden;">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; background-color: """ + COLORS["dashboard_bg"] + """;">
        {%app_entry%}
        <footer>{%config%}</footer>
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""

server = app.server

if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    app.run(debug=True, host="0.0.0.0", port=8050)
