from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette
from config import Config

class SidePanel(QWidget):
    def __init__(self, parent=None, open_settings_callback=None):
        super().__init__(parent)
        self.config = Config()
        self.setup_ui(open_settings_callback)
        self.setFont(QFont("Inter Regular"))

    def setup_ui(self, open_settings_callback):
        # Retrieve the current palette colors
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

        self.setStyleSheet(f"background-color: {background_color};")
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
        self.info_label.setStyleSheet(f"color: {text_color}; font-size: {font_size}px; font-weight: bold; background-color: none;")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)
        self.layout().addStretch()

        # Create a list widget for settings
        self.settings_list = QListWidget()
        self.settings_list.setStyleSheet(f"background-color: transparent; border: none; color: {text_color}; font-size: {font_size - 2}px;")

        # Add settings item to the list
        settings_item = QListWidgetItem("Settings")
        settings_item.setTextAlignment(Qt.AlignLeft)
        self.info_label.setStyleSheet(f"color: {text_color}; font-size: {font_size}px; font-weight: bold; background-color: none;")
        settings_item.setFlags(settings_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(settings_item)

        # Connect the item click event to the callback
        self.settings_list.itemClicked.connect(open_settings_callback)

        self.layout().addWidget(self.settings_list)
        self.layout().insertWidget(1, self.settings_list)  # Insert the list at the top, below the info label

    def apply_theme(self):
        # Retrieve the current palette colors
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()

        self.setStyleSheet(f"background-color: {background_color};")
        self.info_label.setStyleSheet(f"color: {text_color};")

        self.settings_list.setStyleSheet(f"background-color: transparent; border: none; color: {text_color};")
