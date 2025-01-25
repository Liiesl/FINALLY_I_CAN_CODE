from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QTabBar, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QFont

class CustomWindowBar(QWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.init_ui()
        self.start = QPoint(0, 0)

    def init_ui(self):
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

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
