from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class Settings(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setStyleSheet("background-color: #2c2f38;")
        self.setLayout(QVBoxLayout())

        self.info_label = QLabel("Settings Page")
        self.info_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.layout().addWidget(self.info_label)

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(self.back_callback)
        back_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #4f86f7; /* Thicker edge line */
                color: white;
                border-radius: 10px;
                padding: 10px;
                min-height: 40px;
                background-color: #4f86f7; /* Accented blue color */
                text-align: center; /* Center align text */
            }
            QPushButton:hover {
                border-color: #3a6dbf;
                background-color: #3a6dbf; /* Darker blue on hover */
            }
        """)
        self.layout().addWidget(back_button)
