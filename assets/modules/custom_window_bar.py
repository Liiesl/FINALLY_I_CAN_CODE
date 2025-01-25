# assets/modules/custom_window_bar.py
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont

class CustomWindowBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("CustomWindowBar")
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel("SRT Editor")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.title_label)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.remove_tab)
        
        self.layout.addWidget(self.tab_widget, 1)
        
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

    def add_tab(self, content_widget, title):
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
