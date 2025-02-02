from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QListWidgetItem
from PyQt5.QtCore import Qt
import markdown  # You may need to install the markdown package: pip install markdown

class HelpWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)  # Set the size of the window
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left panel: List of sections
        self.section_list = QListWidget()
        self.section_list.addItems(["Introduction", "Getting Started", "Advanced Features", "Troubleshooting"])
        self.section_list.itemClicked.connect(self.load_section_content)
        main_layout.addWidget(self.section_list, 1)  # 1/3 of the width

        # Right panel: Markdown viewer
        self.markdown_viewer = QTextEdit()
        self.markdown_viewer.setReadOnly(True)
        main_layout.addWidget(self.markdown_viewer, 2)  # 2/3 of the width

    def load_section_content(self, item):
        # Load markdown content based on the selected section
        section = item.text()
        if section == "Introduction":
            content = """
# Introduction

Welcome to the application! This is a brief introduction to help you get started.
"""
        elif section == "Getting Started":
            content = """
# Getting Started

Follow these steps to get started with the application:

1. Open the application.
2. Navigate to the settings.
3. Customize your preferences.
"""
        elif section == "Advanced Features":
            content = """
# Advanced Features

This section covers advanced features of the application.
"""
        elif section == "Troubleshooting":
            content = """
# Troubleshooting

If you encounter any issues, try the following:

- Restart the application.
- Check your internet connection.
- Contact support.
"""
        else:
            content = "# No Content Available"

        # Convert markdown to HTML and display it
        html_content = markdown.markdown(content)
        self.markdown_viewer.setHtml(html_content)
