import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from config import Config

class SubtitleShifter(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.subtitle_path = ""
        self.config = Config()
        self.font_size = None  # Initialize font_size attribute
        self.setup_ui()
        self.apply_theme()  # Ensure apply_theme is called before show_whole_shift
        self.show_whole_shift()  # Move show_whole_shift here

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Add Back to Home button
        self.back_button = self.add_button(layout, "Back to Home", self.back_callback)

        # Mode selection
        self.setup_mode_selection(layout)

        # Separator line
        self.add_separator(layout)

        # Stacked widget to switch between modes
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Whole Shift mode
        self.setup_whole_shift_mode()

        # Partial Shift mode
        self.setup_partial_shift_mode()

    def add_button(self, layout, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def add_label(self, layout, text):
        label = QLabel(text)
        layout.addWidget(label)
        return label

    def add_input(self, layout, placeholder="", width=500):
        input_box = QLineEdit()
        input_box.setPlaceholderText(placeholder)
        input_box.setFixedWidth(width)
        layout.addWidget(input_box)
        return input_box

    def add_separator(self, layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

    def setup_mode_selection(self, layout):
        mode_layout = QHBoxLayout()
        self.mode_label = self.add_label(mode_layout, "Select Mode:")

        self.whole_shift_button = self.add_button(mode_layout, "Whole Shift", self.show_whole_shift)
        self.partial_shift_button = self.add_button(mode_layout, "Partial Shift", self.show_partial_shift)

        layout.addLayout(mode_layout)

    def setup_whole_shift_mode(self):
        self.whole_shift_widget = QWidget()
        whole_layout = QVBoxLayout(self.whole_shift_widget)

        # Subtitle file selection
        file_layout = QHBoxLayout()
        self.select_file_button = self.add_button(file_layout, "Select Subtitle File", self.select_subtitle)
        self.file_preview = self.add_label(file_layout, "")
        whole_layout.addLayout(file_layout)

        # Milliseconds input
        ms_layout = QHBoxLayout()
        self.ms_label = self.add_label(ms_layout, "Shift by (milliseconds):")
        self.ms_input = self.add_input(ms_layout, "1000", 100)
        whole_layout.addLayout(ms_layout)

        # Shift button
        self.shift_button = self.add_button(whole_layout, "Shift", self.whole_shift)

        self.stacked_widget.addWidget(self.whole_shift_widget)

    def setup_partial_shift_mode(self):
        self.partial_shift_widget = QWidget()
        partial_layout = QVBoxLayout(self.partial_shift_widget)

        # Subtitle file selection
        file_layout = QHBoxLayout()
        self.select_file_button_partial = self.add_button(file_layout, "Select Subtitle File", self.select_subtitle)
        self.file_preview_partial = self.add_label(file_layout, "")
        partial_layout.addLayout(file_layout)

        # Start time input
        start_layout = QHBoxLayout()
        self.start_label = self.add_label(start_layout, "Start time (hh:mm:ss,fff):")
        self.start_input = self.add_input(start_layout, "00:00:00,000", 150)
        self.start_input.textChanged.connect(lambda: self.format_time_input(self.start_input))
        partial_layout.addLayout(start_layout)

        # End time input
        end_layout = QHBoxLayout()
        self.end_label = self.add_label(end_layout, "End time (hh:mm:ss,fff):")
        self.end_input = self.add_input(end_layout, "00:00:00,000", 150)
        self.end_input.textChanged.connect(lambda: self.format_time_input(self.end_input))
        partial_layout.addLayout(end_layout)

        # Milliseconds input
        ms_layout = QHBoxLayout()
        self.ms_label_partial = self.add_label(ms_layout, "Shift by (milliseconds):")
        self.ms_input_partial = self.add_input(ms_layout, "1000", 100)
        partial_layout.addLayout(ms_layout)

        # Shift button
        self.shift_button_partial = self.add_button(partial_layout, "Shift", self.partial_shift)

        self.stacked_widget.addWidget(self.partial_shift_widget)

    def apply_theme(self):
        # Retrieve the current palette colors
        palette = self.parent().palette()
        self.text_color = palette.color(QPalette.WindowText).name()
        self.background_color = palette.color(QPalette.Window).name()
        self.button_color = palette.color(QPalette.Button).name()
        self.button_text_color = palette.color(QPalette.ButtonText).name()
        self.highlight_color = palette.color(QPalette.Highlight).name()
        self.hover_color = palette.color(QPalette.Highlight).darker().name()

        text_size = self.config.get_text_size()
        self.font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        button_font_size = self.font_size
        label_font_size = self.font_size
        input_font_size = self.font_size

        self.setStyleSheet(f"background-color: {self.background_color};")
        self.file_preview.setStyleSheet(f"color: {self.text_color};")
        self.file_preview_partial.setStyleSheet(f"color: {self.text_color};")
        self.mode_label.setStyleSheet(f"color: {self.text_color};")
        self.ms_label.setStyleSheet(f"color: {self.text_color};")
        self.ms_label_partial.setStyleSheet(f"color: {self.text_color};")
        self.start_label.setStyleSheet(f"color: {self.text_color};")
        self.end_label.setStyleSheet(f"color: {self.text_color};")
        self.ms_input.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")
        self.ms_input_partial.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")
        self.start_input.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")
        self.end_input.setStyleSheet(f"background-color: {self.background_color}; color: {self.text_color};")

        button_style = self.get_button_style()
        self.back_button.setStyleSheet(button_style)
        self.select_file_button.setStyleSheet(button_style)
        self.select_file_button_partial.setStyleSheet(button_style)
        self.shift_button.setStyleSheet(button_style)
        self.shift_button_partial.setStyleSheet(button_style)
        self.whole_shift_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.partial_shift_button.setStyleSheet(self.get_mode_button_style(selected=False))

    def get_button_style(self):
        return f"""
            QPushButton {{
                border: 2px solid {self.highlight_color};
                color: {self.button_text_color};
                border-radius: 10px;
                padding: 10px;
                background-color: {self.button_color};
            }}
            QPushButton:hover {{
                border-color: {self.hover_color};
                background-color: {self.hover_color};
            }}
        """

    def get_mode_button_style(self, selected):
        if selected:
            return f"background-color: {self.highlight_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px; font-size: {self.font_size}px;"
        return f"background-color: {self.button_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px; font-size: {self.font_size}px;"

    def show_whole_shift(self):
        self.stacked_widget.setCurrentWidget(self.whole_shift_widget)
        self.partial_shift_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.whole_shift_button.setStyleSheet(self.get_mode_button_style(selected=True))

    def show_partial_shift(self):
        self.stacked_widget.setCurrentWidget(self.partial_shift_widget)
        self.whole_shift_button.setStyleSheet(self.get_mode_button_style(selected=False))
        self.partial_shift_button.setStyleSheet(self.get_mode_button_style(selected=True))
        
    def select_subtitle(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            self.subtitle_path = file_path
            self.file_preview.setText(os.path.basename(file_path))
            self.file_preview_partial.setText(os.path.basename(file_path))

    def whole_shift(self):
        ms_shift = int(self.ms_input.text())
        if self.subtitle_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Shifted Subtitles", "", "Subtitle Files (*.srt)")
            if save_path:
                shift_subtitle(self.subtitle_path, ms_shift, save_path)
                self.show_success_message("Subtitles shifted successfully!")

    def partial_shift(self):
        start_time = self.start_input.text()
        end_time = self.end_input.text()
        ms_shift = int(self.ms_input_partial.text())
        if self.subtitle_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Shifted Subtitles", "", "Subtitle Files (*.srt)")
            if save_path:
                shift_subtitle_partial(self.subtitle_path, start_time, end_time, ms_shift, save_path)
                self.show_success_message("Subtitles shifted successfully!")

    def show_success_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)

        # Change the text color to black or any visible color
        palette = msg_box.palette()
        palette.setColor(QPalette.WindowText, QColor(Qt.black))
        msg_box.setPalette(palette)

        msg_box.exec_()

    def format_time_input(self, input_box):
        text = input_box.text()
        formatted_text = text[:]
        if len(text) > 2 and text[2] != ':':
            formatted_text = text[:2] + ':' + text[2:]
        if len(text) > 5 and text[5] != ':':
            formatted_text = text[:5] + ':' + text[5:]
        if len(text) > 8 and text[8] != ',':
            formatted_text = text[:8] + ',' + text[8:]
        if text != formatted_text:
            input_box.setText(formatted_text)

def shift_subtitle(file_path, ms_shift, save_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    shifted_content = []
    for line in content:
        if '-->' in line:
            start, end = line.split(' --> ')
            new_start = shift_time(start, ms_shift)
            new_end = shift_time(end, ms_shift)
            shifted_content.append(f'{new_start} --> {new_end}\n')
        else:
            shifted_content.append(line)

    with open(save_path, 'w') as file:
        file.writelines(shifted_content)

def shift_subtitle_partial(file_path, start_time, end_time, ms_shift, save_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    shifted_content = []
    for line in content:
        if '-->' in line:
            start, end = line.split(' --> ')
            if start >= start_time and end <= end_time:
                new_start = shift_time(start, ms_shift)
                new_end = shift_time(end, ms_shift)
                shifted_content.append(f'{new_start} --> {new_end}\n')
            else:
                shifted_content.append(line)
        else:
            shifted_content.append(line)

    with open(save_path, 'w') as file:
        file.writelines(shifted_content)

def shift_time(time_str, ms_shift):
    time_pattern = re.compile(r'(\d+):(\d+):(\d+),(\d+)')
    match = time_pattern.match(time_str)
    if match:
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds + ms_shift

        new_hours = total_ms // 3600000
        total_ms %= 3600000
        new_minutes = total_ms // 60000
        total_ms %= 60000
        new_seconds = total_ms // 1000
        new_ms = total_ms % 1000

        return f'{new_hours:02}:{new_minutes:02}:{new_seconds:02},{new_ms:03}'
    return time_str
