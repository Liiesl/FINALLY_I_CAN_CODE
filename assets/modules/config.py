import json
import os

class Config:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

    def __init__(self, source=None):
        # Default configuration values
        self.data = {
            "safe_area_size": 0,
            "text_size": "small",  # Default text size
            "theme": "dark",       # Default theme
            "tool_usage": {},      # Tracks tool usage frequency
            "recent_tools": [],    # Tracks recently used tools
            "experimental_tools_enabled": False  # New setting for experimental tools
        }
        self.source = source
        self.load()

    def load(self):
        """Load the configuration from the config file."""
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as file:
                self.data = json.load(file)
                # Ensure the new key exists in the loaded data
                self.data.setdefault("experimental_tools_enabled", False)
            if self.source:
                print(f"Config loaded by {self.source}: {self.data}")  # Debug print
            else:
                print(f"Config loaded: {self.data}")  # Debug print
        else:
            if self.source:
                print(f"Config file does not exist, using default values. Loaded by {self.source}")  # Debug print
            else:
                print("Config file does not exist, using default values.")  # Debug print

    def save(self):
        """Save the current configuration to the config file."""
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(self.data, file, indent=4)
            file.flush()  # Ensure data is written to disk
            os.fsync(file.fileno())  # Ensure file is fully written and closed
        if self.source:
            print(f"Config saved by {self.source}: {self.data}")  # Debug print
        else:
            print(f"Config saved: {self.data}")  # Debug print

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

    def get_theme(self):
        return self.data.get("theme", "dark")

    def set_theme(self, theme):
        self.data["theme"] = theme
        self.save()

    def get_tool_usage(self):
        return self.data.get("tool_usage", {})

    def set_tool_usage(self, tool_usage):
        self.data["tool_usage"] = tool_usage
        self.save()

    def get_recent_tools(self):
        return self.data.get("recent_tools", [])

    def set_recent_tools(self, recent_tools):
        self.data["recent_tools"] = recent_tools
        self.save()

    # New methods for experimental tools toggle
    def get_experimental_tools_enabled(self):
        """Get the state of the experimental tools toggle."""
        return self.data.get("experimental_tools_enabled", False)

    def set_experimental_tools_enabled(self, enabled):
        """Set the state of the experimental tools toggle."""
        self.data["experimental_tools_enabled"] = enabled
        self.save()
