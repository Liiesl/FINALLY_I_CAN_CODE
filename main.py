import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QSplitter
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from tools.subtitle_converter import SubtitleConverter
from side_panel import SidePanel  # Import the SidePanel class
from settings import Settings  # Import the Settings class
from config import Config  # Import the Config class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c2f38;")

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.config = Config()  # Load configuration

        self.side_panel = SidePanel(self, self.open_settings)
        self.side_panel.setVisible(False)

        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content.setLayout(self.main_content_layout)

        # Splitter to allow dynamic resizing
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.side_panel)
        self.splitter.addWidget(self.main_content)
        self.splitter.setSizes([0, 1])  # Initially hide the side panel

        self.layout.addWidget(self.splitter)

        # Create a horizontal layout for the top bar
        self.top_bar = QHBoxLayout()
        self.top_bar_added = False  # Flag to check if the top bar has been added

        # Add the side panel toggle button (hamburger menu)
        self.menu_button = None

        self.main_menu()

    def main_menu(self):
        # Clear the main content layout
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Add the side panel toggle button (hamburger menu) if not already created
        if self.menu_button is None:
            self.menu_button = QPushButton()
            menu_icon = qta.icon('fa.bars')
            self.menu_button.setIcon(menu_icon)
            self.menu_button.setFixedSize(30, 30)
            self.menu_button.setStyleSheet("background-color: transparent; border: none;")
            self.menu_button.clicked.connect(self.toggle_side_panel)
            self.top_bar.addWidget(self.menu_button, alignment=Qt.AlignLeft)

        # Add the top bar to the main content layout if not already added
        if not self.top_bar_added:
            self.main_content_layout.insertLayout(0, self.top_bar)
            self.top_bar_added = True

        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)
        scroll_layout = QHBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)

        self.main_content_layout.addWidget(scroll)

        # Apply the safe area margins from config
        safe_area_size = self.config.get_safe_area_size()
        self.main_content_layout.setContentsMargins(safe_area_size, safe_area_size, safe_area_size, safe_area_size)

        # Add tool buttons
        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears."),
            ("Merge SRT Files", "Combine multiple SRT files into one."),
            ("Subtitle Converter", "Convert subtitles between different formats."),
            ("Coming Soon", "New tools will be added here.")
        ]

        for tool in tools:
            scroll_layout.addWidget(self.create_tool_button(tool[0], tool[1]))

        scroll_layout.addStretch()

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid #4f86f7;
                color: white;
                border-radius: 10px;
                padding: 10px;
                min-width: 150px;
                min-height: 200px;
                margin: 10px;
                background-color: #4f86f7;
                text-align: center;
            }
            QPushButton:hover {
                border-color: #3a6dbf;
                background-color: #3a6dbf;
            }
        """)

        name_label = QLabel(tool_name)
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        name_label.setStyleSheet("color: #4f86f7;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Arial", 12))
        description_label.setStyleSheet("color: white;")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)

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
        elif tool_name == "Subtitle Converter":
            self.load_tool(SubtitleConverter)
        else:
            QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")

    def load_tool(self, tool_class):
        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        tool_widget = tool_class(parent=self.main_content, back_callback=self.main_menu)
        self.main_content_layout.addWidget(tool_widget)
        tool_widget.show()

    def toggle_side_panel(self):
        if self.side_panel.isVisible():
            self.splitter.setSizes([0, 1])
            self.side_panel.setVisible(False)
        else:
            self.side_panel.setVisible(True)
            self.splitter.setSizes([self.width() // 2, self.width() // 2])

    def open_settings(self, item=None):
        settings = Settings(parent=self.main_content, back_callback=self.main_menu)
        self.load_tool(settings)

if __name__ == "__main__":
    app = QApplication(sys.argv)

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
