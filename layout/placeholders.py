"""
Placeholder pages for IDP Dashboard navigation.
"""
from dash import html
from config.theme import COLORS


def build_placeholder_page(title: str, description: str = None) -> html.Div:
    """
    Build a placeholder page for navigation items.
    
    Args:
        title: Page title
        description: Optional description text
        
    Returns:
        html.Div: Placeholder page content
    """
    if description is None:
        description = f"This is the {title.lower()} page. Content coming soon."
    
    return html.Div(
        [
            html.H1(title, className="dashboard-title"),
            html.Div(
                [
                    html.Div(
                        style={
                            "width": "80px",
                            "height": "80px",
                            "borderRadius": "50%",
                            "backgroundColor": COLORS["accent_gray"],
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "32px",
                            "marginBottom": "24px",
                        },
                    ),
                    html.P(description, style={"fontSize": "16px", "color": COLORS["text_secondary"], "maxWidth": "500px"}),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": "60px 20px",
                    "textAlign": "center",
                },
            ),
        ],
        className="dashboard-wrapper",
    )


def build_initiatives_page() -> html.Div:
    """Build Initiatives placeholder page."""
    return build_placeholder_page(
        "Initiatives",
        "Track and manage your AI initiatives. View performance metrics, allocate resources, and monitor progress across all services."
    )


def build_analytics_page() -> html.Div:
    """Build Analytics placeholder page."""
    return build_placeholder_page(
        "Analytics",
        "Deep dive into your dashboard analytics. Explore trends, compare periods, and generate detailed reports."
    )


def build_settings_page() -> html.Div:
    """Build Settings placeholder page."""
    return build_placeholder_page(
        "Settings",
        "Configure your dashboard preferences, manage API keys, set up notifications, and customize your experience."
    )
