from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LinkIngestRequest(BaseModel):
    id: str
    url: HttpUrl
    channel: str
    ts: str
    thread_ts: str | None
    user: str | None
    received_at: datetime
