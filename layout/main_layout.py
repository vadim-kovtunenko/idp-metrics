"""
Main application layout with sidebar navigation.
Multi-page layout structure for IDP Dashboard.
"""
from dash import dcc, html

from components.sidebar import build_sidebar
from layout.dashboard import build_dashboard_content
from config.theme import COLORS


def build_main_layout():
    """
    Build the main application layout with sidebar navigation.

    Returns:
        html.Div: Complete application layout with sidebar and content area
    """
    return html.Div(
        [
            # Location component for URL-based routing
            dcc.Location(id="url", refresh=False),

            # Hidden store for current page
            dcc.Store(id="current-page", data="dashboard"),

            # Main container with sidebar and content
            html.Div(
                [
                    # Sidebar navigation (dynamic)
                    html.Div(
                        id="sidebar-container",
                        children=build_sidebar(active_page="dashboard"),
                    ),

                    # Main content area
                    html.Div(
                        id="page-content",
                        className="page-content",
                        children=build_dashboard_content(),
                    ),
                ],
                style={
                    "display": "flex",
                    "minHeight": "100vh",
                },
            ),
        ],
        style={
            "backgroundColor": COLORS["dashboard_bg"],
            "minHeight": "100vh",
        },
    )
