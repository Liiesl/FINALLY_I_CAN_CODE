import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
from config import Config
from assets.buttons.toggle_switch import ToggleSwitch  # Import the ToggleSwitch class

class Settings(QWidget):
    settings_saved = pyqtSignal()  # Define a signal for settings saved

    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.config = Config(source="Settings")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Retrieve the current palette colors
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        button_color = palette.color(QPalette.Button).name()
        button_text_color = palette.color(QPalette.ButtonText).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {highlight_color};
                color: {button_text_color};
                border-radius: 10px;
                padding: 10px;
                min-height: 40px;
                background-color: {button_color};
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {hover_color};
                background-color: {hover_color};
            }}
        """)
        back_button.clicked.connect(self.back_callback)
        layout.addWidget(back_button)

        # Safe Area Slider
        safe_area_layout = QHBoxLayout()
        safe_area_label = QLabel("Safe Area Size (px):")
        safe_area_label.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        safe_area_layout.addWidget(safe_area_label)

        self.safe_area_slider = QSlider(Qt.Horizontal)
        self.safe_area_slider.setMinimum(0)
        self.safe_area_slider.setMaximum(100)
        self.safe_area_slider.setValue(self.config.get_safe_area_size())
        self.safe_area_slider.setTickInterval(10)
        self.safe_area_slider.setTickPosition(QSlider.TicksBelow)
        self.safe_area_slider.valueChanged.connect(self.update_safe_area)
        safe_area_layout.addWidget(self.safe_area_slider)

        self.safe_area_value_label = QLabel(f"{self.config.get_safe_area_size()} px")
        self.safe_area_value_label.setStyleSheet(f"color: {text_color};")
        safe_area_layout.addWidget(self.safe_area_value_label)

        layout.addLayout(safe_area_layout)

        # Text Size Dropdown
        text_size_layout = QHBoxLayout()
        text_size_label = QLabel("Text Size:")
        text_size_label.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        text_size_layout.addWidget(text_size_label)

        self.text_size_dropdown = QComboBox()
        self.text_size_dropdown.addItems(["small", "default", "large", "huge"])
        self.text_size_dropdown.setCurrentText(self.config.get_text_size())
        self.text_size_dropdown.currentTextChanged.connect(self.update_text_size)
        self.text_size_dropdown.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        text_size_layout.addWidget(self.text_size_dropdown)

        layout.addLayout(text_size_layout)

        # Theme Toggle Switch
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        theme_layout.addWidget(theme_label)

        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.set_state(self.config.get_theme())
        self.theme_toggle.mousePressEvent = self.toggle_theme
        theme_layout.addWidget(self.theme_toggle)

        layout.addLayout(theme_layout)

        # Save button
        save_button = QPushButton("Save")
        save_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {highlight_color};
                color: {button_text_color};
                border-radius: 10px;
                padding: 10px;
                min-height: 40px;
                background-color: {button_color};
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {hover_color};
                background-color: {hover_color};
            }}
        """)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setStyleSheet(f"background-color: {background_color};")

    def update_safe_area(self, value):
        self.safe_area_value_label.setText(f"{value} px")

    def update_text_size(self, size):
        self.config.set_text_size(size)
        self.apply_text_size_to_all_pages()

    def apply_text_size_to_all_pages(self):
        # Trigger the text size update in the main window
        self.settings_saved.emit()

    def toggle_theme(self, event):
        current_state = self.theme_toggle.get_state()
        new_state = "light" if current_state == "dark" else "dark"
        self.theme_toggle.set_state(new_state)
        self.config.data["theme"] = new_state  # Update the theme in memory only
        self.apply_theme()

    def apply_theme(self):
        # Trigger the theme update in the main window
        self.settings_saved.emit()

    def save_settings(self):
        self.config.set_safe_area_size(self.safe_area_slider.value())
        self.config.set_text_size(self.text_size_dropdown.currentText())
        self.config.set_theme(self.config.data["theme"])  # Save the theme from memory
        
        self.config.save()  # Ensure the config is saved
        time.sleep(1)  # Add a delay to ensure the config is saved flawlessly
        self.config.load()  # Reload the configuration to ensure it is applied
        
        self.apply_theme()  # Apply theme immediately after saving
        self.settings_saved.emit()  # Emit the settings_saved signal
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        # Do not call self.back_callback() to keep the settings window open
