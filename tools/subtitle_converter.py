from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QListWidget, QComboBox
from PyQt5.QtGui import QFont, QPalette
from tools.subtitleconverter.vtt_converter import convert_to_vtt
from tools.subtitleconverter.ass_converter import convert_to_ass
from tools.subtitleconverter.sub_converter import convert_to_sub
from tools.subtitleconverter.ssa_converter import convert_to_ssa
from tools.subtitleconverter.sbv_converter import convert_to_sbv
from tools.subtitleconverter.dfp_converter import convert_to_dfxp
from tools.subtitleconverter.stl_converter import convert_to_stl
from tools.subtitleconverter.mpl_converter import convert_to_mpl
from tools.subtitleconverter.usf_converter import convert_to_usf
from tools.subtitleconverter.lrc_converter import convert_to_lrc
from tools.subtitleconverter.rt_converter import convert_to_rt
from tools.subtitleconverter.ttml_converter import convert_to_ttml
from tools.subtitleconverter.cap_converter import convert_to_cap
from assets.modules.config import Config
import os

class SubtitleConverter(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.config = Config()
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        layout = QVBoxLayout()

        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        # Back to Home button
        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self.back_callback)
        layout.addWidget(self.back_button)

        # File selection section
        file_layout = QHBoxLayout()

        self.select_file_button = QPushButton("Select File")
        self.select_file_button.clicked.connect(self.select_files)
        file_layout.addWidget(self.select_file_button, 1)

        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list, 2)

        layout.addLayout(file_layout)

        # Target format dropdown
        format_layout = QHBoxLayout()

        self.format_label = QLabel("Select Source Format:")
        format_layout.addWidget(self.format_label)

        self.format_dropdown = QComboBox()
        self.format_dropdown.addItems([
            "SRT (.srt)", "SUB (.sub)", "TXT (.txt)", "ASS (.ass)", "SSA (.ssa)",
            "VTT (.vtt)", "SBV (.sbv)", "DFXP (.dfxp)", "STL (.stl)", "IDX (.idx)",
            "MPL (.mpl)", "USF (.usf)", "LRC (.lrc)", "RT (.rt)", "TTML (.ttml)", "CAP (.cap)"
        ])
        self.format_dropdown.currentIndexChanged.connect(self.update_convert_button)
        format_layout.addWidget(self.format_dropdown)

        layout.addLayout(format_layout)

        # Convert button
        self.convert_button = QPushButton("Convert to CAP")
        self.convert_button.clicked.connect(self.convert_subtitle)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

        # Apply the same style to all buttons
        self.apply_button_styles([self.back_button, self.select_file_button, self.convert_button])

    def apply_theme(self):
        # Retrieve the current palette colors
        palette = self.parent().palette()
        text_color = palette.color(QPalette.WindowText).name()
        background_color = palette.color(QPalette.Window).name()
        button_color = palette.color(QPalette.Button).name()
        button_text_color = palette.color(QPalette.ButtonText).name()
        highlight_color = palette.color(QPalette.Highlight).name()
        hover_color = palette.color(QPalette.Highlight).darker().name()

        self.setStyleSheet(f"background-color: {background_color};")
        self.file_list.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.format_label.setStyleSheet(f"color: {text_color};")
        self.format_dropdown.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

        self.back_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {highlight_color};
                color: {button_text_color};
                border-radius: 10px;
                padding: 10px;
                background-color: {button_color};
            }}
            QPushButton:hover {{
                border-color: {hover_color};
                background-color: {hover_color};
            }}
        """)

        self.select_file_button.setStyleSheet(self.back_button.styleSheet())
        self.convert_button.setStyleSheet(self.back_button.styleSheet())

    def apply_button_styles(self, buttons):
        for button in buttons:
            button.setStyleSheet(self.back_button.styleSheet())

    def select_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Subtitle Files", "", "Subtitle Files (*.srt *.ass *.sub *.txt *.ssa *.vtt *.sbv *.dfxp *.stl *.idx *.mpl *.usf *.lrc *.rt *.ttml *.cap)")
        if file_paths:
            self.file_list.clear()
            for file_path in file_paths:
                self.file_list.addItem(os.path.basename(file_path))
            self.file_list.file_paths = file_paths

    def update_convert_button(self):
        target_format = self.format_dropdown.currentText().split(' ')[0]
        self.convert_button.setText(f"Convert to {target_format}")

    def convert_subtitle(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "Error", "Please select at least one file to convert.")
            return

        target_format = self.format_dropdown.currentText().split(' ')[0].lower()  # Extract format (e.g., "srt")
        for index in range(self.file_list.count()):
            subtitle_path = self.file_list.file_paths[index]
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Converted File", "", f"{target_format.upper()} Files (*.{target_format})")
            if not save_path:
                continue

            try:
                with open(subtitle_path, 'r') as file:
                    content = file.read()

                # Convert the content to the selected format (example for CAP)
                converted_content = convert_to_cap(content, target_format)

                with open(save_path, 'w') as file:
                    file.write(converted_content)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to convert file: {e}")

        QMessageBox.information(self, "Success", f"Subtitle files converted to {target_format.upper()} successfully!")
