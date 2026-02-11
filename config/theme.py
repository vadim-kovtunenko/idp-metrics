"""
Theme configuration for the IDP Dashboard.
Centralized colors and chart styling for consistency and easy maintenance.
"""

# Dashboard & chart colors (Hex)
COLORS = {
    "dashboard_bg": "#2A644E",
    "chart_bg": "#1F5542",
    "line_primary": "#FF7600",
    "axis_grid": "#FFFFFF",
    "axis_text": "#FFFFFF",
    "title_text": "#FFFFFF",
    "axis_tick_muted": "rgba(255, 255, 255, 0.7)",  # smaller, less bright for axis labels
    "kpi_badge_bg": "#2E8B58",
    "kpi_arrow_positive": "#4ADE80",
    "kpi_arrow_negative": "#F87171",
}

# Plotly layout defaults for charts (shared across all charts)
def get_chart_layout_overrides():
    """Return common layout overrides for all charts (background, font, grid)."""
    return {
        "paper_bgcolor": COLORS["chart_bg"],
        "plot_bgcolor": COLORS["chart_bg"],
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
