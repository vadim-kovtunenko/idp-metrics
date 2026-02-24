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
from dash.dependencies import Input, Output, State

from components.charts import donut_chart_rag_sources, line_chart_gigasearch
from components.kpi import format_kpi_value, kpi_badge_children
from config.theme import COLORS
from data.sample_data import get_gigaquery_data, get_gigasearch_data, get_rag_sources_data, get_summarization_data
from layout.dashboard import (
    ALPHA_SIGMA_FILTER_OPTIONS,
    GIGASEARCH_FILTER_OPTIONS,
    SERVICES_SLIDE_TITLES,
    _pct_change_current_vs_previous,
    build_layout,
)

# Create Dash app; assets (e.g. assets/custom.css) are loaded automatically
app = dash.Dash(
    __name__,
    title="IDP Dashboard",
    suppress_callback_exceptions=True,
)
app.layout = build_layout


def _get_services_options(slide_index: int):
    if slide_index == 0:
        return GIGASEARCH_FILTER_OPTIONS
    return ALPHA_SIGMA_FILTER_OPTIONS


@app.callback(
    Output("services-slide-index", "data"),
    Input("services-slide-prev", "n_clicks"),
    Input("services-slide-next", "n_clicks"),
    State("services-slide-index", "data"),
)
def update_services_slide(prev_clicks, next_clicks, current_index):
    from dash import ctx
    if not ctx.triggered_id:
        return current_index or 0
    current_index = current_index or 0
    if ctx.triggered_id == "services-slide-prev":
        return (current_index - 1) % 3
    if ctx.triggered_id == "services-slide-next":
        return (current_index + 1) % 3
    return current_index


@app.callback(
    Output("services-filter-store", "data"),
    Input("services-filter", "value"),
    State("services-slide-index", "data"),
    State("services-filter-store", "data"),
)
def update_services_filter_store(filter_value, slide_index, store):
    if slide_index is None or store is None:
        return store or {"0": "common-wo-sbol", "1": "alpha", "2": "alpha"}
    key = str(slide_index)
    return {**store, key: filter_value}


@app.callback(
    [
        Output("services-chart-title", "children"),
        Output("services-kpi-value", "children"),
        Output("services-kpi-badge", "children"),
        Output("chart-services", "figure"),
        Output("services-filter", "options"),
        Output("services-filter", "value"),
    ],
    Input("services-slide-index", "data"),
    Input("services-filter", "value"),
    State("services-filter-store", "data"),
)
def update_services_content(slide_index, filter_value, filter_store):
    from dash import ctx

    slide_index = slide_index or 0
    filter_store = filter_store or {"0": "common-wo-sbol", "1": "alpha", "2": "alpha"}
    key = str(slide_index)
    # При переключении слайда показываем сохранённый фильтр, иначе — текущий выбор
    if ctx.triggered_id == "services-slide-index":
        current_filter = filter_store.get(key, "common-wo-sbol" if slide_index == 0 else "alpha")
    else:
        current_filter = filter_value or filter_store.get(key, "common-wo-sbol" if slide_index == 0 else "alpha")

    if slide_index == 0:
        df, y_min, y_max = get_gigasearch_data(current_filter)
    elif slide_index == 1:
        df, y_min, y_max = get_summarization_data(current_filter)
    else:
        df, y_min, y_max = get_gigaquery_data(current_filter)

    fig = line_chart_gigasearch(df, y_min, y_max)
    current = df["calls"].iloc[-1]
    pct = _pct_change_current_vs_previous(df["calls"])
    options = _get_services_options(slide_index)

    return (
        SERVICES_SLIDE_TITLES[slide_index],
        format_kpi_value(current),
        kpi_badge_children(pct),
        fig,
        options,
        current_filter,
    )


@app.callback(
    Output("chart-rag", "figure"),
    Input("rag-filter", "value"),
)
def update_rag_chart(filter_value):
    """Обновление графика «Источники RAG» при смене фильтра Alpha/Sigma."""
    filter_value = filter_value or "alpha"
    data = get_rag_sources_data(filter_value)
    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]
    return donut_chart_rag_sources(labels, values)


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
