import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QStackedWidget, QFrame
from PyQt5.QtCore import Qt

class SubtitleShifter(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.subtitle_path = ""
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Add Back to Home button
        self.add_button(layout, "Back to Home", self.back_callback, "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")

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

        # Show the Whole Shift mode by default
        self.show_whole_shift()

    def add_button(self, layout, text, callback, style):
        button = QPushButton(text)
        button.setStyleSheet(style)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def add_label(self, layout, text, style):
        label = QLabel(text)
        label.setStyleSheet(style)
        layout.addWidget(label)
        return label

    def add_input(self, layout, placeholder="", width=100, style="background-color: #3c3f41; color: white; font-size: 14px; padding: 10px;"):
        input_box = QLineEdit()
        input_box.setPlaceholderText(placeholder)
        input_box.setStyleSheet(style)
        input_box.setFixedWidth(width)
        layout.addWidget(input_box)
        return input_box

    def add_separator(self, layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #3c3f41;")
        layout.addWidget(separator)

    def setup_mode_selection(self, layout):
        mode_layout = QHBoxLayout()
        self.add_label(mode_layout, "Select Mode:", "color: white; font-size: 14px;")

        self.whole_shift_button = self.add_button(mode_layout, "Whole Shift", self.show_whole_shift, self.get_mode_button_style(selected=True))
        self.partial_shift_button = self.add_button(mode_layout, "Partial Shift", self.show_partial_shift, self.get_mode_button_style(selected=False))

        layout.addLayout(mode_layout)

    def setup_whole_shift_mode(self):
        self.whole_shift_widget = QWidget()
        whole_layout = QVBoxLayout(self.whole_shift_widget)

        # Subtitle file selection
        file_layout = QHBoxLayout()
        self.add_button(file_layout, "Select Subtitle File", self.select_subtitle, "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.file_preview = self.add_label(file_layout, "", "color: white; font-size: 14px;")
        whole_layout.addLayout(file_layout)

        # Milliseconds input
        ms_layout = QHBoxLayout()
        self.add_label(ms_layout, "Shift by (milliseconds):", "color: white; font-size: 14px;")
        self.ms_input = self.add_input(ms_layout, "1000", 100)
        whole_layout.addLayout(ms_layout)

        # Shift button
        self.add_button(whole_layout, "Shift", self.whole_shift, "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")

        self.stacked_widget.addWidget(self.whole_shift_widget)

    def setup_partial_shift_mode(self):
        self.partial_shift_widget = QWidget()
        partial_layout = QVBoxLayout(self.partial_shift_widget)

        # Subtitle file selection
        file_layout = QHBoxLayout()
        self.add_button(file_layout, "Select Subtitle File", self.select_subtitle, "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.file_preview_partial = self.add_label(file_layout, "", "color: white; font-size: 14px;")
        partial_layout.addLayout(file_layout)

        # Start time input
        start_layout = QHBoxLayout()
        self.add_label(start_layout, "Start time (hh:mm:ss,fff):", "color: white; font-size: 14px;")
        self.start_input = self.add_input(start_layout, "00:00:00,000", 150)
        partial_layout.addLayout(start_layout)

        # End time input
        end_layout = QHBoxLayout()
        self.add_label(end_layout, "End time (hh:mm:ss,fff):", "color: white; font-size: 14px;")
        self.end_input = self.add_input(end_layout, "00:00:00,000", 150)
        partial_layout.addLayout(end_layout)

        # Milliseconds input
        ms_layout = QHBoxLayout()
        self.add_label(ms_layout, "Shift by (milliseconds):", "color: white; font-size: 14px;")
        self.ms_input_partial = self.add_input(ms_layout, "1000", 100)
        partial_layout.addLayout(ms_layout)

        # Shift button
        self.add_button(partial_layout, "Shift", self.partial_shift, "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")

        self.stacked_widget.addWidget(self.partial_shift_widget)

    def get_mode_button_style(self, selected):
        if selected:
            return "background-color: #3a6dbf; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"
        return "background-color: #4f86f7; color: white; border-radius: 5px; padding: 10px; font-size: 14px;"

    def show_whole_shift(self):
        self.stacked_widget.setCurrentWidget(self.whole_shift_widget)
        self.whole_shift_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.partial_shift_button.setStyleSheet(self.get_mode_button_style(selected=False))

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
            # Call function to shift whole subtitle by ms_shift
            shift_subtitle(self.subtitle_path, ms_shift)
            QMessageBox.information(self, "Success", "Subtitles shifted successfully!")

    def partial_shift(self):
        start_time = self.start_input.text()
        end_time = self.end_input.text()
        ms_shift = int(self.ms_input_partial.text())
        if self.subtitle_path:
            # Call function to shift partial subtitle by ms_shift within start and end time
            shift_subtitle_partial(self.subtitle_path, start_time, end_time, ms_shift)
            QMessageBox.information(self, "Success", "Subtitles shifted successfully!")

def shift_subtitle(file_path, ms_shift):
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

    with open(file_path, 'w') as file:
        file.writelines(shifted_content)

def shift_subtitle_partial(file_path, start_time, end_time, ms_shift):
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

    with open(file_path, 'w') as file:
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
