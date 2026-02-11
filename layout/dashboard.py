"""
Main dashboard layout: responsive grid and chart placement.
Each card: title + KPI + graph.
"""
import sys
from pathlib import Path

# Ensure project root is on path when this file is run directly (e.g. Run in IDE)
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dash import dcc, html

from components.charts import line_chart_gigasearch, line_chart_initiatives
from components.kpi import kpi_badge_children, format_kpi_value
from config.theme import COLORS
from data.sample_data import (
    get_gigaquery_data,
    get_gigasearch_data,
    get_initiatives_data,
    get_summarization_data,
)


def _pct_change_current_vs_previous(series):
    """Percentage change: last value vs previous period."""
    if len(series) < 2:
        return 0.0
    prev, current = series.iloc[-2], series.iloc[-1]
    if prev == 0:
        return 0.0
    return (current - prev) / prev * 100


GIGASEARCH_FILTER_OPTIONS = [
    {"label": "common-wo-sbol", "value": "common-wo-sbol"},
    {"label": "common-sbol", "value": "common-sbol"},
    {"label": "alpha", "value": "alpha"},
    {"label": "sigma", "value": "sigma"},
    {"label": "alpha-sbol", "value": "alpha-sbol"},
]

ALPHA_SIGMA_FILTER_OPTIONS = [
    {"label": "Alpha", "value": "alpha"},
    {"label": "Sigma", "value": "sigma"},
    {"label": "Common", "value": "common"},
]


def build_dashboard_content() -> html.Div:
    """Inner dashboard: header + two rows of charts."""
    # Initial GigaSearch state (common-wo-sbol)
    df_gigasearch, y_min, y_max = get_gigasearch_data("common-wo-sbol")
    current_gs = df_gigasearch["calls"].iloc[-1]
    pct_gs = _pct_change_current_vs_previous(df_gigasearch["calls"])
    fig_gigasearch = line_chart_gigasearch(df_gigasearch, y_min, y_max)

    # Initial Summarization (Alpha 0–2M) and GigaQuery (Alpha 0–2M)
    df_summ, ys_min, ys_max = get_summarization_data("alpha")
    current_summ = df_summ["calls"].iloc[-1]
    pct_summ = _pct_change_current_vs_previous(df_summ["calls"])
    fig_summarization = line_chart_gigasearch(df_summ, ys_min, ys_max)

    df_gq, yg_min, yg_max = get_gigaquery_data("alpha")
    current_giga = df_gq["calls"].iloc[-1]
    pct_giga = _pct_change_current_vs_previous(df_gq["calls"])
    fig_gigaquery = line_chart_gigasearch(df_gq, yg_min, yg_max)

    # График инициатив: данные, итоги и прирост за последний месяц
    df_init = get_initiatives_data()
    fig_initiatives = line_chart_initiatives(df_init)
    total_gs = int(df_init["gigasearch"].sum())
    delta_gs = int(df_init["gigasearch"].iloc[-1])
    total_gq = int(df_init["gigaquery"].sum())
    delta_gq = int(df_init["gigaquery"].iloc[-1])
    total_summ = int(df_init["summarization"].sum())
    delta_summ = int(df_init["summarization"].iloc[-1])

    return html.Div(
        [
            html.Header(
                html.H1("IDP Dashboard", className="dashboard-title"),
                className="dashboard-header",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H2("IDP GigaSearch", className="chart-card-title"),
                            html.Div(
                                [
                                    html.Span(
                                        format_kpi_value(current_gs),
                                        id="gigasearch-kpi-value",
                                        className="kpi-value",
                                    ),
                                    html.Span(
                                        kpi_badge_children(pct_gs),
                                        id="gigasearch-kpi-badge",
                                        className="kpi-badge",
                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                    ),
                                ],
                                className="kpi-row",
                            ),
                            dcc.Graph(
                                figure=fig_gigasearch,
                                id="chart-gigasearch",
                                config={"responsive": True, "displayModeBar": False},
                                className="dashboard-chart",
                            ),
                            dcc.RadioItems(
                                id="gigasearch-filter",
                                options=GIGASEARCH_FILTER_OPTIONS,
                                value="common-wo-sbol",
                                className="gigasearch-filter-buttons",
                            ),
                        ],
                        className="chart-card gigasearch-card",
                    ),
                ],
                className="charts-row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H2("Summarization", className="chart-card-title"),
                            html.Div(
                                [
                                    html.Span(
                                        format_kpi_value(current_summ),
                                        id="summarization-kpi-value",
                                        className="kpi-value",
                                    ),
                                    html.Span(
                                        kpi_badge_children(pct_summ),
                                        id="summarization-kpi-badge",
                                        className="kpi-badge",
                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                    ),
                                ],
                                className="kpi-row",
                            ),
                            dcc.Graph(
                                figure=fig_summarization,
                                id="chart-summarization",
                                config={"responsive": True, "displayModeBar": False},
                                className="dashboard-chart",
                            ),
                            dcc.RadioItems(
                                id="summarization-filter",
                                options=ALPHA_SIGMA_FILTER_OPTIONS,
                                value="alpha",
                                className="chart-filter-buttons",
                            ),
                        ],
                        className="chart-card",
                    ),
                    html.Div(
                        [
                            html.H2("GigaQuery", className="chart-card-title"),
                            html.Div(
                                [
                                    html.Span(
                                        format_kpi_value(current_giga),
                                        id="gigaquery-kpi-value",
                                        className="kpi-value",
                                    ),
                                    html.Span(
                                        kpi_badge_children(pct_giga),
                                        id="gigaquery-kpi-badge",
                                        className="kpi-badge",
                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                    ),
                                ],
                                className="kpi-row",
                            ),
                            dcc.Graph(
                                figure=fig_gigaquery,
                                id="chart-gigaquery",
                                config={"responsive": True, "displayModeBar": False},
                                className="dashboard-chart",
                            ),
                            dcc.RadioItems(
                                id="gigaquery-filter",
                                options=ALPHA_SIGMA_FILTER_OPTIONS,
                                value="alpha",
                                className="chart-filter-buttons",
                            ),
                        ],
                        className="chart-card",
                    ),
                ],
                className="charts-row",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        "Количество заведенных инициатив",
                                        className="chart-card-title",
                                    ),
                                    dcc.Graph(
                                        figure=fig_initiatives,
                                        id="chart-initiatives",
                                        config={"responsive": True, "displayModeBar": False},
                                        className="dashboard-chart initiatives-chart",
                                    ),
                                ],
                                className="chart-card initiatives-chart-card",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H2(
                                                "GigaSearch",
                                                className="chart-card-title",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span(
                                                        str(total_gs),
                                                        className="kpi-value",
                                                    ),
                                                    html.Span(
                                                        f"+{delta_gs}" if delta_gs >= 0 else str(delta_gs),
                                                        className="kpi-badge initiative-delta-badge",
                                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                                    ),
                                                ],
                                                className="kpi-row",
                                            ),
                                        ],
                                        className="initiative-plate",
                                    ),
                                    html.Div(
                                        [
                                            html.H2(
                                                "GigaQuery",
                                                className="chart-card-title",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span(
                                                        str(total_gq),
                                                        className="kpi-value",
                                                    ),
                                                    html.Span(
                                                        f"+{delta_gq}" if delta_gq >= 0 else str(delta_gq),
                                                        className="kpi-badge initiative-delta-badge",
                                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                                    ),
                                                ],
                                                className="kpi-row",
                                            ),
                                        ],
                                        className="initiative-plate",
                                    ),
                                    html.Div(
                                        [
                                            html.H2(
                                                "Summarization",
                                                className="chart-card-title",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span(
                                                        str(total_summ),
                                                        className="kpi-value",
                                                    ),
                                                    html.Span(
                                                        f"+{delta_summ}" if delta_summ >= 0 else str(delta_summ),
                                                        className="kpi-badge initiative-delta-badge",
                                                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                                                    ),
                                                ],
                                                className="kpi-row",
                                            ),
                                        ],
                                        className="initiative-plate",
                                    ),
                                ],
                                className="initiative-plates-row",
                            ),
                        ],
                        className="initiatives-column",
                    ),
                ],
                className="charts-row",
            ),
        ],
        className="dashboard",
    )


def build_layout() -> html.Div:
    """Root: one container, adaptive grid, even stretch."""
    return build_dashboard_content()
