from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
from assets.modules.config import Config
from assets.buttons.toggle_switch import ToggleSwitch  # Import the ToggleSwitch class
from assets.modules.custom_window_bar import CustomWindowBar

class Settings(QWidget):
    settings_saved = pyqtSignal()  # Define a signal for settings saved

    def __init__(self, parent=None, back_callback=None, main_window=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.main_window = main_window
        self.setFont(QFont("Inter Regular"))
        self.config = Config(source="Settings")
        self.initial_theme = self.config.get_theme()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        button_color = palette.color(QPalette.Button).name()
        button_text_color = palette.color(QPalette.ButtonText).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

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

        theme_layout = QHBoxLayout()
        theme_label_light = QLabel("Light")
        theme_label_light.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        theme_layout.addWidget(theme_label_light)

        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.set_state(self.config.get_theme())
        self.theme_toggle.mousePressEvent = self.toggle_theme
        theme_layout.addWidget(self.theme_toggle)

        theme_label_dark = QLabel("Dark")
        theme_label_dark.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        theme_layout.addWidget(theme_label_dark)

        layout.addLayout(theme_layout)

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
        self.settings_saved.emit()

    def toggle_theme(self, event):
        current_state = self.theme_toggle.get_state()
        new_state = "light" if current_state == "dark" else "dark"
        self.theme_toggle.set_state(new_state)
        self.config.data["theme"] = new_state
        self.apply_theme()

    def apply_theme(self):
        self.settings_saved.emit()

    def save_settings(self):
        print("Saving settings...")
        
        # Save the settings
        self.config.set_safe_area_size(self.safe_area_slider.value())
        self.config.set_text_size(self.text_size_dropdown.currentText())
        self.config.set_theme(self.config.data["theme"])
        
        self.config.save()
        self.config.load()
    
        # Check if the theme has changed
        new_theme = self.config.get_theme()
        if initial_theme != new_theme:
            # Show a confirmation message box
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText("The theme has been changed. Do you want to relaunch the application?")
            msg_box.setWindowTitle("Relaunch Application")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            
            # Execute the message box and get the user's choice
            choice = msg_box.exec_()
            
            if choice == QMessageBox.Yes:
                # Relaunch the application
                self.relaunch_app()
            else:
                # If the user chooses not to relaunch, just refresh the settings
                if self.main_window is not None:
                    self.main_window.refresh_settings()
        else:
            # If the theme hasn't changed, just refresh the settings
            if self.main_window is not None:
                self.main_window.refresh_settings()
    
    def relaunch_app(self):
        """Relaunch the application."""
        import os
        import sys
        import subprocess
        
        # Get the current script path
        script_path = sys.argv[0]
        
        # Close the current application
        self.main_window.close()
        
        # Relaunch the application
        subprocess.Popen([sys.executable, script_path])
        sys.exit()
