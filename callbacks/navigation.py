"""
Navigation callbacks for sidebar and page routing.
"""
from dash import Input, Output, callback

from layout.dashboard import build_dashboard_content
from components.uikit import build_uikit_content
from components.sidebar import build_sidebar
from layout.placeholders import (
    build_initiatives_page,
    build_analytics_page,
    build_settings_page,
)


# Page mapping
PAGES = {
    "dashboard": build_dashboard_content,
    "uikit": build_uikit_content,
    "initiatives": build_initiatives_page,
    "analytics": build_analytics_page,
    "settings": build_settings_page,
}


@callback(
    Output("page-content", "children"),
    Output("sidebar-container", "children"),
    Output("current-page", "data"),
    Input("url", "pathname"),
)
def update_page(pathname: str | None) -> tuple:
    """
    Update page content based on URL pathname.
    
    Args:
        pathname: Current URL pathname
        
    Returns:
        Tuple of (page_content, sidebar_content, page_id)
    """
    # Default to dashboard
    if pathname is None or pathname == "/":
        pathname = "/dashboard"
    
    # Extract page name from pathname
    page_id = pathname.strip("/") if pathname else "dashboard"
    
    # Validate page exists
    if page_id not in PAGES:
        page_id = "dashboard"
    
    # Get and call page builder function
    page_builder = PAGES.get(page_id, PAGES["dashboard"])
    page_content = page_builder()
    
    # Build sidebar with active page
    sidebar = build_sidebar(active_page=page_id)
    
    return page_content, sidebar, page_id
