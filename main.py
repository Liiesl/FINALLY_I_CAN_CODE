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
        
        self.apply_theme()

    def apply_theme(self):
        theme = self.config.get_theme()
        palette = QPalette()
        
        if theme == "dark":
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
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
            palette.setColor(QPalette.HighlightedText, Qt.white)

        # Add the custom accent color
        accent_color = QColor("#4f86f7")
        palette.setColor(QPalette.Link, accent_color)

        self.setPalette(palette)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {palette.color(QPalette.Window).name()};
                color: {palette.color(QPalette.WindowText).name()};
            }}
            QPushButton {{
                border: 5px solid {palette.color(QPalette.Link).name()};
                color: {palette.color(QPalette.ButtonText).name()};
                border-radius: 15px;
                padding: 10px;
                min-width: 200px;
                min-height: 100px;
                margin: 10px;
                background-color: {palette.color(QPalette.Button).name()};
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {palette.color(QPalette.Link).darker().name()};
                background-color: {palette.color(QPalette.Link).darker().name()};
            }}
            QLabel {{
                color: {palette.color(QPalette.WindowText).name()};
                background-color: transparent;
            }}
            QScrollArea {{
                background-color: {palette.color(QPalette.Window).name()};
            }}
            QFrame {{
                background-color: {palette.color(QPalette.Window).name()};
            }}
        """)

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
        self.left_arrow_button.setStyleSheet(f"background-color: {self.palette().color(QPalette.Link).name()}; border: none;")
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
        self.right_arrow_button.setStyleSheet(f"background-color: {self.palette().color(QPalette.Link).name()}; border: none;")
        self.right_arrow_button.clicked.connect(self.scroll_right)
        navigation_layout.addWidget(self.right_arrow_button)

        self.main_content_layout.addWidget(navigation_frame)

        self.update_safe_area_size()
        self.apply_text_size()
        self.update_tool_button_visibility()
        self.resizeEvent = self.update_tool_button_visibility

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()

        name_label = QLabel(tool_name)
        name_label.setFont(self.inter_extra_bold_font)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(self.inter_regular_font)
        description_label.setAlignment(Qt.AlignCenter)

        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)

        button.clicked.connect(lambda: self.tool_selected(tool_name))
        return button

    # ... (Other methods remain unchanged)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())import sys
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
        
        self.apply_theme()

    def apply_theme(self):
        theme = self.config.get_theme()
        palette = QPalette()
        
        if theme == "dark":
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
        else:
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, Qt.white)
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
            palette.setColor(QPalette.HighlightedText, Qt.white)

        # Add the custom accent color
        accent_color = QColor("#4f86f7")
        palette.setColor(QPalette.Link, accent_color)

        self.setPalette(palette)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {palette.color(QPalette.Window).name()};
                color: {palette.color(QPalette.WindowText).name()};
            }}
            QPushButton {{
                border: 5px solid {palette.color(QPalette.Link).name()};
                color: {palette.color(QPalette.ButtonText).name()};
                border-radius: 15px;
                padding: 10px;
                min-width: 200px;
                min-height: 100px;
                margin: 10px;
                background-color: {palette.color(QPalette.Button).name()};
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {palette.color(QPalette.Link).darker().name()};
                background-color: {palette.color(QPalette.Link).darker().name()};
            }}
            QLabel {{
                color: {palette.color(QPalette.WindowText).name()};
                background-color: transparent;
            }}
            QScrollArea {{
                background-color: {palette.color(QPalette.Window).name()};
            }}
            QFrame {{
                background-color: {palette.color(QPalette.Window).name()};
            }}
        """)

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
        self.left_arrow_button.setStyleSheet(f"background-color: {self.palette().color(QPalette.Link).name()}; border: none;")
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
        self.right_arrow_button.setStyleSheet(f"background-color: {self.palette().color(QPalette.Link).name()}; border: none;")
        self.right_arrow_button.clicked.connect(self.scroll_right)
        navigation_layout.addWidget(self.right_arrow_button)

        self.main_content_layout.addWidget(navigation_frame)

        self.update_safe_area_size()
        self.apply_text_size()
        self.update_tool_button_visibility()
        self.resizeEvent = self.update_tool_button_visibility

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()

        name_label = QLabel(tool_name)
        name_label.setFont(self.inter_extra_bold_font)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(self.inter_regular_font)
        description_label.setAlignment(Qt.AlignCenter)

        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)

        button.clicked.connect(lambda: self.tool_selected(tool_name))
        return button

    # ... (Other methods remain unchanged)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
