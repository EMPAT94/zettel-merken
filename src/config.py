import os, json
from pathlib import Path


class Email:
    """Email object in config containing sender details."""

    USER: str
    PASS: str
    HOST: str
    PORT: int

    def __init__(self, email) -> None:
        self.USER = email["USER"]
        self.PASS = email["PASS"]
        self.HOST = email["HOST"]
        self.PORT = email["PORT"]


class Config:
    """Config object build from config.json."""

    NOTE_DIRS: list[str]
    EMAIL: Email
    RECEIVERS: list[str]
    DB_PATH: str
    SCHEDULE_DAYS: list[int]
    MAX_NOTES_PER_MAIL: int
    IGNORE_FILES: list[str]
    IGNORE_DIRS: list[str]
    INCLUDE_EXT: list[str]

    def __init__(self, config) -> None:
        self.NOTE_DIRS = config["NOTE_DIRS"]
        self.EMAIL = Email(config["EMAIL"])
        self.RECEIVERS = config["RECEIVERS"]
        self.DB_PATH = config["DB_PATH"]
        self.SCHEDULE_DAYS = config["SCHEDULE_DAYS"]
        self.MAX_NOTES_PER_MAIL = config["MAX_NOTES_PER_MAIL"]
        self.IGNORE_FILES = config["IGNORE_FILES"]
        self.IGNORE_DIRS = config["IGNORE_DIRS"]
        self.INCLUDE_EXT = config["INCLUDE_EXT"]


def get_app_path() -> Path:
    """Returns either ~/.config/zettel_merken or ~/zettel_merken if .config not found."""
    home = Path("~").expanduser()

    if (home / ".config").exists():
        app_path = home / ".config" / "zettel_merken"
    else:
        app_path = home / "zettel_merken"

    if not app_path.exists():
        os.mkdir(app_path)

    return app_path


class ConfigNotFound(BaseException):
    pass


def get_config(app_path: Path) -> Config:
    """Parses file config.json into Config class."""
    config_file = app_path / "config.json"

    if not config_file.exists():
        raise ConfigNotFound("Config file not found.")

    with open(config_file) as config:
        return Config(json.load(config))
