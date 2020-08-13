import yaml
from pathlib import Path


class Config:
    def __init__(self, filename="config.yaml"):
        CONFIG = yaml.safe_load((Path(__file__).parent / filename).open())

        self.IGNORE_FILE = CONFIG.get("ignore_file")
        self.IGNORED_FILES = CONFIG.get("ignore", [])

        self.AUTHOR = CONFIG.get("author", "")
        self.CACHE_CONFIG = {
            "DEBUG": CONFIG.get("cache").get("debug"),
            "CACHE_TYPE": "filesystem",  # Flask-Caching related configs
            "CACHE_DEFAULT_TIMEOUT": int(CONFIG.get("cache").get("timeout")),
            "CACHE_DIR": CONFIG.get("cache").get("dir"),
        }
