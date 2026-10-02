import logging
import os

from slack_bolt import App

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)


@app.event("app_mention")
def handle_mention(event, say):
    """Reply in a thread when someone @mentions the bot."""
    thread_ts = event.get("thread_ts") or event["ts"]
    say(text=f"Hi <@{event['user']}>, you said: {event['text']}", thread_ts=thread_ts)


@app.event("message")
def handle_message(event, say):
    """Echo direct messages. Ignores bots, edits, and channel messages."""
    if event.get("channel_type") != "im":
        return
    if event.get("bot_id") or event.get("subtype"):
        return
    say(f"You said: {event.get('text', '')}")


@app.command("/hello")
def handle_hello(ack, respond, command):
    """Slash command. Must ack within 3 seconds."""
    ack()
    respond(f"Hello <@{command['user_id']}>!")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
