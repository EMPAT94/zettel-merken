import json

from dataclasses import dataclass, field
from pathlib import Path


class ConfigNotFound(Exception):
    pass


@dataclass
class Config:
    """Config object build from config.json"""

    @dataclass
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

    def __post_init__(self):
        self.EMAIL = Config.Email(**self.EMAIL)

    def load_from_file(config_file: Path):
        """Parses file config.json into Config class."""

        if not config_file.exists():
            raise ConfigNotFound

        with open(config_file) as f:
            return Config(**json.load(f))
