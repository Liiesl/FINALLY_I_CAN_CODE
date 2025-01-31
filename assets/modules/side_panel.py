from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QMessageBox, QScrollArea, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette
from assets.modules.config import Config
from assets.changelog.changelog_window import ChangelogWindow
import os
import importlib

class SidePanel(QWidget):
    def __init__(self, parent=None, open_settings_callback=None):
        super().__init__(parent)
        self.config = Config()
        self.open_settings_callback = open_settings_callback
        self.current_palette()
        self.setup_ui()
        self.update_colors()
        self.setFont(QFont("Inter Regular"))

    def setup_ui(self):
        self.setStyleSheet(f"background-color: {self.background_color};")
        self.setFixedWidth(self.parent().width() // 3)
        self.setLayout(QVBoxLayout())

        text_size = self.config.get_text_size()
        self.font_size = {
            "small": 14,
            "default": 16,
            "large": 18,
            "huge": 20
        }.get(text_size, 16)

        self.info_label = QLabel("Tools")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.info_label)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search tools...")
        self.search_bar.textChanged.connect(self.filter_tools)
        self.layout().addWidget(self.search_bar)

        self.tools_list = QListWidget()
        self.tools_list.itemClicked.connect(self.handle_tool_clicked)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.tools_list)
        self.layout().addWidget(self.scroll_area)

        self.settings_list = QListWidget()
        settings_item = QListWidgetItem("Settings")
        settings_item.setFlags(settings_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(settings_item)

        changelog_item = QListWidgetItem("Changelog")
        changelog_item.setFlags(changelog_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(changelog_item)

        self.settings_list.itemClicked.connect(self.handle_item_clicked)
        self.layout().addWidget(self.settings_list)

        self.credit_label = QLabel("brought to you by\nLiiesl on GitHub")
        self.credit_label.setAlignment(Qt.AlignLeft)
        self.credit_label.setOpenExternalLinks(True)
        self.credit_label.mousePressEvent = self.show_socials
        self.credit_label.setStyleSheet(f"font-size: {self.font_size}px;")
        self.layout().addWidget(self.credit_label)

    def filter_tools(self, text):
        for i in range(self.tools_list.count()):
            item = self.tools_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def handle_tool_clicked(self, item):
        tool_name = item.data(Qt.UserRole)
        self.parent().open_tool(tool_name)

    def add_tool(self, tool_name):
        tool_item = QListWidgetItem(tool_name.replace('_', ' ').title())
        tool_item.setData(Qt.UserRole, tool_name)
        self.tools_list.addItem(tool_item)

    def current_palette(self):
        palette = self.parent().palette()
        self.text_color = palette.color(QPalette.WindowText).name()
        self.background_color = palette.color(QPalette.Window).name()
        self.highlight_color = palette.color(QPalette.Highlight).name()
        self.hover_color = palette.color(QPalette.Highlight).darker().name()

    def update_colors(self):
        # Re-fetch the current palette
        palette = self.current_palette()

        self.setStyleSheet(f"background-color: {self.background_color};")
        
        self.info_label.setStyleSheet(f"color: {self.text_color}; font-size: {self.font_size}px; font-weight: bold; background-color: none;")

        self.settings_list.setStyleSheet(f"background-color: transparent; border: none; color: {self.text_color}; font-size: {self.font_size - 2}px;")
    
    def handle_item_clicked(self, item):
        if item.text() == "Settings":
            # Handle the settings click event
            self.open_settings_callback()
        elif item.text() == "Changelog":
            # Handle the changelog click event
            self.open_changelog_window()

    def open_changelog_window(self):
        # Check if changelog window is already open
        if not hasattr(self, 'changelog_window') or not self.changelog_window.isVisible():
            self.changelog_window = ChangelogWindow(self)
            self.changelog_window.show()
        else:
            self.changelog_window.raise_()
            self.changelog_window.activateWindow()

    def show_socials(self, event):
        # Create a message box to display social media links
        socials_message = (
            "GitHub: Liiesl\n"
            "Instagram: @suryaalingga\n"
            "YouTube: @Vfrix"
        )
        QMessageBox.information(self, "Socials", socials_message)

