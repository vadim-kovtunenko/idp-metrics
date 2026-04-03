"""
Reusable chart components built with Plotly.
Clean, minimal design matching reference dashboard.
"""
from typing import Literal

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


def _format_month_axis(dates: pd.DatetimeIndex) -> list[str]:
    """Format dates for x-axis labels (e.g. 2/25, 3/25)."""
    return [f"{d.month}/{d.strftime('%y')}" for d in dates]


def _y_ticks_from_range(y_min: float, y_max: float) -> tuple[list[float], list[str]]:
    """Return (tickvals, ticktext) for a given y range, without first label (0)."""
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


def line_chart(
    df: pd.DataFrame,
    y_min: float,
    y_max: float,
    y_tick_vals: list[float] | None = None,
    y_tick_texts: list[str] | None = None,
    show_secondary: bool = False,
) -> go.Figure:
    """
    Clean line chart with dot grid background.
    
    Args:
        df: DataFrame with 'calls' column and DatetimeIndex
        y_min: Y-axis minimum value
        y_max: Y-axis maximum value
        y_tick_vals: Custom Y tick values (optional)
        y_tick_texts: Custom Y tick labels (optional)
        show_secondary: Show secondary dotted line (comparison)
    """
    x = _format_month_axis(df.index)
    y = df["calls"].tolist()

    fig = go.Figure()
    
    # Secondary line (comparison/dotted)
    if show_secondary:
        y_secondary = [v * 1.15 for v in y]  # Simulated comparison data
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y_secondary,
                mode="lines",
                line=dict(color=COLORS["chart_line_secondary"], width=2, dash="dot"),
                opacity=0.5,
                showlegend=False,
            )
        )
    
    # Main line
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            fill="tozeroy",
            fillcolor=hex_to_rgba(COLORS["chart_line"], 0.08),
            line=dict(color=COLORS["chart_line"], width=2.5, shape="spline", smoothing=0.3),
        )
    )

    layout = get_chart_layout_overrides()
    layout["xaxis"]["tickangle"] = 0
    layout["yaxis"]["range"] = [y_min, y_max]
    layout["yaxis"]["tickformat"] = ",.0f"
    
    # Dot grid effect
    layout["xaxis"]["gridcolor"] = COLORS["chart_grid"]
    layout["yaxis"]["gridcolor"] = COLORS["chart_grid"]
    layout["xaxis"]["gridwidth"] = 1
    layout["yaxis"]["gridwidth"] = 1
    
    if y_tick_vals and y_tick_texts:
        layout["yaxis"]["tickvals"] = y_tick_vals
        layout["yaxis"]["ticktext"] = y_tick_texts
    else:
        tick_vals, tick_text = _y_ticks_from_range(y_min, y_max)
        layout["yaxis"]["tickvals"] = tick_vals
        layout["yaxis"]["ticktext"] = tick_text

    fig.update_layout(**layout)
    return fig


def multi_line_chart(
    df: pd.DataFrame,
    columns: dict[str, str],
    y_min: float,
    y_max: float,
    y_tick_vals: list[float] | None = None,
    y_tick_texts: list[str] | None = None,
    legend_below: bool = True,
) -> go.Figure:
    """
    Multi-line chart with area fill for multiple series.
    
    Args:
        df: DataFrame with columns and DatetimeIndex
        columns: Dict mapping display name to column name
        y_min: Y-axis minimum value
        y_max: Y-axis maximum value
        y_tick_vals: Custom Y tick values (optional)
        y_tick_texts: Custom Y tick labels (optional)
        legend_below: Whether to show legend below chart
    """
    x = _format_month_axis(df.index)
    
    layout = get_chart_layout_overrides()
    layout["showlegend"] = True
    
    if legend_below:
        layout["legend"] = {
            "orientation": "h",
            "yanchor": "top",
            "y": -0.25,
            "xanchor": "center",
            "x": 0.5,
            "font": {"color": COLORS["text_muted"], "size": 12},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(0,0,0,0)",
            "itemwidth": 30,
            "tracegroupgap": 0,
        }
        layout["margin"]["t"] = 30
        layout["margin"]["b"] = 60
        layout["margin"]["l"] = 40
        layout["margin"]["r"] = 20
    
    layout["yaxis"]["range"] = [y_min, y_max]
    layout["yaxis"]["tickformat"] = ",.0f"
    
    if y_tick_vals and y_tick_texts:
        layout["yaxis"]["tickvals"] = y_tick_vals
        layout["yaxis"]["ticktext"] = y_tick_texts
    
    layout["xaxis"]["categoryarray"] = list(x)
    layout["xaxis"]["categoryorder"] = "array"
    layout["xaxis"]["range"] = [0, len(x) - 1] if x else [0, 1]
    layout["xaxis"]["fixedrange"] = True

    fig = go.Figure()
    color_values = list(CHART_ACCENT_COLORS)
    
    for i, (name, col) in enumerate(columns.items()):
        color = color_values[i % len(color_values)]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=df[col].tolist(),
                mode="lines",
                name=name,
                showlegend=False,
                fill="tozeroy",
                fillcolor=hex_to_rgba(color, 0.1),
                line=dict(color=color, width=2, shape="spline", smoothing=0.3),
            )
        )
    
    # Add legend markers
    for i, name in enumerate(columns.keys()):
        color = color_values[i % len(color_values)]
        fig.add_trace(
            go.Scatter(
                x=[""],
                y=[-10],
                mode="markers",
                name=name,
                showlegend=True,
                marker=dict(
                    symbol="circle",
                    size=10,
                    color=color,
                ),
            )
        )
    
    fig.update_layout(**layout)
    return fig


def donut_chart(labels: list[str], values: list[float | int]) -> go.Figure:
    """
    Clean donut chart with legend on the right.
    
    Args:
        labels: Category labels
        values: Category values
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
        "font": {"color": COLORS["text_primary"], "size": 12},
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "rgba(0,0,0,0)",
        "itemwidth": 30,
    }
    layout["margin"]["t"] = 30
    layout["margin"]["b"] = 40
    layout["margin"]["l"] = 20
    layout["margin"]["r"] = 120
    layout["height"] = 280

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color=CHART_FRAME_BG, width=3)),
                textinfo="none",
                hoverinfo="label+value+percent",
                sort=False,
            )
        ]
    )
    fig.update_layout(**layout)
    return fig
