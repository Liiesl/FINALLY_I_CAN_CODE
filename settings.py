from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtGui import QFont

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Example setting: Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Select Theme:")
        theme_label.setFont(QFont("Arial", 14))
        theme_layout.addWidget(theme_label)

        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(["Dark", "Light"])
        theme_layout.addWidget(self.theme_dropdown)

        layout.addLayout(theme_layout)

        # Example setting: Default file path
        path_layout = QHBoxLayout()
        path_label = QLabel("Default File Path:")
        path_label.setFont(QFont("Arial", 14))
        path_layout.addWidget(path_label)

        self.path_input = QLineEdit()
        path_layout.addWidget(self.path_input)

        layout.addLayout(path_layout)

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.setFont(QFont("Arial", 12))
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.setFont(QFont("Arial", 12))
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 400, 200)

    def save_settings(self):
        # Implement your save functionality here
        selected_theme = self.theme_dropdown.currentText()
        default_path = self.path_input.text()

        # Example: Show a message box with the settings
        QMessageBox.information(self, "Settings Saved", f"Theme: {selected_theme}\nDefault File Path: {default_path}")
        self.close()
