import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QSplitter, QFrame
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation

from tools.subtitle_converter import SubtitleConverter
from tools.subtitle_shifter import SubtitleShifter
from side_panel import SidePanel
from settings import Settings
from config import Config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #2c2f38;")

        # Load the Inter fonts
        QFontDatabase.addApplicationFont("assets/fonts/Inter-Regular.otf")
        QFontDatabase.addApplicationFont("assets/fonts/Inter-ExtraBold.otf")

        self.inter_regular_font = QFont("Inter Regular")
        self.inter_extra_bold_font = QFont("Inter ExtraBold")

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.config = Config()
        self.main_menu_active = True

        self.side_panel = SidePanel(self, self.open_settings)
        self.side_panel.setVisible(False)
        self.side_panel.setFont(self.inter_regular_font)

        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content.setLayout(self.main_content_layout)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.side_panel)
        self.splitter.addWidget(self.main_content)
        self.splitter.setSizes([0, 1])

        self.layout.addWidget(self.splitter)

        self.top_bar = QHBoxLayout()
        self.top_bar_added = False

        self.menu_button = None

        self.main_menu()

    def main_menu(self):
        self.main_menu_active = True

        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        if self.menu_button is None:
            self.menu_button = QPushButton()
            menu_icon = qta.icon('fa.bars')
            self.menu_button.setIcon(menu_icon)
            self.menu_button.setFixedSize(30, 30)
            self.menu_button.setStyleSheet("background-color: transparent; border: none;")
            self.menu_button.clicked.connect(self.toggle_side_panel)
            self.top_bar.addWidget(self.menu_button, alignment=Qt.AlignLeft)

        if not self.top_bar_added:
            self.main_content_layout.insertLayout(0, self.top_bar)
            self.top_bar_added = True

        self.tool_buttons_container = QWidget()
        self.tool_buttons_layout = QHBoxLayout(self.tool_buttons_container)
        self.tool_buttons_layout.setContentsMargins(0, 0, 0, 0)

        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears."),
            ("Merge SRT Files", "Combine multiple SRT files into one."),
            ("Subtitle Converter", "Convert subtitles between different formats."),
            ("Subtitle Shifter", "Shift subtitles by milliseconds."),
            ("Coming Soon", "More tools will be added in the future.")
        ]

        for tool in tools:
            self.tool_buttons_layout.addWidget(self.create_tool_button(tool[0], tool[1]))

        self.tool_buttons_layout.addStretch()

        navigation_frame = QFrame()
        navigation_layout = QHBoxLayout(navigation_frame)
        navigation_layout.setContentsMargins(0, 0, 0, 0)

        self.left_arrow_button = QPushButton()
        left_arrow_icon = qta.icon('fa.chevron-left')
        self.left_arrow_button.setIcon(left_arrow_icon)
        self.left_arrow_button.setFixedSize(50, 300)
        self.left_arrow_button.setStyleSheet("background-color: #4f86f7; border: none;")
        self.left_arrow_button.clicked.connect(self.scroll_left)
        navigation_layout.addWidget(self.left_arrow_button)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tool_buttons_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area = scroll_area
        navigation_layout.addWidget(scroll_area)

        self.right_arrow_button = QPushButton()
        right_arrow_icon = qta.icon('fa.chevron-right')
        self.right_arrow_button.setIcon(right_arrow_icon)
        self.right_arrow_button.setFixedSize(50, 300)
        self.right_arrow_button.setStyleSheet("background-color: #4f86f7; border: none;")
        self.right_arrow_button.clicked.connect(self.scroll_right)
        navigation_layout.addWidget(self.right_arrow_button)

        self.main_content_layout.addWidget(navigation_frame)

        self.update_safe_area_size()
        self.apply_text_size()
        self.update_tool_button_visibility()
        self.resizeEvent = self.update_tool_button_visibility

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()
        button.setStyleSheet("""
            QPushButton {
                border: 5px solid #4f86f7;
                color: white;
                border-radius: 15px;
                padding: 10px;
                min-width: 200px;
                min-height: 400px;
                margin: 10px;
                background-color: #2c2f38;
                text-align: center;
            }
            QPushButton:hover {
                border-color: #3a6dbf;
                background-color: #3a6dbf;
            }
        """)

        name_label = QLabel(tool_name)
        name_label.setFont(self.inter_extra_bold_font)
        name_label.setStyleSheet("color: #4f86f7; background-color: transparent;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(self.inter_regular_font)
        description_label.setStyleSheet("color: #D3D3D3; background-color: transparent;")
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
            tool_widget = LongerAppearanceSRT(parent=self.main_content, back_callback=self.main_menu)
            tool_widget.setFont(self.inter_regular_font)
            self.load_tool(tool_widget)
        elif tool_name == "Merge SRT Files":
            from tools.merge_srt import MergeSRT
            self.load_tool(MergeSRT(parent=self.main_content, back_callback=self.main_menu))
        elif tool_name == "Subtitle Converter":
            self.load_tool(SubtitleConverter(parent=self.main_content, back_callback=self.main_menu))
        elif tool_name == "Subtitle Shifter":
            self.load_tool(SubtitleShifter(parent=self.main_content, back_callback=self.main_menu))
        else:
            QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")

    def load_tool(self, tool_widget):
        self.main_menu_active = False

        for i in reversed(range(self.main_content_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

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
        settings_widget = Settings(parent=self.main_content, back_callback=self.main_menu)
        settings_widget.setFont(self.inter_regular_font)
        self.load_tool(settings_widget)

    def update_safe_area_size(self):
        self.config = Config()
        safe_area_size = self.config.get_safe_area_size()
        self.main_content_layout.setContentsMargins(safe_area_size, safe_area_size, safe_area_size, safe_area_size)

    def apply_text_size(self):
        text_size = self.config.get_text_size()
        font_size = {
            "small": 16,   # Changed values
            "default": 20, # Changed values
            "large": 24,   # Changed values
            "huge": 28     # Changed values
        }.get(text_size, 20)

        self.setStyleSheet(f"""
            * {{
                font-size: {font_size}px;
            }}
        """)

    def update_tool_button_visibility(self, event=None):
        if self.main_menu_active and self.tool_buttons_container:
            container_width = self.tool_buttons_container.width()
            button_width = 220
            visible_buttons = container_width // button_width
            for i in range(self.tool_buttons_layout.count()):
                item = self.tool_buttons_layout.itemAt(i)
                if item is not None and item.widget() is not None:
                    if i < visible_buttons:
                        item.widget().setVisible(True)
                    else:
                        item.widget().setVisible(False)

    def scroll_left(self):
        current_value = self.scroll_area.horizontalScrollBar().value()
        new_value = max(0, current_value - 220)
        self.animate_scroll(current_value, new_value)

    def scroll_right(self):
        max_value = self.scroll_area.horizontalScrollBar().maximum()
        current_value = self.scroll_area.horizontalScrollBar().value()
        new_value = min(max_value, current_value + 220)
        self.animate_scroll(current_value, new_value)

    def animate_scroll(self, start_value, end_value):
        animation = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
        animation.setDuration(500)
        animation.setStartValue(start_value)
        animation.setEndValue(end_value)
        animation.start()
        self.animation = animation

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
