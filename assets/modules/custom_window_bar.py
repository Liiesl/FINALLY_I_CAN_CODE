from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar, QApplication, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor
import qtawesome as qta 

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.setMouseTracking(True)
        self.resize_edge = None  # Tracks which edge is being resized
        self.resize_handle_size = 5  # Size of the resize handle (smaller for better sensitivity)
        self.pressing = False  # Tracks if the mouse is pressed
        self.start = QPoint(0, 0)  # Tracks the initial mouse position
        self.current_palette()

        self.init_ui()

        self.update_colors()

    def init_ui(self):
        self.setFixedHeight(50)
        self.edge_threshold = 10
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(f"background-color: {self.button_color}; color : {self.button_color};")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)  # Remove spacing between widgets
        self.setLayout(self.layout)

        self.create_tab_bar()
        self.create_buttons()

    def setup_initial_tabs(self):
        # Add the first tab but hide it
        self.add_tab("Hidden Tab")
        self.tab_bar.setTabVisible(0, False)  # Hide the first tab
        self.add_tab("Subtl")  # This will be the visible tab

    def current_palette(self):
        print("palette is being loaded by custom window bar")
        palette = self.parent.palette()
        self.text_color = palette.color(QPalette.WindowText).name()
        self.background_color = palette.color(QPalette.Window).name()
        self.button_color = palette.color(QPalette.Button).name()
        self.button_text_color = palette.color(QPalette.ButtonText).name()
        self.highlight_color = palette.color(QPalette.Highlight).name()
        self.hover_color = palette.color(QPalette.Highlight).darker().name()

        self.update()

    def update_colors(self):
        print("updating custom window bar's palette")
        palette = self.current_palette()

        # Update main background
        self.setStyleSheet(f"background-color: {self.button_color}; color : {self.button_color};")

        # Update tab bar styles
        self.tab_bar.setStyleSheet(f"""
            QTabBar::tab {{
                height: 50px;
                padding: 0px 10px;
                margin: 0;
                border: none;
                background: {self.button_color};
                color: {self.text_color};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
            QTabBar::tab:selected {{
                background: {self.background_color};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
        """)

        # Update new tab button style
        self.new_tab_button.setStyleSheet(f"""
            QPushButton {{
                color: {self.button_text_color};
                background: transparent;
                border: none;
                font-size: 40px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
            }}
        """)

        # Update window control buttons
        button_style = f"""
            QPushButton {{
                color: {self.text_color};
                background: transparent;
                border: none;
                font-size: 40px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.2);
            }}
        """
        self.min_button.setStyleSheet(button_style)
        self.max_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet(button_style)

        # Update close buttons on existing tabs
        for index in range(1, self.tab_bar.count()):  # Skip hidden tab
            close_button = self.tab_bar.tabButton(index, QTabBar.RightSide)
            if close_button:
                close_button.setStyleSheet(f"""
                    QPushButton {{
                        color: {self.text_color};
                        background: transparent;
                        border: none;
                        font-size: 18px;
                    }}
                    QPushButton:hover {{
                        background: rgba(255, 0, 0, 0.5);
                    }}
                """)
        self.update()

    def create_tab_bar(self):
        self.tab_bar = QTabBar(self)  # Use the custom tab bar
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(False)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.layout.addWidget(self.tab_bar)

        self.tab_bar.addTab = lambda text: self._add_tab_wrapper(text)
        self.tab_bar.tabButton = lambda index, button_type: self._tab_button_wrapper(index, button_type)

        # Add the "add tab" button directly to the right of the tabs
        self.new_tab_button = QPushButton(qta.icon('fa.plus'), '')
        self.new_tab_button.setFixedSize(50, 50)
        self.new_tab_button.clicked.connect(lambda: self.add_tab("Subtl"))  # Change tab name to "Subtl"
        self.layout.addWidget(self.new_tab_button)

        # Add a spacer to leave space between the tabs and the window buttons
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.spacer)

    def _add_tab_wrapper(self, text):
        index = QTabBar.addTab(self.tab_bar, text)
        if index != 0:
            self.tab_bar.setTabButton(index, QTabBar.RightSide, self.create_close_button(index))
        return index

    def _tab_button_wrapper(self, index, button_type):
        if index == 0 and button_type == QTabBar.RightSide:
            return None
        return QTabBar.tabButton(self.tab_bar, index, button_type)

    def create_close_button(self, index):
        close_button = QPushButton(qta.icon('fa.close'), '')
        close_button.setFixedSize(20, 20)
        close_button.clicked.connect(lambda: self.tab_bar.tabCloseRequested.emit(index))
        return close_button

    def create_buttons(self):
        self.min_button = QPushButton(qta.icon('fa.window-minimize'), '')
        self.min_button.setFixedSize(50, 50)
        self.min_button.clicked.connect(self.parent.showMinimized)
        self.layout.addWidget(self.min_button)

        self.max_button = QPushButton(qta.icon('fa.window-maximize'), '')
        self.max_button.setFixedSize(50, 50)
        self.max_button.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.max_button)

        self.close_button = QPushButton(qta.icon('fa.close'), '')
        self.close_button.setFixedSize(50, 50)
        self.close_button.clicked.connect(self.parent.close)
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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressing = True
            self.start = self.mapToGlobal(event.pos())
            self.resize_edge = self.get_resize_edge(event.pos())

    def mouseMoveEvent(self, event):
        if self.pressing == True:
            if self.resize_edge:
                self.resize_window(event)
            else:
                self.move_window(event)
        else:
            mouse_pos = event.pos()
            width, height = self.width(), self.height()

            # Check if the mouse is near the edges
            near_left = mouse_pos.x() <= self.edge_threshold
            near_right = mouse_pos.x() >= width - self.edge_threshold
            near_top = mouse_pos.y() <= self.edge_threshold
            near_bottom = mouse_pos.y() >= height - self.edge_threshold

            # Change the cursor based on the edge
            if near_left and near_top:
                self.setCursor(Qt.SizeFDiagCursor)  # Top-left corner
            elif near_right and near_top:
                self.setCursor(Qt.SizeBDiagCursor)  # Top-right corner
            elif near_left and near_bottom:
                self.setCursor(Qt.SizeBDiagCursor)  # Bottom-left corner
            elif near_right and near_bottom:
                self.setCursor(Qt.SizeFDiagCursor)  # Bottom-right corner
            elif near_left or near_right:
                self.setCursor(Qt.SizeHorCursor)  # Left or right edge
            elif near_top or near_bottom:
                self.setCursor(Qt.SizeVerCursor)  # Top or bottom edge
            else:
                self.setCursor(Qt.ArrowCursor)  # Default cursor

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
        self.update()

    def move_window(self, event):
        global_pos = self.mapToGlobal(event.pos())
        delta = global_pos - self.start
        self.start = global_pos
        self.move(self.pos() + delta)
