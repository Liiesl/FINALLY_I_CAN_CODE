from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QComboBox, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette
from assets.modules.config import Config
from assets.buttons.toggle_switch import ToggleSwitch  # Import the ToggleSwitch class
from assets.modules.custom_window_bar import CustomWindowBar
import os
import shutil
import json

class Settings(QWidget):
    settings_saved = pyqtSignal()  # Define a signal for settings saved
    experimental_tools_toggled = pyqtSignal(bool)  # Signal for toggling experimental tools

    def __init__(self, parent=None, back_callback=None, main_window=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.main_window = main_window
        self.setFont(QFont("Inter Regular"))
        self.config = Config(source="Settings")
        self.initial_theme = self.config.get_theme()
        self.initial_experimental_tools = self.config.get_experimental_tools()  # Add this method to your Config class if not present

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

        # Experimental Tools Toggle
        experimental_tools_layout = QHBoxLayout()
        experimental_tools_label = QLabel("Enable Experimental Tools:")
        experimental_tools_label.setStyleSheet(f"color: {text_color}; font-size: 26px;")
        experimental_tools_layout.addWidget(experimental_tools_label)
        self.experimental_tools_toggle = ToggleSwitch()
        self.experimental_tools_toggle.set_state("dark" if self.config.get_experimental_tools_enabled() else "light")
        self.experimental_tools_toggle.stateChanged.connect(self.toggle_experimental_tools)
        experimental_tools_layout.addWidget(self.experimental_tools_toggle)
        layout.addLayout(experimental_tools_layout)

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

        # Horizontal Layout for Export and Load Buttons
        export_load_layout = QHBoxLayout()

        # Export Config Button
        export_config_button = QPushButton("Export Settings")
        export_config_button.setStyleSheet(f"""
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
        export_config_button.clicked.connect(self.export_config)
        export_load_layout.addWidget(export_config_button)

        # Load Settings Button
        load_settings_button = QPushButton("Load Settings")
        load_settings_button.setStyleSheet(f"""
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
        load_settings_button.clicked.connect(self.load_settings)
        export_load_layout.addWidget(load_settings_button)

        # Add the horizontal layout to the main layout
        layout.addLayout(export_load_layout)

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

    def toggle_experimental_tools(self):
        """Toggle the state of experimental tools."""
        current_state = self.experimental_tools_toggle.get_state() == "dark"
        self.config.set_experimental_tools_enabled(current_state)

    def save_settings(self):
        print("Saving settings...")
        # Save the settings
        self.config.set_safe_area_size(self.safe_area_slider.value())
        self.config.set_text_size(self.text_size_dropdown.currentText())
        self.config.set_theme(self.config.data["theme"])
        self.config.set_experimental_tools_enabled(self.experimental_tools_toggle.get_state() == "dark")
        self.config.save()
        self.config.load()
        # Check if the theme has changed
        new_theme = self.config.get_theme()
        new_experimental_tools = self.config.get_experimental_tools()  # Retrieve the updated experimental tools state
        
        theme_changed = self.initial_theme != new_theme
        experimental_tools_changed = self.initial_experimental_tools != new_experimental_tools

        if theme_changed or experimental_tools_changed:
            # Show a confirmation message box
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText(
                "The theme or experimental tools settings has been changed.\n\n"
                "You need to relaunch the application for the change to fully take effect,\n\n"
                "Do you want to relaunch the application?"
            )
            msg_box.setWindowTitle("Relaunch Application")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setStyleSheet("""
            QMessageBox {
            color: black;
            }
            QMessageBox QLabel {
            color: black;
            }
            QMessageBox QPushButton {
            color: black;
            }
            """)
            # Execute the message box and get the user's choice
            choice = msg_box.exec_()
            if choice == QMessageBox.Yes:
                # Relaunch the application
                self.relaunch_app()
            else:
                self.config.set_theme(self.initial_theme)
                self.theme_toggle.set_state(self.initial_theme)  # Update toggle position
                self.config.save()
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

    def export_config(self):
        """Export the config.json file to a user-selected directory."""
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly  # Only show directories, no files
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Export Config", "", options=options)

        if directory:
            # Path to the original config.json
            original_config_path = os.path.join(os.path.dirname(__file__), "config.json")
            
            # Destination path in the selected directory
            destination_path = os.path.join(directory, "config.json")

            try:
                # Copy the config.json file to the selected directory
                shutil.copy(original_config_path, destination_path)
                QMessageBox.information(self, "Export Successful", f"Config file exported successfully to:\n{destination_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export config file:\n{str(e)}")

    def load_settings(self):
        """Load settings from a user-selected config.json file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Config File", "", "JSON Files (*.json);;All Files (*)", options=options
        )
    
        if not file_path:
            return  # User canceled the file dialog
    
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "File Not Found", "The selected file does not exist.")
                return
    
            # Check if the file has a valid extension
            if not file_path.lower().endswith(".json"):
                QMessageBox.critical(self, "Invalid File", "Please select a valid JSON file.")
                return
    
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                QMessageBox.warning(self, "Empty Config", "The config file is empty. Using default values.")
                self.config.load()  # Reload default values
                self.refresh_ui_from_config()
                return
    
            # Read and validate the selected config.json file
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
    
                    # Check for duplicate keys in the JSON
                    def has_duplicate_keys(json_string):
                        import json
                        from collections import Counter
                        parsed = json.loads(json_string)
                        counter = Counter(parsed.keys())
                        duplicates = [key for key, count in counter.items() if count > 1]
                        if duplicates:
                            raise ValueError(f"Duplicate keys found: {', '.join(duplicates)}")
    
                    has_duplicate_keys(content)
    
                    new_config_data = json.loads(content)
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Encoding Error", "The config file contains invalid or unsupported characters.")
                return
            except json.JSONDecodeError as decode_error:
                QMessageBox.critical(self, "Load Failed", f"Invalid JSON format: {decode_error}")
                return
    
            # Validate the structure of the loaded config
            required_keys = {"safe_area_size", "text_size", "theme"}
            optional_keys = {"recent_tools": [], "tool_usage": {}}
    
            # Check for missing required keys
            missing_keys = required_keys - new_config_data.keys()
            if missing_keys:
                raise ValueError(f"Invalid config file: Missing required keys: {', '.join(missing_keys)}")
    
            # Validate data types and assign default values for optional keys
            type_checks = {
                "safe_area_size": int,
                "text_size": str,
                "theme": str,
                "recent_tools": list,
                "tool_usage": dict,
            }
    
            for key, expected_type in type_checks.items():
                if key in new_config_data and not isinstance(new_config_data[key], expected_type):
                    raise ValueError(f"Invalid type for '{key}': Expected {expected_type.__name__}, got {type(new_config_data[key]).__name__}")
                elif key not in new_config_data and key in optional_keys:
                    new_config_data[key] = optional_keys[key]
    
            # Validate specific values
            valid_text_sizes = {"small", "default", "large", "huge"}
            valid_themes = {"light", "dark"}
    
            if new_config_data["safe_area_size"] < 0:
                raise ValueError("Invalid value for 'safe_area_size': Must be non-negative.")
    
            if new_config_data["text_size"] not in valid_text_sizes:
                raise ValueError(f"Invalid value for 'text_size': Must be one of {valid_text_sizes}.")
    
            if new_config_data["theme"] not in valid_themes:
                raise ValueError(f"Invalid value for 'theme': Must be one of {valid_themes}.")
    
            # Replace the current config.json with the new data
            current_config_path = os.path.join(os.path.dirname(__file__), "config.json")
            try:
                with open(current_config_path, "w") as file:
                    json.dump(new_config_data, file, indent=4)
            except PermissionError:
                QMessageBox.critical(self, "Permission Error", "Unable to save the config file due to insufficient permissions.")
                return
            except OSError as e:
                QMessageBox.critical(self, "Save Failed", f"Failed to save settings due to disk space or permissions: {str(e)}")
                return
    
            # Reload the settings in the application
            self.config.load()
            self.refresh_ui_from_config()

            # Detect theme change and trigger relaunch logic
            new_theme = new_config_data["theme"]
            if self.initial_theme != new_theme:
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setText(
                    "The theme has been changed.\n\n"
                    "You need to relaunch the application for the change to fully take effect,\n\n"
                    "Do you want to relaunch the application?"
                )
                msg_box.setWindowTitle("Relaunch Application")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg_box.setStyleSheet("""
                    QMessageBox {
                        color: black;
                    }
                    QMessageBox QLabel {
                        color: black;
                    }
                    QMessageBox QPushButton {
                        color: black;
                    }
                """)
    
                # Execute the message box and get the user's choice
                choice = msg_box.exec_()
                if choice == QMessageBox.Yes:
                    self.relaunch_app()
                else:
                    # Revert to the original theme if the user chooses not to relaunch
                    self.config.set_theme(current_theme)
                    self.theme_toggle.set_state(current_theme)  # Update toggle position
                    self.config.save()
    
            QMessageBox.information(self, "Load Successful", "Settings loaded successfully.")
    
        except ValueError as ve:
            QMessageBox.critical(self, "Load Failed", f"Failed to load settings: {str(ve)}")
        except Exception as e:
            QMessageBox.critical(self, "Load Failed", f"An unexpected error occurred while loading settings:\n{str(e)}")

    def refresh_ui_from_config(self):
        """Refresh the UI elements based on the current config."""
        self.safe_area_slider.setValue(self.config.get_safe_area_size())
        self.safe_area_value_label.setText(f"{self.config.get_safe_area_size()} px")
        self.text_size_dropdown.setCurrentText(self.config.get_text_size())
        self.theme_toggle.set_state(self.config.get_theme())
        self.experimental_tools_toggle.set_state("dark" if self.config.get_experimental_tools_enabled() else "light")
