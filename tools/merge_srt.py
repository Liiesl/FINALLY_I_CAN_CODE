import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel, QLineEdit, QStackedWidget, QFrame, QSizePolicy, QComboBox, QListWidget, QSpacerItem
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QPalette
from PyQt5.QtCore import Qt
from .smprocessing import merge_subtitles, read_file, write_file
from config import Config

class MergeSRT(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.config = Config()
        self.main_subtitle_path = ""
        self.secondary_subtitle_paths = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
    
        # Retrieve the current palette colors
        palette = self.parent().palette()
        self.text_color = palette.color(QPalette.WindowText).name()
        self.background_color = palette.color(QPalette.Window).name()
        self.button_color = palette.color(QPalette.Button).name()
        self.button_text_color = palette.color(QPalette.ButtonText).name()
        self.highlight_color = palette.color(QPalette.Highlight).name()
        self.hover_color = palette.color(QPalette.Highlight).darker().name()
    
        self.setStyleSheet(f"background-color: {self.background_color};")
        
        text_size = self.config.get_text_size()
        self.font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)
    
        button_font_size = self.font_size - 12
        label_font_size = self.font_size - 12
        input_font_size = self.font_size - 12
    
        # Back to Home button
        self.add_button(layout, "Back to Home", self.back_callback, f"background-color: {self.button_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
    
        # Mode selection
        self.setup_mode_selection(layout, button_font_size, label_font_size, self.button_color, self.button_text_color, self.highlight_color, self.hover_color)
    
        # Separator line
        self.add_separator(layout)
    
        # Stacked widget to switch between modes
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
    
        # Glue End to End mode
        self.setup_glue_end_to_end_mode(button_font_size, label_font_size, input_font_size, self.button_color, self.button_text_color, self.highlight_color, self.hover_color, self.text_color)
    
        # Stacked Merge mode
        self.setup_stacked_merge_mode(button_font_size, label_font_size, input_font_size, self.button_color, self.button_text_color, self.highlight_color, self.hover_color, self.text_color)
    
        # Show the Glue End to End mode by default
        self.show_glue_end_to_end()
    
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

    def add_input(self, layout, placeholder="", width=500,):
        input_box = QLineEdit()
        input_box.setPlaceholderText(placeholder)
        input_box.setStyleSheet(style)
        input_box.setMinimumWidth(width)
        layout.addWidget(input_box)
        return input_box

    def add_separator(self, layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #3c3f41;")
        layout.addWidget(separator)

    def setup_mode_selection(self, layout, button_font_size, label_font_size, button_color, button_text_color, highlight_color, hover_color):
        mode_layout = QHBoxLayout()
        self.add_label(mode_layout, "Select Mode:", f"color: {button_text_color}; font-size: {label_font_size}px;")
    
        self.glue_end_to_end_button = self.add_button(mode_layout, "Glue End to End", self.show_glue_end_to_end, self.get_mode_button_style(selected=False, font_size=button_font_size, button_color=button_color, text_color=button_text_color, highlight_color=highlight_color))
        self.stacked_merge_button = self.add_button(mode_layout, "Stacked Merge", self.show_stacked_merge, self.get_mode_button_style(selected=True, font_size=button_font_size, button_color=button_color, text_color=button_text_color, highlight_color=highlight_color))
    
        layout.addLayout(mode_layout)
        
    def setup_glue_end_to_end_mode(self, button_font_size, label_font_size, input_font_size, button_color, button_text_color, highlight_color, hover_color, text_color):
        self.glue_end_to_end_widget = QWidget()
        glue_layout = QVBoxLayout(self.glue_end_to_end_widget)
    
        # Main subtitle file selection
        main_file_layout = QHBoxLayout()
        self.main_subtitle_button = self.add_button(main_file_layout, "Select Main Subtitle", self.select_main_subtitle, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        self.main_file_preview = self.add_label(main_file_layout, "", f"color: {text_color}; font-size: {label_font_size}px;")
        glue_layout.addLayout(main_file_layout)
    
        # Secondary subtitle file selection
        secondary_file_layout = QHBoxLayout()
        self.secondary_subtitle_button = self.add_button(secondary_file_layout, "Select Secondary Subtitle", self.select_secondary_subtitle, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        self.secondary_file_preview = self.add_label(secondary_file_layout, "", f"color: {text_color}; font-size: {label_font_size}px;")
        glue_layout.addLayout(secondary_file_layout)
    
        # Base length input
        base_length_layout = QHBoxLayout()
        self.base_length_label = self.add_label(base_length_layout, "Length of main subtitle's video:", f"color: {text_color}; font-size: {label_font_size}px;")
        base_length_layout.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        self.base_length_input = self.add_input(base_length_layout, "00:00:00", 100, f"background-color: #3c3f41; color: white; font-size: {input_font_size}px; padding: 10px;")
        self.base_length_input.textChanged.connect(self.format_base_length)
        glue_layout.addLayout(base_length_layout)
    
        # Export button
        self.export_button = self.add_button(glue_layout, "Export", self.glue_end_to_end_merge, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        glue_layout.addWidget(self.export_button, alignment=Qt.AlignRight)
    
        self.stacked_widget.addWidget(self.glue_end_to_end_widget)
    
    def setup_stacked_merge_mode(self, button_font_size, label_font_size, input_font_size, button_color, button_text_color, highlight_color, hover_color, text_color):
        self.stacked_merge_widget = QWidget()
        stacked_layout = QVBoxLayout(self.stacked_merge_widget)
    
        # Main subtitle file selection
        main_file_layout = QHBoxLayout()
        self.main_subtitle_button = self.add_button(main_file_layout, "Select Main Subtitle", self.select_main_subtitle, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        self.main_file_preview = self.add_label(main_file_layout, "", f"color: {text_color}; font-size: {label_font_size}px;")
        stacked_layout.addLayout(main_file_layout)
    
        # Secondary subtitle file selection (multiple files)
        secondary_file_layout = QVBoxLayout()
        self.secondary_subtitle_button = self.add_button(secondary_file_layout, "Select Secondary Subtitles", self.select_multiple_secondary_subtitles, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        self.secondary_file_list = QListWidget()
        self.secondary_file_list.setStyleSheet(f"background-color: #3c3f41; color: white; font-size: {label_font_size}px;")
        secondary_file_layout.addWidget(self.secondary_file_list)
        stacked_layout.addLayout(secondary_file_layout)
    
        # Color options
        self.setup_color_options(stacked_layout, input_font_size, label_font_size)
    
        # Export button
        self.stacked_export_button = self.add_button(stacked_layout, "Export", self.stacked_merge, f"background-color: {button_color}; color: {button_text_color}; border-radius: 5px; padding: 10px; font-size: {button_font_size}px;")
        stacked_layout.addWidget(self.stacked_export_button, alignment=Qt.AlignRight)
    
        self.stacked_widget.addWidget(self.stacked_merge_widget)
        
    def setup_color_options(self, layout, input_font_size, label_font_size):
        color_layout = QVBoxLayout()
        self.color_label = self.add_label(color_layout, "Color options:", f"color: {self.text_color}; font-size: {label_font_size}px;")

        self.color_combo = QComboBox()
        self.color_combo.addItems(["None", "Color the merged subtitles"])
        self.color_combo.setStyleSheet(f"background-color: (self.button_color); color: {self.text_color}; font-size: {input_font_size}px;")
        self.color_combo.currentIndexChanged.connect(self.toggle_color_options)
        color_layout.addWidget(self.color_combo)

        self.color_palette_layout = QHBoxLayout()
        self.color_palette = QComboBox()
        self.add_color_options_to_palette()
        self.color_palette.setStyleSheet(f"background-color: (self.button_color); color: {self.text_color}; font-size: {input_font_size}px;")
        self.color_palette_layout.addWidget(self.color_palette)

        self.hex_input = self.add_input(self.color_palette_layout, "#000000", 100, f"background-color: (self.button_color); color: {self.text_color}; font-size: {input_font_size}px; padding: 10px;")
        color_layout.addLayout(self.color_palette_layout)

        # Initially hide color options
        self.toggle_color_options()

        layout.addLayout(color_layout)

    def get_mode_button_style(self, selected, font_size, button_color, text_color, highlight_color):
        if selected:
            return f"background-color: {highlight_color}; color: {text_color}; border-radius: 5px; padding: 10px; font-size: {font_size}px;"
        return f"background-color: {button_color}; color: {text_color}; border-radius: 5px; padding: 10px; font-size: {font_size}px;"    
       
    def show_glue_end_to_end(self):
        self.stacked_widget.setCurrentWidget(self.glue_end_to_end_widget)
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(
            selected=True, 
            font_size=self.font_size - 12,
            button_color=self.button_color,
            text_color=self.button_text_color,
            highlight_color=self.highlight_color
        ))
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(
            selected=False, 
            font_size=self.font_size - 12,
            button_color=self.button_color,
            text_color=self.button_text_color,
            highlight_color=self.highlight_color
        ))

    def show_stacked_merge(self):
        self.stacked_widget.setCurrentWidget(self.stacked_merge_widget)
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(
            selected=False, 
            font_size=self.font_size - 12,
            button_color=self.button_color,
            text_color=self.button_text_color,
            highlight_color=self.highlight_color
        ))
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(
            selected=True, 
            font_size=self.font_size - 12,
            button_color=self.button_color,
            text_color=self.button_text_color,
            highlight_color=self.highlight_color
        ))

    def select_main_subtitle(self):
        file_path = self.select_subtitle_file()
        if file_path:
            self.main_subtitle_path = file_path
            self.main_file_preview.setText(os.path.basename(file_path))

    def select_secondary_subtitle(self):
        file_path = self.select_subtitle_file()
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

    def select_subtitle_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Subtitle File", "", "Subtitle Files (*.srt)")
        return file_path

    def format_base_length(self, text):
        formatted_text = text[:8]
        if len(formatted_text) in [2, 5] and len(formatted_text) < 8:
            formatted_text += ":"
        self.base_length_input.setText(formatted_text)

    def glue_end_to_end_merge(self):
        base_length = self.base_length_input.text()
        if not self.validate_time_format(base_length):
            self.show_error("Invalid time format. Please enter time in hh:mm:ss format.")
            return

        if not self.main_subtitle_path or not self.secondary_subtitle_path:
            self.show_error("Please select both main and secondary subtitle files.")
            return

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
            main_content = read_file(main_path)
            secondary_content = read_file(secondary_path)

            offset_content = self.offset_subtitle_times(secondary_content, offset_seconds)
            merged_content = main_content + '\n\n' + offset_content

            save_path = self.save_file("Save Merged File", "merged.srt")
            if save_path:
                write_file(save_path, merged_content)
                self.show_success("Merged file saved successfully!")
        except Exception as e:
            self.show_error(f"An error occurred while merging the files.\n\n{e}")

    def offset_subtitle_times(self, content, offset_seconds):
        return '\n'.join(self.offset_line(line, offset_seconds) if ' --> ' in line else line for line in content.split('\n'))

    def offset_line(self, line, offset_seconds):
        try:
            start, end = line.split(' --> ')
            new_start = self.add_seconds_to_time(start, offset_seconds)
            new_end = self.add_seconds_to_time(end, offset_seconds)
            return f"{new_start} --> {new_end}"
        except ValueError:
            return line

    def add_seconds_to_time(self, time_str, seconds):
        hours, minutes, secs, millis = map(int, time_str.replace(',', ':').split(':'))
        total_seconds = hours * 3600 + minutes * 60 + secs + seconds
        new_hours = total_seconds // 3600
        new_minutes = (total_seconds % 3600) // 60
        new_seconds = total_seconds % 60
        return f"{new_hours:02}:{new_minutes:02}:{new_seconds:02},{millis:03}"

    def toggle_color_options(self):
        is_visible = self.color_combo.currentText() == "Color the merged subtitles"
        self.color_palette.setVisible(is_visible)
        self.hex_input.setVisible(is_visible)

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
            self.show_error("Please select the main subtitle and at least one secondary subtitle file.")
            return

        color_hex = self.get_selected_color()
        try:
            merged_content = merge_subtitles(self.main_subtitle_path, self.secondary_subtitle_paths, color_hex)
            save_path = self.save_file("Save Merged File", "merged.srt")
            if save_path:
                write_file(save_path, merged_content)
                self.show_success("Merged file saved successfully!")
        except Exception as e:
            self.show_error(f"An error occurred while merging the files.\n\n{e}")

    def get_selected_color(self):
        if self.color_combo.currentText() == "Color the merged subtitles":
            color_hex = self.hex_input.text().strip()
            if not color_hex:
                selected_color = self.color_palette.currentText()
                color_hex = {
                    "Red": "#FF0000",
                    "Orange": "#FFA500",
                    "Yellow": "#FFFF00",
                    "Green": "#008000",
                    "Blue": "#0000FF",
                    "Indigo": "#4B0082",
                    "Violet": "#EE82EE"
                }.get(selected_color, "#FFFFFF")  # Default to white if no color selected
            return color_hex
        return None

    def save_file(self, dialog_title, default_name):
        save_path, _ = QFileDialog.getSaveFileName(self, dialog_title, default_name, "Subtitle Files (*.srt)")
        return save_path

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_success(self, message):
        QMessageBox.information(self, "Success", message)
