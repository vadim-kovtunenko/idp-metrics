"""
Sidebar navigation component for IDP Dashboard.
Modern light theme based on reference design.
"""
from dash import html
from dash import dcc
from config.theme import COLORS


# Menu items configuration with Unicode icons (clean, minimalist)
MENU_ITEMS = [
    {"id": "dashboard", "label": "Dashboard", "icon": "⊞"},
    {"id": "uikit", "label": "UI Kit", "icon": "◉"},
    {"id": "initiatives", "label": "Initiatives", "icon": "◫"},
    {"id": "analytics", "label": "Analytics", "icon": "📈"},
    {"id": "settings", "label": "Settings", "icon": "⚙"},
]


def sidebar_logo():
    """Create sidebar logo/brand block."""
    return html.Div(
        [
            html.Div(
                html.Span("IDP", style={"fontSize": "20px", "fontWeight": "700"}),
                style={
                    "width": "40px",
                    "height": "40px",
                    "borderRadius": "10px",
                    "background": COLORS["accent_blue"],
                    "color": COLORS["text_on_accent"],
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                },
            ),
            html.Span("Dashboard", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_primary"]}),
        ],
        style={"display": "flex", "alignItems": "center", "gap": "12px", "marginBottom": "32px"},
    )


def sidebar_menu_item(item, active=False):
    """Create a single menu item."""
    return dcc.Link(
        html.Div(
            [
                # Icon
                html.Span(
                    item["icon"],
                    style={"fontSize": "18px", "width": "24px", "textAlign": "center", "lineHeight": "1"},
                ),
                html.Span(item["label"], style={"fontSize": "14px", "fontWeight": "500"}),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "12px",
                "padding": "12px 16px",
                "borderRadius": "10px",
                "cursor": "pointer",
                "transition": "all 0.2s ease",
                "color": COLORS["accent_blue"] if active else COLORS["text_secondary"],
                "background": COLORS["accent_gray"] if active else "transparent",
                "marginBottom": "4px",
                "textDecoration": "none",
            },
            className="sidebar-menu-item active" if active else "sidebar-menu-item",
        ),
        href=f"/{item['id']}",
        style={"textDecoration": "none", "display": "block"},
    )


def sidebar_logout():
    """Create logout button at bottom of sidebar."""
    return html.Div(
        [
            html.Div(
                [
                    html.Span("⎋", style={"fontSize": "18px", "width": "24px", "textAlign": "center", "lineHeight": "1"}),
                    html.Span("Logout", style={"fontSize": "14px", "fontWeight": "500"}),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "gap": "12px",
                    "padding": "12px 16px",
                    "borderRadius": "10px",
                    "cursor": "pointer",
                    "transition": "all 0.2s ease",
                    "color": COLORS["text_secondary"],
                },
                className="sidebar-menu-item",
            ),
        ],
        style={"marginTop": "auto"},
    )


def build_sidebar(active_page="dashboard"):
    """
    Build the complete sidebar navigation.
    
    Args:
        active_page: ID of the currently active page
        
    Returns:
        html.Div: Sidebar component
    """
    return html.Div(
        [
            # Logo
            sidebar_logo(),
            
            # Menu items
            html.Div(
                [sidebar_menu_item(item, active=(item["id"] == active_page)) for item in MENU_ITEMS],
                style={"display": "flex", "flexDirection": "column"},
            ),
            
            # Logout
            sidebar_logout(),
        ],
        className="sidebar",
        style={
            "width": "260px",
            "minHeight": "100vh",
            "background": COLORS["dashboard_bg"],
            "borderRight": f"1px solid {COLORS['border']}",
            "padding": "32px 24px",
            "display": "flex",
            "flexDirection": "column",
        },
    )
