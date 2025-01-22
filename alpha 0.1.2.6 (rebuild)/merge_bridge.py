from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt

# Correct import paths
from tools.glue_end_to_end_merge import GlueEndToEndMerge
from tools.stacked_merge import StackedMerge

class MergeBridge(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Merge SRT Files')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for the mode selection buttons
        mode_layout = QHBoxLayout()

        glue_button = QPushButton('Glue End to End Merge')
        glue_button.clicked.connect(self.show_glue_end_to_end_merge)
        mode_layout.addWidget(glue_button)

        stacked_button = QPushButton('Stacked Merge')
        stacked_button.clicked.connect(self.show_stacked_merge)
        mode_layout.addWidget(stacked_button)

        layout.addLayout(mode_layout)

        # Create a stacked widget to hold the merge interfaces
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)

        # Add Glue End to End Merge widget
        self.glue_merge_widget = GlueEndToEndMerge(parent=self)
        self.stacked_widget.addWidget(self.glue_merge_widget)

        # Add Stacked Merge widget
        self.stacked_merge_widget = StackedMerge(parent=self)
        self.stacked_widget.addWidget(self.stacked_merge_widget)

        # Show the Glue End to End Merge interface by default
        self.show_glue_end_to_end_merge()

    def show_glue_end_to_end_merge(self):
        self.stacked_widget.setCurrentWidget(self.glue_merge_widget)

    def show_stacked_merge(self):
        self.stacked_widget.setCurrentWidget(self.stacked_merge_widget)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    window = MergeBridge()
    window.show()
    app.exec_()