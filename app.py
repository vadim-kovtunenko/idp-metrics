"""
IDP Dashboard — entry point.
Run from repository root: python app.py
"""
import threading
import webbrowser

import dash

from layout.main_layout import build_main_layout
from config.theme import COLORS

# Import callbacks to register them
import callbacks  # noqa: F401

# Create Dash app; assets (e.g. assets/custom.css) are loaded automatically
app = dash.Dash(
    __name__,
    title="IDP Dashboard",
    suppress_callback_exceptions=True,
)
app.layout = build_main_layout()

# Apply dashboard background to the outer page
app.index_string = """<!DOCTYPE html>
<html style="overflow-x: hidden;">
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    </head>
    <body style="margin:0; background-color: """ + COLORS["dashboard_bg"] + """;">
        {%app_entry%}
        <footer>{%config%}</footer>
        {%scripts%}
        {%renderer%}
    </body>
</html>
"""

server = app.server

if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    app.run(debug=True, host="0.0.0.0", port=8050)
