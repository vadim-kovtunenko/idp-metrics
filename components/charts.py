"""
Reusable chart components built with Plotly.
Each chart function accepts data and returns a Plotly figure with shared theme.
"""
import pandas as pd
import plotly.graph_objects as go

from config.theme import (
    CHART_FRAME_BG,
    COLORS,
    CHART_ACCENT_COLORS,
    RAG_SOURCE_COLORS,
    get_chart_layout_overrides,
    hex_to_rgba,
)


def _format_month_axis(dates: pd.DatetimeIndex) -> list:
    """Format dates for x-axis labels (e.g. 2/25, 3/25)."""
    return [f"{d.month}/{d.strftime('%y')}" for d in dates]


def _y_ticks_from_range(y_min: float, y_max: float) -> tuple:
    """Return (tickvals, ticktext) for a given y range, без первой метки (0)."""
    if y_max >= 1_000_000:
        step = (y_max - y_min) / 4
        vals = [y_min + i * step for i in range(1, 5)]
        texts = [
            f"{int(v / 1e6)}M" if v >= 1e6 else f"{int(v / 1e3)}K" if v >= 1e3 else "0"
            for v in vals
        ]
    else:
        step = (y_max - y_min) / 4
        vals = [y_min + i * step for i in range(1, 5)]
        texts = [f"{int(v / 1e3)}K" if v >= 1000 else "0" for v in vals]
    return vals, texts


def line_chart_gigasearch(df: pd.DataFrame, y_min: float, y_max: float) -> go.Figure:
    """
    Line chart for IDP GigaSearch with configurable y range.
    X-axis: months.
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["line_primary"], 0.06),
            line=dict(color=COLORS["line_primary"], width=2, shape="spline", smoothing=0.2),
        )
    )

    tick_vals, tick_text = _y_ticks_from_range(y_min, y_max)
    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [y_min, y_max]
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickvals"] = tick_vals
    layout["yaxis"]["ticktext"] = tick_text

    fig.update_layout(**layout)
    return fig


def line_chart_rag_common_sbol(df: pd.DataFrame) -> go.Figure:
    """
    Line chart: RAG Common & SBOL — monthly service calls.
    Y-axis: 20M–45M, X-axis: months.
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["line_primary"], 0.06),
            line=dict(color=COLORS["line_primary"], width=2, shape="spline", smoothing=0.2),
        )
    )

    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [20_000_000, 45_000_000]
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickprefix"] = ""
    # Format y ticks as "20M", "25M", etc.
    layout["yaxis"]["tickvals"] = [25e6, 30e6, 35e6, 40e6, 45e6]
    layout["yaxis"]["ticktext"] = ["25M", "30M", "35M", "40M", "45M"]

    fig.update_layout(**layout)
    return fig


def line_chart_rag_common(df: pd.DataFrame) -> go.Figure:
    """
    Line chart: RAG Common — monthly service calls.
    Y-axis: 500K–3M, X-axis: months.
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["line_primary"], 0.06),
            line=dict(color=COLORS["line_primary"], width=2, shape="spline", smoothing=0.2),
        )
    )

    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [500_000, 3_000_000]
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickvals"] = [1e6, 1.5e6, 2e6, 2.5e6, 3e6]
    layout["yaxis"]["ticktext"] = ["1M", "1.5M", "2M", "2.5M", "3M"]

    fig.update_layout(**layout)
    return fig


def line_chart_summarization(df: pd.DataFrame) -> go.Figure:
    """
    Line chart: Summarization — monthly service calls.
    Y-axis: 0–2M, X-axis: months.
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["line_primary"], 0.06),
            line=dict(color=COLORS["line_primary"], width=2, shape="spline", smoothing=0.2),
        )
    )

    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [0, 2_000_000]
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickvals"] = [500_000, 1e6, 1.5e6, 2e6]
    layout["yaxis"]["ticktext"] = ["500K", "1M", "1.5M", "2M"]

    fig.update_layout(**layout)
    return fig


def line_chart_gigaquery(df: pd.DataFrame) -> go.Figure:
    """
    Line chart: GigaQuery — monthly service calls.
    Y-axis: 0–2M, X-axis: months.
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["line_primary"], 0.06),
            line=dict(color=COLORS["line_primary"], width=2, shape="spline", smoothing=0.2),
        )
    )

    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [0, 2_000_000]
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickvals"] = [500_000, 1e6, 1.5e6, 2e6]
    layout["yaxis"]["ticktext"] = ["500K", "1M", "1.5M", "2M"]

    fig.update_layout(**layout)
    return fig


# Цвета линий графика инициатив (три серии)
INITIATIVES_LINE_COLORS = {
    "GigaSearch": CHART_ACCENT_COLORS[0],
    "GigaQuery": CHART_ACCENT_COLORS[1],
    "Summarization": CHART_ACCENT_COLORS[2],
}


def line_chart_initiatives(df: pd.DataFrame) -> go.Figure:
    """
    Линейная диаграмма: количество заведённых инициатив по месяцам.
    Три линии: GigaSearch, GigaQuery, Summarization.
    Y: 0–60, X: месяцы. Легенда под графиком.
    """
    x = _format_month_axis(df.index)
    layout = get_chart_layout_overrides()
    layout["showlegend"] = True
    layout["legend"] = {
        "orientation": "h",
        "yanchor": "top",
        "y": -0.2,
        "xanchor": "center",
        "x": 0.5,
        "font": {"color": COLORS["axis_text"], "size": 11},
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "rgba(0,0,0,0)",
        "itemwidth": 30,
        "tracegroupgap": 0,
    }
    layout["margin"]["t"] = 36
    layout["margin"]["b"] = 78
    layout["margin"]["l"] = 40
    layout["margin"]["r"] = 20
    layout["yaxis"]["range"] = [0, 60]
    layout["yaxis"]["autorange"] = False
    layout["yaxis"]["tickformat"] = ",.0f"
    layout["yaxis"]["tickvals"] = [15, 30, 45, 60]
    layout["yaxis"]["ticktext"] = ["15", "30", "45", "60"]
    # Ось X: 12 месяцев + пустая категория для трасс легенды; видим только [0, 11] — на всю ширину
    layout["xaxis"]["categoryarray"] = list(x) + [""]
    layout["xaxis"]["categoryorder"] = "array"
    layout["xaxis"]["range"] = [0, 11]
    layout["xaxis"]["autorange"] = False
    layout["xaxis"]["fixedrange"] = True

    fig = go.Figure()
    # Основные линии графика (без маркеров на графике)
    for name, col in [("GigaSearch", "gigasearch"), ("GigaQuery", "gigaquery"), ("Summarization", "summarization")]:
        color = INITIATIVES_LINE_COLORS[name]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[col].tolist(),
                mode="lines",
                name=name,
                showlegend=False,
                fill="tozeroy",
                fillcolor=hex_to_rgba(color, 0.06),
                line=dict(color=color, width=2, shape="spline", smoothing=0.2),
            )
        )
    # Только для легенды: «пончики» в цветах линий; точка за пределами видимой области
    for name in ["GigaSearch", "GigaQuery", "Summarization"]:
        color = INITIATIVES_LINE_COLORS[name]
        fig.add_trace(
            go.Scatter(
                x=[""],  # категория вне основных 12 месяцев — не попадёт в range [-0.5, 11.5]
                y=[-10],
                mode="markers",
                name=name,
                showlegend=True,
                marker=dict(
                    symbol="circle-open",
                    size=11,
                    line=dict(width=3, color=color),
                    color=color,
                ),
            )
        )
    fig.update_layout(**layout)
    return fig


def donut_chart_rag_sources(labels: list, values: list) -> go.Figure:
    """
    Круговая диаграмма-бублик «Источники RAG».
    Легенда справа от графика, те же цвета что и в других графиках.
    """
    colors = [RAG_SOURCE_COLORS[i % len(RAG_SOURCE_COLORS)] for i in range(len(labels))]
    layout = get_chart_layout_overrides()
    layout["showlegend"] = True
    layout["legend"] = {
        "orientation": "v",
        "yanchor": "middle",
        "y": 0.5,
        "xanchor": "left",
        "x": 1.02,
        "font": {"color": COLORS["axis_text"], "size": 11},
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "rgba(0,0,0,0)",
        "itemwidth": 30,
    }
    layout["margin"]["t"] = 36
    layout["margin"]["b"] = 50
    layout["margin"]["l"] = 20
    layout["margin"]["r"] = 140
    layout["height"] = 266

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color=CHART_FRAME_BG, width=2)),
                textinfo="none",
                hoverinfo="label+value+percent",
                sort=False,
            )
        ]
    )
    fig.update_layout(**layout)
    return fig
