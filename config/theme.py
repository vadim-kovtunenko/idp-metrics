"""
Theme configuration for the IDP Dashboard.
Centralized colors and chart styling for consistency and easy maintenance.
"""

# Dashboard & chart colors (Hex)
COLORS = {
    "dashboard_bg": "#DFE4E9",
    "chart_bg": "#FAFAFA",
    "line_primary": "#3541FB",  # один график — по умолчанию
    "axis_grid": "#333333",
    "axis_text": "#000000",
    "title_text": "#000000",
    "axis_tick_muted": "#333333",
    # Плашки KPI: фон и стрелка
    "kpi_badge_bg": "#DBFDEC",
    "kpi_badge_border": "#b8e8c8",
    "kpi_arrow_positive": "#48B785",
    "kpi_arrow_negative": "#F87171",
}

# Акцентные цвета графиков: несколько серий — 47E3FF, 3B8BFA, 3541FB
CHART_ACCENT_COLORS = ("#47E3FF", "#3B8BFA", "#3541FB")

# Plotly layout defaults for charts (shared across all charts)
CHART_FRAME_BG = "#FAFAFA"  # фон рамки и области графика


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex #RRGGBB to rgba(r,g,b,alpha)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def get_chart_layout_overrides():
    """Return common layout overrides for all charts (background, font, grid)."""
    return {
        "paper_bgcolor": CHART_FRAME_BG,
        "plot_bgcolor": CHART_FRAME_BG,
        "font": {"color": COLORS["axis_text"], "family": "Helvetica, Arial, sans-serif"},
        "xaxis": {
            "showgrid": False,
            "linecolor": COLORS["axis_grid"],
            "tickfont": {"color": COLORS["axis_tick_muted"], "size": 11},
            "zerolinecolor": COLORS["axis_grid"],
        },
        "yaxis": {
            "showgrid": False,
            "linecolor": COLORS["axis_grid"],
            "tickfont": {"color": COLORS["axis_tick_muted"], "size": 11},
            "zerolinecolor": COLORS["axis_grid"],
        },
        "margin": {"t": 50, "b": 50, "l": 60, "r": 30},
        "height": 266,  # 30% less than 380px
        "showlegend": False,
    }
