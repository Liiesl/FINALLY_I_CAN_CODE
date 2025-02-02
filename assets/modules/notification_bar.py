# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPalette
import qtawesome as qta  # Import QtAwesome for icons

class NotificationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # No padding inside the rectangle
        self.layout.setSpacing(0)  # No spacing between elements

        # Notifications list
        self.current_index = 0
        self.notifications = [
            ("💡", "Tip: You can merge multiple SRT files into one."),
            ("🎉", "New Feature: Try out the Multilingual Merge tool!"),
            ("⏰", "Reminder: You last used the Subtitle Shifter 2 days ago."),
            ("📰", "News: Check out our latest blog post on subtitle editing!")
        ]

        # Get colors from the parent widget's palette
        palette = self.parent().palette() if self.parent() else QPalette()
        self.highlight_color = palette.color(QPalette.Highlight).name()  # Background color
        self.text_color = palette.color(QPalette.WindowText).name()  # Text color

        # Container for the animated labels
        self.container = QFrame(self)
        self.container.setStyleSheet(f"""
            QFrame {{
                background-color: {self.highlight_color};
                border: 2px solid {self.text_color};
                border-radius: 5px;
            }}
        """)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 5, 10, 5)
        self.container_layout.setSpacing(10)
        self.layout.addWidget(self.container)

        # Emoji Label
        self.label_emoji = QLabel()
        self.label_emoji.setStyleSheet(f"font-size: 20px; color: {self.text_color};")
        self.container_layout.addWidget(self.label_emoji)

        # Text Label
        self.label_text = QLabel()
        self.label_text.setStyleSheet(f"color: {self.text_color}; padding: 5px;")
        self.container_layout.addWidget(self.label_text)

        # Timer for notifications
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_notification)
        self.start_timer()

        # Animation properties
        self.animation_duration = 500  # Duration of the animation in milliseconds
        self.update_notification()  # Initialize with the first notification

    def start_timer(self):
        """Start the timer to cycle through notifications."""
        self.timer.start(10000)  # Change notification every 10 seconds

    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()

    def update_notification(self):
        """Update the notification bar with the current notification."""
        emoji, text = self.notifications[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)

    def animate_notification(self):
        """Animate the transition to the next notification."""
        # Create animations for sliding out and sliding in
        self.slide_out_animation = QPropertyAnimation(self.container, b"geometry")
        self.slide_in_animation = QPropertyAnimation(self.container, b"geometry")

        # Get the current geometry of the container
        current_geometry = self.container.geometry()

        # Slide out: Move the container upward
        self.slide_out_animation.setDuration(self.animation_duration)
        self.slide_out_animation.setStartValue(current_geometry)
        self.slide_out_animation.setEndValue(
            QRect(current_geometry.x(), current_geometry.y() - current_geometry.height(), 
                  current_geometry.width(), current_geometry.height())
        )
        self.slide_out_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Update to the next notification
        self.current_index = (self.current_index + 1) % len(self.notifications)
        self.update_notification()

        # Slide in: Move the container back into view
        self.slide_in_animation.setDuration(self.animation_duration)
        self.slide_in_animation.setStartValue(
            QRect(current_geometry.x(), current_geometry.y() + current_geometry.height(), 
                  current_geometry.width(), current_geometry.height())
        )
        self.slide_in_animation.setEndValue(current_geometry)
        self.slide_in_animation.setEasingCurve(QEasingCurve.InQuad)

        # Connect animations and start
        self.slide_out_animation.finished.connect(self.slide_in_animation.start)
        self.slide_out_animation.start()

    def add_notification(self, emoji, message):
        """Add a new notification to the list."""
        self.notifications.append((emoji, message))

    def remove_notification(self, index):
        """Remove a notification from the list."""
        if 0 <= index < len(self.notifications):
            self.notifications.pop(index)
