# assets/modules/custom_window_bar.py
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette

class CustomWindowBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("CustomWindowBar")
        
        self._startPos = None
        self._startMovePos = None
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        self.tab_widget.setMovable(True)
        
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 30)
        self.add_tab_button.clicked.connect(self.add_tab)
        
        self.layout.addWidget(self.tab_widget, 1)
        self.layout.addWidget(self.add_tab_button)
        
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.minimize_window)
        
        self.maximize_button = QPushButton("□")
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.maximize_window)
        
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close_window)
        
        self.layout.addWidget(self.minimize_button)
        self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)
        
        self.setStyleSheet("""
            QFrame#CustomWindowBar {
                background-color: #333;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                border: none;
                color: white;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
    
    def minimize_window(self):
        self.window().showMinimized()
        
    def maximize_window(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
        
    def close_window(self):
        self.window().close()

    def add_tab(self, content_widget=None, title="New Tab"):
        if content_widget is None:
            content_widget = QWidget()  # Placeholder widget for the new tab
        self.tab_widget.addTab(content_widget, title)
        
    def remove_tab(self, index):
        self.tab_widget.removeTab(index)

    def apply_palette(self, palette):
        self.setStyleSheet(f"""
            QFrame#CustomWindowBar {{
                background-color: {palette.color(QPalette.Window).name()};
            }}
            QLabel {{
                color: {palette.color(QPalette.WindowText).name()};
            }}
            QPushButton {{
                color: {palette.color(QPalette.WindowText).name()};
            }}
            QPushButton:hover {{
                background-color: {palette.color(QPalette.Highlight).name()};
            }}
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = event.globalPos()
            self._startMovePos = self.window().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self._startPos
            self.window().move(self._startMovePos + delta)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._startPos = None
            self._startMovePos = None
            event.accept()
