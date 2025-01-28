from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor
import qtawesome as qta

class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(False)  # Disable default close button
        
        palette = self.parent().palette()
        self.text_color = self.palette.color(QPalette.WindowText).name()
        self.background_color = self.palette.color(QPalette.Window).name()
        self.button_color = self.palette.color(QPalette.Button).name()
        self.button_text_color = self.palette.color(QPalette.ButtonText).name()
        self.highlight_color = self.palette.color(QPalette.Highlight).name()
        self.hover_color = self.palette.color(QPalette.Highlight).darker().name()

    def addTab(self, text):
        index = super().addTab(text)
        # Add a close button to all tabs except the first one
        if index != 0:
            self.setTabButton(index, QTabBar.RightSide, self.create_close_button(index))
        return index

    def create_close_button(self, index):
        close_button = QPushButton(qta.icon('fa.close'), '')
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.tabCloseRequested.emit(index))
        close_button.setStyleSheet("""
            QPushButton {
                color: {self.text_color};
                background: transparent;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 0.5);
            }
        """)
        return close_button

    def tabButton(self, index, button_type):
        # Override to remove the close button for the first tab
        if index == 0 and button_type == QTabBar.RightSide:
            return None
        return super().tabButton(index, button_type)


class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.start = QPoint(0, 0)
        self.pressing = False  # Track if the mouse is pressed
        self.resize_edge = None  # Track which edge is being resized
        self.resize_handle_size = 5  # Size of the resize handle (smaller for better sensitivity)

        palette = self.parent().palette()
        self.text_color = self.palette.color(QPalette.WindowText).name()
        self.background_color = self.palette.color(QPalette.Window).name()
        self.button_color = self.palette.color(QPalette.Button).name()
        self.button_text_color = self.palette.color(QPalette.ButtonText).name()
        self.highlight_color = self.palette.color(QPalette.Highlight).name()
        self.hover_color = self.palette.color(QPalette.Highlight).darker().name()
        
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(50)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Remove spacing between widgets
        self.setLayout(self.layout)

        self.create_tab_bar()
        self.create_buttons()

        # Add the first tab but hide it
        self.add_tab("Hidden Tab")
        self.tab_bar.setTabVisible(0, False)  # Hide the first tab

        # Create a new tab and make it visible
        self.add_tab("Subtl")  # This will be the visible tab

    def create_tab_bar(self):
        self.tab_bar = CustomTabBar(self)  # Use the custom tab bar
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        # Set the tab bar style
        self.tab_bar.setStyleSheet(f"""
            QTabBar::tab {{
                padding: 2px 10px;  /* Adjust padding to fit the title */
                margin: 0;          
                border: none;      
                background: {self.button_color};  /* Make the tab background transparent */
                color: {self.text_color};  /* Use the button text color */
            }}
            QTabBar::tab:selected {{
                background: {self.background_color};  /* Use the background color for the selected tab */
            }}
        """)

        self.layout.addWidget(self.tab_bar)

        # Add the "add tab" button directly to the right of the tabs
        self.new_tab_button = QPushButton(qta.icon('fa.plus'), '')
        self.new_tab_button.setFixedSize(50, 50)
        self.new_tab_button.clicked.connect(lambda: self.add_tab("Subtl"))  # Change tab name to "Subtl"

        # Set the "+" button style
        self.new_tab_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.button_text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 40px;  /* Increase font size for better visibility */
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }}
        """)
        self.layout.addWidget(self.new_tab_button)

        # Add a spacer to leave space between the tabs and the window buttons
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer)

    def create_buttons(self):
        self.min_button = QPushButton(qta.icon('fa.window-minimize'), '')
        self.min_button.setFixedSize(50, 50)
        self.min_button.clicked.connect(self.parent.showMinimized)

        # Set the minimize button style
        self.min_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 40px;  /* Increase font size for better visibility */
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }}
        """)
        self.layout.addWidget(self.min_button)

        self.max_button = QPushButton(qta.icon('fa.window-maximize'), '')
        self.max_button.setFixedSize(50, 50)
        self.max_button.clicked.connect(self.toggle_maximize_restore)

        # Set the maximize button style
        self.max_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 40px;  /* Increase font size for better visibility */
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }}
        """)
        self.layout.addWidget(self.max_button)

        self.close_button = QPushButton(qta.icon('fa.close'), '')
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.parent.close)

        # Set the close button style
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.text_color};  
                background: transparent;  
                border: none;  
                font-size: 40px;  
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }}
        """)
        self.layout.addWidget(self.close_button)

    def add_tab(self, title):
        self.tab_bar.addTab(title)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        self.parent.create_new_tab_content()

    def close_tab(self, index):
        # Prevent closing the first tab
        if index == 0:
            return
        self.tab_bar.removeTab(index)
        self.parent.remove_tab_content(index)
        if self.tab_bar.count() == 0:
            self.add_tab("Subtl")  # Ensure at least one tab exists

    def change_tab(self, index):
        self.parent.display_tab_content(index)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
