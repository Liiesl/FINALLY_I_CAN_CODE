from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QTabBar, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QFont

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.start = QPoint(0, 0)
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.create_buttons()
        self.create_tab_bar()

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

        self.new_tab_button = QPushButton('+')
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        self.layout.addWidget(self.new_tab_button)

    def create_tab_bar(self):
        self.tab_bar = QTabBar(self)
        self.tab_bar.setMovable(True)
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        self.tab_bar.currentChanged.connect(self.change_tab)

        self.layout.addWidget(self.tab_bar)

        self.add_tab("SRT Editor")

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

    def close_tab(self, index):
        self.tab_bar.removeTab(index)
        if self.tab_bar.count() == 0:
            self.add_tab("SRT Editor")

    def change_tab(self, index):
        pass  # Handle tab change if necessary

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def add_new_tab(self):
        self.add_tab("New Tab")

    def apply_theme(self, theme):
        palette = self.app.palette()
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
