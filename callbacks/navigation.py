"""
Navigation callbacks for sidebar and page routing.
"""
from dash import Input, Output, State, callback, ctx

from layout.dashboard import build_dashboard_content
from components.uikit import build_uikit_content
from components.sidebar import build_sidebar
from layout.placeholders import (
    build_initiatives_page,
    build_analytics_page,
    build_settings_page,
)
from data.sample_data import get_service_calls_data, get_service_kpi, TIME_PERIODS
from components.charts import line_chart
from components.kpi import format_kpi_value, kpi_badge_children
from config.theme import COLORS


# Page mapping
PAGES = {
    "dashboard": build_dashboard_content,
    "uikit": build_uikit_content,
    "initiatives": build_initiatives_page,
    "analytics": build_analytics_page,
    "settings": build_settings_page,
}


@callback(
    Output("page-content", "children"),
    Output("sidebar-container", "children"),
    Output("current-page", "data"),
    Input("url", "pathname"),
)
def update_page(pathname: str | None) -> tuple:
    """
    Update page content based on URL pathname.
    
    Args:
        pathname: Current URL pathname
        
    Returns:
        Tuple of (page_content, sidebar_content, page_id)
    """
    # Default to dashboard
    if pathname is None or pathname == "/":
        pathname = "/dashboard"
    
    # Extract page name from pathname
    page_id = pathname.strip("/") if pathname else "dashboard"
    
    # Validate page exists
    if page_id not in PAGES:
        page_id = "dashboard"
    
    # Get and call page builder function
    page_builder = PAGES.get(page_id, PAGES["dashboard"])
    page_content = page_builder()
    
    # Build sidebar with active page
    sidebar = build_sidebar(active_page=page_id)
    
    return page_content, sidebar, page_id


@callback(
    [
        Output("chart-services", "figure"),
        Output("service-kpi-value", "children"),
        Output("service-kpi-badge", "children"),
        Output("service-kpi-delta", "children"),
        Output("btn-period-all", "className"),
        Output("btn-period-3", "className"),
        Output("btn-period-6", "className"),
    ],
    [
        Input("service-filter-dropdown", "value"),
        Input("btn-period-all", "n_clicks"),
        Input("btn-period-3", "n_clicks"),
        Input("btn-period-6", "n_clicks"),
    ],
    prevent_initial_call=False,
)
def update_service_chart(service, n_all, n_3, n_6):
    """
    Update service chart and KPI based on filters.
    
    Args:
        service: Selected service (gigasearch, gigaquery, summarization)
        n_all: Clicks on "All" button
        n_3: Clicks on "Last 3 months" button
        n_6: Clicks on "Last 6 months" button
        
    Returns:
        Tuple of (figure, kpi_value, kpi_badge, kpi_delta, btn_all_class, btn_3_class, btn_6_class)
    """
    # Determine active time period
    trigger = ctx.triggered_id
    if trigger == "btn-period-3":
        period = "last_3"
    elif trigger == "btn-period-6":
        period = "last_6"
    else:
        period = "all"
    
    # Get data
    df = get_service_calls_data(service=service, period=period)
    kpi = get_service_kpi(service=service)
    
    # Build chart
    y_min = 0
    y_max = max(df["calls"]) * 1.2 if len(df["calls"]) > 0 else 1_000_000
    fig = line_chart(df, y_min, y_max, show_secondary=True)
    
    # Format KPI
    current_formatted = format_kpi_value(kpi["current"])
    delta_sign = "+" if kpi["delta"] >= 0 else ""
    delta_formatted = f"{delta_sign}{format_kpi_value(kpi['delta'])}"
    pct_value = abs(kpi['delta_pct'])
    kpi_badge = kpi_badge_children(pct_value)
    
    # Update button classes
    btn_all_class = "chart-control-btn active" if period == "all" else "chart-control-btn"
    btn_3_class = "chart-control-btn active" if period == "last_3" else "chart-control-btn"
    btn_6_class = "chart-control-btn active" if period == "last_6" else "chart-control-btn"
    
    return (
        fig,
        current_formatted,
        kpi_badge,
        delta_formatted,
        btn_all_class,
        btn_3_class,
        btn_6_class,
    )
