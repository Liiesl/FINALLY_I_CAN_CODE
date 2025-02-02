# notification_bar.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer

class NotificationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(10)
        self.current_index = 0
        self.tips = [
            ("💡", "Tip: You can merge multiple SRT files into one."),
            ("⏰", "Tip: Use the Subtitle Shifter to adjust timing."),
            ("🔄", "Tip: Convert subtitles between different formats."),
            ("🌐", "Tip: Merge subtitles in different languages with colors."),
        ]
        self.label_emoji = QLabel()
        self.label_text = QLabel()
        self.label_emoji.setStyleSheet("font-size: 20px;")
        self.label_text.setStyleSheet("color: white; background-color: #333; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.label_emoji)
        self.layout.addWidget(self.label_text)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tip)
        self.start_timer()

    def start_timer(self):
        """Start the timer to cycle through tips."""
        self.update_tip()  # Show the first tip immediately
        self.timer.start(10000)  # Change tip every 10 seconds

    def update_tip(self):
        """Update the notification bar with the next tip."""
        emoji, text = self.tips[self.current_index]
        self.label_emoji.setText(emoji)
        self.label_text.setText(text)
        self.current_index = (self.current_index + 1) % len(self.tips)

    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()
