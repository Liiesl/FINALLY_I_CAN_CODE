from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont

class Settings(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Create a horizontal layout for the back button
        button_layout = QHBoxLayout()

        back_button = QPushButton("Back to Main Menu")
        back_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 15px; font-size: 14px;")
        back_button.clicked.connect(self.back_to_main_menu)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)

        # Example setting: Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Select Theme:")
        theme_label.setFont(QFont("Arial", 14))
        theme_label.setStyleSheet("color: white;")
        theme_layout.addWidget(theme_label)

        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(["Dark", "Light"])
        self.theme_dropdown.setStyleSheet("background-color: #3c3f41; color: white; font-size: 14px; padding: 15px;")
        theme_layout.addWidget(self.theme_dropdown)

        layout.addLayout(theme_layout)

        # Example setting: Default file path
        path_layout = QHBoxLayout()
        path_label = QLabel("Default File Path:")
        path_label.setFont(QFont("Arial", 14))
        path_label.setStyleSheet("color: white;")
        path_layout.addWidget(path_label)

        self.path_input = QLineEdit()
        self.path_input.setStyleSheet("background-color: #3c3f41; color: white; font-size: 14px; padding: 15px;")
        path_layout.addWidget(self.path_input)

        layout.addLayout(path_layout)

        # Save and Cancel buttons
        save_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 15px; font-size: 14px;")
        save_button.clicked.connect(self.save_settings)
        save_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 15px; font-size: 14px;")
        cancel_button.clicked.connect(self.close)
        save_layout.addWidget(cancel_button)

        layout.addLayout(save_layout)

    def back_to_main_menu(self):
        # Close the settings widget and call the back callback to show the main menu
        self.close()
        if self.back_callback:
            self.back_callback()

    def save_settings(self):
        selected_theme = self.theme_dropdown.currentText()
        default_path = self.path_input.text()
        QMessageBox.information(self, "Settings Saved", f"Theme: {selected_theme}\nDefault File Path: {default_path}")
        self.close()
