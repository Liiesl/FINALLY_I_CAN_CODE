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

        # Create a new main content widget for the tab
        new_main_content = QWidget()
        new_main_content_layout = QVBoxLayout(new_main_content)
        new_main_content.setLayout(new_main_content_layout)

        # Add the side panel and main content to the splitter
        new_splitter.addWidget(new_side_panel)
        new_splitter.addWidget(new_main_content)
        new_splitter.setSizes([0, 1])  # Initially hide the side panel
    
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

    def main_menu(self, layout=None):
        # Get the current main content layout for the active tab
        current_splitter = self.tab_contents.currentWidget()
        if current_splitter is not None:
            main_content = current_splitter.widget(1)  # Main content is the second widget in the splitter
            main_content_layout = main_content.layout()
            self.main_menu_active = True
            # Clear the existing layout
            self.clear_layout(main_content_layout)

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
            self.text_color = palette.color(QPalette.Text).name()
            self.background_color = palette.color(QPalette.Base).name()
            self.placeholder_color = palette.color(QPalette.PlaceholderText).name()
            self.button_color = palette.color(QPalette.Button).name()
            self.button_text_color = palette.color(QPalette.ButtonText).name()
            self.highlight_color = self.app.palette().color(QPalette.Highlight).name()
            self.base_color = self.app.palette().color(QPalette.Base).name()
            self.text_color = self.app.palette().color(QPalette.Text).name()
            self.highlight_text_color = self.app.palette().color(QPalette.HighlightedText).name()
            self.border_color = palette.color(QPalette.Highlight).name()
            self.button_color = palette.color(QPalette.Button).name()
            self.hover_background_color = palette.color(QPalette.Highlight).name()
            self.hover_border_color = palette.color(QPalette.Highlight).darker().name()
            
            search_icon = qta.icon('fa5s.search', color=self.text_color)
            self.search_field.addAction(search_icon, QLineEdit.LeadingPosition)
            self.search_field.setStyleSheet(f"""
                QLineEdit {{
                    background-color: {self.button_color};
                    color: {self.button_text_color};
                    border: 2px solid {self.highlight_color};
                    border-radius: 20px;
                    padding: 5px 5px 5px 35px;
                }}
                QLineEdit::placeholder {{
                    color: {self.placeholder_color};
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
    
            # Add categories and tools dynamicallym
            self.add_categories_and_tools(main_content_layout)
    
            # Apply theme and text size
            self.apply_text_size()
            self.apply_theme()
            self.update_tool_button_visibility()

    def add_categories_and_tools(self, layout):
        # Create main horizontal layout (categories + scroll area)
        main_h_layout = QHBoxLayout()
        main_h_layout.setContentsMargins(20, 20, 20, 20)
        main_h_layout.setSpacing(30)

        # Create category buttons panel (left side)
        category_panel = QWidget()
        category_layout = QVBoxLayout(category_panel)
        category_layout.setContentsMargins(0, 0, 0, 0)
        category_layout.setSpacing(8)

        # Initialize tool buttons
        self.tool_buttons = []

        # Define tools
        tools = [
            ("Longer Appearance SRT", "Increase the duration each subtitle appears.", ["appearance", "timing"]),
            ("Merge SRT Files", "Combine multiple SRT files into one.", ["merge"]),
            ("Subtitle Converter", "Convert subtitles between different formats.", ["conversion"]),
            ("Subtitle Shifter", "Shift subtitles by milliseconds.", ["timing"]),
            ("Multilingual Merge", "Merge subtitles in different languages with colors.", ["merge", "translation"]),
            ("Coming Soon", "More tools will be added in the future.", ["other"])
        ]
        tools_dict = {name: (desc, categories) for name, desc, categories in tools}

        self.tools = tools
        self.tools_dict = tools_dict

        # Get unique categories
        all_categories = set()
        for tool in tools:
            all_categories.update(tool[2])

        # Create category buttons
        for category in sorted(all_categories):
            btn = QPushButton(category.upper())
            btn.setCheckable(True)
            # Apply dynamic text size based on app's configuration
            self.config = Config(source="MainWindow")
            text_size = self.config.get_text_size()
            font_size = {
                "small": 10,
                "default": 18,
                "large": 26,
                "huge": 34
            }.get(text_size, 26) # Default to 26 if text size is unknown
            btn.setFont(QFont("Inter Regular", font_size))
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid {self.highlight_color};
                    border-radius: 15px;
                    padding: 8px;
                    margin: 4px;
                    background-color: {self.base_color};
                    color: {self.text_color};
                }}
                QPushButton:checked {{
                    background-color: {self.highlight_color};
                    color: {self.highlight_text_color};
                }}
            """)
            btn.clicked.connect(self.update_category_filters)
            self.category_buttons[category] = btn
            category_layout.addWidget(btn)

        category_layout.addStretch()
        main_h_layout.addWidget(category_panel, stretch=1)

        # Create scroll area for tools
        scroll_content = QWidget()
        main_scroll_layout = QVBoxLayout(scroll_content)
        main_scroll_layout.setContentsMargins(20, 20, 20, 20)
        main_scroll_layout.setSpacing(30)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_content)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area = scroll_area

        # Add tools dynamically
        self.add_tool_sections(main_scroll_layout, tools)

        main_h_layout.addWidget(self.scroll_area, stretch=4)
        layout.addLayout(main_h_layout)

    def add_tool_sections(self, layout, tools):
        # Add Most Used Tools section
        most_used_label = QLabel("Most Used Tools")
        most_used_label.setFont(self.inter_extra_bold_font)
        layout.addWidget(most_used_label)
        self.most_used_label = most_used_label

        most_used_widget = QWidget()
        most_used_layout = QHBoxLayout(most_used_widget)
        most_used_layout.setContentsMargins(0, 0, 0, 0)
        self.most_used_widget = most_used_widget

        self.tool_usage = self.config.get_tool_usage()
        has_tool_usage = any(self.tool_usage.values())

        if has_tool_usage:
            for tool_name in sorted(self.tool_usage, key=lambda x: -self.tool_usage[x])[:3]:
                button, _ = self.create_tool_button(tool_name, self.tools_dict.get(tool_name, ("Popular tool", []))[0], self.tools_dict.get(tool_name, ("Popular tool", []))[1])
                most_used_layout.addWidget(button)
            layout.addWidget(most_used_widget)
        else:
            most_used_label.hide()
            most_used_widget.hide()

        # Add Recent Tools section
        recent_label = QLabel("Recent Tools")
        recent_label.setFont(self.inter_extra_bold_font)
        layout.addWidget(recent_label)
        self.recent_label = recent_label

        recent_widget = QWidget()
        recent_layout = QHBoxLayout(recent_widget)
        recent_layout.setContentsMargins(0, 0, 0, 0)
        self.recent_widget = recent_widget

        self.recent_tools = self.config.get_recent_tools()
        has_recent_tools = len(self.recent_tools) > 0

        if has_recent_tools:
            for tool_name in self.recent_tools[:3]:
                button, _ = self.create_tool_button(tool_name, self.tools_dict.get(tool_name, ("Recently used tool", []))[0], self.tools_dict.get(tool_name, ("Recently used tool", []))[1])
                recent_layout.addWidget(button)
            layout.addWidget(recent_widget)
        else:
            recent_label.hide()
            recent_widget.hide()

        # Add All Tools section
        all_tools_label = QLabel("All Tools")
        all_tools_label.setFont(self.inter_extra_bold_font)
        layout.addWidget(all_tools_label)

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
            button, _ = self.create_tool_button(tool[0], tool[1], tool[2])
            row = index // columns
            col = index % columns
            all_tools_grid.addWidget(button, row, col)
            self.tool_buttons.append(button)

        layout.addWidget(all_tools_widget)

    def create_tool_button(self, tool_name, tool_description, categories):
        # Create the button
        button = QPushButton()
        button.setFixedSize(250, 150)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.setStyleSheet(f"""
            QPushButton {{
                border: rgba(255, 255, 255, 0);
                color: rgba(255, 255, 255, 0);
                border-radius: 15px;
                padding: 10px;
                margin: 10px;
                background-color: rgba(255, 255, 255, 0);
                text-align: center;
            }}
            QPushButton:hover {{
                border-color: {self.hover_border_color};
                background-color: {self.hover_background_color};
            }}
        """)
        # Define a placeholder emoji for each tool (you can customize these later)
        emojis = {
            "Longer Appearance SRT": "⏳",
            "Merge SRT Files": "✨",
            "Subtitle Converter": "🔄",
            "Subtitle Shifter": "➡️",
            "Multilingual Merge": "🌍",
            "Coming Soon": "🚀"
        }
    
        # Get the emoji for the current tool
        emoji = emojis.get(tool_name, "❓")  # Default to question mark if no emoji is defined
    
        # Combine the emoji and tool name into a single label
        combined_text = f"{emoji} {tool_name}"
        text_size = self.config.get_text_size()
        font_size = {
            "small": 18,
            "default": 26,
            "large": 34,
            "huge": 42
        }.get(text_size, 26)
    
        # Create the combined label
        combined_label = QLabel(combined_text)
        combined_label.setFont(QFont("Inter ExtraBold", font_size, QFont.Bold))
        combined_label.setStyleSheet(f"color: {self.text_color}; background-color: transparent;")
        combined_label.setAlignment(Qt.AlignCenter)
        combined_label.setWordWrap(True)  # Enable text wrapping

        # Layout for the button
        button_layout = QVBoxLayout(button)
        button_layout.addWidget(combined_label)
        button_layout.addStretch()
        button_layout.setAlignment(Qt.AlignCenter)
    
        # Create the description label (hidden by default)
        description_label = QLabel(tool_description)
        description_label.setFont(QFont("Inter Regular", font_size))
        description_label.setStyleSheet(f"""
            color: {self.text_color};
            background-color: {self.base_color};
            padding: 10px;
            border: 2px solid {self.highlight_color};
            border-radius: 10px;
        """)
        description_label.setWordWrap(True)
        description_label.hide()  # Hide initially
        description_label.setFixedSize(300, 200)
        description_label.setParent(self)  # Set MainWindow as the parent
    
        # Show description on hover
        def show_description(event):
            # Get the global position of the button
            button_global_pos = button.mapToGlobal(QPoint(0, 0))
            
            # Get the size of the button and description label
            button_size = button.size()
            description_size = description_label.size()
            
            # Get the current window geometry (global coordinates)
            window_geometry = self.geometry()
            window_top_left = self.mapToGlobal(QPoint(0, 0))
            window_bottom_right = window_top_left + QPoint(window_geometry.width(), window_geometry.height())
            
            # Calculate potential positions for the description label
            pos_right = button_global_pos + QPoint(button_size.width(), 0)  # To the right of the button
            pos_left = button_global_pos - QPoint(description_size.width(), 0)  # To the left of the button
            
            # Ensure the description label stays within the window bounds
            if pos_right.x() + description_size.width() <= window_bottom_right.x():
                # If there's enough space to the right, place it to the right
                final_pos = pos_right
            elif pos_left.x() >= window_top_left.x():
                # If there's enough space to the left, place it to the left
                final_pos = pos_left
            else:
                # If neither side has enough space, default to the left
                final_pos = pos_left
            
            # Adjust vertical position to align with the button and stay within window bounds
            final_pos.setY(button_global_pos.y())  # Align top edge with the button
            
            # Check if the description label fits vertically within the window
            if final_pos.y() + description_size.height() > window_bottom_right.y():
                # If it doesn't fit below, move it above the button
                final_pos.setY(button_global_pos.y() - description_size.height())
            
            if final_pos.y() < window_top_left.y():
                # If it doesn't fit above, move it back below the button
                final_pos.setY(button_global_pos.y())
            
            # Move and show the description label
            description_label.move(final_pos)
            description_label.show()
            
        def hide_description(event):
            description_label.hide()
    
        # Assign custom event handlers for hover events
        button.enterEvent = lambda event: show_description(event)  # On hover enter
        button.leaveEvent = lambda event: hide_description(event)  # On hover leave
    
        # Connect the tool selection action
        button.clicked.connect(lambda: self.tool_selected(tool_name))
    
        return button, description_label
    
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
                msg_box = QMessageBox()
                msg_box.setText("More tools will be added soon!")
                msg_box.setWindowTitle("Coming Soon!")
                msg_box.setStyleSheet("""
                QMessageBox {
                color: black;
                }
                QMessageBox QLabel {
                color: black;
                }
                QMessageBox QPushButton {
                color: black;
                }
                """)
                msg_box.exec_()
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
        self.apply_theme()  # Update theme

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

    def filter_tools(self, search_text):
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

            text_match = search_text in name or search_text in desc
            category_match = not self.active_categories or bool(categories & self.active_categories)
            visible = text_match and category_match
            button.setVisible(visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())
