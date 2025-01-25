import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton

class CustomTab(QWidget):
    def __init__(self, title):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Add a label and a button in the tab
        self.label = QLabel(f'This is the content of {title}', self)
        self.layout.addWidget(self.label)
        self.button = QPushButton('Click Me', self)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Custom Browser Window with Tabs')
        self.setGeometry(100, 100, 800, 600)
        
        # Create a tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add tabs
        self.add_new_tab('Tab 1')
        self.add_new_tab('Tab 2')

    def add_new_tab(self, title):
        new_tab = CustomTab(title)
        self.tabs.addTab(new_tab, title)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())
