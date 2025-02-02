# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette
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
            border: 2px solid {self.text_color};  /* Add a visible border */
            border-radius: 5px;
        }}
        """)

        # Timer for automatic notifications
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_notification)
        self.start_timer()
        
        self.update_notification()  # Initialize with the first notification

    def update_notification(self):
        """Update the notification bar with the current notification."""
        emoji, text = self.notifications[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)

        # Trigger slide-up animation
        self.slide_up_animation()

    def start_timer(self):
        """Start the timer to cycle through notifications."""
        self.timer.start(10000)  # Change notification every 10 seconds
        
    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()

    def slide_up_animation(self):
        """Perform a slide-up animation for the notification bar."""
        # Create a property animation for the geometry of the widget
        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(300)  # Duration of the animation in milliseconds

        # Get the current geometry of the widget
        current_geometry = self.geometry()

        # Define the start and end positions for the animation
        start_pos = QRect(current_geometry.x(), current_geometry.y(), current_geometry.width(), current_geometry.height())
        end_pos = QRect(current_geometry.x(), current_geometry.y() - 20, current_geometry.width(), current_geometry.height())

        # Set the animation keyframes
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)

        # Start the animation
        animation.start()

    def next_notification(self):
        """Move to the next notification."""
        self.current_index = (self.current_index + 1) % len(self.notifications)
        self.update_notification()
        self.slide_up_animation()

    def previous_notification(self):
        """Move to the previous notification."""
        self.current_index = (self.current_index - 1) % len(self.notifications)
        self.update_notification()

    def add_notification(self, emoji, message):
        """Add a new notification to the list."""
        self.notifications.append((emoji, message))

    def remove_notification(self, index):
        """Remove a notification from the list."""
        if 0 <= index < len(self.notifications):
            self.notifications.pop(index)
