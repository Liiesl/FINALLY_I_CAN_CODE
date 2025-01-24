from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLabel, QApplication
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import Qt
import os

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
        
        # Create a QTextEdit for the changelog content
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)
        
        self.apply_palette()
        self.load_changelog()

    def apply_palette(self):
        palette = QApplication.instance().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.title_label.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.text_edit.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

    def load_changelog(self):
        changelog_path = os.path.join(os.path.dirname(__file__), 'changelog.txt')
        try:
            with open(changelog_path, 'r') as file:
                content = file.read()
                # Use HTML to center-align the text
                html_content = f"<div style='text-align: center;'>{content.replace('\n', '<br>')}</div>"
                self.text_edit.setHtml(html_content)
        except FileNotFoundError:
            self.text_edit.setHtml("<div style='text-align: center;'>Changelog file not found.</div>")
