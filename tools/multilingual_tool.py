import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, 
                             QMessageBox, QLabel, QListWidget, QColorDialog, QListWidgetItem, QStyledItemDelegate)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from assets.modules.config import Config
from .smprocessing import merge_subtitles, read_file, write_file

class MultilingualTool(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
        self.setFont(QFont("Inter Regular"))
        self.config = Config()
        self.subtitle_paths = []
        self.colors = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        palette = self.parent().palette()
        self.text_color = palette.color(QPalette.WindowText).name()
        self.background_color = palette.color(QPalette.Window).name()
        self.button_color = palette.color(QPalette.Button).name()
        self.button_text_color = palette.color(QPalette.ButtonText).name()
        self.setStyleSheet(f"background-color: {self.background_color};")

        # Back button
        self.add_button(layout, "Back to Home", self.back_callback, 
                       f"background-color: {self.button_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px;")

        # File selection
        self.add_button(layout, "Select Subtitles", self.select_subtitles, 
                       f"background-color: {self.button_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px;")

        # List widget for files and colors
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"background-color: {self.button_color}; color: {self.text_color};")
        layout.addWidget(self.list_widget)

        # Export button
        self.add_button(layout, "Export", self.export_merged, 
                       f"background-color: {self.button_color}; color: {self.button_text_color}; border-radius: 5px; padding: 10px;")

    def add_button(self, layout, text, callback, style):
        button = QPushButton(text)
        button.setStyleSheet(style)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    def select_subtitles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Subtitle Files", "", "Subtitle Files (*.srt)")
        if files:
            self.subtitle_paths = files
            self.colors = ['#FFFFFF'] * len(files)  # Default to white
            self.update_list_widget()

    def update_list_widget(self):
        self.list_widget.clear()
        for idx, (path, color) in enumerate(zip(self.subtitle_paths, self.colors)):
            item = QListWidgetItem(os.path.basename(path))
            item.setData(Qt.UserRole, idx)
            item.setBackground(QColor(color))
            item.setForeground(QColor("black"))
            self.list_widget.addItem(item)
        self.list_widget.itemDoubleClicked.connect(self.change_color)

    def change_color(self, item):
        idx = item.data(Qt.UserRole)
        color = QColorDialog.getColor(QColor(self.colors[idx]), self, "Choose Subtitle Color")
        if color.isValid():
            self.colors[idx] = color.name()
            self.update_list_widget()

    def export_merged(self):
        if not self.subtitle_paths:
            QMessageBox.critical(self, "Error", "Please select at least one subtitle file.")
            return

        # Create a dummy main subtitle (empty content)
        dummy_main = "dummy_main.srt"
        with open(dummy_main, 'w') as f:
            f.write("")

        try:
            merged_content = merge_subtitles(
                dummy_main,
                self.subtitle_paths,
                self.colors
            )
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged File", "multilingual.srt", "Subtitle Files (*.srt)")
            if save_path:
                write_file(save_path, merged_content)
                QMessageBox.information(self, "Success", "Merged file saved successfully!")
            os.remove(dummy_main)  # Cleanup
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n\n{str(e)}")
            if os.path.exists(dummy_main):
                os.remove(dummy_main)
