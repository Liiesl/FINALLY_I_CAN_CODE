import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QListWidget, QComboBox

class SubtitleConverter(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Back to Home button
        back_button = QPushButton("Back to Home")
        back_button.clicked.connect(self.back_callback)
        layout.addWidget(back_button)

        # File selection section
        file_layout = QHBoxLayout()

        select_file_button = QPushButton("Select File")
        select_file_button.clicked.connect(self.select_files)
        file_layout.addWidget(select_file_button)

        self.file_list = QListWidget()
        self.file_list.setFixedWidth(200)
        file_layout.addWidget(self.file_list)

        layout.addLayout(file_layout)

        # Target format dropdown
        format_layout = QHBoxLayout()

        format_label = QLabel("Select Target Format:")
        format_layout.addWidget(format_label)

        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems([
            "SRT (.srt)", "SUB (.sub)", "TXT (.txt)", "ASS (.ass)", "SSA (.ssa)", "VTT (.vtt)",
            "SBV (.sbv)", "DFXP (.dfxp)", "STL (.stl)", "IDX (.idx)", "MPL (.mpl)", "USF (.usf)",
            "LRC (.lrc)", "RT (.rt)", "TTML (.ttml)", "CAP (.cap)"
        ])
        format_layout.addWidget(self.format_dropdown)

        layout.addLayout(format_layout)

        # Convert button
        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert_subtitle)
        layout.addWidget(convert_button)

        self.setLayout(layout)

        # Apply the same style to all buttons
        self.apply_button_styles([back_button, select_file_button, convert_button])

    def apply_button_styles(self, buttons):
        for button in buttons:
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid #4f86f7; /* Thicker edge line */
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    min-height: 40px;
                    background-color: #4f86f7; /* Accented blue color */
                    text-align: center; /* Center align text */
                }
                QPushButton:hover {
                    border-color: #3a6dbf;
                    background-color: #3a6dbf; /* Darker blue on hover */
                }
            """)

    def select_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Subtitle Files", "", "Subtitle Files (*.srt *.sub *.txt *.ass *.ssa *.vtt *.sbv *.dfxp *.stl *.idx *.mpl *.usf *.lrc *.rt *.ttml *.cap)")
        if file_paths:
            self.file_list.addItems(file_paths)

    def convert_subtitle(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Error", "Please select at least one file to convert.")
            return

        target_format = self.format_dropdown.currentText().split(' ')[0].lower()  # Extract format (e.g., "srt")
        for index in range(self.file_list.count()):
            srt_path = self.file_list.item(index).text()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Converted File", "", f"{target_format.upper()} Files (*.{target_format})")
            if not save_path:
                return

            try:
                with open(srt_path, 'r') as file:
                    content = file.read()

                # Handle different conversions
                if target_format == "vtt":
                    converted_content = self.convert_to_vtt(content)
                elif target_format == "srt":
                    converted_content = self.convert_to_srt(content)
                elif target_format == "sub":
                    converted_content = self.convert_to_sub(content)
                elif target_format == "txt":
                    converted_content = self.convert_to_txt(content)
                elif target_format == "ass":
                    converted_content = self.convert_to_ass(content)
                elif target_format == "ssa":
                    converted_content = self.convert_to_ssa(content)
                elif target_format == "sbv":
                    converted_content = self.convert_to_sbv(content)
                elif target_format == "dfxp":
                    converted_content = self.convert_to_dfxp(content)
                elif target_format == "stl":
                    converted_content = self.convert_to_stl(content)
                elif target_format == "idx":
                    converted_content = self.convert_to_idx(content)
                elif target_format == "mpl":
                    converted_content = self.convert_to_mpl(content)
                elif target_format == "usf":
                    converted_content = self.convert_to_usf(content)
                elif target_format == "lrc":
                    converted_content = self.convert_to_lrc(content)
                elif target_format == "rt":
                    converted_content = self.convert_to_rt(content)
                elif target_format == "ttml":
                    converted_content = self.convert_to_ttml(content)
                elif target_format == "cap":
                    converted_content = self.convert_to_cap(content)
                else:
                    converted_content = content

                with open(save_path, 'w') as file:
                    file.write(converted_content)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to convert file: {e}")
        
        QMessageBox.information(self, "Success", "Subtitle files converted successfully!")

    def convert_to_vtt(self, content):
        vtt_content = "WEBVTT\n\n" + content
        return re.sub(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', r'\1:\2:\3.\4', vtt_content)  # Replace ',' with '.'

    def convert_to_srt(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_sub(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_txt(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_ass(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_ssa(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_sbv(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_dfxp(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_stl(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_idx(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_mpl(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_usf(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_lrc(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_rt(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_ttml(self, content):
        # Implement conversion logic if needed
        return content

    def convert_to_cap(self, content):
        # Implement conversion logic if needed
        return content