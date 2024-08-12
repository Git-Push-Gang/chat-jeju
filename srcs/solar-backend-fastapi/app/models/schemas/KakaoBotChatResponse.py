from dataclasses import dataclass
from typing import List


@dataclass
class SimpleText:
    text: str


@dataclass
class Output:
    simpleText: SimpleText


@dataclass
class Template:
    outputs: List[Output]


@dataclass
class KakaoBotChatResponse:
    version: str
    template: Template
