import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QComboBox, QListWidget, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt

class StackedMerge(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.main_subtitle_path = ""
        self.secondary_subtitle_paths = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Main subtitle file selection
        main_file_layout = QHBoxLayout()
        self.main_subtitle_button = QPushButton("Select Main Subtitle")
        self.main_subtitle_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.main_subtitle_button.clicked.connect(self.select_main_subtitle)
        main_file_layout.addWidget(self.main_subtitle_button)

        self.main_file_preview = QLabel("")
        self.main_file_preview.setStyleSheet("color: white; font-size: 12px;")
        main_file_layout.addWidget(self.main_file_preview)

        layout.addLayout(main_file_layout)

        # Secondary subtitle file selection (multiple files)
        secondary_file_layout = QVBoxLayout()
        self.secondary_subtitle_button = QPushButton("Select Secondary Subtitles")
        self.secondary_subtitle_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.secondary_subtitle_button.clicked.connect(self.select_multiple_secondary_subtitles)
        secondary_file_layout.addWidget(self.secondary_subtitle_button)

        self.secondary_file_list = QListWidget()
        self.secondary_file_list.setStyleSheet("background-color: #3c3f41; color: white; font-size: 12px;")
        secondary_file_layout.addWidget(self.secondary_file_list)

        layout.addLayout(secondary_file_layout)

        # Color options
        color_layout = QVBoxLayout()
        self.color_label = QLabel("Color options:")
        self.color_label.setStyleSheet("color: white; font-size: 14px;")
        color_layout.addWidget(self.color_label)

        self.none_checkbox = QCheckBox("None")
        self.color_checkbox = QCheckBox("Color the merged subtitles")
        self.none_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.color_checkbox.setStyleSheet("color: white; font-size: 14px;")
        self.none_checkbox.setChecked(True)

        self.none_checkbox.stateChanged.connect(self.toggle_color_options)
        self.color_checkbox.stateChanged.connect(self.toggle_color_options)

        color_checks_layout = QHBoxLayout()
        color_checks_layout.addWidget(self.none_checkbox)
        color_checks_layout.addWidget(self.color_checkbox)
        color_layout.addLayout(color_checks_layout)

        # Color palette
        self.color_palette_layout = QHBoxLayout()
        self.color_palette = QComboBox()
        self.add_color_options_to_palette()
        self.color_palette.setStyleSheet("background-color: #3c3f41; color: white; font-size: 14px; padding: 10px;")
        self.color_palette_layout.addWidget(self.color_palette)

        self.hex_input = QLineEdit()
        self.hex_input.setPlaceholderText("#000000")
        self.hex_input.setStyleSheet("background-color: #3c3f41; color: white; font-size: 14px; padding: 10px;")
        self.color_palette_layout.addWidget(self.hex_input)

        color_layout.addLayout(self.color_palette_layout)
        self.color_palette_layout.setEnabled(False)

        layout.addLayout(color_layout)

        # Export button
        self.export_button = QPushButton("Export")
        self.export_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.export_button.clicked.connect(self.stacked_merge)
        layout.addWidget(self.export_button, alignment=Qt.AlignRight)

    def select_main_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Main Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.main_subtitle_path = file_path
            self.main_file_preview.setText(os.path.basename(file_path))

    def select_multiple_secondary_subtitles(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Secondary Subtitle Files", "", "Subtitle Files (*.srt)")
        if file_paths:
            self.secondary_subtitle_paths = file_paths
            self.secondary_file_list.clear()
            for path in file_paths:
                self.secondary_file_list.addItem(os.path.basename(path))

    def toggle_color_options(self):
        if self.color_checkbox.isChecked():
            self.color_palette_layout.setEnabled(True)
            self.none_checkbox.setChecked(False)
        else:
            self.color_palette_layout.setEnabled(False)
            self.none_checkbox.setChecked(True)

    def add_color_options_to_palette(self):
        colors = {
            "Red": "#FF0000",
            "Orange": "#FFA500",
            "Yellow": "#FFFF00",
            "Green": "#008000",
            "Blue": "#0000FF",
            "Indigo": "#4B0082",
            "Violet": "#EE82EE"
        }
        for color_name, color_hex in colors.items():
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(color_hex))
            icon = QIcon(pixmap)
            self.color_palette.addItem(icon, color_name)

    def stacked_merge(self):
        if not self.main_subtitle_path or not self.secondary_subtitle_paths:
            QMessageBox.critical(self, "Error", "Please select the main subtitle and at least one secondary subtitle file.")
            return

        color_hex = None
        if self.color_checkbox.isChecked():
            if self.hex_input.text():
                color_hex = self.hex_input.text()
            else:
                selected_color = self.color_palette.currentText()
                if selected_color:
                    color_hex = {
                        "Red": "#FF0000",
                        "Orange": "#FFA500",
                        "Yellow": "#FFFF00",
                        "Green": "#008000",
                        "Blue": "#0000FF",
                        "Indigo": "#4B0082",
                        "Violet": "#EE82EE"
                    }.get(selected_color)

        self.merge_subtitles_stacked(self.main_subtitle_path, self.secondary_subtitle_paths, color_hex)

    def merge_subtitles_stacked(self, main_path, secondary_paths, color_hex):
        try:
            with open(main_path, 'r', encoding='utf-8') as main_file:
                main_content = main_file.read()

            merged_content = main_content

            for secondary_path in secondary_paths:
                with open(secondary_path, 'r', encoding='utf-8') as secondary_file:
                    secondary_content = secondary_file.read()
                if color_hex:
                    secondary_content = self.apply_color_to_subtitles(secondary_content, color_hex)
                merged_content += '\n\n' + secondary_content

            # Save merged file
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged File", "merged.srt", "Subtitle Files (*.srt)")
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(merged_content)
                QMessageBox.information(self, "Success", f"Merged file saved successfully!")
            else:
                print("Save operation cancelled")

        except Exception as e:
            print(f"Failed to merge files: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred while merging the files.\n\n{e}")

    def apply_color_to_subtitles(self, content, color_hex):
        colored_content = ""
        for line in content.split('\n'):
            if '-->' in line:
                colored_content += line + '\n'
            else:
                colored_content += f'<font color="{color_hex}">{line}</font>\n'
        return colored_content