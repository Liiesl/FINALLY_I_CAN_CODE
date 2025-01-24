from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class VersionBlock(QWidget):
    def __init__(self, version, changes, parent=None):
        super().__init__(parent)
        self.version = version
        self.changes = changes
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Create the toggle button
        self.toggle_button = QPushButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setFixedSize(20, 20)
        self.toggle_button.setStyleSheet("QPushButton {border: none;}")
        self.toggle_button.setText("▼")
        self.toggle_button.clicked.connect(self.toggle_changes)

        # Create the version label with HTML for center alignment
        self.version_label = QLabel(f"<div style='text-align: center;'>{self.version}</div>")
        self.version_label.setFont(QFont("Inter ExtraBold", 20))

        # Create the changes label with HTML for center alignment
        changes_html = "<br>".join(self.changes)
        self.changes_label = QLabel(f"<div style='text-align: center;'>{changes_html}</div>")
        self.changes_label.setWordWrap(True)

        # Add the toggle button and version label to a horizontal layout
        self.header_layout = QHBoxLayout()
        self.header_layout.addWidget(self.toggle_button)
        self.header_layout.addWidget(self.version_label)
        self.header_layout.addStretch()

        # Add the header and changes to the main layout
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.changes_label)

        self.setLayout(self.layout)

    def toggle_changes(self):
        if self.toggle_button.isChecked():
            self.changes_label.show()
            self.toggle_button.setText("▼")
        else:
            self.changes_label.hide()
            self.toggle_button.setText("▶")
