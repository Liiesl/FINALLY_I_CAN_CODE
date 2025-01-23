from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("background-color: #2c2f38;")
        
        layout = QVBoxLayout(self)
        # Add your settings UI elements here
        label = QLabel("Settings Page", self)
        label.setFont(QFont("Arial", 14))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
