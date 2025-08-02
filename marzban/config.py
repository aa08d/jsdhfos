from dataclasses import dataclass


@dataclass
class MarzbanConfig:
    url: str
    username: str
    password: str
