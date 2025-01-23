import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import qtawesome as qta  # Import QtAwesome for icons
from settings import Settings  # Import the Settings class
from tools.subtitle_converter import SubtitleConverter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("MainWindow: Initializing")
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet("background-color: #2c2f38;")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.side_page = None
        self.hamburger_button = None
        self.settings_widget = None

        self.init_ui()

    def init_ui(self):
        print("MainWindow: Initializing UI")
        # Create a layout for the main content
        self.main_layout = QVBoxLayout()

        # Add the hamburger button at the top left corner
        self.add_hamburger_button()

        # Add the main menu content
        self.main_menu()

        # Clear any existing layout before setting the new one
        if self.central_widget.layout() is not None:
            QWidget().setLayout(self.central_widget.layout())
        self.central_widget.setLayout(self.main_layout)
        self.central_widget.show()  # Ensure the central widget is visible

    def add_hamburger_button(self):
        print("MainWindow: Adding Hamburger Button")
        # Create a container for the hamburger button
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)  # No margins
        container_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # Align to top-left

        # Create the hamburger button
        self.hamburger_button = QPushButton()
        self.hamburger_button.setFixedSize(30, 30)  # Make the button smaller
        self.hamburger_button.setIcon(qta.icon('fa.bars'))  # Use FontAwesome 'bars' icon
        self.hamburger_button.setIconSize(self.hamburger_button.size())
        self.hamburger_button.setStyleSheet("border: none; background: transparent;")
        self.hamburger_button.clicked.connect(self.toggle_side_page)

        container_layout.addWidget(self.hamburger_button)
        self.main_layout.addWidget(container, alignment=Qt.AlignTop | Qt.AlignLeft)
        container.show()  # Ensure the container is visible

    def main_menu(self):
        print("MainWindow: Adding Main Menu")
        # Clear the central widget layout
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget(scroll)
        scroll_layout = QHBoxLayout(scroll_content)
        scroll.setWidget(scroll_content)

        self.main_layout.addWidget(scroll)
        scroll.show()  # Ensure the scroll area is visible

        # Add tool buttons
        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears."),
            ("Merge SRT Files", "Combine multiple SRT files into one."),
            ("Subtitle Converter", "Convert subtitles between different formats."),
            ("Settings", "Configure application settings.")
        ]

        for tool in tools:
            scroll_layout.addWidget(self.create_tool_button(tool[0], tool[1]))

        scroll_layout.addStretch()
        scroll_content.show()  # Ensure the scroll content is visible

    def create_tool_button(self, tool_name, tool_description):
        print(f"MainWindow: Creating Tool Button for {tool_name}")
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
        button.show()  # Ensure button is visible
        return button

    def tool_selected(self, tool_name):
        print(f"MainWindow: Tool Selected - {tool_name}")
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
        print(f"MainWindow: Loading Tool - {tool_class.__name__}")
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        tool_widget = tool_class(parent=self.central_widget, back_callback=self.main_menu)
        self.main_layout.addWidget(tool_widget)
        tool_widget.show()

    def open_settings(self):
        print("MainWindow: Opening Settings")
        self.load_tool(Settings)

    def toggle_side_page(self):
        print("MainWindow: Toggling Side Page")
        if self.side_page and self.side_page.isVisible():
            self.side_page.hide()
        else:
            self.show_side_page()

    def show_side_page(self):
        print("MainWindow: Showing Side Page")
        if self.side_page is None:
            self.side_page = SidePage(self)
        
        self.position_side_page()
        self.side_page.show()

    def position_side_page(self):
        print("MainWindow: Positioning Side Page")
        # Position the side page just below the hamburger button
        button_pos = self.hamburger_button.mapToGlobal(QPoint(0, 0))
        button_height = self.hamburger_button.height()
        # Glue the left edge of the side page to the left edge of the window
        self.side_page.move(self.geometry().left(), button_pos.y() + button_height)

    def moveEvent(self, event):
        if self.side_page and self.side_page.isVisible():
            self.position_side_page()
        super().moveEvent(event)

    def resizeEvent(self, event):
        if self.side_page and self.side_page.isVisible():
            self.position_side_page()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if self.side_page and self.side_page.isVisible():
            if not self.side_page.geometry().contains(event.globalPos()) and not self.hamburger_button.geometry().contains(event.pos()):
                self.side_page.hide()
        super().mousePressEvent(event)

class SidePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("SidePage: Initializing")
        self.setWindowTitle("Side Page")
        self.setGeometry(0, 0, 200, 400)
        self.setStyleSheet("background-color: #2c2f38;")
        
        layout = QVBoxLayout(self)

        # Add list of clickable texts
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Add settings item
        settings_item = QListWidgetItem("Settings")
        self.list_widget.addItem(settings_item)

        # Connect item click to the corresponding function
        self.list_widget.itemClicked.connect(self.handle_item_clicked)

    def handle_item_clicked(self, item):
        print(f"SidePage: Item Clicked - {item.text()}")
        if item.text() == "Settings":
            self.parent().open_settings()
        self.hide()

if __name__ == "__main__":
    try:
        print("Starting Application")
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
        print("Application Running")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
