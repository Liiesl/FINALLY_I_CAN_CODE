from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QListWidget, QComboBox
from tools.subtitleconverter.vtt_converter import convert_to_vtt
from tools.subtitleconverter.ass_converter import convert_to_ass
from tools.subtitleconverter.sub_converter import convert_to_sub
from tools.subtitleconverter.ssa_converter import convert_to_ssa
from tools.subtitleconverter.sbv_converter import convert_to_sbv
from tools.subtitleconverter.dfp_converter import convert_to_dfp
from tools.subtitleconverter.stl_converter import convert_to_stl
from tools.subtitleconverter.mpl_converter import convert_to_mpl
from tools.subtitleconverter.usf_converter import convert_to_usf
from tools.subtitleconverter.lrc_converter import convert_to_lrc
from tools.subtitleconverter.rt_converter import convert_to_rt
from tools.subtitleconverter.ttml_converter import convert_to_ttml
from tools.subtitleconverter.cap_converter import convert_to_cap  # Import CAP converter

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

        format_label = QLabel("Select Source Format:")
        format_layout.addWidget(format_label)

        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems([
            "SRT (.srt)", "ASS (.ass)", "SUB (.sub)", "TXT (.txt)", "SSA (.ssa)",
            "SBV (.sbv)", "DFXP (.dfxp)", "STL (.stl)", "MPL (.mpl)", "USF (.usf)",
            "LRC (.lrc)", "RT (.rt)", "TTML (.ttml)", "CAP (.cap)"
            # Add more formats as needed
        ])
        format_layout.addWidget(self.format_dropdown)

        layout.addLayout(format_layout)

        # Convert button
        convert_button = QPushButton("Convert to CAP")
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
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Subtitle Files", "", "Subtitle Files (*.srt *.ass *.sub *.txt *.ssa *.sbv *.dfxp *.stl *.mpl *.usf *.lrc *.rt *.ttml *.cap)")
        if file_paths:
            self.file_list.addItems(file_paths)

    def convert_subtitle(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Error", "Please select at least one file to convert.")
            return

        target_format = self.format_dropdown.currentText().split(' ')[0].lower()  # Extract format (e.g., "srt")
        for index in range(self.file_list.count()):
            subtitle_path = self.file_list.item(index).text()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Converted File", "", "CAP Files (*.cap)")
            if not save_path:
                continue

            try:
                with open(subtitle_path, 'r') as file:
                    content = file.read()

                # Convert the content to CAP
                converted_content = convert_to_cap(content, target_format)

                with open(save_path, 'w') as file:
                    file.write(converted_content)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to convert file: {e}")

        QMessageBox.information(self, "Success", "Subtitle files converted to CAP successfully!")