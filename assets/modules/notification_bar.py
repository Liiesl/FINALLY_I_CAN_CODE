# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

class NotificationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)
        self.current_index = 0
        self.notifications = [
            ("💡", "Tip: You can merge multiple SRT files into one."),
            ("🎉", "New Feature: Try out the Multilingual Merge tool!"),
            ("⏰", "Reminder: You last used the Subtitle Shifter 2 days ago."),
            ("📰", "News: Check out our latest blog post on subtitle editing!")
        ]
        self.label_emoji = QLabel()
        self.label_text = QLabel()
        self.label_emoji.setStyleSheet("font-size: 20px;")
        self.label_text.setStyleSheet("color: white; background-color: #333; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.label_emoji)
        self.layout.addWidget(self.label_text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_notification)
        self.start_timer()

    def start_timer(self):
        """Start the timer to cycle through notifications."""
        self.update_notification()  # Show the first notification immediately
        self.timer.start(10000)  # Change notification every 10 seconds

    def update_notification(self):
        """Update the notification bar with the next notification."""
        emoji, text = self.notifications[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)
        self.current_index = (self.current_index + 1) % len(self.notifications)

    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()

    def add_notification(self, emoji, message):
        """Add a new notification to the list."""
        self.notifications.append((emoji, message))

    def remove_notification(self, index):
        """Remove a notification from the list."""
        if 0 <= index < len(self.notifications):
            self.notifications.pop(index)
