from PyQt5.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, 
                             QScrollArea, QFrame, QHBoxLayout, QSizePolicy)
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
        main_layout.setContentsMargins(20, 10, 20, 10)  # Vertical spacing between blocks
        main_layout.setSpacing(20)

        # Version label
        version_label = QLabel(self.version)
        version_label.setFont(QFont("Inter ExtraBold", 20))
        version_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        version_label.setFixedWidth(150)
        main_layout.addWidget(version_label)

        # Vertical line container (stretches full height)
        line_container = QWidget()
        line_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        line_layout = QVBoxLayout(line_container)
        line_layout.setContentsMargins(0, -10, 0, -10)  # Negative margins to span spacing
        line_layout.setSpacing(0)

        # Composite icon (circle outline + dot)
        icon = qta.icon("mdi.circle-outline", color="#0078D4").pixmap(24, 24)
        painter = QPainter(icon)
        dot_icon = qta.icon("mdi.circle", color="#0078D4").pixmap(8, 8)
        painter.drawPixmap(8, 8, dot_icon)
        painter.end()
        
        icon_label = QLabel()
        icon_label.setPixmap(icon)
        line_layout.addWidget(icon_label, alignment=Qt.AlignTop)

        # Vertical line
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setLineWidth(1)
        line.setStyleSheet(f"border-color: {self.palette().color(QPalette.WindowText).name()};")
        line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        line_layout.addWidget(line)

        main_layout.addWidget(line_container)

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
        
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Title label
        self.title_label = QLabel("What's New")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Inter ExtraBold", 24))
        self.layout.addWidget(self.title_label)
        
        # Scroll area setup
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(0)  # No spacing between version blocks
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        self.apply_palette()
        self.load_changelog()
        
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

    def apply_palette(self):
        palette = QApplication.instance().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        scrollbar_color = palette.color(QPalette.Button).name()
        handle_color = palette.color(QPalette.Highlight).name()
        
        # Base styling
        self.setStyleSheet(f"""
            background-color: {background_color};
            color: {text_color};
        """)
        self.scroll_content.setStyleSheet(f"background-color: {background_color};")
        
        # Scrollbar styling
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
            self.add_version_block(version, changes)
        
        # Add spacer to push content up
        self.scroll_layout.addStretch()

    def add_version_block(self, version, changes):
        version_block = VersionBlock(version, changes)
        self.scroll_layout.addWidget(version_block)
