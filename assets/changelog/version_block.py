from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea
from PyQt5.QtGui import QPalette, QApplication, QFont
from PyQt5.QtCore import Qt
import os
from .version_block import VersionBlock

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
        version = None
        changes = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('-'):
                if version and changes:
                    self.add_version_block(version, changes)
                version = stripped_line
                changes = []
            elif stripped_line.startswith('-'):
                changes.append(stripped_line)
        if version and changes:
            self.add_version_block(version, changes)

    def add_version_block(self, version, changes):
        version_block = VersionBlock(version, changes, self)
        self.scroll_layout.addWidget(version_block)
