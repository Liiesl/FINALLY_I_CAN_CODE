import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QStackedWidget, QFrame, QSpacerItem, QSizePolicy, QComboBox, QListWidget, QCheckBox, QGroupBox, QFormLayout
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt

class MergeSRT(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.main_subtitle_path = ""
        self.secondary_subtitle_paths = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        back_button.clicked.connect(self.back_callback)
        layout.addWidget(back_button)

        # Create a horizontal layout for the mode selection buttons
        mode_layout = QHBoxLayout()

        mode_label = QLabel("Select Mode:")
        mode_label.setStyleSheet("color: white; font-size: 14px;")
        mode_layout.addWidget(mode_label)

        self.glue_end_to_end_button = QPushButton("Glue End to End")
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.glue_end_to_end_button.clicked.connect(self.show_glue_end_to_end)
        mode_layout.addWidget(self.glue_end_to_end_button)

        self.stacked_merge_button = QPushButton("Stacked Merge")
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.stacked_merge_button.clicked.connect(self.show_stacked_merge)
        mode_layout.addWidget(self.stacked_merge_button)

        layout.addLayout(mode_layout)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #3c3f41;")
        layout.addWidget(separator)

        # Stacked widget to switch between modes
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Glue End to End mode
        self.glue_end_to_end_widget = QWidget()
        glue_layout = QVBoxLayout(self.glue_end_to_end_widget)

        # Main subtitle file selection
        main_file_layout = QHBoxLayout()
        self.main_subtitle_button = QPushButton("Select Main Subtitle")
        self.main_subtitle_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.main_subtitle_button.clicked.connect(self.select_main_subtitle)
        main_file_layout.addWidget(self.main_subtitle_button)

        self.main_file_preview = QLabel("")
        self.main_file_preview.setStyleSheet("color: white; font-size: 12px;")
        main_file_layout.addWidget(self.main_file_preview)

        glue_layout.addLayout(main_file_layout)

        # Secondary subtitle file selection
        secondary_file_layout = QHBoxLayout()
        self.secondary_subtitle_button = QPushButton("Select Secondary Subtitle")
        self.secondary_subtitle_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.secondary_subtitle_button.clicked.connect(self.select_secondary_subtitle)
        secondary_file_layout.addWidget(self.secondary_subtitle_button)

        self.secondary_file_preview = QLabel("")
        self.secondary_file_preview.setStyleSheet("color: white; font-size: 12px;")
        secondary_file_layout.addWidget(self.secondary_file_preview)

        glue_layout.addLayout(secondary_file_layout)

        # Base length input
        base_length_layout = QHBoxLayout()
        self.base_length_label = QLabel("Length of main subtitle's video:")
        self.base_length_label.setStyleSheet("color: white; font-size: 14px;")
        base_length_layout.addWidget(self.base_length_label)

        # Spacer item to ensure 5px gap between text and input box
        base_length_layout.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.base_length_input = QLineEdit()
        self.base_length_input.setPlaceholderText("00:00:00")
        self.base_length_input.setStyleSheet("background-color: #3c3f41; color: white; font-size: 14px; padding: 10px;")
        self.base_length_input.setFixedWidth(100)
        self.base_length_input.textChanged.connect(self.format_base_length)
        base_length_layout.addWidget(self.base_length_input)

        glue_layout.addLayout(base_length_layout)

        # Export button
        self.export_button = QPushButton("Export")
        self.export_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.export_button.clicked.connect(self.glue_end_to_end_merge)
        glue_layout.addWidget(self.export_button, alignment=Qt.AlignRight)

        # Add Glue End to End widget to stacked widget
        self.stacked_widget.addWidget(self.glue_end_to_end_widget)

        # Stacked Merge mode
        self.stacked_merge_widget = QWidget()
        stacked_layout = QVBoxLayout(self.stacked_merge_widget)

        # Main subtitle file selection
        main_file_layout = QHBoxLayout()
        self.main_subtitle_button_stacked = QPushButton("Select Main Subtitle")
        self.main_subtitle_button_stacked.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.main_subtitle_button_stacked.clicked.connect(self.select_main_subtitle)
        main_file_layout.addWidget(self.main_subtitle_button_stacked)

        self.main_file_preview_stacked = QLabel("")
        self.main_file_preview_stacked.setStyleSheet("color: white; font-size: 12px;")
        main_file_layout.addWidget(self.main_file_preview_stacked)

        stacked_layout.addLayout(main_file_layout)

        # Secondary subtitle file selection (multiple files)
        secondary_file_layout = QVBoxLayout()
        self.secondary_subtitle_button_stacked = QPushButton("Select Secondary Subtitles")
        self.secondary_subtitle_button_stacked.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.secondary_subtitle_button_stacked.clicked.connect(self.select_multiple_secondary_subtitles)
        secondary_file_layout.addWidget(self.secondary_subtitle_button_stacked)

        self.secondary_file_list = QListWidget()
        self.secondary_file_list.setStyleSheet("background-color: #3c3f41; color: white; font-size: 12px;")
        secondary_file_layout.addWidget(self.secondary_file_list)

        stacked_layout.addLayout(secondary_file_layout)

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

        stacked_layout.addLayout(color_layout)

        # Export button
        self.stacked_export_button = QPushButton("Export")
        self.stacked_export_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.stacked_export_button.clicked.connect(self.stacked_merge)
        stacked_layout.addWidget(self.stacked_export_button, alignment=Qt.AlignRight)

        # Add Stacked Merge widget to stacked widget
        self.stacked_widget.addWidget(self.stacked_merge_widget)

        # Show the Glue End to End mode by default
        self.show_glue_end_to_end()

    def get_mode_button_style(self, selected=False):
        if selected:
            return "background-color: #3a6dbf; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"
        else:
            return "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"

    def show_glue_end_to_end(self):
        self.stacked_widget.setCurrentWidget(self.glue_end_to_end_widget)
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(selected=False))

    def show_stacked_merge(self):
        self.stacked_widget.setCurrentWidget(self.stacked_merge_widget)
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(selected=True))

    def select_main_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Main Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.main_subtitle_path = file_path
            self.main_file_preview.setText(os.path.basename(file_path))
            self.main_file_preview_stacked.setText(os.path.basename(file_path))

    def select_secondary_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Secondary Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.secondary_subtitle_path = file_path
            self.secondary_file_preview.setText(os.path.basename(file_path))

    def select_multiple_secondary_subtitles(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Secondary Subtitle Files", "", "Subtitle Files (*.srt)")
        if file_paths:
            self.secondary_subtitle_paths = file_paths
            self.secondary_file_list.clear()
            for path in file_paths:
                self.secondary_file_list.addItem(os.path.basename(path))

    def format_base_length(self, text):
        if len(text) > 8:
            text = text[:8]
        if len(text) in [2, 5] and len(text) < 8:
            self.base_length_input.setText(text + ":")
        else:
            self.base_length_input.setText(text)

    def glue_end_to_end_merge(self):
        # Retrieve base length input
        base_length = self.base_length_input.text()
        if not self.validate_time_format(base_length):
            QMessageBox.critical(self, "Error", "Invalid time format. Please enter time in hh:mm:ss format.")
            return

        if not self.main_subtitle_path or not self.secondary_subtitle_path:
            QMessageBox.critical(self, "Error", "Please select both main and secondary subtitle files.")
            return

        # Perform the merge
        base_seconds = self.time_to_seconds(base_length)
        self.merge_subtitles_end_to_end(self.main_subtitle_path, self.secondary_subtitle_path, base_seconds)

    def validate_time_format(self, time_str):
        parts = time_str.split(':')
        if len(parts) != 3:
            return False
        try:
            hours, minutes, seconds = map(int, parts)
            return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
        except ValueError:
            return False

    def time_to_seconds(self, time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    def merge_subtitles_end_to_end(self, main_path, secondary_path, offset_seconds):
        try:
            with open(main_path, 'r', encoding='utf-8') as main_file:
                main_content = main_file.read()

            with open(secondary_path, 'r', encoding='utf-8') as secondary_file:
                secondary_content = secondary_file.read()

            # Offset secondary subtitles by base length
            offset_content = self.offset_subtitle_times(secondary_content, offset_seconds)

            # Merge contents
            merged_content = main_content + '\n\n' + offset_content

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

    def offset_subtitle_times(self, content, offset_seconds):
        def offset_line(line):
            try:
                start, end = line.split(' --> ')
                new_start = self.add_seconds_to_time(start, offset_seconds)
                new_end = self.add_seconds_to_time(end, offset_seconds)
                return f"{new_start} --> {new_end}"
            except ValueError:
                return line

        return '\n'.join(offset_line(line) if ' --> ' in line else line for line in content.split('\n'))

    def add_seconds_to_time(self, time_str, seconds):
        hours, minutes, secs, millis = map(int, time_str.replace(',', ':').split(':'))
        total_seconds = hours * 3600 + minutes * 60 + secs + seconds
        new_hours = total_seconds // 3600
        new_minutes = (total_seconds % 3600) // 60
        new_seconds = total_seconds % 60
        return f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{millis:03}"

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
                colored_content += f'<font color="{color_hex}