"""
KPI block component: current value + percentage change (triangle + badge).
"""
from urllib.parse import quote

from dash import html

from config.theme import COLORS


def format_kpi_value(value: float) -> str:
    """Format numeric value for KPI display: 35.0M, 1.2M, 350.6k."""
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{value:.0f}"


def _rounded_triangle_svg_data_uri(up: bool, color: str) -> str:
    """SVG triangle with rounded corners, as data URI. Up=True = ▲, Up=False = ▼."""
    path_d = "M 8 3 L 13 13 L 3 13 Z" if up else "M 8 13 L 13 3 L 3 3 Z"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">'
        f'<path d="{path_d}" fill="{color}" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>'
        f"</svg>"
    )
    return "data:image/svg+xml," + quote(svg)


def kpi_badge_children(pct_change: float):
    """Return [Img, Span] for the KPI badge (for use in callbacks)."""
    is_positive = pct_change >= 0
    arrow_color = COLORS["kpi_arrow_positive"] if is_positive else COLORS["kpi_arrow_negative"]
    triangle_src = _rounded_triangle_svg_data_uri(is_positive, arrow_color)
    pct_str = f"{abs(pct_change):.0f}%"
    return [
        html.Img(
            src=triangle_src,
            alt="▲" if is_positive else "▼",
            className="kpi-triangle",
        ),
        html.Span(pct_str, className="kpi-badge-text"),
    ]


def kpi_card(title: str, current: float, pct_change: float) -> html.Div:
    """
    Card with title and KPI row: large current value + rounded triangle + badge with %.
    """
    is_positive = pct_change >= 0
    arrow_color = COLORS["kpi_arrow_positive"] if is_positive else COLORS["kpi_arrow_negative"]
    triangle_src = _rounded_triangle_svg_data_uri(is_positive, arrow_color)
    pct_str = f"{abs(pct_change):.0f}%"

    return html.Div(
        [
            html.H2(title, className="chart-card-title"),
            html.Div(
                [
                    html.Span(format_kpi_value(current), className="kpi-value"),
                    html.Span(
                        [
                            html.Img(
                                src=triangle_src,
                                alt="▲" if is_positive else "▼",
                                className="kpi-triangle",
                            ),
                            html.Span(pct_str, className="kpi-badge-text"),
                        ],
                        className="kpi-badge",
                        style={"backgroundColor": COLORS["kpi_badge_bg"]},
                    ),
                ],
                className="kpi-row",
            ),
        ],
        className="chart-card-header",
    )
