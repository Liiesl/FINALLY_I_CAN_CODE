import os
import json

class Config:
    CONFIG_PATH = "config.json"

    def __init__(self):
        self.config_data = self.load_config()

    def load_config(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "r") as file:
                return json.load(file)
        return {}

    def save_config(self):
        with open(self.CONFIG_PATH, "w") as file:
            json.dump(self.config_data, file, indent=4)

    def get_safe_area_size(self):
        return self.config_data.get("safe_area_size", 20)

    def set_safe_area_size(self, size):
        self.config_data["safe_area_size"] = size
        self.save_config()

    def get_text_size(self):
        return self.config_data.get("text_size", "default")

    def set_text_size(self, size):
        self.config_data["text_size"] = size
        self.save_config()

    def get_default_save_directory(self):
        return self.config_data.get("default_save_directory", os.path.expanduser("~"))

    def set_default_save_directory(self, directory):
        self.config_data["default_save_directory"] = directory
        self.save_config()
