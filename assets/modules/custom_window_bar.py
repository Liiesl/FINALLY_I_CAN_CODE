from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.start = QPoint(0, 0)
        self.pressing = False  # Track if the mouse is pressed
        self.resize_edge = None  # Track which edge is being resized
        self.resize_handle_size = 5  # Size of the resize handle (smaller for better sensitivity)
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Remove spacing between widgets
        self.setLayout(self.layout)

        self.create_tab_bar()
        self.create_buttons()

    def create_tab_bar(self):
        self.tab_bar = QTabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        # Adjust tab bar styling to fit the title
        self.tab_bar.setStyleSheet("""
            QTabBar::tab {
                padding: 2px 10px;  /* Adjust padding to fit the title */
                margin: 0;          /* Remove extra margin */
                border: none;       /* Remove border */
            }
            QTabBar {
                background: transparent;  /* Make the tab bar background transparent */
            }
        """)

        self.layout.addWidget(self.tab_bar)

        # Add the "add tab" button directly to the right of the tabs
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(lambda: self.add_tab("New Tab"))
        self.layout.addWidget(self.new_tab_button)

        # Add a spacer to leave space between the tabs and the window buttons
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer)

        self.add_tab("SRT Editor")

    def create_buttons(self):
        self.min_button = QPushButton('-')
        self.min_button.setFixedSize(30, 30)
        self.min_button.clicked.connect(self.parent.showMinimized)
        self.layout.addWidget(self.min_button)

        self.max_button = QPushButton('□')
        self.max_button.setFixedSize(30, 30)
        self.max_button.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.max_button)

        self.close_button = QPushButton('x')
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.parent.close)
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

    def add_tab(self, title):
        self.tab_bar.addTab(title)
        self.tab_bar.setCurrentIndex(self.tab_bar.count() - 1)
        self.parent.create_new_tab_content()

    def close_tab(self, index):
        self.tab_bar.removeTab(index)
        self.parent.remove_tab_content(index)
        if self.tab_bar.count() == 0:
            self.add_tab("SRT Editor")

    def change_tab(self, index):
        self.parent.display_tab_content(index)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def apply_theme(self, theme):
        palette = QApplication.instance().palette()
        background_color = palette.color(QPalette.Window).name()
        text_color = palette.color(QPalette.WindowText).name()

        # Slightly darker background for the window/tab bar
        darker_background = QColor(background_color).darker(110).name()

        # Set styles for the window bar, tab bar, and buttons
        self.setStyleSheet(f"""
            CustomWindowBar {{
                background-color: {darker_background};
                color: {text_color};
            }}

            QTabBar::tab {{
                background-color: {darker_background};
                color: {text_color};
                padding: 2px 10px;  /* Adjust padding to fit the title */
                margin: 0;          /* Remove extra margin */
                border: none;       /* Remove border */
            }}

            QPushButton {{
                background-color: {darker_background};
                color: {text_color};
                border: none;
                padding: 0;
                margin: 0;
            }}

            QPushButton:hover {{
                background-color: {QColor(darker_background).darker(120).name()};
            }}
        """)
