from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette
from assets.modules.config import Config
from assets.changelog.changelog_window import ChangelogWindow

class SidePanel(QWidget):
    def __init__(self, parent=None, open_settings_callback=None):
        super().__init__(parent)
        self.config = Config()
        self.open_settings_callback = open_settings_callback
        self.current_palette()
        self.setup_ui(open_settings_callback)
        self.update_colors()
        self.setFont(QFont("Inter Regular"))

    def setup_ui(self, open_settings_callback):
        self.setFixedWidth(self.parent().width() // 2)
        self.setLayout(QVBoxLayout())

        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        self.info_label = QLabel("Side Panel Content")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)
        self.layout().addStretch()

        # Create a list widget for settings
        self.settings_list = QListWidget()

        # Add settings item to the list
        settings_item = QListWidgetItem("Settings")
        settings_item.setTextAlignment(Qt.AlignLeft)
        settings_item.setFlags(settings_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(settings_item)

        # Add changelog item to the list
        changelog_item = QListWidgetItem("Changelog")
        changelog_item.setTextAlignment(Qt.AlignLeft)
        changelog_item.setFlags(changelog_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(changelog_item)

        # Connect the item click event to the callback
        self.settings_list.itemClicked.connect(self.handle_item_clicked)

        self.layout().addWidget(self.settings_list)
        self.layout().insertWidget(1, self.settings_list)  # Insert the list at the top, below the info label

    def current_palette(self):
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

    def update_colors(self):
        # Re-fetch the current palette
        palette = self.current_palette()

        self.setStyleSheet(f"background-color: {background_color};")
        
        self.info_label.setStyleSheet(f"color: {text_color}; font-size: {font_size}px; font-weight: bold; background-color: none;")

        self.settings_list.setStyleSheet(f"background-color: transparent; border: none; color: {text_color}; font-size: {font_size - 2}px;")
    
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
