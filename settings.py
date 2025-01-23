from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider
from PyQt5.QtCore import Qt
from config import Config

class Settings(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.config = Config()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(self.back_callback)
        layout.addWidget(back_button)

        # Safe Area Slider
        safe_area_label = QLabel("Safe Area Size (px):")
        safe_area_label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(safe_area_label)

        self.safe_area_slider = QSlider(Qt.Horizontal)
        self.safe_area_slider.setMinimum(0)
        self.safe_area_slider.setMaximum(100)
        self.safe_area_slider.setValue(self.config.get_safe_area_size())
        self.safe_area_slider.setTickInterval(10)
        self.safe_area_slider.setTickPosition(QSlider.TicksBelow)
        self.safe_area_slider.valueChanged.connect(self.update_safe_area)
        layout.addWidget(self.safe_area_slider)

        self.safe_area_value_label = QLabel(f"{self.config.get_safe_area_size()} px")
        self.safe_area_value_label.setStyleSheet("color: white;")
        layout.addWidget(self.safe_area_value_label)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #2c2f38;")

    def update_safe_area(self, value):
        self.safe_area_value_label.setText(f"{value} px")

    def save_settings(self):
        self.config.set_safe_area_size(self.safe_area_slider.value())
        self.back_callback()
