from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel,
                             QScrollArea, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPalette, QFont, QPainter
from PyQt5.QtCore import Qt
import os
import qtawesome as qta

class VersionBlock(QWidget):
    def __init__(self, version, changes, parent=None):
        super().__init__(parent)
        self.version = version
        self.changes = changes
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        # Top and bottom margins create space between blocks, left/right margins removed
        main_layout.setContentsMargins(20, 30, 20, 30)
        main_layout.setSpacing(20)

        # Version title
        version_label = QLabel(self.version)
        version_label.setFont(QFont("Inter ExtraBold", 20))
        version_label.setFixedWidth(150)
        version_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        main_layout.addWidget(version_label)

        # Changes list
        changes_html = "<ul style='margin: 0; padding-left: 20px;'>"
        for change in self.changes:
            cleaned_change = change.strip().lstrip('- ')
            changes_html += f"<li style='margin-bottom: 5px;'>{cleaned_change}</li>"
        changes_html += "</ul>"
        
        changes_label = QLabel(changes_html)
        changes_label.setFont(QFont("Inter", 12))
        changes_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        changes_label.setWordWrap(True)
        changes_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_layout.addWidget(changes_label, stretch=1)

class ChangelogWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("What's New")
        self.setGeometry(300, 200, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title label
        self.title_label = QLabel("What's New")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Inter ExtraBold", 24))
        main_layout.addWidget(self.title_label)

        # Scroll area setup
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Main content with columns
        self.scroll_content = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(20, 0, 20, 0)
        self.scroll_layout.setSpacing(20)

        # Left column for version titles
        self.titles_column = QWidget()
        self.titles_layout = QVBoxLayout(self.titles_column)
        self.titles_layout.setContentsMargins(0, 0, 0, 0)
        self.titles_layout.setSpacing(30)  # Vertical gap between versions
        self.scroll_layout.addWidget(self.titles_column)

        # Vertical line between columns
        self.vertical_line = QFrame()
        self.vertical_line.setFrameShape(QFrame.VLine)
        self.vertical_line.setLineWidth(2)
        self.scroll_layout.addWidget(self.vertical_line)

        # Right column for changes
        self.changes_column = QWidget()
        self.changes_layout = QVBoxLayout(self.changes_column)
        self.changes_layout.setContentsMargins(0, 0, 0, 0)
        self.changes_layout.setSpacing(30)  # Matches title spacing
        self.scroll_layout.addWidget(self.changes_column, stretch=1)

        self.apply_palette()
        self.load_changelog()
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

    def apply_palette(self):
        palette = QApplication.instance().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        scrollbar_color = palette.color(QPalette.Button).name()
        handle_color = palette.color(QPalette.Highlight).name()

        self.setStyleSheet(f"""
            background-color: {background_color};
            color: {text_color};
            QFrame {{
                color: {text_color};
            }}
        """)
        self.scroll_content.setStyleSheet(f"background-color: {background_color};")
        self.vertical_line.setStyleSheet(f"background-color: {text_color};")

        # Scrollbar styling (unchanged)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
            }}
            QScrollBar:vertical {{
                background: {scrollbar_color};
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {handle_color};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                background: none;
                border: none;
                width: 0px;
                height: 0px;
            }}
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)

    def load_changelog(self):
        changelog_path = os.path.join(os.path.dirname(__file__), 'changelog.txt')
        try:
            with open(changelog_path, 'r') as file:
                self.parse_changelog(file.read())
        except FileNotFoundError:
            error_label = QLabel("Changelog file not found.")
            error_label.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(error_label)

    def parse_changelog(self, content):
        versions = []
        current_version = None
        current_changes = []

        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            if not line.startswith('-'):
                if current_version:
                    versions.append((current_version, current_changes))
                current_version = line
                current_changes = []
            else:
                current_changes.append(line)

        if current_version:
            versions.append((current_version, current_changes))

        # Show latest versions first
        versions.reverse()

        for version, changes in versions:
            # Create version title
            version_label = QLabel(version)
            version_label.setFont(QFont("Inter ExtraBold", 20))
            version_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.titles_layout.addWidget(version_label)
            
            # Create changes list
            changes_html = "<ul style='margin: 0; padding-left: 20px;'>"
            for change in changes:
                cleaned_change = change.strip().lstrip('- ')
                changes_html += f"<li style='margin-bottom: 5px;'>{cleaned_change}</li>"
            changes_html += "</ul>"
            
            changes_label = QLabel(changes_html)
            changes_label.setFont(QFont("Inter", 12))
            changes_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            changes_label.setWordWrap(True)
            changes_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.changes_layout.addWidget(changes_label)

        # Add spacing at the end
        self.titles_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.changes_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def add_version_block(self, version, changes):
        version_block = VersionBlock(version, changes)
        self.scroll_layout.addWidget(version_block)
