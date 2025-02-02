# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPalette
import qtawesome as qta  # Import QtAwesome for icons

class NotificationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)  # Padding inside the rectangle
        self.layout.setSpacing(3)  # Spacing between elements

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

        # Left Arrow Button
        self.left_arrow = QPushButton()
        self.left_arrow.setIcon(qta.icon('fa5s.angle-left', color=self.text_color))  # Use QtAwesome icon
        self.left_arrow.setStyleSheet("background-color: transparent; border: none;")
        self.left_arrow.clicked.connect(self.previous_notification)
        self.layout.addWidget(self.left_arrow)

        # Emoji Label
        self.label_emoji = QLabel()
        self.label_emoji.setStyleSheet(f"font-size: 20px; color: {self.text_color};")
        self.layout.addWidget(self.label_emoji)

        # Text Label
        self.label_text = QLabel()
        self.label_text.setStyleSheet(f"color: {self.text_color}; padding: 5px;")
        self.layout.addWidget(self.label_text)

        # Right Arrow Button
        self.right_arrow = QPushButton()
        self.right_arrow.setIcon(qta.icon('fa5s.angle-right', color=self.text_color))  # Use QtAwesome icon
        self.right_arrow.setStyleSheet("background-color: transparent; border: none;")
        self.right_arrow.clicked.connect(self.next_notification)
        self.layout.addWidget(self.right_arrow)

        # Set background color of the entire widget using the highlight color
        self.setStyleSheet(f"""
            NotificationBar {{
                background-color: {self.highlight_color};
                border: 2px solid {self.text_color};
                border-radius: 5px;
            }}
        """)

        # Timer for automatic notifications
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
        # Create animations for sliding out and sliding in (for both emoji and text)
        self.slide_out_animation_emoji = QPropertyAnimation(self.label_emoji, b"geometry")
        self.slide_in_animation_emoji = QPropertyAnimation(self.label_emoji, b"geometry")
        self.slide_out_animation_text = QPropertyAnimation(self.label_text, b"geometry")
        self.slide_in_animation_text = QPropertyAnimation(self.label_text, b"geometry")

        # Get the current geometry of the emoji and text labels
        emoji_geometry = self.label_emoji.geometry()
        text_geometry = self.label_text.geometry()

        # Slide out: Move the emoji and text labels upward
        self.slide_out_animation_emoji.setDuration(self.animation_duration)
        self.slide_out_animation_emoji.setStartValue(emoji_geometry)
        self.slide_out_animation_emoji.setEndValue(
            QRect(emoji_geometry.x(), emoji_geometry.y() - emoji_geometry.height(),
                  emoji_geometry.width(), emoji_geometry.height())
        )
        self.slide_out_animation_emoji.setEasingCurve(QEasingCurve.OutQuad)

        self.slide_out_animation_text.setDuration(self.animation_duration)
        self.slide_out_animation_text.setStartValue(text_geometry)
        self.slide_out_animation_text.setEndValue(
            QRect(text_geometry.x(), text_geometry.y() - text_geometry.height(),
                  text_geometry.width(), text_geometry.height())
        )
        self.slide_out_animation_text.setEasingCurve(QEasingCurve.OutQuad)

        # Update to the next notification
        self.current_index = (self.current_index + 1) % len(self.notifications)
        self.update_notification()

        # Slide in: Move the emoji and text labels back into view
        self.slide_in_animation_emoji.setDuration(self.animation_duration)
        self.slide_in_animation_emoji.setStartValue(
            QRect(emoji_geometry.x(), emoji_geometry.y() + emoji_geometry.height(),
                  emoji_geometry.width(), emoji_geometry.height())
        )
        self.slide_in_animation_emoji.setEndValue(emoji_geometry)
        self.slide_in_animation_emoji.setEasingCurve(QEasingCurve.InQuad)

        self.slide_in_animation_text.setDuration(self.animation_duration)
        self.slide_in_animation_text.setStartValue(
            QRect(text_geometry.x(), text_geometry.y() + text_geometry.height(),
                  text_geometry.width(), text_geometry.height())
        )
        self.slide_in_animation_text.setEndValue(text_geometry)
        self.slide_in_animation_text.setEasingCurve(QEasingCurve.InQuad)

        # Connect animations and start
        self.slide_out_animation_emoji.finished.connect(self.slide_in_animation_emoji.start)
        self.slide_out_animation_text.finished.connect(self.slide_in_animation_text.start)
        self.slide_out_animation_emoji.start()
        self.slide_out_animation_text.start()

    def next_notification(self):
        """Move to the next notification."""
        self.current_index = (self.current_index + 1) % len(self.notifications)
        self.animate_notification()
        self.reset_timer()

    def previous_notification(self):
        """Move to the previous notification."""
        self.current_index = (self.current_index - 1) % len(self.notifications)
        self.animate_notification()
        self.reset_timer()

    def reset_timer(self):
        """Stop and restart the timer."""
        self.stop_timer()
        self.start_timer()

    def add_notification(self, emoji, message):
        """Add a new notification to the list."""
        self.notifications.append((emoji, message))

    def remove_notification(self, index):
        """Remove a notification from the list."""
        if 0 <= index < len(self.notifications):
            self.notifications.pop(index)
