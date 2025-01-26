from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor

class CustomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)  # Enable close buttons on tabs

    def tabButton(self, index, button_type):
        # Override to remove the close button for the first tab
        if index == 0 and button_type == QTabBar.RightSide:
            return None
        return super().tabButton(index, button_type)

    def tabLayoutChange(self):
        super().tabLayoutChange()
        # Ensure the close button is styled correctly
        for index in range(self.count()):
            close_button = self.tabButton(index, QTabBar.RightSide)
            if close_button:
                close_button.setStyleSheet("""
                    QPushButton {
                        color: {self.button_text_color};  
                        background: transparent;  
                        border: none;  
                        font-size: 16px;  
                    }
                    QPushButton:hover {
                        background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
                    }
                """.format(self=self.parent()))

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
        self.setFixedHeight(30)
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

    def create_tab_bar(self):
        self.tab_bar = CustomTabBar(self)  # Use the custom tab bar
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)  # Enable close buttons on tabs

        # Set the tab bar style
        self.tab_bar.setStyleSheet("""
            QTabBar::tab {
                padding: 2px 10px;  /* Adjust padding to fit the title */
                margin: 0;          
                border: none;      
                background: {self.button_color};  /* Make the tab background transparent */
                color: {self.button_text_color};  /* Use the button text color */
            }
            QTabBar::tab:selected {
                background: {self.background_color};  /* Use the background color for the selected tab */
            }
        """.format(self=self))

        self.tab_bar.tabCloseRequested.connect(self.close_tab)  # Connect the close button signal

        self.layout.addWidget(self.tab_bar)

        # Add the "add tab" button directly to the right of the tabs
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(lambda: self.add_tab("Subtl"))  # Change tab name to "Subtl"

        # Set the "+" button style
        self.new_tab_button.setStyleSheet("""
            QPushButton {
                color: {self.button_text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 16px;  /* Increase font size for better visibility */
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }
        """.format(self=self))
        self.layout.addWidget(self.new_tab_button)

        # Add a spacer to leave space between the tabs and the window buttons
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer)

        self.add_tab("Subtl")  # Change the first tab name to "Subtl"

    def create_buttons(self):
        self.min_button = QPushButton('-')
        self.min_button.setFixedSize(30, 30)
        self.min_button.clicked.connect(self.parent.showMinimized)

        # Set the minimize button style
        self.min_button.setStyleSheet("""
            QPushButton {
                color: {self.button_text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 16px;  /* Increase font size for better visibility */
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }
        """.format(self=self))
        self.layout.addWidget(self.min_button)

        self.max_button = QPushButton('□')
        self.max_button.setFixedSize(30, 30)
        self.max_button.clicked.connect(self.toggle_maximize_restore)

        # Set the maximize button style
        self.max_button.setStyleSheet("""
            QPushButton {
                color: {self.button_text_color};  /* Use the button text color */
                background: transparent;  /* Make the background transparent */
                border: none;  /* Remove border */
                font-size: 16px;  /* Increase font size for better visibility */
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }
        """.format(self=self))
        self.layout.addWidget(self.max_button)

        self.close_button = QPushButton('x')
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.parent.close)

        # Set the close button style
        self.close_button.setStyleSheet("""
            QPushButton {
                color: {self.button_text_color};  
                background: transparent;  
                border: none;  
                font-size: 16px;  
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);  /* Add a hover effect */
            }
        """.format(self=self))
        self.layout.addWidget(self.close_button)

    def close_tab(self, index):
        self.tab_bar.removeTab(index)
        self.parent.remove_tab_content(index)

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

    def add_tab(self, title):
        self.tab_bar.addTab(title)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        self.parent.create_new_tab_content()

    def change_tab(self, index):
        self.parent.display_tab_content(index)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
