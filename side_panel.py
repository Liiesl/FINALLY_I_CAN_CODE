from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class SidePanel(QWidget):
    def __init__(self, parent=None, open_settings_callback=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setFixedWidth(parent.width() // 2)
        self.setLayout(QVBoxLayout())

        self.info_label = QLabel("Side Panel Content")
        self.info_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)
        self.layout().addStretch()

        # Add settings link
        self.settings_label = QLabel("<a href='#'>Settings</a>")
        self.settings_label.setStyleSheet("color: #4f86f7; font-size: 16px;")
        self.settings_label.setAlignment(Qt.AlignCenter)
        self.settings_label.setOpenExternalLinks(False)
        self.settings_label.linkActivated.connect(open_settings_callback)
        self.layout().addWidget(self.settings_label)
