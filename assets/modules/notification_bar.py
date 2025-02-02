# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPalette, QFontMetrics
import qtawesome as qta  # Import QtAwesome for icons


class NotificationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)  # Padding inside the rectangle
        self.layout.setSpacing(10)  # Spacing between elements

        # Notifications list
        self.current_index = 0
        self.notifications = [
            ("💡", "Tip: You can merge multiple SRT files into one."),
            ("🎉", "New Feature: Try out the Multilingual Merge tool!"),
            ("⏰", "Reminder: You last used the Subtitle Shifter 2 days ago."),
            ("📰", "News: Check out our latest blog post on subtitle editing!")
        ]

        # Animation duration (in milliseconds)
        self.animation_duration = 500

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

        # Invisible Frame to hold emoji and text
        self.content_frame = QFrame(self)
        self.content_frame.setStyleSheet("background-color: transparent; border: none;")
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(10)

        # Emoji Label
        self.label_emoji = QLabel()
        self.label_emoji.setStyleSheet(f"font-size: 20px; color: {self.text_color};")
        self.content_layout.addWidget(self.label_emoji)

        # Text Label
        self.label_text = QLabel()
        self.label_text.setStyleSheet(f"color: {self.text_color}; padding: 5px;")
        self.content_layout.addWidget(self.label_text)

        # Add the invisible frame to the main layout
        self.layout.addWidget(self.content_frame)

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
                border: 2px solid {self.text_color};  /* Add a visible border */
                border-radius: 5px;
            }}
        """)

        # Timer for automatic notifications
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_notification)
        self.start_timer()

        # Initialize with the first notification
        self.update_notification()

    def update_notification(self):
        """Update the notification bar with the current notification."""
        emoji, text = self.notifications[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)

        # Dynamically adjust the width of the content frame
        self.adjust_frame_width()

    def adjust_frame_width(self):
        """
        Adjust the width of the content frame based on the text and emoji.
        """
        # Calculate the width of the emoji label
        emoji_metrics = QFontMetrics(self.label_emoji.font())
        emoji_width = emoji_metrics.width(self.label_emoji.text())

        # Calculate the width of the text label
        text_metrics = QFontMetrics(self.label_text.font())
        text_width = text_metrics.width(self.label_text.text())

        # Add spacing and padding
        total_width = emoji_width + text_width + 20  # Add some padding

        # Set the new width for the content frame
        frame_height = self.content_frame.height()
        self.content_frame.setFixedWidth(total_width)

    def start_timer(self):
        """Start the timer to cycle through notifications."""
        self.timer.start(10000)  # Change notification every 10 seconds

    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()

    def reset_timer(self):
        self.stop_timer()
        self.start_timer()

    def next_notification(self):
        """Move to the next notification."""
        self.animate_notification(direction="up")
        self.reset_timer()

    def previous_notification(self):
        """Move to the previous notification."""
        self.animate_notification(direction="down")
        self.reset_timer()

    def add_notification(self, emoji, message):
        """Add a new notification to the list."""
        self.notifications.append((emoji, message))

    def remove_notification(self, index):
        """Remove a notification from the list."""
        if 0 <= index < len(self.notifications):
            self.notifications.pop(index)

    def animate_notification(self, direction):
        """
        Animate the transition to the next or previous notification.
        :param direction: "up" for next notification, "down" for previous notification.
        """
        # Create animations for sliding out and sliding in (for the content frame)
        self.slide_out_animation = QPropertyAnimation(self.content_frame, b"geometry")
        self.slide_in_animation = QPropertyAnimation(self.content_frame, b"geometry")

        # Get the current geometry of the content frame
        frame_geometry = self.content_frame.geometry()

        # Slide out: Move the content frame upward or downward based on direction
        self.slide_out_animation.setDuration(self.animation_duration)
        self.slide_out_animation.setStartValue(frame_geometry)

        if direction == "up":
            # Slide up: Move the frame upward
            self.slide_out_animation.setEndValue(
                QRect(frame_geometry.x(), frame_geometry.y() - frame_geometry.height(),
                      frame_geometry.width(), frame_geometry.height())
            )
        elif direction == "down":
            # Slide down: Move the frame downward
            self.slide_out_animation.setEndValue(
                QRect(frame_geometry.x(), frame_geometry.y() + frame_geometry.height(),
                      frame_geometry.width(), frame_geometry.height())
            )

        self.slide_out_animation.setEasingCurve(QEasingCurve.OutQuad)

        # Update to the next or previous notification
        if direction == "up":
            self.current_index = (self.current_index + 1) % len(self.notifications)
        elif direction == "down":
            self.current_index = (self.current_index - 1) % len(self.notifications)
        self.update_notification()

        # Slide in: Move the content frame back into view
        self.slide_in_animation.setDuration(self.animation_duration)

        if direction == "up":
            # Slide in from below for "up" direction
            self.slide_in_animation.setStartValue(
                QRect(frame_geometry.x(), frame_geometry.y() + frame_geometry.height(),
                      frame_geometry.width(), frame_geometry.height())
            )
        elif direction == "down":
            # Slide in from above for "down" direction
            self.slide_in_animation.setStartValue(
                QRect(frame_geometry.x(), frame_geometry.y() - frame_geometry.height(),
                      frame_geometry.width(), frame_geometry.height())
            )

        self.slide_in_animation.setEndValue(frame_geometry)
        self.slide_in_animation.setEasingCurve(QEasingCurve.InQuad)

        # Connect animations and start
        self.slide_out_animation.finished.connect(self.slide_in_animation.start)
        self.slide_out_animation.start()
