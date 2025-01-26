import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QSplitter, QFrame, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation

from tools.subtitle_converter import SubtitleConverter
from tools.subtitle_shifter import SubtitleShifter
from assets.modules.side_panel import SidePanel
from assets.modules.settings import Settings
from assets.modules.config import Config
from assets.modules.custom_window_bar import CustomWindowBar  # Import the CustomWindowBar

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.tab_contents = QStackedWidget()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove native window bar
        self.setStyleSheet("background-color: {background_color};")

        QFontDatabase.addApplicationFont("assets/fonts/Inter-Regular.otf")
        QFontDatabase.addApplicationFont("assets/fonts/Inter-ExtraBold.otf")
        
        self.inter_regular_font = QFont("Inter Regular")
        self.inter_extra_bold_font = QFont("Inter ExtraBold")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.config = Config(source="MainWindow")
        self.main_menu_active = True

        self.menu_button = None
        self.top_bar = QHBoxLayout()
        self.top_bar_added = False

        self.custom_window_bar = CustomWindowBar(self, self.app)
        self.layout.addWidget(self.custom_window_bar)

        self.tab_contents = QStackedWidget()
        self.layout.addWidget(self.tab_contents)

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

        self.tab_contents.addWidget(self.splitter)
        
        self.top_bar_added = False

        self.create_new_tab_content()

        self.apply_theme()

    def create_new_tab_content(self):
        # Create a new splitter for the tab
        new_splitter = QSplitter(Qt.Horizontal)
    
        # Create a new side panel for the tab
        new_side_panel = SidePanel(self, self.open_settings)
        new_side_panel.setVisible(False)
        new_side_panel.setFont(self.inter_regular_font)
    
        # Create a new main content widget for the tab
        new_main_content = QWidget()
        new_main_content_layout = QVBoxLayout(new_main_content)
        new_main_content.setLayout(new_main_content_layout)

        # Initialize top_bar and menu_button for the new tab
        self.top_bar_added = False
    
        # Add the side panel and main content to the splitter
        new_splitter.addWidget(new_side_panel)
        new_splitter.addWidget(new_main_content)
        new_splitter.setSizes([0, 1])
    
        # Add the splitter to the tab contents
        self.tab_contents.addWidget(new_splitter)
        self.tab_contents.setCurrentWidget(new_splitter)
    
        # Replicate the main menu layout in the new tab
        self.replicate_main_menu(new_main_content_layout)
    
    def replicate_main_menu(self, layout):
        # Use the new method to create the main menu layout
        self.top_bar_added = False
        self.main_menu(layout)

    def remove_tab_content(self, index):
        widget = self.tab_contents.widget(index)
        if widget is not None:
            self.tab_contents.removeWidget(widget)
            widget.deleteLater()  # Clean up the widget

    def display_tab_content(self, index):
        self.tab_contents.setCurrentIndex(index)

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
            palette.setColor(QPalette.Button, QColor(33, 35, 41))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
            palette.setColor(QPalette.HighlightedText, Qt.white)
        elif theme == "light":
            palette.setColor(QPalette.Window, Qt.white)
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(220, 220, 220))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor(75, 110, 175))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
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

        self.app.setPalette(palette)
        self.custom_window_bar.apply_theme(theme)

    def create_tool_button(self, tool_name, tool_description):
        button = QPushButton()

        palette = self.app.palette()
        background_color = palette.color(QPalette.Base).name()
        border_color = palette.color(QPalette.Highlight).name()
        text_color = palette.color(QPalette.ButtonText).name()
        hover_background_color = palette.color(QPalette.Highlight).name()
        hover_border_color = palette.color(QPalette.Highlight).darker().name()

        button.setStyleSheet(f"""
            QPushButton {{
                border: 5px solid {border_color};
                color: rgba(255, 255, 255, 0);
                border-radius: 15px;
                padding: 10px;
                min-width: 300px;
                min-height: 400px;
                margin: 10px;
                background-color: {background_color};
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {hover_border_color};
                background-color: {hover_background_color};
            }}
        """)

        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        name_label = QLabel(tool_name)
        name_label.setFont(QFont("Inter ExtraBold", font_size, QFont.Bold))
        name_label.setStyleSheet(f"color: {border_color}; background-color: transparent;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Inter Regular", font_size))
        description_label.setStyleSheet(f"color: {text_color}; background-color: transparent;")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)

        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)

        button.clicked.connect(lambda: self.tool_selected(tool_name))
        return button
    
    def main_menu(self, layout=None):
        self.main_menu_active = True

        target_layout = layout if layout is not None else self.main_content_layout

        if not hasattr(self, 'top_bar') or self.top_bar is None:
            print("Reinitializing self.top_bar")
            self.top_bar = QHBoxLayout()

        for i in reversed(range(target_layout.count())):
            widget = self.main_content_layout.itemAt(i).widget()
            if widget is not None and item.layout() is not self.top_bar:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    target_layout.removeItem(item)
                    
        if self.menu_button is None:
            self.menu_button = QPushButton()
            menu_icon = qta.icon('fa.bars')
            self.menu_button.setIcon(menu_icon)
            self.menu_button.setFixedSize(30, 30)
            self.menu_button.setStyleSheet("color: {button_text_color}; background-color:{button_color}; border: none; border-radius: 3px;")
            self.menu_button.clicked.connect(self.toggle_side_panel)
            self.top_bar.addWidget(self.menu_button, alignment=Qt.AlignLeft)

        if not self.top_bar_added:
            print("Inserting self.top_bar into target_layout")
            target_layout.insertLayout(0, self.top_bar)
            if layout is not None:
                layout.parent().top_bar_added = True
            else:
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
        self.left_arrow_button.setFixedSize(50, 75)
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
        self.right_arrow_button.setFixedSize(50, 75)
        self.right_arrow_button.setStyleSheet("background-color: #4f86f7; border: none;")
        self.right_arrow_button.clicked.connect(self.scroll_right)
        navigation_layout.addWidget(self.right_arrow_button)

        target_layout.addWidget(navigation_frame)

        if layout is None:
            self.update_safe_area_size()
            self.apply_text_size()
            self.update_tool_button_visibility()
            self.resizeEvent = self.update_tool_button_visibility

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
        settings_widget = Settings(parent=self.main_content, back_callback=self.main_menu, main_window=self)
        settings_widget.setFont(self.inter_regular_font)
        settings_widget.settings_saved.connect(self.apply_theme)
        self.load_tool(settings_widget)

    def update_safe_area_size(self):
        self.config = Config(source="MainWindow")
        safe_area_size = self.config.get_safe_area_size()
        self.main_content_layout.setContentsMargins(safe_area_size, safe_area_size, safe_area_size, safe_area_size)

    def apply_text_size(self):
        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)

        self.setStyleSheet(f"""
            * {{
                font-size: {font_size}px;
            }}
        """)

    def refresh_settings(self):
        self.update_safe_area_size()
        self.apply_text_size()
        self.apply_theme()

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

    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())
