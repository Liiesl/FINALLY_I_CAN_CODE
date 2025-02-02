# assets/modules/notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
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

        # Get the highlight color from the parent widget's palette
        palette = self.parent().palette() if self.parent() else QPalette()
        self.highlight_color = palette.color(QPalette.Highlight).name()

        # Left Arrow Button
        self.left_arrow = QPushButton()
        self.left_arrow.setIcon(qta.icon('fa5s.angle-left', color='black'))  # Use QtAwesome icon
        self.left_arrow.setStyleSheet("background-color: transparent; border: none;")
        self.left_arrow.clicked.connect(self.previous_notification)
        self.layout.addWidget(self.left_arrow)

        # Emoji Label
        self.label_emoji = QLabel()
        self.label_emoji.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(self.label_emoji)

        # Text Label
        self.label_text = QLabel()
        self.label_text.setStyleSheet("color: black; padding: 5px;")
        self.layout.addWidget(self.label_text)

        # Right Arrow Button
        self.right_arrow = QPushButton()
        self.right_arrow.setIcon(qta.icon('fa5s.angle-right', color='black'))  # Use QtAwesome icon
        self.right_arrow.setStyleSheet("background-color: transparent; border: none;")
        self.right_arrow.clicked.connect(self.next_notification)
        self.layout.addWidget(self.right_arrow)

        # Set background color of the entire widget using the highlight color
        self.setStyleSheet(f"""
            NotificationBar {{
                background-color: {self.highlight_color};
                border: 1px solid #ccc;
                border-radius: 5px;
            }}
        """)

        # Initialize with the first notification
        self.update_notification()

    def update_notification(self):
        """Update the notification bar with the current notification."""
        emoji, text = self.notifications[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)

    def next_notification(self):
        """Move to the next notification."""
        self.current_index = (self.current_index + 1) % len(self.notifications)
        self.update_notification()

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
