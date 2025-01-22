from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
import os

class GlueEndToEndMerge(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_subtitle_path = ""
        self.secondary_subtitle_path = ""
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Mode selection buttons
        mode_layout = QHBoxLayout()

        self.glue_button = QPushButton('Glue End to End Merge')
        self.glue_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.glue_button.clicked.connect(self.show_glue_end_to_end)
        mode_layout.addWidget(self.glue_button)

        self.stacked_button = QPushButton('Stacked Merge')
        self.stacked_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.stacked_button.clicked.connect(self.show_stacked_merge)
        mode_layout.addWidget(self.stacked_button)

        layout.addLayout(mode_layout)

        # Select main subtitle file
        self.main_subtitle_button = QPushButton('Select Main Subtitle')
        self.main_subtitle_button.clicked.connect(self.select_main_subtitle)
        layout.addWidget(self.main_subtitle_button)

        self.main_file_preview = QLabel('')
        layout.addWidget(self.main_file_preview)

        # Select secondary subtitle file
        self.secondary_subtitle_button = QPushButton('Select Secondary Subtitle')
        self.secondary_subtitle_button.clicked.connect(self.select_secondary_subtitle)
        layout.addWidget(self.secondary_subtitle_button)

        self.secondary_file_preview = QLabel('')
        layout.addWidget(self.secondary_file_preview)

        # Base length input
        self.base_length_input = QLineEdit()
        self.base_length_input.setPlaceholderText("00:00:00")
        self.base_length_input.textChanged.connect(self.format_base_length)
        layout.addWidget(self.base_length_input)

        # Export button
        self.export_button = QPushButton('Glue End to End Merge')
        self.export_button.setStyleSheet("background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.export_button.clicked.connect(self.glue_end_to_end_merge)
        layout.addWidget(self.export_button, alignment=Qt.AlignRight)

    def get_mode_button_style(self, selected=False):
        if selected:
            return "background-color: #3a6dbf; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"
        else:
            return "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"

    def show_glue_end_to_end(self):
        # Set style for glue button as selected
        self.glue_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.stacked_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.show()

    def show_stacked_merge(self):
        # Set style for stacked button as selected
        self.glue_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.stacked_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.parent().show_stacked_merge()

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

    def offset_subtitle_times(self, content, offset_seconds):
        # This method offsets the times in the subtitle content by the given number of seconds.
        # Implement the logic for offsetting subtitle times here.
        return content