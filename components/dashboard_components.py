"""
Dashboard components: wallet cards, assets list, allocation bars.
"""
from typing import Any

from dash import html, dcc

from config.theme import COLORS


# Icon SVGs for wallet cards and assets
ICONS = {
    "gigasearch": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>',
    "gigaquery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    "summarization": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "atom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/></svg>',
    "terra": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "osmosis": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="2"/></svg>',
}


def _icon_svg(icon_svg: str) -> dcc.Markdown:
    """Render SVG icon using Markdown."""
    return dcc.Markdown(icon_svg, dangerously_allow_html=True)


def wallet_card(
    label: str,
    value: str,
    subvalue: str | None = None,
    card_type: str = "light",
    icon: str | None = None,
) -> html.Div:
    """
    Create a wallet card component.
    
    Args:
        label: Card label text
        value: Main value to display
        subvalue: Optional secondary value
        card_type: "light", "dark", or "accent"
        icon: Optional SVG icon string
    """
    card_class = "wallet-card"
    if card_type == "light":
        card_class += " wallet-card-light"
    elif card_type == "dark":
        card_class += " wallet-card-dark"
    elif card_type == "accent":
        card_class += " wallet-card-accent"
    
    icon_element = None
    if icon:
        icon_element = html.Div(
            _icon_svg(icon),
            className="wallet-card-icon",
        )
    
    return html.Div(
        [
            icon_element,
            html.Div(label, className="wallet-card-label"),
            html.Div(value, className="wallet-card-value"),
            html.Div(subvalue, className="wallet-card-subvalue") if subvalue else None,
        ],
        className=card_class,
    )


def wallet_cards_row(
    total_staked: str,
    total_rewards: str,
    available: str,
) -> html.Div:
    """
    Create a row of wallet cards.
    
    Args:
        total_balance: Total balance value
        total_staked: Total staked value
        total_rewards: Total rewards value
        available: Available amount
    """
    return html.Div(
        [
            wallet_card("Total staked", total_staked, card_type="light", icon=ICONS["atom"]),
            wallet_card("Total rewards", total_rewards, card_type="dark", icon=ICONS["gigasearch"]),
            wallet_card("Available", available, card_type="accent", icon=ICONS["gigaquery"]),
        ],
        className="wallet-cards-row",
    )


def asset_item(
    name: str,
    subname: str,
    value_primary: str,
    value_secondary: str,
    show_actions: bool = True,
) -> html.Div:
    """
    Create an asset list item.
    
    Args:
        name: Asset name
        subname: Asset subname/description
        value_primary: Primary value
        value_secondary: Secondary value
        show_actions: Whether to show Vote/Stake buttons
    """
    actions = None
    if show_actions:
        actions = html.Div(
            [
                html.Button("Vote", className="asset-btn asset-btn-vote"),
                html.Button("Stake", className="asset-btn asset-btn-stake"),
            ],
            className="asset-actions",
        )
    
    return html.Div(
        [
            html.Div(
                [
                    html.Div(className="asset-icon"),
                    html.Div(
                        [
                            html.Div(name, className="asset-name"),
                            html.Div(subname, className="asset-subname"),
                        ],
                        className="asset-info",
                    ),
                ],
                className="asset-left",
            ),
            html.Div(
                [
                    html.Div(value_primary, className="asset-value-primary"),
                    html.Div(value_secondary, className="asset-value-secondary"),
                ],
                className="asset-value",
            ),
            actions,
        ],
        className="asset-item",
    )


def assets_list(assets: list[dict[str, str]]) -> html.Div:
    """
    Create a list of assets.
    
    Args:
        assets: List of dicts with keys: name, subname, value_primary, value_secondary
    """
    return html.Div(
        [asset_item(a["name"], a["subname"], a["value_primary"], a["value_secondary"]) for a in assets],
        className="assets-list",
    )


def allocation_item(
    name: str,
    staked_percent: int,
    available_percent: int,
    icon: str | None = None,
) -> html.Div:
    """
    Create an allocation bar item.
    
    Args:
        name: Allocation name
        staked_percent: Staked percentage (0-100)
        available_percent: Available percentage (0-100)
        icon: Optional SVG icon
    """
    dotted_percent = 100 - staked_percent - available_percent
    
    icon_element = None
    if icon:
        icon_element = _icon_svg(icon)
    
    return html.Div(
        [
            html.Div(
                [
                    icon_element,
                    html.Span(name),
                ],
                className="allocation-name",
            ),
            html.Div(
                [
                    html.Div(
                        className="allocation-bar-staked",
                        style={"width": f"{staked_percent}%"},
                    ),
                    html.Div(
                        className="allocation-bar-available",
                        style={"width": f"{available_percent}%"},
                    ),
                    html.Div(
                        className="allocation-bar-dotted",
                        style={"width": f"{dotted_percent}%"},
                    ),
                ],
                className="allocation-bar-container",
            ),
            html.Div(f"{staked_percent}%", className="allocation-percent"),
        ],
        className="allocation-item",
    )


def allocation_list(allocations: list[dict[str, Any]]) -> html.Div:
    """
    Create a list of allocation bars.
    
    Args:
        allocations: List of dicts with keys: name, staked_percent, available_percent, icon (optional)
    """
    return html.Div(
        [allocation_item(a["name"], a["staked_percent"], a["available_percent"], a.get("icon")) for a in allocations],
        className="allocation-list",
    )


def allocation_legend() -> html.Div:
    """Create allocation legend."""
    return html.Div(
        [
            html.Div(
                [
                    html.Div(className="allocation-legend-color", style={"background": COLORS["accent_blue"]}),
                    html.Span("Staked"),
                ],
                className="allocation-legend-item",
            ),
            html.Div(
                [
                    html.Div(className="allocation-legend-color", style={"background": "#E8E8E8"}),
                    html.Span("Available"),
                ],
                className="allocation-legend-item",
            ),
        ],
        className="allocation-legend",
    )
