from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import Qt
import os

class VersionBlock(QWidget):
    def __init__(self, version, changes, parent=None, show_changes=True):
        super().__init__(parent)
        self.version = version
        self.changes = changes
        self.init_ui(show_changes)

    def init_ui(self, show_changes):
        self.layout = QVBoxLayout()

        # Create the toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(show_changes)
        self.toggle_button.setFixedSize(20, 20)
        self.toggle_button.setStyleSheet("QPushButton {border: none;}")
        self.toggle_button.setText("▼" if show_changes else "▶")
        self.toggle_button.clicked.connect(self.toggle_changes)

        # Create the version label
        self.version_label = QLabel(self.version)
        self.version_label.setFont(QFont("Inter ExtraBold", 20))
        self.version_label.setAlignment(Qt.AlignCenter)

        # Create the changes label with HTML for center alignment
        changes_html = "<br>".join(self.changes)
        self.changes_label = QLabel(f"<div style='text-align: center;'>{changes_html}</div>")
        self.changes_label.setWordWrap(True)
        self.changes_label.setAlignment(Qt.AlignCenter)
        self.changes_label.setVisible(show_changes)

        # Add the toggle button and version label to a horizontal layout
        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.toggle_button)
        self.header_layout.addWidget(self.version_label)
        self.header_layout.setAlignment(Qt.AlignCenter)  # Center align the header layout

        # Add the header and changes to the main layout
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.changes_label)

        self.setLayout(self.layout)

    def toggle_changes(self):
        if self.toggle_button.isChecked():
            self.changes_label.show()
            self.toggle_button.setText("▼")
        else:
            self.changes_label.hide()
            self.toggle_button.setText("▶")

class ChangelogWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("What's New")
        self.setGeometry(300, 200, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create a QLabel for the title
        self.title_label = QLabel("What's New")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Inter ExtraBold", 50))
        self.layout.addWidget(self.title_label)
        
        # Create a scroll area for the version blocks
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        
        self.apply_palette()
        self.load_changelog()
        
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def apply_palette(self):
        palette = QApplication.instance().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.title_label.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.scroll_content.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

    def load_changelog(self):
        changelog_path = os.path.join(os.path.dirname(__file__), 'changelog.txt')
        try:
            with open(changelog_path, 'r') as file:
                content = file.read()
                self.parse_changelog(content)
        except FileNotFoundError:
            self.scroll_layout.addWidget(QLabel("Changelog file not found."))

    def parse_changelog(self, content):
        lines = content.split('\n')
        versions = []
        changes = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('-'):
                if versions and changes:
                    versions.append((version, changes))
                version = stripped_line
                changes = []
            elif stripped_line.startswith('-'):
                changes.append(stripped_line)
        if version and changes:
            versions.append((version, changes))

        # Reverse the order of versions to show the latest version on top
        versions.reverse()

        # Add version blocks to layout
        for index, (version, changes) in enumerate(versions):
            show_changes = index < 5  # Show changes for the latest 5 versions
            self.add_version_block(version, changes, show_changes)

    def add_version_block(self, version, changes, show_changes):
        version_block = VersionBlock(version, changes, self, show_changes)
        self.scroll_layout.addWidget(version_block)
