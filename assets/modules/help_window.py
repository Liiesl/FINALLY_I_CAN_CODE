import os
import sys
import re
import markdown
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication  # Import QApplication to access the global app instance
from assets.modules.config import Config

def resource_path(relative_path):
    """Get the absolute path to a resource. Works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)  # Set the size of the window

        # Load markdown and CSS files using resource_path
        self.markdown_file_path = resource_path("assets/modules/help.md")
        self.markdown_content = self.read_markdown_file()
        self.headers = self.extract_headers(self.markdown_content)

        # Get configuration for text size and theme
        self.config = Config(source="MainWindow")
        self.text_size = self.get_text_size()
        self.palette = self.get_palette()

        # Convert markdown to styled HTML
        self.html_content = self.convert_to_html_with_styling()

        # Set up the UI
        self.setup_ui()

    def read_markdown_file(self):
        """Read the markdown file and return its content."""
        if os.path.exists(self.markdown_file_path):
            with open(self.markdown_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def extract_headers(self, markdown_content):
        """Extract headers and subheaders from the markdown content."""
        headers = []
        lines = markdown_content.split('\n')
        for line in lines:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                level = len(match.group(1))  # Number of '#' indicates the header level
                title = match.group(2).strip()
                headers.append((level, title))
        return headers

    def get_text_size(self):
        """Get the text size from the configuration."""
        text_size = self.config.get_text_size()
        return {
            "small": 14,
            "default": 18,
            "large": 22,
            "huge": 26
        }.get(text_size, 18)

    def get_palette(self):
        """Get the current palette colors."""
        # Use QApplication.instance() to access the global app instance
        app = QApplication.instance()
        palette = app.palette() if app else None
        if not palette:
            raise RuntimeError("Could not access the application palette.")

        return {
            "background_color": palette.color(palette.Window).name(),
            "text_color": palette.color(palette.WindowText).name(),
            "link_color": "#0366d6",  # GitHub-like link color
            "code_background_color": palette.color(palette.Base).name(),
        }

    def convert_to_html_with_styling(self):
        """Convert markdown to styled HTML using custom CSS."""
        extensions = ['extra', 'codehilite', 'toc']
        html_content = markdown.markdown(self.markdown_content, extensions=extensions)

        # Generate dynamic CSS based on palette and text size
        css_content = f"""
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: {self.text_size}px;
            line-height: 1.6;
            color: {self.palette['text_color']};
            background-color: {self.palette['background_color']};
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
            border-bottom: 1px solid {self.palette['text_color']};
            padding-bottom: 0.3em;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 16px;
        }}
        a {{
            color: {self.palette['link_color']};
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        pre {{
            background-color: {self.palette['code_background_color']};
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
        }}
        code {{
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 85%;
            background-color: rgba(27, 31, 35, 0.05);
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }}
        table {{
            display: block;
            width: 100%;
            overflow: auto;
            border-spacing: 0;
            border-collapse: collapse;
            margin-top: 0;
            margin-bottom: 16px;
        }}
        th {{
            font-weight: 600;
        }}
        td, th {{
            padding: 6px 13px;
            border: 1px solid {self.palette['text_color']};
        }}
        blockquote {{
            margin: 0;
            padding: 0 1em;
            color: {self.palette['text_color']};
            border-left: 0.25em solid {self.palette['text_color']};
        }}
        """

        # Wrap the HTML content with the CSS
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        return styled_html

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left panel: List of sections (headers)
        self.section_list = QListWidget()
        for level, title in self.headers:
            item = QListWidgetItem(title)
            item.setData(Qt.UserRole, title)  # Store the header title for later use
            self.section_list.addItem(item)
        self.section_list.itemClicked.connect(self.scroll_to_section)
        main_layout.addWidget(self.section_list, 1)  # 1/3 of the width

        # Right panel: Markdown viewer using QWebEngineView
        self.markdown_viewer = QWebEngineView()
        self.markdown_viewer.setHtml(self.html_content)  # Display the styled HTML content
        main_layout.addWidget(self.markdown_viewer, 2)  # 2/3 of the width

    def scroll_to_section(self, item):
        """Scroll to the selected section in the markdown viewer."""
        selected_title = item.data(Qt.UserRole)
        anchor = self.generate_anchor(selected_title)
        self.markdown_viewer.page().runJavaScript(f"document.getElementById('{anchor}').scrollIntoView();")

    def generate_anchor(self, title):
        """Generate an anchor name for a given header title."""
        # Convert the title to lowercase and replace spaces with hyphens
        anchor = title.lower().replace(" ", "-")
        return anchor
