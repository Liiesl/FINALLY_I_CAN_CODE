import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #2c2f38;")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.main_menu()

    def main_menu(self):
        # Clear the central widget layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # Add safe area around the edges
        self.layout.setContentsMargins(100, 100, 100, 100)

        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)
        scroll_layout = QHBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)
        
        self.layout.addWidget(scroll)

        # Add tool buttons
        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears."),
            ("Merge SRT Files", "Combine multiple SRT files into one."),
            ("Coming Soon", "New tools will be added here.")
        ]

        for tool in tools:
            scroll_layout.addWidget(self.create_tool_button(tool[0], tool[1]))

        scroll_layout.addStretch()

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                border: 10px solid #4f86f7; /* Thicker edge line */
                color: white;
                border-radius: 10px;
                padding: 10px;
                min-width: 150px;
                min-height: 200px;
                margin: 10px;
                background-color: #2c2f38; /* Same as background color */
                text-align: center; /* Center align text */
            }
            QPushButton:hover {
                border-color: #3a6dbf;
            }
        """)

        # Create name label
        name_label = QLabel(tool_name)
        name_label.setFont(QFont("Arial", 18, QFont.Bold))  # Larger and bold font
        name_label.setStyleSheet("color: #4f86f7;")
        name_label.setWordWrap(True)  # Enable word wrap
        name_label.setAlignment(Qt.AlignCenter)  # Center align text
        
        # Create description label
        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Arial", 12))
        description_label.setStyleSheet("color: white;")
        description_label.setWordWrap(True)  # Enable word wrap
        description_label.setAlignment(Qt.AlignCenter)  # Center align text
        
        # Create layout for the button
        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)
        
        button.clicked.connect(lambda: self.tool_selected(tool_name))
        return button

    def tool_selected(self, tool_name):
        if tool_name == "Longer Appearance SRT":
            from tools.longer_appearance import LongerAppearanceSRT
            self.load_tool(LongerAppearanceSRT)
        elif tool_name == "Merge SRT Files":
            from tools.merge_srt import MergeSRT
            self.load_tool(MergeSRT)
        else:
            QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")

    def load_tool(self, tool_class):
        # Clear the central widget layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        tool_widget = tool_class(parent=self.central_widget, back_callback=self.main_menu)
        self.layout.addWidget(tool_widget)
        tool_widget.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set dark theme
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(44, 47, 56))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(44, 47, 56))
    palette.setColor(QPalette.AlternateBase, QColor(66, 69, 79))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(44, 47, 56))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())