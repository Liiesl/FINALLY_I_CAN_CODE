from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTabBar
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.start = QPoint(0, 0)
        self.pressing = False
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.create_tab_bar()
        self.create_buttons()

    def create_tab_bar(self):
        self.tab_bar = QTabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.layout.addWidget(self.tab_bar)

        self.add_tab("SRT Editor")

    def create_buttons(self):
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(lambda: self.add_tab("New Tab"))
        self.layout.addWidget(self.new_tab_button)

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

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.pressing:
            diff = event.globalPos() - self.start
            self.parent.move(self.parent.pos() + diff)
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressing = False

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

        self.setStyleSheet(f"""
            CustomWindowBar {{
                background-color: {background_color};
                color: {text_color};
            }}

            QTabBar::tab {{
                background-color: {background_color};
                color: {text_color};
            }}
        """)
    def resizeEvent(self, event):
        self.resize_handle_size = 8
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if not self.pressing:
            if event.pos().x() < self.resize_handle_size:
                self.setCursor(Qt.SizeHorCursor)
            elif event.pos().y() < self.resize_handle_size:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True
            self.resize_edge = self.get_resize_edge(event.pos())

    def mouseReleaseEvent(self, event):
        self.pressing = False
        self.resize_edge = None

    def get_resize_edge(self, pos):
        if pos.x() < self.resize_handle_size:
            return 'left'
        elif pos.y() < self.resize_handle_size:
            return 'top'
        else:
            return None

    def resize_window(self, event):
        if self.resize_edge == 'left':
            diff = event.globalPos() - self.start
            new_width = self.parent.width() - diff.x()
            if new_width > self.parent.minimumWidth():
                self.parent.resize(new_width, self.parent.height())
                self.start = event.globalPos()
        elif self.resize_edge == 'top':
            diff = event.globalPos() - self.start
            new_height = self.parent.height() - diff.y()
            if new_height > self.parent.minimumHeight():
                self.parent.resize(self.parent.width(), new_height)
                self.start = event.globalPos()
