from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

class SidePanel(QWidget):
    def __init__(self, parent=None, open_settings_callback=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setFixedWidth(parent.width() // 2)
        self.setLayout(QVBoxLayout())

        self.info_label = QLabel("Side Panel Content")
        self.info_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background-color: transparent;")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)
        self.layout().addStretch()

        # Create a list widget for settings
        self.settings_list = QListWidget()
        self.settings_list.setStyleSheet("background-color: transparent; border: none; color: white; font-size: 16px;")

        # Add settings item to the list
        settings_item = QListWidgetItem("Settings")
        settings_item.setTextAlignment(Qt.AlignLeft)
        settings_item.setFlags(settings_item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.settings_list.addItem(settings_item)

        # Connect the item click event to the callback
        self.settings_list.itemClicked.connect(lambda: open_settings_callback())

        self.layout().addWidget(self.settings_list)
        self.layout().insertWidget(1, self.settings_list)  # Insert the list at the top, below the info label
