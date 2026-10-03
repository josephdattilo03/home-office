import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_bot.slack_models import (
    AppMentionEvent,
    MessageEvent,
    PostMessageResponse,
    SlashCommand,
)
from slack_bot.utils import is_link

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def handle_mention(event, say):
    """Reply in a thread when someone @mentions the bot."""
    mention = AppMentionEvent.model_validate(event)
    resp = say(
        text=f"Hi <@{mention.user}>, you said: {mention.text}",
        thread_ts=mention.thread_ts or mention.ts,
    )
    posted = PostMessageResponse.model_validate(resp.data)
    logger.info("replied in %s at ts=%s", posted.channel, posted.ts)


@app.event("message")
def handle_direct_message(event, say):
    """Echo direct messages. Ignores bots, edits, and channel messages."""
    msg = MessageEvent.model_validate(event)
    if msg.channel_type != "im":
        return
    if msg.bot_id or msg.subtype:
        return
    say(f"You said: {msg.text}")


@app.message(matchers=[is_link])
def handle_links(message, say, logger):
    resp = say("This message was a link!")


@app.command("/hello")
def handle_hello(ack, respond, command):
    """Slash command. Must ack within 3 seconds."""
    ack()
    cmd = SlashCommand.model_validate(command)
    respond(f"Hello <@{cmd.user_id}>!")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
