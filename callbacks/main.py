"""
Dash callbacks for the IDP Dashboard.
All callbacks are registered here to separate concerns from app.py.
"""
from typing import Any

from dash import Input, Output, State, callback, ctx

from components.charts import donut_chart, line_chart
from components.kpi import format_kpi_value, kpi_badge_children
from data.sample_data import (
    get_gigaquery_data,
    get_gigasearch_data,
    get_summarization_data,
)
from layout.dashboard import (
    ALPHA_SIGMA_FILTER_OPTIONS,
    GIGASEARCH_FILTER_OPTIONS,
    SERVICES_SLIDE_TITLES,
    pct_change_current_vs_previous,
)


def _get_services_options(slide_index: int) -> list[dict[str, str]]:
    """Get filter options based on slide index."""
    if slide_index == 0:
        return GIGASEARCH_FILTER_OPTIONS
    return ALPHA_SIGMA_FILTER_OPTIONS


@callback(
    Output("services-slide-index", "data"),
    Input("services-slide-prev", "n_clicks"),
    Input("services-slide-next", "n_clicks"),
    State("services-slide-index", "data"),
)
def update_services_slide(
    prev_clicks: int | None,
    next_clicks: int | None,
    current_index: int | None,
) -> int:
    """Handle services carousel navigation."""
    if not ctx.triggered_id:
        return current_index or 0
    
    current_index = current_index or 0
    if ctx.triggered_id == "services-slide-prev":
        return (current_index - 1) % 3
    if ctx.triggered_id == "services-slide-next":
        return (current_index + 1) % 3
    return current_index


@callback(
    [
        Output("services-chart-title", "children"),
        Output("chart-services", "figure"),
    ],
    Input("services-slide-index", "data"),
    Input("services-slide-prev", "n_clicks"),
    Input("services-slide-next", "n_clicks"),
    State("services-filter-store", "data"),
)
def update_services_chart(
    slide_index: int | None,
    prev_clicks: int | None,
    next_clicks: int | None,
    filter_store: dict[str, str] | None,
) -> tuple[str, Any]:
    """Update services chart based on slide selection."""
    slide_index = slide_index or 0
    filter_store = filter_store or {"0": "common-wo-sbol", "1": "alpha", "2": "alpha"}
    key = str(slide_index)
    current_filter = filter_store.get(key, "common-wo-sbol" if slide_index == 0 else "alpha")

    # Get data based on slide
    if slide_index == 0:
        df, y_min, y_max = get_gigasearch_data(current_filter)
    elif slide_index == 1:
        df, y_min, y_max = get_summarization_data(current_filter)
    else:
        df, y_min, y_max = get_gigaquery_data(current_filter)

    fig = line_chart(df, y_min, y_max, show_secondary=True)

    return SERVICES_SLIDE_TITLES[slide_index], fig
