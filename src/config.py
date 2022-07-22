import json

from dataclasses import dataclass, field
from pathlib import Path


class ConfigNotFound(BaseException):
    pass


@dataclass(frozen=True)
class Config:
    """Config object build from config.json"""

    @dataclass(frozen=True)
    class Email:
        USER: str
        PASS: str = field(repr=False)
        HOST: str
        PORT: int

    NOTE_DIRS: list[str]
    EMAIL: Email
    RECEIVERS: list[str]
    SCHEDULE_DAYS: list[int]
    MAX_NOTES_PER_MAIL: int
    IGNORE_FILES: list[str]
    IGNORE_DIRS: list[str]
    INCLUDE_EXT: list[str]


def get_config(config_file: Path) -> Config:
    """Parses file config.json into Config class."""

    if not config_file.exists():
        raise ConfigNotFound(f"Config file not found at {config_file}")

    with open(config_file) as f:
        config = json.load(f)
        email = config["EMAIL"]
        del config["EMAIL"]
        return Config(**config, EMAIL=Config.Email(**email))
