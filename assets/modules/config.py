import json
import os

class Config:
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
    
    def __init__(self, source=None):
        self.data = {
            "safe_area_size": 0,
            "text_size": "small",  # Default text size
            "theme": "dark",       # Default theme
            "recent_tools": [],    # Default recent tools
            "tool_usage": {}       # Default tool usage
        }
        self.source = source
        self.load()

    def load(self):
        """Load configuration data from the config file."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as file:
                    loaded_data = json.load(file)
                
                # Validate loaded data
                if not isinstance(loaded_data, dict):
                    raise ValueError("Invalid config file: Root element must be a dictionary.")
                
                # Merge loaded data with defaults to ensure no keys are missing
                self.data.update(loaded_data)
            
            except json.JSONDecodeError as decode_error:
                print(f"Failed to decode JSON: {decode_error}. Using default values.")
            except ValueError as ve:
                print(f"Validation error: {ve}. Using default values.")
        else:
            print("Config file does not exist, using default values.")

        if self.source:
            print(f"Config loaded by {self.source}: {self.data}")
        else:
            print(f"Config loaded: {self.data}")
    def save(self):
        """Save configuration data to the config file."""
        try:
            with open(self.CONFIG_FILE, "w") as file:
                json.dump(self.data, file, indent=4)
                file.flush()  # Ensure data is written to disk
                os.fsync(file.fileno())  # Ensure file is fully written and closed
            
            if self.source:
                print(f"Config saved by {self.source}: {self.data}")
            else:
                print(f"Config saved: {self.data}")
        
        except Exception as e:
            print(f"Failed to save config file: {e}")

    def get_safe_area_size(self):
        return self.data.get("safe_area_size", 0)

    def set_safe_area_size(self, size):
        if not isinstance(size, int):
            raise ValueError(f"Invalid type for safe_area_size: Expected int, got {type(size).__name__}")
        self.data["safe_area_size"] = size
        self.save()

    def get_text_size(self):
        return self.data.get("text_size", "small")

    def set_text_size(self, size):
        if not isinstance(size, str):
            raise ValueError(f"Invalid type for text_size: Expected str, got {type(size).__name__}")
        self.data["text_size"] = size
        self.save()

    def get_theme(self):
        return self.data.get("theme", "dark")

    def set_theme(self, theme):
        if not isinstance(theme, str):
            raise ValueError(f"Invalid type for theme: Expected str, got {type(theme).__name__}")
        self.data["theme"] = theme
        self.save()

    def get_tool_usage(self):
        return self.data.get("tool_usage", {})

    def set_tool_usage(self, tool_usage):
        if not isinstance(tool_usage, dict):
            raise ValueError(f"Invalid type for tool_usage: Expected dict, got {type(tool_usage).__name__}")
        self.data["tool_usage"] = tool_usage
        self.save()

    def get_recent_tools(self):
        return self.data.get("recent_tools", [])

    def set_recent_tools(self, recent_tools):
        if not isinstance(recent_tools, list):
            raise ValueError(f"Invalid type for recent_tools: Expected list, got {type(recent_tools).__name__}")
        self.data["recent_tools"] = recent_tools
        self.save()
