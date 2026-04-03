"""
Main dashboard layout: redesigned to match reference screenshot.
Two-column layout with wallet section, charts, assets, and allocation.
"""
from dash import dcc, html

from components.charts import donut_chart, line_chart, multi_line_chart
from components.kpi import format_kpi_value, kpi_badge_children
from components.dashboard_components import wallet_cards_row, assets_list, allocation_list, allocation_legend
from config.theme import COLORS
from data.sample_data import (
    get_initiatives_data,
    get_rag_sources_data,
    get_service_calls_data,
    get_service_kpi,
    SERVICE_FILTER_OPTIONS,
    TIME_PERIODS,
)


def pct_change_current_vs_previous(series) -> float:
    """Calculate percentage change: last value vs previous period."""
    if len(series) < 2:
        return 0.0
    prev, current = series.iloc[-2], series.iloc[-1]
    if prev == 0:
        return 0.0
    return (current - prev) / prev * 100


ALPHA_SIGMA_FILTER_OPTIONS = [
    {"label": "Alpha", "value": "alpha"},
    {"label": "Sigma", "value": "sigma"},
    {"label": "Common", "value": "common"},
]

SERVICES_SLIDE_TITLES = ["GigaSearch", "Summarization", "GigaQuery"]


def build_dashboard_content() -> html.Div:
    """Build dashboard matching reference screenshot layout."""
    # Get initial data for GigaSearch with "all" period
    df_initial = get_service_calls_data(service="gigasearch", period="all")
    kpi = get_service_kpi("gigasearch")
    
    # Build chart
    y_min = 0
    y_max = max(df_initial["calls"]) * 1.2
    fig_initial = line_chart(df_initial, y_min, y_max, show_secondary=True)
    
    # Format KPI values
    current_formatted = format_kpi_value(kpi["current"])
    delta_sign = "+" if kpi["delta"] >= 0 else ""
    delta_formatted = f"{delta_sign}{format_kpi_value(kpi['delta'])}"
    pct_value = abs(kpi['delta_pct'])
    pct_str = f"{pct_value:.1f}%"
    
    # Initiatives chart
    df_init = get_initiatives_data()
    fig_initiatives = multi_line_chart(
        df_init,
        columns={"GigaSearch": "gigasearch", "GigaQuery": "gigaquery", "Summarization": "summarization"},
        y_min=0,
        y_max=60,
        y_tick_vals=[15, 30, 45, 60],
        y_tick_texts=["15", "30", "45", "60"],
    )

    # RAG sources donut chart
    rag_data = get_rag_sources_data("alpha")
    rag_labels = [d["label"] for d in rag_data]
    rag_values = [d["value"] for d in rag_data]
    fig_rag = donut_chart(rag_labels, rag_values)

    # Totals for initiative plates
    total_gs = int(df_init["gigasearch"].sum())
    delta_gs = int(df_init["gigasearch"].iloc[-1])
    total_gq = int(df_init["gigaquery"].sum())
    delta_gq = int(df_init["gigaquery"].iloc[-1])
    total_summ = int(df_init["summarization"].sum())
    delta_summ = int(df_init["summarization"].iloc[-1])

    # Assets data (based on initiatives)
    assets_data = [
        {
            "name": "GigaSearch",
            "subname": f"{int(df_init['gigasearch'].iloc[-1])} calls this month",
            "value_primary": f"${total_gs / 1000:.2f}K",
            "value_secondary": f"{int(df_init['gigasearch'].iloc[-1])} GS",
        },
        {
            "name": "GigaQuery",
            "subname": f"{int(df_init['gigaquery'].iloc[-1])} calls this month",
            "value_primary": f"${total_gq / 1000:.2f}K",
            "value_secondary": f"{int(df_init['gigaquery'].iloc[-1])} GQ",
        },
        {
            "name": "Summarization",
            "subname": f"{int(df_init['summarization'].iloc[-1])} calls this month",
            "value_primary": f"${total_summ / 1000:.2f}K",
            "value_secondary": f"{int(df_init['summarization'].iloc[-1])} SUM",
        },
    ]

    # Allocation data
    total_calls = total_gs + total_gq + total_summ
    if total_calls > 0:
        gs_percent = int((total_gs / total_calls) * 100)
        gq_percent = int((total_gq / total_calls) * 100)
        summ_percent = int((total_summ / total_calls) * 100)
    else:
        gs_percent = gq_percent = summ_percent = 33

    allocations_data = [
        {"name": "GigaSearch", "staked_percent": gs_percent, "available_percent": max(0, 100 - gs_percent - 20)},
        {"name": "GigaQuery", "staked_percent": gq_percent, "available_percent": max(0, 100 - gq_percent - 20)},
        {"name": "Summarization", "staked_percent": summ_percent, "available_percent": max(0, 100 - summ_percent - 20)},
    ]

    return html.Div(
        [
            dcc.Store(id="services-slide-index", data=0),
            dcc.Store(id="service-filter", data="gigasearch"),
            dcc.Store(id="time-period-filter", data="all"),

            # Header
            html.Header(
                html.H1("Dashboard", className="dashboard-title"),
                className="dashboard-header",
            ),

            # Main grid: left column (chart + assets) and right column (wallet + allocation)
            html.Div(
                [
                    # Left column
                    html.Div(
                        [
                            # Main chart card
                            html.Div(
                                [
                                    # Chart header with KPI
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Span(current_formatted, className="kpi-value", id="service-kpi-value"),
                                                            html.Div(
                                                                kpi_badge_children(pct_value),
                                                                className="kpi-badge",
                                                                id="service-kpi-badge",
                                                                style={
                                                                    "backgroundColor": COLORS["kpi_badge_bg"],
                                                                    "color": COLORS["kpi_badge_text"],
                                                                },
                                                            ),
                                                        ],
                                                        className="kpi-row",
                                                    ),
                                                    html.Div(delta_formatted, className="text-secondary", id="service-kpi-delta", style={"marginTop": "4px", "fontSize": "14px"}),
                                                ],
                                                style={"flex": "1"},
                                            ),
                                            # Time period filter buttons
                                            html.Div(
                                                [
                                                    html.Button(
                                                        "All",
                                                        className="chart-control-btn active",
                                                        id="btn-period-all",
                                                        n_clicks=0,
                                                    ),
                                                    html.Button(
                                                        "Last 3 months",
                                                        className="chart-control-btn",
                                                        id="btn-period-3",
                                                        n_clicks=0,
                                                    ),
                                                    html.Button(
                                                        "Last 6 months",
                                                        className="chart-control-btn",
                                                        id="btn-period-6",
                                                        n_clicks=0,
                                                    ),
                                                ],
                                                className="chart-controls",
                                            ),
                                        ],
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "16px"},
                                    ),

                                    # Chart
                                    dcc.Graph(
                                        figure=fig_initial,
                                        id="chart-services",
                                        config={"responsive": True, "displayModeBar": False},
                                        className="dashboard-chart",
                                    ),

                                    # Service selector dropdown
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                options=SERVICE_FILTER_OPTIONS,
                                                value="gigasearch",
                                                clearable=False,
                                                id="service-filter-dropdown",
                                                style={
                                                    "width": "200px",
                                                    "borderRadius": "8px",
                                                    "border": f"1px solid {COLORS['border']}",
                                                },
                                            ),
                                        ],
                                        style={"display": "flex", "justifyContent": "center", "alignItems": "center", "marginTop": "16px"},
                                    ),
                                ],
                                className="chart-card main-chart-card",
                            ),
                            
                            # Assets section
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H2("Your assets", className="chart-card-title", style={"textTransform": "none", "fontSize": "18px", "margin": 0}),
                                            html.Span("View all →", className="view-all-link"),
                                        ],
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px"},
                                    ),
                                    assets_list(assets_data),
                                ],
                                className="chart-card",
                                style={"marginTop": "24px"},
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                    
                    # Right column
                    html.Div(
                        [
                            # Wallet section
                            html.Div(
                                [
                                    html.H2("Your wallet", className="chart-card-title", style={"textTransform": "none", "fontSize": "18px", "margin": "0 0 16px 0"}),
                                    html.Div("Total balance", className="text-secondary", style={"fontSize": "13px", "marginBottom": "8px"}),
                                    html.Div(
                                        [
                                            html.Span(current_formatted, style={"fontSize": "32px", "fontWeight": "600", "color": COLORS["text_primary"]}),
                                            html.Div(
                                                [
                                                    html.Button("▼", className="chart-control-btn", style={"width": "32px", "height": "32px", "marginLeft": "8px"}),
                                                    html.Button("▲", className="chart-control-btn", style={"width": "32px", "height": "32px"}),
                                                ],
                                                style={"float": "right"},
                                            ),
                                        ],
                                        style={"marginBottom": "4px"},
                                    ),
                                    html.Div(f"{int(kpi['current'])} units", className="text-muted", style={"fontSize": "13px", "marginBottom": "20px"}),
                                    
                                    # Wallet cards
                                    wallet_cards_row(
                                        total_staked=f"${total_gs / 1000:.0f}K",
                                        total_rewards=f"${total_gq / 1000:.0f}K",
                                        available=f"{delta_gs}",
                                    ),
                                ],
                                className="chart-card",
                            ),
                            
                            # Allocation section
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H2("Your allocation", className="chart-card-title", style={"textTransform": "none", "fontSize": "18px", "margin": 0}),
                                            allocation_legend(),
                                        ],
                                        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px"},
                                    ),
                                    allocation_list(allocations_data),
                                ],
                                className="chart-card",
                                style={"marginTop": "24px"},
                            ),
                        ],
                        style={"flex": "1", "marginLeft": "24px"},
                    ),
                ],
                className="dashboard-grid",
            ),
        ],
        className="dashboard-wrapper",
    )
