from dataclasses import dataclass, field
from typing import Optional, Dict, Any

from app.models.schemas.chat import ChatRequest


@dataclass
class Intent:
    id: str
    name: str


@dataclass
class User:
    id: str
    type: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Block:
    id: str
    name: str


@dataclass
class UserRequest:
    callbackUrl: Optional[str]
    timezone: str
    params: Dict[str, str]
    block: Block
    utterance: str  # 사용자 발화
    lang: Optional[str]
    user: User


@dataclass
class Bot:
    id: str
    name: str


@dataclass
class Action:
    name: str
    clientExtra: Optional[Any]
    params: Dict[str, Any]
    id: str
    detailParams: Dict[str, Any]


@dataclass
class KakaoBotChatRequest:
    intent: Intent
    userRequest: UserRequest
    bot: Bot
    action: Action

    def to_chat_request(self, collection="embeddings", model="solar-1-mini-chat") -> ChatRequest:
        return ChatRequest(messages=[self.userRequest.utterance], collection=collection, model=model)
