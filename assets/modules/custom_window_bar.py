from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint, QRect

class CustomWindowBar(QWidget):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.init_ui()

        # Resize handling
        self.resize_margin = 10  # Margin for detecting resize areas
        self.resize_direction = None
        self.dragging = False
        self.offset = QPoint()

    def init_ui(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Title label
        self.title_label = QLabel("SRT Editor")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 14px;")
        self.layout.addWidget(self.title_label)

        # Minimize button
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(QIcon.fromTheme("window-minimize"))
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.setStyleSheet("background-color: transparent; border: none;")
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.layout.addWidget(self.minimize_button)

        # Maximize/Restore button
        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(QIcon.fromTheme("window-maximize"))
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.setStyleSheet("background-color: transparent; border: none;")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.maximize_button)

        # Close button
        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon.fromTheme("window-close"))
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background-color: transparent; border: none;")
        self.close_button.clicked.connect(self.parent.close)
        self.layout.addWidget(self.close_button)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setIcon(QIcon.fromTheme("window-maximize"))
        else:
            self.parent.showMaximized()
            self.maximize_button.setIcon(QIcon.fromTheme("window-restore"))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Check if the mouse is near the edges for resizing
            self.resize_direction = self.get_resize_direction(event.pos())
            if self.resize_direction:
                self.offset = event.globalPos()
            else:
                # Otherwise, handle window dragging
                self.dragging = True
                self.offset = event.globalPos() - self.parent.pos()

    def mouseMoveEvent(self, event):
        if self.resize_direction:
            # Handle window resizing
            self.handle_resize(event.globalPos())
        elif self.dragging:
            # Handle window dragging
            self.parent.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.resize_direction = None

    def get_resize_direction(self, pos):
        """Determine which edge or corner the mouse is near for resizing."""
        rect = self.parent.rect()
        if pos.x() <= self.resize_margin:
            if pos.y() <= self.resize_margin:
                return "top-left"
            elif pos.y() >= rect.height() - self.resize_margin:
                return "bottom-left"
            else:
                return "left"
        elif pos.x() >= rect.width() - self.resize_margin:
            if pos.y() <= self.resize_margin:
                return "top-right"
            elif pos.y() >= rect.height() - self.resize_margin:
                return "bottom-right"
            else:
                return "right"
        elif pos.y() <= self.resize_margin:
            return "top"
        elif pos.y() >= rect.height() - self.resize_margin:
            return "bottom"
        return None

    def handle_resize(self, global_pos):
        """Resize the window based on the direction and mouse movement."""
        rect = self.parent.rect()
        delta = global_pos - self.offset
        new_rect = QRect(self.parent.geometry())

        if self.resize_direction == "left":
            new_rect.setLeft(new_rect.left() + delta.x())
        elif self.resize_direction == "right":
            new_rect.setRight(new_rect.right() + delta.x())
        elif self.resize_direction == "top":
            new_rect.setTop(new_rect.top() + delta.y())
        elif self.resize_direction == "bottom":
            new_rect.setBottom(new_rect.bottom() + delta.y())
        elif self.resize_direction == "top-left":
            new_rect.setTopLeft(new_rect.topLeft() + delta)
        elif self.resize_direction == "top-right":
            new_rect.setTopRight(new_rect.topRight() + delta)
        elif self.resize_direction == "bottom-left":
            new_rect.setBottomLeft(new_rect.bottomLeft() + delta)
        elif self.resize_direction == "bottom-right":
            new_rect.setBottomRight(new_rect.bottomRight() + delta)

        self.parent.setGeometry(new_rect)
        self.offset = global_pos
