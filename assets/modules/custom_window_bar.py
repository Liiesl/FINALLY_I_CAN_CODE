from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor

class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(False)  # Disable default close button
        self.parent = parent  # Reference to the parent window

    def addTab(self, text):
        index = super().addTab(text)
        # Add a close button to all tabs except the first one
        if index != 0:
            self.setTabButton(index, QTabBar.RightSide, self.create_close_button(index))
        return index

    def create_close_button(self, index):
        close_button = QPushButton('✖')
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.tabCloseRequested.emit(index))
        close_button.setStyleSheet("""
            QPushButton {
                color: black;
                background: transparent;
                border: none;
                font-size: 12px;
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

    def add_tab(self, title):
        index = self.addTab(title)
        self.setCurrentIndex(self.count() - 1)
        self.parent.create_new_tab_content()

    def close_tab(self, index):
        # Prevent closing the first tab
        if index == 0:
            return
        self.removeTab(index)
        self.parent.remove_tab_content(index)
        if self.count() == 0:
            self.add_tab("Subtl")  # Ensure at least one tab exists

    def change_tab(self, index):
        self.parent.display_tab_content(index)

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.start = QPoint(0, 0)
        self.pressing = False  # Track if the mouse is pressed
        self.resize_edge = None  # Track which edge is being resized
        self.resize_handle_size = 5  # Size of the resize handle (smaller for better sensitivity)

        self.palette = QApplication.instance().palette()
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
        
        self.setStyleSheet(f"""
            CustomWindowBar {{
                background-color: {self.highlight_color}; 
            }}
        """)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Remove spacing between widgets
        self.setLayout(self.layout)

        self.create_tab_bar()
        self.create_buttons()

        # Add the first tab but hide it
        self.tab_bar.add_tab("Hidden Tab")
        self.tab_bar.setTabVisible(0, False)  # Hide the first tab

        # Create a new tab and make it visible
        self.tab_bar.add_tab("Subtl")  # This will be the visible tab

    def create_tab_bar(self):
        self.tab_bar = CustomTabBar(self)  # Use the custom tab bar
        self.tab_bar.tabCloseRequested.connect(self.tab_bar.close_tab)
        self.tab_bar.currentChanged.connect(self.tab_bar.change_tab)

        # Set the tab bar style
        self.tab_bar.setStyleSheet(f"""
            QTabBar::tab {{
                padding: 2px 10px;  /* Adjust padding to fit the title */
                margin: 0;          
                border: none;      
                background: {self.button_color};  /* Make the tab background transparent */
                color: {self.button_text_color};  /* Use the button text color */
            }}
            QTabBar::tab:selected {{
                background: {self.background_color};  /* Use the background color for the selected tab */
            }}
        """)

        self.layout.addWidget(self.tab_bar)

        # Add the "add tab" button directly to the right of the tabs
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(50, 50)
        self.new_tab_button.clicked.connect(lambda: self.tab_bar.add_tab("Subtl"))  # Change tab name to "Subtl"

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
        self.min_button = QPushButton('-')
        self.min_button.setFixedSize(50, 50)
        self.min_button.clicked.connect(self.parent.showMinimized)

        # Set the minimize button style
        self.min_button.setStyleSheet(f"""
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
        self.layout.addWidget(self.min_button)

        self.max_button = QPushButton('❏')
        self.max_button.setFixedSize(50, 50)
        self.max_button.clicked.connect(self.toggle_maximize_restore)

        # Set the maximize button style
        self.max_button.setStyleSheet(f"""
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
        self.layout.addWidget(self.max_button)

        self.close_button = QPushButton('✖')
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.parent.close)

        # Set the close button style
        self.close_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.button_text_color};  
                background: transparent;  
                border: none;  
                font-size: 40px;  
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }}
        """)
        self.layout.addWidget(self.close_button)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True
            self.resize_edge = self.get_resize_edge(event.globalPos())

    def mouseMoveEvent(self, event):
        if self.pressing and self.resize_edge:
            self.resize_window(event)
        elif event.buttons() == Qt.LeftButton and self.pressing:
            # Move the window
            diff = event.globalPos() - self.start
            self.parent.move(self.parent.pos() + diff)
            self.start = event.globalPos()
        else:
            # Change cursor when near the edges or corners of the window
            self.update_cursor(event.globalPos())

    def mouseReleaseEvent(self, event):
        self.pressing = False
        self.resize_edge = None
        self.setCursor(Qt.ArrowCursor)

    def enterEvent(self, event):
        # Update cursor when the mouse enters the widget
        self.update_cursor(QCursor.pos())  # Use global mouse position

    def leaveEvent(self, event):
        # Reset cursor when the mouse leaves the widget
        self.setCursor(Qt.ArrowCursor)

    def update_cursor(self, global_pos):
        # Change cursor based on the mouse position relative to the window's absolute edges
        edge = self.get_resize_edge(global_pos)
        if edge == 'left' or edge == 'right':
            self.setCursor(Qt.SizeHorCursor)
        elif edge == 'top' or edge == 'bottom':
            self.setCursor(Qt.SizeVerCursor)
        elif edge == 'top-left' or edge == 'bottom-right':
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge == 'top-right' or edge == 'bottom-left':
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def get_resize_edge(self, global_pos):
        # Get the parent window's geometry
        window_rect = self.parent.geometry()

        # Check if the mouse is near the edges or corners of the window
        if (global_pos.x() <= window_rect.left() + self.resize_handle_size and
            global_pos.y() <= window_rect.top() + self.resize_handle_size):
            return 'top-left'
        elif (global_pos.x() >= window_rect.right() - self.resize_handle_size and
              global_pos.y() <= window_rect.top() + self.resize_handle_size):
            return 'top-right'
        elif (global_pos.x() <= window_rect.left() + self.resize_handle_size and
              global_pos.y() >= window_rect.bottom() - self.resize_handle_size):
            return 'bottom-left'
        elif (global_pos.x() >= window_rect.right() - self.resize_handle_size and
              global_pos.y() >= window_rect.bottom() - self.resize_handle_size):
            return 'bottom-right'
        elif global_pos.x() <= window_rect.left() + self.resize_handle_size:
            return 'left'
        elif global_pos.x() >= window_rect.right() - self.resize_handle_size:
            return 'right'
        elif global_pos.y() <= window_rect.top() + self.resize_handle_size:
            return 'top'
        elif global_pos.y() >= window_rect.bottom() - self.resize_handle_size:
            return 'bottom'
        else:
            return None

    def resize_window(self, event):
        if self.resize_edge == 'left':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() - diff.x()
            if new_width > self.parent.minimumWidth():
                self.parent.resize(new_width, self.parent.height())
                self.start = event.globalPos()
        elif self.resize_edge == 'right':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() + diff.x()
            if new_width > self.parent.minimumWidth():
                self.parent.resize(new_width, self.parent.height())
                self.start = event.globalPos()
        elif self.resize_edge == 'top':
            diff = event.globalPos() - self.start
            new_height = self.parent.height() - diff.y()
            if new_height > self.parent.minimumHeight():
                self.parent.resize(self.parent.width(), new_height)
                self.start = event.globalPos()
        elif self.resize_edge == 'bottom':
            diff = event.globalPos() - self.start
            new_height = self.parent.height() + diff.y()
            if new_height > self.parent.minimumHeight():
                self.parent.resize(self.parent.width(), new_height)
                self.start = event.globalPos()
        elif self.resize_edge == 'top-left':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() - diff.x()
            new_height = self.parent.height() - diff.y()
            if new_width > self.parent.minimumWidth() and new_height > self.parent.minimumHeight():
                self.parent.resize(new_width, new_height)
                self.start = event.globalPos()
        elif self.resize_edge == 'top-right':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() + diff.x()
            new_height = self.parent.height() - diff.y()
            if new_width > self.parent.minimumWidth() and new_height > self.parent.minimumHeight():
                self.parent.resize(new_width, new_height)
                self.start = event.globalPos()
        elif self.resize_edge == 'bottom-left':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() - diff.x()
            new_height = self.parent.height() + diff.y()
            if new_width > self.parent.minimumWidth() and new_height > self.parent.minimumHeight():
                self.parent.resize(new_width, new_height)
                self.start = event.globalPos()
        elif self.resize_edge == 'bottom-right':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() + diff.x()
            new_height = self.parent.height() + diff.y()
            if new_width > self.parent.minimumWidth() and new_height > self.parent.minimumHeight():
                self.parent.resize(new_width, new_height)
                self.start = event.globalPos()

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
