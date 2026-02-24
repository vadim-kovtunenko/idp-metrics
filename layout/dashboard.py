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

from components.charts import donut_chart_rag_sources, line_chart_gigasearch, line_chart_initiatives
from components.kpi import kpi_badge_children, format_kpi_value
from config.theme import COLORS
from data.sample_data import (
    get_gigaquery_data,
    get_gigasearch_data,
    get_initiatives_data,
    get_rag_sources_data,
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


SERVICES_SLIDE_TITLES = ["Вызовы GigaSearch", "Вызовы Summarization", "Вызовы GigaQuery"]


def build_dashboard_content() -> html.Div:
    """Inner dashboard: header + services carousel + row with initiatives."""
    # Начальное состояние: первый слайд (GigaSearch)
    df_gs, y_min, y_max = get_gigasearch_data("common-wo-sbol")
    fig_initial = line_chart_gigasearch(df_gs, y_min, y_max)
    current_initial = df_gs["calls"].iloc[-1]
    pct_initial = _pct_change_current_vs_previous(df_gs["calls"])

    # График инициатив
    df_init = get_initiatives_data()
    fig_initiatives = line_chart_initiatives(df_init)

    # График «Источники RAG» (бублик)
    rag_data = get_rag_sources_data("alpha")
    rag_labels = [d["label"] for d in rag_data]
    rag_values = [d["value"] for d in rag_data]
    fig_rag = donut_chart_rag_sources(rag_labels, rag_values)
    total_gs = int(df_init["gigasearch"].sum())
    delta_gs = int(df_init["gigasearch"].iloc[-1])
    total_gq = int(df_init["gigaquery"].sum())
    delta_gq = int(df_init["gigaquery"].iloc[-1])
    total_summ = int(df_init["summarization"].sum())
    delta_summ = int(df_init["summarization"].iloc[-1])

    return html.Div(
        [
            dcc.Store(id="services-slide-index", data=0),
            dcc.Store(
                id="services-filter-store",
                data={"0": "common-wo-sbol", "1": "alpha", "2": "alpha"},
            ),
            html.Header(
                html.H1("IDP Dashboard", className="dashboard-title"),
                className="dashboard-header",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Button(
                                        "‹",
                                        id="services-slide-prev",
                                        className="services-slide-arrow",
                                        title="Предыдущий график",
                                        n_clicks=0,
                                    ),
                                    html.Div(
                                        [
                                            html.H2(
                                                SERVICES_SLIDE_TITLES[0],
                                                id="services-chart-title",
                                                className="chart-card-title services-slide-title",
                                            ),
                                            html.Div(
                                                [
                                                    html.Span(
                                                        format_kpi_value(current_initial),
                                                        id="services-kpi-value",
                                                        className="kpi-value",
                                                    ),
                                                    html.Span(
                                                        kpi_badge_children(pct_initial),
                                                        id="services-kpi-badge",
                                                        className="kpi-badge",
                                                        style={"backgroundColor": COLORS["kpi_badge_bg"], "border": f"1px solid {COLORS['kpi_badge_border']}"},
                                                    ),
                                                ],
                                                className="kpi-row",
                                            ),
                                        ],
                                        className="services-slide-title-kpi-block",
                                    ),
                                    html.Button(
                                        "›",
                                        id="services-slide-next",
                                        className="services-slide-arrow",
                                        title="Следующий график",
                                        n_clicks=0,
                                    ),
                                ],
                                className="services-slide-header",
                            ),
                            dcc.Graph(
                                figure=fig_initial,
                                id="chart-services",
                                config={"responsive": True, "displayModeBar": False},
                                className="dashboard-chart",
                            ),
                            dcc.RadioItems(
                                id="services-filter",
                                options=GIGASEARCH_FILTER_OPTIONS,
                                value="common-wo-sbol",
                                className="services-filter-buttons",
                            ),
                        ],
                        className="chart-card services-carousel-card",
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
                                                                        style={"backgroundColor": COLORS["kpi_badge_bg"], "border": f"1px solid {COLORS['kpi_badge_border']}"},
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
                                                                        style={"backgroundColor": COLORS["kpi_badge_bg"], "border": f"1px solid {COLORS['kpi_badge_border']}"},
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
                                                                        style={"backgroundColor": COLORS["kpi_badge_bg"], "border": f"1px solid {COLORS['kpi_badge_border']}"},
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
                                        className="initiatives-left-block",
                                    ),
                                    html.Div(
                                        [
                                            html.H2(
                                                "Источники RAG",
                                                className="chart-card-title",
                                            ),
                                            dcc.Graph(
                                                figure=fig_rag,
                                                id="chart-rag",
                                                config={"responsive": True, "displayModeBar": False},
                                                className="dashboard-chart rag-donut-chart",
                                            ),
                                            dcc.RadioItems(
                                                id="rag-filter",
                                                options=[
                                                    {"label": "Alpha", "value": "alpha"},
                                                    {"label": "Sigma", "value": "sigma"},
                                                ],
                                                value="alpha",
                                                className="rag-filter-buttons",
                                            ),
                                        ],
                                        className="chart-card rag-chart-card",
                                    ),
                                ],
                                className="initiatives-charts-row",
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
