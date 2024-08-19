from dataclasses import dataclass, field
from typing import List, Optional


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
class Data:
    text: str


@dataclass
class KakaoBotChatResponse:
    version: str = field(default="2.0")
    useCallback: Optional[bool] = None
    data: Optional[Data] = None
    template: Optional[Template] = None
