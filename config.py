import json
import os

class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        self.data = {
            "safe_area_size": 0,
            "text_size": "small"  # Default text size
        }
        self.load()

    def load(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                self.data = json.load(file)

    def save(self):
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_safe_area_size(self):
        return self.data.get("safe_area_size", 0)

    def set_safe_area_size(self, size):
        self.data["safe_area_size"] = size
        self.save()

    def get_text_size(self):
        return self.data.get("text_size", "small")

    def set_text_size(self, size):
        self.data["text_size"] = size
        self.save()
