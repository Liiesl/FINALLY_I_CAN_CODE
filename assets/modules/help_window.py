import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QListWidgetItem
from PyQt5.QtCore import Qt
import markdown  # You may need to install the markdown package: pip install markdown

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)  # Set the size of the window
        self.markdown_file_path = os.path.join(os.path.dirname(__file__), "help.md")  # Path to the markdown file
        self.markdown_content = self.read_markdown_file()
        self.headers = self.extract_headers(self.markdown_content)
        self.html_content = self.convert_to_html_with_anchors()
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

    def convert_to_html_with_anchors(self):
        """Convert markdown to HTML with anchors for headers."""
        extensions = ['toc']  # Enable table of contents extension for automatic anchor generation
        html_content = markdown.markdown(self.markdown_content, extensions=extensions)
        return html_content

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

        # Right panel: Markdown viewer
        self.markdown_viewer = QTextEdit()
        self.markdown_viewer.setReadOnly(True)
        self.markdown_viewer.setHtml(self.html_content)  # Display the full markdown content
        main_layout.addWidget(self.markdown_viewer, 2)  # 2/3 of the width

    def scroll_to_section(self, item):
        """Scroll to the selected section in the markdown viewer."""
        selected_title = item.data(Qt.UserRole)
        anchor = self.generate_anchor(selected_title)
        self.markdown_viewer.scrollToAnchor(anchor)

    def generate_anchor(self, title):
        """Generate an anchor name for a given header title."""
        # Convert the title to lowercase and replace spaces with hyphens
        anchor = title.lower().replace(" ", "-")
        return anchor
