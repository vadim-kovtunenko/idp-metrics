"""
UI Kit component for IDP Dashboard.
Comprehensive design system reference with all UI components.
"""
from dash import html, dcc
from config.theme import COLORS


def color_palette():
    """Display color palette with all theme colors."""
    colors = [
        {"name": "Dashboard BG", "value": COLORS["dashboard_bg"], "text": COLORS["text_primary"]},
        {"name": "Card BG", "value": COLORS["card_bg"], "text": COLORS["text_primary"]},
        {"name": "Card BG Secondary", "value": COLORS["card_bg_secondary"], "text": COLORS["text_primary"]},
        {"name": "Card BG Dark", "value": COLORS["card_bg_dark"], "text": COLORS["text_on_dark"]},
        {"name": "Card BG Accent", "value": COLORS["card_bg_accent"], "text": COLORS["text_on_accent"]},
        {"name": "Text Primary", "value": COLORS["text_primary"], "text": "#FFFFFF"},
        {"name": "Text Secondary", "value": COLORS["text_secondary"], "text": "#FFFFFF"},
        {"name": "Text Muted", "value": COLORS["text_muted"], "text": "#FFFFFF"},
        {"name": "Accent Blue", "value": COLORS["accent_blue"], "text": COLORS["text_on_accent"]},
        {"name": "Accent Black", "value": COLORS["accent_black"], "text": "#FFFFFF"},
        {"name": "Border", "value": COLORS["border"], "text": COLORS["text_primary"]},
    ]
    
    return html.Div(
        [
            html.H3("Color Palette", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                style={
                                    "width": "100%",
                                    "height": "80px",
                                    "borderRadius": "8px",
                                    "backgroundColor": color["value"],
                                    "border": f"1px solid {COLORS['border']}",
                                    "marginBottom": "8px",
                                },
                            ),
                            html.Div(color["name"], style={"fontSize": "12px", "color": COLORS["text_secondary"], "marginBottom": "4px"}),
                            html.Div(color["value"], style={"fontSize": "11px", "color": COLORS["text_muted"], "fontFamily": "monospace"}),
                        ],
                        style={"flex": "1", "minWidth": "120px"},
                    )
                    for color in colors
                ],
                style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "32px"},
            ),
        ],
        className="uikit-section",
    )


def typography():
    """Display typography scale."""
    return html.Div(
        [
            html.H3("Typography", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Dashboard Title", style={"fontSize": "28px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "4px"}),
                            html.Div("28px / Semibold", style={"fontSize": "12px", "color": COLORS["text_muted"]}),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.Div("Card Title", style={"fontSize": "18px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "4px"}),
                            html.Div("18px / Semibold", style={"fontSize": "12px", "color": COLORS["text_muted"]}),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.Div("Body Text Regular", style={"fontSize": "15px", "fontWeight": "400", "color": COLORS["text_primary"], "marginBottom": "4px"}),
                            html.Div("15px / Regular", style={"fontSize": "12px", "color": COLORS["text_muted"]}),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.Div("Secondary Text", style={"fontSize": "13px", "fontWeight": "500", "color": COLORS["text_secondary"], "marginBottom": "4px"}),
                            html.Div("13px / Medium", style={"fontSize": "12px", "color": COLORS["text_muted"]}),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.Div("Muted Text", style={"fontSize": "12px", "fontWeight": "400", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div("12px / Regular", style={"fontSize": "12px", "color": COLORS["text_muted"]}),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                ],
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "24px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def buttons():
    """Display button styles."""
    return html.Div(
        [
            html.H3("Buttons", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Button("Primary Button", className="btn btn-primary", style={
                                "padding": "12px 24px",
                                "borderRadius": "8px",
                                "border": "none",
                                "backgroundColor": COLORS["button_primary"],
                                "color": COLORS["button_primary_text"],
                                "fontSize": "14px",
                                "fontWeight": "500",
                                "cursor": "pointer",
                                "marginRight": "12px",
                                "marginBottom": "12px",
                            }),
                            html.Button("Secondary Button", className="btn btn-secondary", style={
                                "padding": "12px 24px",
                                "borderRadius": "8px",
                                "border": "none",
                                "backgroundColor": COLORS["button_secondary"],
                                "color": COLORS["button_secondary_text"],
                                "fontSize": "14px",
                                "fontWeight": "500",
                                "cursor": "pointer",
                                "marginRight": "12px",
                                "marginBottom": "12px",
                            }),
                            html.Button("Outline Button", className="btn btn-outline", style={
                                "padding": "12px 24px",
                                "borderRadius": "8px",
                                "border": f"1px solid {COLORS['border']}",
                                "backgroundColor": "transparent",
                                "color": COLORS["text_primary"],
                                "fontSize": "14px",
                                "fontWeight": "500",
                                "cursor": "pointer",
                                "marginRight": "12px",
                                "marginBottom": "12px",
                            }),
                        ],
                        style={"marginBottom": "24px"},
                    ),
                    html.Div(
                        [
                            html.Button("Small", className="btn btn-sm", style={
                                "padding": "8px 16px",
                                "borderRadius": "6px",
                                "border": "none",
                                "backgroundColor": COLORS["button_primary"],
                                "color": COLORS["button_primary_text"],
                                "fontSize": "12px",
                                "fontWeight": "500",
                                "cursor": "pointer",
                                "marginRight": "12px",
                            }),
                            html.Button("Large", className="btn btn-lg", style={
                                "padding": "16px 32px",
                                "borderRadius": "10px",
                                "border": "none",
                                "backgroundColor": COLORS["button_primary"],
                                "color": COLORS["button_primary_text"],
                                "fontSize": "16px",
                                "fontWeight": "500",
                                "cursor": "pointer",
                            }),
                        ],
                    ),
                ],
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def cards():
    """Display card variations."""
    return html.Div(
        [
            html.H3("Cards", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("Default Card", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "8px"}),
                            html.Div("Card content with default styling", style={"fontSize": "14px", "color": COLORS["text_secondary"]}),
                        ],
                        className="card card-default",
                        style={
                            "padding": "24px",
                            "borderRadius": "12px",
                            "backgroundColor": COLORS["card_bg"],
                            "border": f"1px solid {COLORS['border']}",
                            "flex": "1",
                            "minWidth": "200px",
                        },
                    ),
                    html.Div(
                        [
                            html.Div("Secondary Card", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_primary"], "marginBottom": "8px"}),
                            html.Div("Card with secondary background", style={"fontSize": "14px", "color": COLORS["text_secondary"]}),
                        ],
                        className="card card-secondary",
                        style={
                            "padding": "24px",
                            "borderRadius": "12px",
                            "backgroundColor": COLORS["card_bg_secondary"],
                            "border": "none",
                            "flex": "1",
                            "minWidth": "200px",
                        },
                    ),
                    html.Div(
                        [
                            html.Div("Dark Card", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_on_dark"], "marginBottom": "8px"}),
                            html.Div("Card with dark background", style={"fontSize": "14px", "color": COLORS["text_muted"]}),
                        ],
                        className="card card-dark",
                        style={
                            "padding": "24px",
                            "borderRadius": "12px",
                            "backgroundColor": COLORS["card_bg_dark"],
                            "border": "none",
                            "flex": "1",
                            "minWidth": "200px",
                        },
                    ),
                    html.Div(
                        [
                            html.Div("Accent Card", style={"fontSize": "16px", "fontWeight": "600", "color": COLORS["text_on_accent"], "marginBottom": "8px"}),
                            html.Div("Card with accent background", style={"fontSize": "14px", "color": COLORS["text_on_accent"]}),
                        ],
                        className="card card-accent",
                        style={
                            "padding": "24px",
                            "borderRadius": "12px",
                            "backgroundColor": COLORS["card_bg_accent"],
                            "border": "none",
                            "flex": "1",
                            "minWidth": "200px",
                        },
                    ),
                ],
                style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def kpi_components():
    """Display KPI and metric components."""
    return html.Div(
        [
            html.H3("KPI Components", className="uikit-section-title"),
            html.Div(
                [
                    # KPI with badge
                    html.Div(
                        [
                            html.Div("Total Calls", style={"fontSize": "13px", "color": COLORS["text_secondary"], "marginBottom": "8px"}),
                            html.Div(
                                [
                                    html.Span("2,345", style={"fontSize": "36px", "fontWeight": "600", "color": COLORS["text_primary"], "marginRight": "12px"}),
                                    html.Div(
                                        [
                                            html.Span("▼", style={"fontSize": "10px", "marginRight": "4px"}),
                                            html.Span("12.5%", style={"fontSize": "13px", "fontWeight": "500"}),
                                        ],
                                        style={
                                            "display": "inline-flex",
                                            "alignItems": "center",
                                            "padding": "6px 12px",
                                            "borderRadius": "20px",
                                            "backgroundColor": "#F87171",
                                            "color": "#FFFFFF",
                                        },
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                        ],
                        style={"padding": "20px", "borderRadius": "12px", "backgroundColor": COLORS["card_bg"], "border": f"1px solid {COLORS['border']}", "flex": "1"},
                    ),
                    # Positive KPI
                    html.Div(
                        [
                            html.Div("Success Rate", style={"fontSize": "13px", "color": COLORS["text_secondary"], "marginBottom": "8px"}),
                            html.Div(
                                [
                                    html.Span("98.2%", style={"fontSize": "36px", "fontWeight": "600", "color": COLORS["text_primary"], "marginRight": "12px"}),
                                    html.Div(
                                        [
                                            html.Span("▲", style={"fontSize": "10px", "marginRight": "4px"}),
                                            html.Span("3.2%", style={"fontSize": "13px", "fontWeight": "500"}),
                                        ],
                                        style={
                                            "display": "inline-flex",
                                            "alignItems": "center",
                                            "padding": "6px 12px",
                                            "borderRadius": "20px",
                                            "backgroundColor": "#48B785",
                                            "color": "#FFFFFF",
                                        },
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                        ],
                        style={"padding": "20px", "borderRadius": "12px", "backgroundColor": COLORS["card_bg"], "border": f"1px solid {COLORS['border']}", "flex": "1"},
                    ),
                ],
                style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def form_elements():
    """Display form elements."""
    return html.Div(
        [
            html.H3("Form Elements", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Text Input", style={"fontSize": "13px", "fontWeight": "500", "color": COLORS["text_primary"], "marginBottom": "8px", "display": "block"}),
                            dcc.Input(
                                type="text",
                                placeholder="Enter text...",
                                style={
                                    "width": "100%",
                                    "padding": "12px 16px",
                                    "borderRadius": "8px",
                                    "border": f"1px solid {COLORS['border']}",
                                    "fontSize": "14px",
                                    "color": COLORS["text_primary"],
                                    "backgroundColor": COLORS["card_bg"],
                                    "outline": "none",
                                },
                            ),
                        ],
                        style={"flex": "1", "marginRight": "16px"},
                    ),
                    html.Div(
                        [
                            html.Label("Select", style={"fontSize": "13px", "fontWeight": "500", "color": COLORS["text_primary"], "marginBottom": "8px", "display": "block"}),
                            dcc.Dropdown(
                                options=[
                                    {"label": "Option 1", "value": "1"},
                                    {"label": "Option 2", "value": "2"},
                                    {"label": "Option 3", "value": "3"},
                                ],
                                value="1",
                                clearable=False,
                                style={
                                    "width": "100%",
                                    "borderRadius": "8px",
                                    "border": f"1px solid {COLORS['border']}",
                                    "fontSize": "14px",
                                    "color": COLORS["text_primary"],
                                    "backgroundColor": COLORS["card_bg"],
                                    "cursor": "pointer",
                                },
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={"display": "flex", "marginBottom": "24px"},
            ),
            # Checkbox and Radio
            html.Div(
                [
                    html.Label(
                        [dcc.Input(type="checkbox", value=True, style={"marginRight": "8px"}), "Checkbox Label"],
                        style={"fontSize": "14px", "color": COLORS["text_primary"], "marginRight": "24px", "cursor": "pointer"},
                    ),
                    html.Label(
                        [dcc.Input(type="radio", name="radio", value=True, style={"marginRight": "8px"}), "Radio Label"],
                        style={"fontSize": "14px", "color": COLORS["text_primary"], "cursor": "pointer"},
                    ),
                ],
                style={"marginTop": "16px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def tables():
    """Display table styles."""
    return html.Div(
        [
            html.H3("Tables", className="uikit-section-title"),
            html.Div(
                [
                    html.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Name", style={"textAlign": "left", "padding": "12px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["text_secondary"]}),
                                        html.Th("Status", style={"textAlign": "left", "padding": "12px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["text_secondary"]}),
                                        html.Th("Value", style={"textAlign": "right", "padding": "12px", "fontSize": "13px", "fontWeight": "500", "color": COLORS["text_secondary"]}),
                                    ],
                                    style={"borderBottom": f"1px solid {COLORS['border']}"},
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td("GigaSearch", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"]}),
                                            html.Td(
                                                html.Span("Active", style={
                                                    "padding": "4px 12px",
                                                    "borderRadius": "12px",
                                                    "fontSize": "12px",
                                                    "fontWeight": "500",
                                                    "backgroundColor": "#E8F5E9",
                                                    "color": "#48B785",
                                                }),
                                                style={"padding": "12px"},
                                            ),
                                            html.Td("$2.34K", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"], "textAlign": "right"}),
                                        ],
                                        style={"borderBottom": f"1px solid {COLORS['border']}"},
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("GigaQuery", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"]}),
                                            html.Td(
                                                html.Span("Active", style={
                                                    "padding": "4px 12px",
                                                    "borderRadius": "12px",
                                                    "fontSize": "12px",
                                                    "fontWeight": "500",
                                                    "backgroundColor": "#E8F5E9",
                                                    "color": "#48B785",
                                                }),
                                                style={"padding": "12px"},
                                            ),
                                            html.Td("$1.89K", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"], "textAlign": "right"}),
                                        ],
                                        style={"borderBottom": f"1px solid {COLORS['border']}"},
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("Summarization", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"]}),
                                            html.Td(
                                                html.Span("Pending", style={
                                                    "padding": "4px 12px",
                                                    "borderRadius": "12px",
                                                    "fontSize": "12px",
                                                    "fontWeight": "500",
                                                    "backgroundColor": "#FFF3E0",
                                                    "color": "#FF9800",
                                                }),
                                                style={"padding": "12px"},
                                            ),
                                            html.Td("$0.95K", style={"padding": "12px", "fontSize": "14px", "color": COLORS["text_primary"], "textAlign": "right"}),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                        style={"width": "100%", "borderCollapse": "collapse"},
                    ),
                ],
                style={
                    "backgroundColor": COLORS["card_bg"],
                    "borderRadius": "12px",
                    "border": f"1px solid {COLORS['border']}",
                    "overflow": "hidden",
                },
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def icons_and_badges():
    """Display icons and badge styles."""
    return html.Div(
        [
            html.H3("Icons & Badges", className="uikit-section-title"),
            html.Div(
                [
                    # Status badges
                    html.Div(
                        [
                            html.Div("Status Badges", style={"fontSize": "13px", "color": COLORS["text_secondary"], "marginBottom": "12px"}),
                            html.Div(
                                [
                                    html.Span("Success", style={
                                        "padding": "6px 14px",
                                        "borderRadius": "16px",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "backgroundColor": "#48B785",
                                        "color": "#FFFFFF",
                                        "marginRight": "8px",
                                    }),
                                    html.Span("Warning", style={
                                        "padding": "6px 14px",
                                        "borderRadius": "16px",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "backgroundColor": "#FF9800",
                                        "color": "#FFFFFF",
                                        "marginRight": "8px",
                                    }),
                                    html.Span("Error", style={
                                        "padding": "6px 14px",
                                        "borderRadius": "16px",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "backgroundColor": "#F87171",
                                        "color": "#FFFFFF",
                                        "marginRight": "8px",
                                    }),
                                    html.Span("Info", style={
                                        "padding": "6px 14px",
                                        "borderRadius": "16px",
                                        "fontSize": "13px",
                                        "fontWeight": "500",
                                        "backgroundColor": COLORS["accent_blue"],
                                        "color": COLORS["text_on_accent"],
                                    }),
                                ],
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                    # Icon buttons
                    html.Div(
                        [
                            html.Div("Icon Buttons", style={"fontSize": "13px", "color": COLORS["text_secondary"], "marginBottom": "12px"}),
                            html.Div(
                                [
                                    html.Button("🔍", style={
                                        "width": "40px",
                                        "height": "40px",
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['border']}",
                                        "backgroundColor": COLORS["card_bg"],
                                        "fontSize": "18px",
                                        "cursor": "pointer",
                                        "marginRight": "8px",
                                    }),
                                    html.Button("⚙", style={
                                        "width": "40px",
                                        "height": "40px",
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['border']}",
                                        "backgroundColor": COLORS["card_bg"],
                                        "fontSize": "18px",
                                        "cursor": "pointer",
                                        "marginRight": "8px",
                                    }),
                                    html.Button("🔔", style={
                                        "width": "40px",
                                        "height": "40px",
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['border']}",
                                        "backgroundColor": COLORS["card_bg"],
                                        "fontSize": "18px",
                                        "cursor": "pointer",
                                        "marginRight": "8px",
                                    }),
                                    html.Button("⋮", style={
                                        "width": "40px",
                                        "height": "40px",
                                        "borderRadius": "8px",
                                        "border": f"1px solid {COLORS['border']}",
                                        "backgroundColor": COLORS["card_bg"],
                                        "fontSize": "18px",
                                        "cursor": "pointer",
                                    }),
                                ],
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={"display": "flex", "gap": "32px", "marginBottom": "24px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def spacing_guide():
    """Display spacing and layout guide."""
    return html.Div(
        [
            html.H3("Spacing & Layout", className="uikit-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div("8px", style={"fontSize": "12px", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div(style={"height": "8px", "backgroundColor": COLORS["accent_blue"], "borderRadius": "2px", "marginBottom": "8px"}),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Div("16px", style={"fontSize": "12px", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div(style={"height": "16px", "backgroundColor": COLORS["accent_blue"], "borderRadius": "2px", "marginBottom": "8px"}),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Div("24px", style={"fontSize": "12px", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div(style={"height": "24px", "backgroundColor": COLORS["accent_blue"], "borderRadius": "2px", "marginBottom": "8px"}),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Div("32px", style={"fontSize": "12px", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div(style={"height": "32px", "backgroundColor": COLORS["accent_blue"], "borderRadius": "2px", "marginBottom": "8px"}),
                        ],
                        style={"flex": "1"},
                    ),
                    html.Div(
                        [
                            html.Div("40px", style={"fontSize": "12px", "color": COLORS["text_muted"], "marginBottom": "4px"}),
                            html.Div(style={"height": "40px", "backgroundColor": COLORS["accent_blue"], "borderRadius": "2px", "marginBottom": "8px"}),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={"display": "flex", "gap": "16px", "alignItems": "flex-end", "marginBottom": "24px"},
            ),
            html.Div(
                [
                    html.Div("Border Radius: 8px (default), 12px (cards), 16px (large elements)", style={"fontSize": "13px", "color": COLORS["text_secondary"]}),
                ],
                style={"marginTop": "16px"},
            ),
        ],
        className="uikit-section",
        style={"marginBottom": "32px"},
    )


def build_uikit_content():
    """
    Build complete UI Kit page content.
    
    Returns:
        html.Div: UI Kit page with all design system components
    """
    return html.Div(
        [
            html.Div(
                [
                    # Page header
                    html.Div(
                        [
                            html.H1("UI Kit", className="dashboard-title"),
                            html.P(
                                "Design system and component library for IDP Dashboard",
                                className="text-secondary",
                                style={"fontSize": "15px", "marginTop": "8px"},
                            ),
                        ],
                        style={"marginBottom": "32px"},
                    ),
                    
                    # Color palette
                    color_palette(),
                    
                    # Typography
                    typography(),
                    
                    # Buttons
                    buttons(),
                    
                    # Cards
                    cards(),
                    
                    # KPI Components
                    kpi_components(),
                    
                    # Form Elements
                    form_elements(),
                    
                    # Tables
                    tables(),
                    
                    # Icons & Badges
                    icons_and_badges(),
                    
                    # Spacing Guide
                    spacing_guide(),
                ],
                className="uikit-content-wrapper",
            ),
        ],
        className="uikit-page",
    )
