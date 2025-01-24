from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QBrush

class ToggleSwitch(QWidget):
    stateChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.setCursor(Qt.PointingHandCursor)

        self._state = False  # Default state (False for "light", True for "dark")
        self._circle_position = 0  # Position of the circle

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
        background_color = QColor('#4f86f7') if self._state else QColor('#cccccc')
        painter.setBrush(QBrush(background_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)

        # Draw circle
        circle_color = QColor('#ffffff')
        painter.setBrush(QBrush(circle_color))
        painter.setPen(Qt.NoPen)
        circle_rect = QRect(self._circle_position, 0, 30, 30)
        painter.drawEllipse(circle_rect)

    def mousePressEvent(self, event):
        self._state = not self._state
        self.animate_circle()
        self.stateChanged.emit()  # Emit the custom signal when state changes

    def animate_circle(self):
        start_value = 0 if self._state else 30
        end_value = 30 if self._state else 0

        self.animation.setStartValue(start_value)
        self.animation.setEndValue(end_value)
        self.animation.start()

    def get_state(self):
        return "dark" if self._state else "light"

    def set_state(self, state):
        self._state = (state == "dark")
        self._circle_position = 30 if self._state else 0
        self.update()

    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()
