import sys
import qtawesome as qta
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea, QMessageBox, QSplitter, QFrame, QStackedWidget, QLineEdit, QGridLayout, QSizePolicy
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer 

from tools.subtitle_converter import SubtitleConverter
from tools.subtitle_shifter import SubtitleShifter
from assets.modules.side_panel import SidePanel
from assets.modules.settings import Settings
from assets.modules.config import Config
from assets.modules.custom_window_bar import CustomWindowBar  # Import the CustomWindowBar
from assets.modules.notification_bar import NotificationBar  # Import the NotificationBar

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.tab_contents = QStackedWidget()
        self.setMouseTracking(True)
        
        self.init_ui()

        self.refresh_settings()
        
    def init_ui(self):
        self.setWindowTitle("SRT Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.edge_threshold = 10
        self.setWindowFlags(Qt.FramelessWindowHint)

        QFontDatabase.addApplicationFont("assets/fonts/Inter-Regular.otf")
        QFontDatabase.addApplicationFont("assets/fonts/Inter-ExtraBold.otf")
        self.inter_regular_font = QFont("Inter Regular")
        self.inter_extra_bold_font = QFont("Inter ExtraBold")

        self.active_categories = set()
        self.category_buttons = {}

        self.apply_theme()

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.config = Config(source="MainWindow")
        self.main_menu_active = True
        self.experimental_tools_enabled = self.config.get_experimental_tools_enabled()
        self.experimental_tools_enabled = False

        self.custom_window_bar = CustomWindowBar(self, self.app)
        self.layout.addWidget(self.custom_window_bar)

        self.custom_window_bar.setup_initial_tabs()  # Add this line to create initial tabs
        
        self.tab_contents = QStackedWidget()
        self.layout.addWidget(self.tab_contents)

        self.side_panel = SidePanel(self, self.open_settings)
        self.side_panel.setVisible(False)
        self.side_panel.setFont(self.inter_regular_font)
        
        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content.setLayout(self.main_content_layout)
        
        self.top_bar = QHBoxLayout()
        self.top_bar_added = False
        self.menu_button = None

        self.create_new_tab_content()

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

        # Store reference to the FIRST splitter
        if not hasattr(self, 'splitter'):
            self.splitter = new_splitter  # Maintain reference for initial tab

        # Replicate the main menu layout in the new tab
        self.main_menu(new_main_content_layout)

    def remove_tab_content(self, index):
        widget = self.tab_contents.widget(index)
        if widget is not None:
            self.tab_contents.removeWidget(widget)
            widget.deleteLater()  # Clean up the widget

    def display_tab_content(self, index):
        self.tab_contents.setCurrentIndex(index)

    def create_tool_button(self, tool_name, tool_description, categories):

        # Get the actual description from the tuple if needed
        if isinstance(tool_description, tuple):
            tool_description = tool_description[0]
        
        is_experimental = "experimental" in categories
        button = QPushButton()
        button.setFixedSize(300, 200)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        palette = self.app.palette()
        background_color = palette.color(QPalette.Base).name()
        border_color = palette.color(QPalette.Highlight).name()
        button_color = palette.color(QPalette.Button).name()
        button_text_color = palette.color(QPalette.ButtonText).name()
        text_color = palette.color(QPalette.ButtonText).name()
        hover_background_color = palette.color(QPalette.Highlight).name()
        hover_border_color = palette.color(QPalette.Highlight).darker().name()

        button.setStyleSheet(f"""
            QPushButton {{
                border: 5px solid {border_color};
                color: rgba(255, 255, 255, 0);
                border-radius: 15px;
                padding: 10px;
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
        name_label.setFont(QFont("Inter ExtraBold", font_size +10, QFont.Bold))
        name_label.setStyleSheet(f"color: {border_color}; background-color: transparent;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Inter Regular", font_size -18))
        description_label.setStyleSheet(f"color: {text_color}; background-color: transparent;")
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)

        button_layout = QVBoxLayout(button)
        button_layout.addWidget(name_label)
        button_layout.addWidget(description_label)

        button.clicked.connect(lambda: self.tool_selected(tool_name))
        button.setVisible(self.experimental_tools_enabled or not is_experimental)
        return button

    def main_menu(self, layout=None):
        # Get the current main content layout for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()

            self.main_content_layout = main_content_layout

            self.main_menu_active = True

            # Clear the existing layout
            for i in reversed(range(main_content_layout.count())):
                widget = main_content_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Add the top bar with the menu button
            top_bar_widget = QWidget()
            self.top_bar = QHBoxLayout(top_bar_widget)
            self.top_bar.setContentsMargins(0, 0, 0, 0)
            
            self.menu_button = QPushButton()
            menu_icon = qta.icon('fa.bars')
            self.menu_button.setIcon(menu_icon)
            self.menu_button.setFixedSize(30, 30)
            self.menu_button.setStyleSheet("color: {button_text_color}; background-color: transparent; border: none; border-radius: 3px;")
            self.menu_button.clicked.connect(self.toggle_side_panel)

            self.search_field = QLineEdit()
            self.search_field.setPlaceholderText("Search tools...")
            self.search_field.setFixedWidth(700)
            
            palette = self.app.palette()
            text_color = palette.color(QPalette.Text).name()
            bg_color = palette.color(QPalette.Base).name()
            placeholder_color = palette.color(QPalette.PlaceholderText).name()
            button_color = palette.color(QPalette.Button).name()
            button_text_color = palette.color(QPalette.ButtonText).name()

            search_icon = qta.icon('fa5s.search', color=text_color)
            self.search_field.addAction(search_icon, QLineEdit.LeadingPosition)
            self.search_field.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {button_color};
                    color: {button_text_color};
                    border: 2px solid {palette.color(QPalette.Highlight).name()};
                    border-radius: 20px;
                    padding: 5px 5px 5px 35px;
                }}
                QLineEdit::placeholder {{
                    color: {palette.color(QPalette.PlaceholderText).name()};
                }}
            """)

            self.search_field.textChanged.connect(self.filter_tools)

            self.top_bar.addWidget(self.menu_button, alignment=Qt.AlignLeft)
            self.top_bar.addWidget(self.search_field, alignment=Qt.AlignRight)
            main_content_layout.addWidget(top_bar_widget)

            # Add the NotificationBar below the top bar
            self.notification_bar = NotificationBar(self)
            if hasattr(self, 'notification_bar'):
                main_content_layout.addWidget(self.notification_bar)
            
            if layout is None:
                container_layout = QVBoxLayout()
            else:
                container_layout = layout

            # Create main horizontal layout (categories + scroll area)
            main_h_layout = QHBoxLayout()
            main_h_layout.setContentsMargins(20, 20, 20, 20)
            main_h_layout.setSpacing(30)

            # Create category buttons panel (left side)
            category_panel = QWidget()
            category_layout = QVBoxLayout(category_panel)
            category_layout.setContentsMargins(0, 0, 0, 0)
            category_layout.setSpacing(8)

            # Add this line before the tools loop
            self.tool_buttons = []

            tools = [
                ("Longer Appearance SRT", "Increase the duration each subtitle appears.", ["appearance", "timing"]),
                ("Merge SRT Files", "Combine multiple SRT files into one.", ["merge"]),
                ("Subtitle Converter", "Convert subtitles between different formats.", ["conversion"]),
                ("Subtitle Shifter", "Shift subtitles by milliseconds.", ["timing"]),
                ("Multilingual Merge", "Merge subtitles in different languages with colors.", ["merge", "translation", "experimental"]),
                ("Coming Soon", "More tools will be added in the future.", ["other"])
            ]
            tools_dict = {name: (desc, categories) for name, desc, categories in tools}

            self.tools = tools
            
            # Get unique categories
            all_categories = set()
            for tool in tools:
                all_categories.update(tool[2])

            for category in sorted(all_categories):
                btn = QPushButton(category.upper())
                btn.setCheckable(True)

                highlight_color = self.app.palette().color(QPalette.Highlight).name()
                base_color = self.app.palette().color(QPalette.Base).name()
                text_color = self.app.palette().color(QPalette.Text).name()
                highlight_text_color = self.app.palette().color(QPalette.HighlightedText).name()
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border: 2px solid {highlight_color};
                        border-radius: 15px;
                        padding: 8px;
                        margin: 4px;
                        background-color: {base_color};
                        color: {text_color};
                    }}
                    QPushButton:checked {{
                        background-color: {highlight_color};
                        color: {highlight_text_color};
                    }}
                """)
                btn.clicked.connect(self.update_category_filters)
                self.category_buttons[category] = btn
                category_layout.addWidget(btn)

            category_layout.addStretch()
            main_h_layout.addWidget(category_panel, stretch=1)

            navigation_frame = QFrame()
            navigation_layout = QHBoxLayout(navigation_frame)
            navigation_layout.setContentsMargins(0, 0, 0, 0)

            # Create a main scroll widget to hold all sections
            scroll_content = QWidget()
            main_scroll_layout = QVBoxLayout(scroll_content)
            main_scroll_layout.setContentsMargins(20, 20, 20, 20)
            main_scroll_layout.setSpacing(30)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(scroll_content)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.scroll_content = scroll_content
            self.scroll_area = scroll_area

            most_used_label = QLabel("Most Used Tools")
            most_used_label.setFont(self.inter_extra_bold_font)
            most_used_label.setStyleSheet("color: palette(WindowText);")
            main_scroll_layout.addWidget(most_used_label)
            self.most_used_label = most_used_label

            most_used_widget = QWidget()
            most_used_layout = QHBoxLayout(most_used_widget)
            most_used_layout.setContentsMargins(0, 0, 0, 0)
            self.most_used_widget = most_used_widget

            self.tool_usage = self.config.get_tool_usage()
            has_tool_usage = any(self.tool_usage.values())
            
            if has_tool_usage:
                for tool_name in sorted(self.tool_usage, key=lambda x: -self.tool_usage[x])[:3]:
                    btn = self.create_tool_button(tool_name, tools_dict.get(tool_name, ("Popular tool", []))[0], tools_dict.get(tool_name, ("Popular tool", []))[1])
                    most_used_layout.addWidget(btn)
                main_scroll_layout.addWidget(most_used_widget)
            else:
                most_used_label.hide()
                most_used_widget.hide()

            # Add Recent section
            recent_label = QLabel("Recent Tools")
            recent_label.setFont(self.inter_extra_bold_font)
            recent_label.setStyleSheet("color: palette(WindowText);")
            main_scroll_layout.addWidget(recent_label)
            self.recent_label = recent_label

            recent_widget = QWidget()
            recent_layout = QHBoxLayout(recent_widget)
            recent_layout.setContentsMargins(0, 0, 0, 0)
            self.recent_widget = recent_widget

            self.recent_tools = self.config.get_recent_tools()
            has_recent_tools = len(self.recent_tools) > 0  # Check if there are any recent tools
            
            if has_recent_tools:
                for tool_name in self.recent_tools[:3]:
                    btn = self.create_tool_button(tool_name, tools_dict.get(tool_name, ("Recently used tool", []))[0], tools_dict.get(tool_name, ("Recently used tool", []))[1])               
                    recent_layout.addWidget(btn)
                main_scroll_layout.addWidget(recent_widget)
            else:
                recent_label.hide()
                recent_widget.hide()

            all_tools_label = QLabel("All Tools")
            all_tools_label.setFont(self.inter_extra_bold_font)
            all_tools_label.setStyleSheet("color: palette(WindowText);")
            main_scroll_layout.addWidget(all_tools_label)
            
            # Create a widget to hold the grid
            all_tools_widget = QWidget()
            all_tools_grid = QGridLayout(all_tools_widget)
            all_tools_grid.setHorizontalSpacing(20)
            all_tools_grid.setVerticalSpacing(20)
            all_tools_grid.setColumnStretch(0, 0)  # Prevent column stretching
            all_tools_grid.setColumnStretch(1, 0)
            all_tools_grid.setColumnStretch(2, 0)
            all_tools_grid.setRowStretch(0, 0)     # Prevent row stretching
            all_tools_grid.setRowStretch(1, 0)
            columns = 3

            for index, tool in enumerate(tools):
                btn = self.create_tool_button(tool[0], tool[1], tool[2])
                row = index // columns
                col = index % columns
                all_tools_grid.addWidget(btn, row, col)
                self.tool_buttons.append(btn)
            main_scroll_layout.addWidget(all_tools_widget)

            scroll_area.setWidget(scroll_content)
            main_h_layout.addWidget(self.scroll_area, stretch=4)
            main_content_layout.addLayout(main_h_layout)

            self.apply_text_size()
            self.apply_theme()
            self.update_tool_button_visibility()

    def on_tag_selected(self):
        self.most_used_label.hide()
        self.most_used_widget.hide()
        self.recent_label.hide()
        self.recent_widget.hide()

    def on_tag_deselected(self):
        self.most_used_label.show()
        self.most_used_widget.show()
        self.recent_label.show()
        self.recent_widget.show()

    def tool_selected(self, tool_name):
        self.tool_usage[tool_name] = self.tool_usage.get(tool_name, 0) + 1

        # Update recent tools
        if tool_name in self.recent_tools:
            self.recent_tools.remove(tool_name)
        self.recent_tools.insert(0, tool_name)
        if len(self.recent_tools) > 3:
            self.recent_tools = self.recent_tools[:3]

        self.config.set_tool_usage(self.tool_usage)
        self.config.set_recent_tools(self.recent_tools)

        self.notification_bar.add_notification("⏰", f"Reminder: You last used the {tool_name} tool just now.")


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
            elif tool_name == "Multilingual Merge":
                from tools.multilingual_tool import MultilingualTool
                tool_widget = MultilingualTool(parent=main_content, back_callback=self.main_menu)
                self.load_tool(tool_widget, main_content_layout)
            else:
                QMessageBox.information(self, "Coming Soon", "This feature is coming soon!")
                return

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def load_tool(self, tool_widget, layout):
        self.main_menu_active = False

            # Clear the existing layout
        while layout.count():
            child = layout.takeAt(0)  # Remove items sequentially
            if child.widget():
                child.widget().deleteLater()  # Properly destroy widgets
            elif child.layout():
                # Recursively clear nested layouts (if any exist)
                self.clear_layout(child.layout())
                
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

            settings_widget.experimental_tools_toggled.connect(self.toggle_experimental_tools)

            # Load the settings widget into the current tab's main content layout
            self.load_tool(settings_widget, main_content_layout)

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
        print("refreshing the settings")
        self.apply_text_size()  # Update text size
        self.apply_theme()  # Update theme)
        self.toggle_experimental_tools(self.experimental_tools_enabled)

        self.custom_window_bar.current_palette()
        self.custom_window_bar.update_colors()
        self.side_panel.current_palette()
        self.side_panel.update_colors()

    def update_tool_button_visibility(self, event=None):
        if self.main_menu_active and self.tool_buttons:
            # Only handle automatic visibility if there's no search filter
            if not self.search_field.text():
                container_width = self.scroll_area.width()
                button_width = 220
                visible_buttons = max(1, container_width // button_width)
                for i, button in enumerate(self.tool_buttons):
                    button.setVisible(i < visible_buttons)

                for button in self.tool_buttons:
                    button.setVisible(True)

    def update_category_filters(self):
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            # Get the main content widget for the current tab
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()
            
            self.active_categories.clear()
            for category, btn in self.category_buttons.items():
                if btn.isChecked():
                    self.active_categories.add(category)
                    
            if self.active_categories:
                self.on_tag_selected()
            else:
                self.on_tag_deselected()
            self.filter_tools(self.search_field.text())

    def toggle_experimental_tools(self, enabled):
        """Toggle the visibility of experimental tools."""
        self.experimental_tools_enabled = enabled
        self.filter_tools(self.search_field.text())

    def filter_tools(self, search_text):
        if not hasattr(self, 'search_field') or self.search_field is None:
            return  # Exit if search_field is not available
        search_text = search_text.lower()
        
        if search_text.strip():  # Check if there is any non-whitespace text
            self.on_tag_selected()
        else:
            self.on_tag_deselected()
            
        for index, tool in enumerate(self.tools):
            button = self.tool_buttons[index]
            name = tool[0].lower()
            desc = tool[1].lower()
            categories = set(tool[2])

            is_experimental = "experimental" in categories

            text_match = search_text in name or search_text in desc
            category_match = not self.active_categories or bool(categories & self.active_categories)
            visible = text_match and category_match and (self.experimental_tools_enabled or not is_experimental)
            
            button.setVisible(visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())
