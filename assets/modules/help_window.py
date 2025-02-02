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
        self.section_list.itemClicked.connect(self.load_section_content)
        main_layout.addWidget(self.section_list, 1)  # 1/3 of the width

        # Right panel: Markdown viewer
        self.markdown_viewer = QTextEdit()
        self.markdown_viewer.setReadOnly(True)
        main_layout.addWidget(self.markdown_viewer, 2)  # 2/3 of the width

    def load_section_content(self, item):
        """Load the markdown content corresponding to the selected header."""
        selected_title = item.data(Qt.UserRole)
        content = self.get_section_content(selected_title)
        html_content = markdown.markdown(content)
        self.markdown_viewer.setHtml(html_content)

    def get_section_content(self, selected_title):
        """Get the markdown content for the selected section."""
        lines = self.markdown_content.split('\n')
        content = []
        capture = False
        for line in lines:
            match = re.match(r'^(#+)\s+(.*)', line)
            if match:
                title = match.group(2).strip()
                if title == selected_title:
                    capture = True
                    continue
                elif capture:
                    break
            if capture:
                content.append(line)
        return '\n'.join(content)
