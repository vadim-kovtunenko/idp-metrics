"""
Theme configuration for the IDP Dashboard.
Dark theme based on reference design.
"""

# Dashboard colors (Dark theme)
COLORS = {
    # Backgrounds
    "dashboard_bg": "#FFFFFF",
    "card_bg": "#FFFFFF",
    "card_bg_secondary": "#F0F0F5",
    "card_bg_dark": "#1A1A1A",
    "card_bg_accent": "#A8D5E2",
    
    # Text
    "text_primary": "#1A1A1A",
    "text_secondary": "#6B6B6B",
    "text_muted": "#9B9B9B",
    "text_on_dark": "#FFFFFF",
    "text_on_accent": "#1A1A1A",
    
    # Borders and dividers
    "border": "#E8E8E8",
    "divider": "#F0F0F0",
    
    # Chart colors
    "chart_bg": "#FFFFFF",
    "chart_grid": "#E8E8E8",
    "chart_line": "#1A1A1A",
    "chart_line_secondary": "#A8D5E2",
    "chart_fill": "rgba(26, 26, 26, 0.1)",
    
    # Accent colors
    "accent_blue": "#A8D5E2",
    "accent_blue_dark": "#7FB8D0",
    "accent_black": "#1A1A1A",
    "accent_gray": "#F0F0F5",
    
    # KPI badges
    "kpi_badge_bg": "#1A1A1A",
    "kpi_badge_text": "#FFFFFF",
    "kpi_arrow_positive": "#48B785",
    "kpi_arrow_negative": "#F87171",
    
    # Buttons
    "button_primary": "#1A1A1A",
    "button_primary_text": "#FFFFFF",
    "button_secondary": "#A8D5E2",
    "button_secondary_text": "#1A1A1A",
    "button_hover": "#333333",
}

# Chart accent colors for multiple series
CHART_ACCENT_COLORS = ("#1A1A1A", "#A8D5E2", "#7FB8D0")

# RAG source colors
RAG_SOURCE_COLORS = ("#1A1A1A", "#A8D5E2", "#7FB8D0", "#48B785")

# Plotly layout defaults
CHART_FRAME_BG = "#FFFFFF"


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex #RRGGBB to rgba(r,g,b,alpha)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def get_chart_layout_overrides():
    """Return common layout overrides for all charts."""
    return {
        "paper_bgcolor": CHART_FRAME_BG,
        "plot_bgcolor": CHART_FRAME_BG,
        "font": {"color": COLORS["text_primary"], "family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif", "size": 12},
        "xaxis": {
            "showgrid": True,
            "gridcolor": COLORS["chart_grid"],
            "gridwidth": 1,
            "linecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_muted"], "size": 11},
            "zerolinecolor": COLORS["border"],
        },
        "yaxis": {
            "showgrid": True,
            "gridcolor": COLORS["chart_grid"],
            "gridwidth": 1,
            "linecolor": COLORS["border"],
            "tickfont": {"color": COLORS["text_muted"], "size": 11},
            "zerolinecolor": COLORS["border"],
        },
        "margin": {"t": 40, "b": 40, "l": 50, "r": 30},
        "height": 280,
        "showlegend": False,
    }
