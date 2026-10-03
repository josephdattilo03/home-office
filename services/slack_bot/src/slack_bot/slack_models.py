from typing import Any, Literal

from pydantic import BaseModel


class AppMentionEvent(BaseModel):
    """Incoming `app_mention` event: what `handle_mention` receives as `event`."""

    type: Literal["app_mention"]
    user: str
    text: str
    ts: str
    channel: str
    team: str | None = None
    thread_ts: str | None = None
    blocks: list[dict[str, Any]] = []


class BotProfile(BaseModel):
    id: str
    app_id: str
    user_id: str
    name: str
    team_id: str
    deleted: bool = False


class MessageEvent(BaseModel):
    """Incoming `message` event: what `handle_message` receives as `event`."""

    type: Literal["message"]
    channel: str
    ts: str
    event_ts: str | None = None
    user: str | None = None  # absent on some subtypes (e.g. message_changed)
    text: str = ""
    channel_type: Literal["im", "channel", "group", "mpim"] | None = None
    subtype: str | None = None  # None for a plain new message
    thread_ts: str | None = None
    team: str | None = None
    bot_id: str | None = None  # set when a bot posted it
    bot_profile: BotProfile | None = None
    blocks: list[dict[str, Any]] = []


class PostedMessage(BaseModel):
    """The `message` object inside a chat.postMessage response."""

    type: Literal["message"]
    user: str
    text: str
    ts: str
    bot_id: str | None = None
    app_id: str | None = None
    team: str | None = None
    bot_profile: BotProfile | None = None
    thread_ts: str | None = None
    parent_user_id: str | None = None
    blocks: list[dict[str, Any]] = []


class PostMessageResponse(BaseModel):
    """Body returned by chat.postMessage (what `say(...)` returns)."""

    ok: bool
    channel: str
    ts: str
    message: PostedMessage


class SlashCommand(BaseModel):
    """Slash command invocation: what `handle_hello` receives as `command`."""

    command: str
    text: str = ""
    user_id: str
    user_name: str
    channel_id: str
    channel_name: str
    team_id: str
    team_domain: str
    api_app_id: str
    is_enterprise_install: bool = False
    enterprise_id: str | None = None
    response_url: str
    trigger_id: str
