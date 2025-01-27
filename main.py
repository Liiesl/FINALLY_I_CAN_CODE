import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QSplitter, QFrame, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint

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
        
        self.resize_edge = None  # Tracks which edge is being resized
        self.resize_handle_size = 5  # Size of the resize handle (smaller for better sensitivity)
        self.pressing = False  # Tracks if the mouse is pressed
        self.start = QPoint(0, 0)  # Tracks the initial mouse position



    def init_ui(self):
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
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
        
        self.top_bar = QHBoxLayout()
        self.top_bar_added = False
        self.menu_button = None
        
        self.create_new_tab_content()

        self.apply_theme()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start = self.mapToGlobal(event.pos())
            self.resize_edge = self.get_resize_edge(event.pos())

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.resize_edge:
                self.resize_window(event)
            else:
                self.move_window(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = False
            self.resize_edge = None

    def get_resize_edge(self, pos):
        rect = self.rect()
        handle_size = self.resize_handle_size

        if pos.x() <= handle_size and pos.y() <= handle_size:
            return 'top-left'
        elif pos.x() >= rect.width() - handle_size and pos.y() <= handle_size:
            return 'top-right'
        elif pos.x() <= handle_size and pos.y() >= rect.height() - handle_size:
            return 'bottom-left'
        elif pos.x() >= rect.width() - handle_size and pos.y() >= rect.height() - handle_size:
            return 'bottom-right'
        elif pos.x() <= self.resize_handle_size:
            return 'left'
        elif pos.x() >= rect.width() - self.resize_handle_size:
            return 'right'
        elif pos.y() <= self.resize_handle_size:
            return 'top'
        elif pos.y() >= rect.height() - self.resize_handle_size:
            return 'bottom'
        return None

    def resize_window(self, event):
        global_pos = self.mapToGlobal(event.pos())
        delta = global_pos - self.start
        self.start = global_pos

        geometry = self.geometry()
        if self.resize_edge == 'left':
            geometry.setLeft(geometry.left() + delta.x())
        elif self.resize_edge == 'right':
            geometry.setRight(geometry.right() + delta.x())
        elif self.resize_edge == 'top':
            geometry.setTop(geometry.top() + delta.y())
        elif self.resize_edge == 'bottom':
            geometry.setBottom(geometry.bottom() + delta.y())
        elif self.resize_edge == 'top-left':
            geometry.setTopLeft(geometry.topLeft() + delta)
        elif self.resize_edge == 'top-right':
            geometry.setTopRight(geometry.topRight() + delta)
        elif self.resize_edge == 'bottom-left':
            geometry.setBottomLeft(geometry.bottomLeft() + delta)
        elif self.resize_edge == 'bottom-right':
            geometry.setBottomRight(geometry.bottomRight() + delta)


        self.setGeometry(geometry)

    def update_cursor_shape(self, pos):
        edge = self.get_resize_edge(pos)
        if edge in ('left', 'right'):
            self.setCursor(Qt.SizeHorCursor)
        elif edge in ('top', 'bottom'):
            self.setCursor(Qt.SizeVerCursor)
        elif edge in ('top-left', 'bottom-right'):
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge in ('top-right', 'bottom-left'):
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def move_window(self, event):
        global_pos = self.mapToGlobal(event.pos())
        delta = global_pos - self.start
        self.start = global_pos
        self.move(self.pos() + delta)


    def create_new_tab_content(self):
        # Create a new splitter for the tab
        new_splitter = QSplitter(Qt.Horizontal)
    
        # Create a new side panel for the tab
        new_side_panel = SidePanel(self, self.open_settings)
        new_side_panel.setVisible(False)
        new_side_panel.setFont(self.inter_regular_font)
        
        self.top_bar = QHBoxLayout()
        self.top_bar_added = False
        self.menu_button = None
    
        # Create a new main content widget for the tab
        new_main_content = QWidget()
        new_main_content_layout = QVBoxLayout(new_main_content)
        new_main_content.setLayout(new_main_content_layout)
    
        # Add the side panel and main content to the splitter
        new_splitter.addWidget(new_side_panel)
        new_splitter.addWidget(new_main_content)
        new_splitter.setSizes([0, 1])
    
        # Add the splitter to the tab contents
        self.tab_contents.addWidget(new_splitter)
        self.tab_contents.setCurrentWidget(new_splitter)
    
        # Replicate the main menu layout in the new tab
        self.main_menu(new_main_content_layout)

    def remove_tab_content(self, index):
        widget = self.tab_contents.widget(index)
        if widget is not None:
            self.tab_contents.removeWidget(widget)
            widget.deleteLater()  # Clean up the widget

    def display_tab_content(self, index):
        self.tab_contents.setCurrentIndex(index)

    def apply_theme(self):
        self.config = Config(source="MainWindow")
        theme = self.config.get_theme()
        print(f"Applying theme: {theme}")
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
        self.setPalette(palette)
        self.update()

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
        # Get the current main content layout for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()

            self.main_menu_active = True

            # Clear the existing layout
            for i in reversed(range(main_content_layout.count())):
                widget = main_content_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Add the top bar with the menu button
            if not self.top_bar_added:
                # Add the top bar with the menu button
                self.top_bar = QHBoxLayout()
                self.menu_button = QPushButton()
                menu_icon = qta.icon('fa.bars')
                self.menu_button.setIcon(menu_icon)
                self.menu_button.setFixedSize(30, 30)
                self.menu_button.setStyleSheet("color: {button_text_color}; background-color:{button_color}; border: none; border-radius: 3px;")
                self.menu_button.clicked.connect(self.toggle_side_panel)
                self.top_bar.addWidget(self.menu_button, alignment=Qt.AlignLeft)
                main_content_layout.addLayout(self.top_bar)
                self.top_bar_added = True  # Mark the top bar as added
                
            # Add the tool buttons
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

            # Add navigation arrows
            navigation_frame = QFrame()
            navigation_layout = QHBoxLayout(navigation_frame)
            navigation_layout.setContentsMargins(0, 0, 0, 0)

            left_arrow_button = QPushButton()
            left_arrow_icon = qta.icon('fa.chevron-left')
            left_arrow_button.setIcon(left_arrow_icon)
            left_arrow_button.setFixedSize(50, 75)
            left_arrow_button.setStyleSheet("background-color: #4f86f7; border: none;")
            left_arrow_button.clicked.connect(self.scroll_left)
            navigation_layout.addWidget(left_arrow_button)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.tool_buttons_container)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_area = scroll_area
            navigation_layout.addWidget(scroll_area)

            right_arrow_button = QPushButton()
            right_arrow_icon = qta.icon('fa.chevron-right')
            right_arrow_button.setIcon(right_arrow_icon)
            right_arrow_button.setFixedSize(50, 75)
            right_arrow_button.setStyleSheet("background-color: #4f86f7; border: none;")
            right_arrow_button.clicked.connect(self.scroll_right)
            navigation_layout.addWidget(right_arrow_button)

            main_content_layout.addWidget(navigation_frame)

            self.update_safe_area_size()
            self.apply_text_size()
            self.apply_theme()
            self.update_tool_button_visibility()
            self.resizeEvent = self.update_tool_button_visibility

    def tool_selected(self, tool_name):
        # Get the current splitter for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            # Get the main content widget for the current tab
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()
    
            if tool_name == "Longer Appearance SRT":
                from tools.longer_appearance import LongerAppearanceSRT
                tool_widget = LongerAppearanceSRT(parent=main_content, back_callback=self.main_menu)
                tool_widget.setFont(self.inter_regular_font)
                self.load_tool(tool_widget, main_content_layout)
            elif tool_name == "Merge SRT Files":
                from tools.merge_srt import MergeSRT
                tool_widget = MergeSRT(parent=main_content, back_callback=self.main_menu)
                self.load_tool(tool_widget, main_content_layout)
            elif tool_name == "Subtitle Converter":
                tool_widget = SubtitleConverter(parent=main_content, back_callback=self.main_menu)
                self.load_tool(tool_widget, main_content_layout)
            elif tool_name == "Subtitle Shifter":
                tool_widget = SubtitleShifter(parent=main_content, back_callback=self.main_menu)
                self.load_tool(tool_widget, main_content_layout)
            else:
                QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")
    
    def load_tool(self, tool_widget, layout):
        self.main_menu_active = False
    
        # Clear the existing layout
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
    
        # Add the tool widget to the layout
        layout.addWidget(tool_widget)
        tool_widget.show()

    def toggle_side_panel(self):
        # Get the current splitter for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            side_panel = current_splitter.widget(0)  # Side panel is the first widget in the splitter
            if side_panel.isVisible():
                current_splitter.setSizes([0, 1])  # Hide the side panel
                side_panel.setVisible(False)
            else:
                side_panel.setVisible(True)
                current_splitter.setSizes([self.width() // 2, self.width() // 2])  # Show the side panel

    def open_settings(self, item=None):
        # Get the current splitter for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            # Get the main content widget for the current tab
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()
    
            # Create the settings widget
            settings_widget = Settings(parent=self.main_content, back_callback=self.main_menu, main_window=self)
            settings_widget.setFont(self.inter_regular_font)
            settings_widget.settings_saved.connect(self.apply_theme)
    
            # Load the settings widget into the current tab's main content layout
            self.load_tool(settings_widget, main_content_layout)
            
    def update_safe_area_size(self):
        self.config = Config(source="MainWindow")
        safe_area_size = self.config.get_safe_area_size()
        for i in range(self.tab_contents.count()):
            tab_widget = self.tab_contents.widget(i)
            if tab_widget:
                main_content = tab_widget.widget(1)  # Main content is the second widget in the splitter
                if main_content:
                    main_content_layout = main_content.layout()
                    if main_content_layout:
                        main_content_layout.setContentsMargins(
                            safe_area_size, safe_area_size, safe_area_size, safe_area_size
                        )
            
    def apply_text_size(self):
        self.config = Config(source="MainWindow")
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
        self.update_safe_area_size()  # Update safe area size
        self.apply_text_size()  # Update text size
        self.apply_theme()  # Update theme

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
