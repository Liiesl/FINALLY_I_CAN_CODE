from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class SidePanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setFixedWidth(parent.width() // 2)
        self.setLayout(QVBoxLayout())

        self.info_label = QLabel("Side Panel Content")
        self.info_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)
        self.layout().addStretch()
