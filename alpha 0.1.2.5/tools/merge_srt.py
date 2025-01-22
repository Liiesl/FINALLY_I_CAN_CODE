from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MergeSRT(QWidget):
    def __init__(self, parent=None, back_callback=None):
        super().__init__(parent)
        self.back_callback = back_callback
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
        self.glue_end_to_end_button.setStyleSheet(self.get_mode_button_style(selected=True))
        self.glue_end_to_end_button.clicked.connect(self.show_glue_end_to_end)
        mode_layout.addWidget(self.glue_end_to_end_button)

        self.stacked_merge_button = QPushButton("Stacked Merge")
        self.stacked_merge_button.setStyleSheet(self.get_mode_button_style(selected=False))
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

        # Add Glue End to End Merge widget
        from tools.glue_end_to_end_merge import GlueEndToEndMerge
        self.glue_end_to_end_widget = GlueEndToEndMerge(parent=self.stacked_widget)
        self.stacked_widget.addWidget(self.glue_end_to_end_widget)

        # Add Stacked Merge widget
        from tools.stacked_merge import StackedMerge
        self.stacked_merge_widget = StackedMerge(parent=self.stacked_widget)
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