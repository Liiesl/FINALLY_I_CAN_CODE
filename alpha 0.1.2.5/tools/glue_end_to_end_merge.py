import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt

class GlueEndToEndMerge(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.main_subtitle_path = ""
        self.secondary_subtitle_path = ""
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

        # Secondary subtitle file selection
        secondary_file_layout = QHBoxLayout()
        self.secondary_subtitle_button = QPushButton("Select Secondary Subtitle")
        self.secondary_subtitle_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.secondary_subtitle_button.clicked.connect(self.select_secondary_subtitle)
        secondary_file_layout.addWidget(self.secondary_subtitle_button)

        self.secondary_file_preview = QLabel("")
        self.secondary_file_preview.setStyleSheet("color: white; font-size: 12px;")
        secondary_file_layout.addWidget(self.secondary_file_preview)

        layout.addLayout(secondary_file_layout)

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

        layout.addLayout(base_length_layout)

        # Export button
        self.export_button = QPushButton("Export")
        self.export_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.export_button.clicked.connect(self.glue_end_to_end_merge)
        layout.addWidget(self.export_button, alignment=Qt.AlignRight)

    def select_main_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Main Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.main_subtitle_path = file_path
            self.main_file_preview.setText(os.path.basename(file_path))

    def select_secondary_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Secondary Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.secondary_subtitle_path = file_path
            self.secondary_file_preview.setText(os.path.basename(file_path))

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