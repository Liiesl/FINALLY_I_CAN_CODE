from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush

class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)

        self.state = False  # Default state (False for "light", True for "dark")
        self.circle_position = 0  # Position of the circle

        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setDuration(200)

        self.setStyleSheet("""
            background-color: #4f86f7;
            border-radius: 15px;
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        background_color = QColor('#4f86f7') if self.state else QColor('#cccccc')
        painter.setBrush(QBrush(background_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)

        # Draw circle
        circle_color = QColor('#ffffff')
        painter.setBrush(QBrush(circle_color))
        painter.setPen(Qt.NoPen)
        circle_rect = QRect(self.circle_position, 0, 30, 30)
        painter.drawEllipse(circle_rect)

    def mousePressEvent(self, event):
        self.state = not self.state
        self.animate_circle()

    def animate_circle(self):
        start_value = 0 if self.state else 30
        end_value = 30 if self.state else 0

        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.start()

    def get_state(self):
        return "dark" if self.state else "light"

    def set_state(self, state):
        self.state = (state == "dark")
        self.circle_position = 30 if self.state else 0
        self.update()

    def get_circle_position(self):
        return self.circle_position

    def set_circle_position(self, pos):
        self.circle_position = pos
        self.update()

    circle_position = Qt.Property(int, get_circle_position, set_circle_position)
