import os
import sys
import re
import markdown
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QSplitter, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
import qtawesome as qta  # Import QtAwesome for icons

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
        self.html_content = self.convert_to_html_with_styling()

        # Initialize the UI
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

    def convert_to_html_with_styling(self):
        """Convert markdown to styled HTML using a custom CSS file."""
        # Define markdown extensions for syntax highlighting and table of contents
        extensions = ['extra', 'codehilite', 'toc']
        html_content = markdown.markdown(self.markdown_content, extensions=extensions)

        # Load custom CSS for styling
        css_path = resource_path("assets/modules/styles.css")
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        else:
            css_content = ""  # Default to no CSS if the file is missing

        # Wrap the HTML content with the CSS
        styled_html = f"""
        <style>{css_content}</style>
        {html_content}
        """
        return styled_html

    def setup_ui(self):
        # Main layout using QSplitter for resizable panels
        main_splitter = QSplitter(Qt.Horizontal)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(main_splitter)

        # Left panel: List of sections (headers)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # Add a collapsible button with an arrow icon
        self.toggle_button = QPushButton(qta.icon('fa5s.angle-left'), "")
        self.toggle_button.setFixedSize(20, 20)
        self.toggle_button.clicked.connect(self.toggle_navigation)
        left_layout.addWidget(self.toggle_button, alignment=Qt.AlignRight)

        self.section_list = QListWidget()
        self.section_list.setFont(QFont("Arial", 14))  # Increase text size
        
    for level, title in self.headers:
        item = QListWidgetItem(title)
        item.setData(Qt.UserRole, title)  # Store the header title for later use
        
        # Set font size based on header level with increased size gap
        font_size = max(8, 28 - (level * 5))  # Increase the size gap by multiplying level by 4
        font = QFont("Arial", font_size)
        
        # Add indentation based on the header level
        indent = level * 20  # Each level gets an additional 20 pixels of indentation
        item.setText(f"{' ' * (indent // 10)}{title}")  # Approximate tab-like spacing
        
        item.setFont(font)
        self.section_list.addItem(item)
        
        self.section_list.itemClicked.connect(self.scroll_to_section)
        left_layout.addWidget(self.section_list)

        # Right panel: Markdown viewer using QWebEngineView
        self.markdown_viewer = QWebEngineView()
        self.markdown_viewer.setHtml(self.html_content)  # Display the styled HTML content

        # Add widgets to the splitter
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(self.markdown_viewer)

        # Set initial sizes for the splitter
        main_splitter.setSizes([200, 600])

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

    def toggle_navigation(self):
        """Toggle the visibility of the navigation panel."""
        if self.section_list.isVisible():
            self.section_list.hide()
            self.toggle_button.setIcon(qta.icon('fa5s.angle-right'))
        else:
            self.section_list.show()
            self.toggle_button.setIcon(qta.icon('fa5s.angle-left'))
