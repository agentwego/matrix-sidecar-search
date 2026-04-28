from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class MatrixEvent:
    stream_ordering: int
    event_id: str
    room_id: str
    sender: str
    origin_server_ts: int
    event_type: str
    content: dict[str, Any]


def extract_searchable_text(event: MatrixEvent) -> str:
    """Extract text that is safe and useful for full-text recall."""

    if event.event_type != "m.room.message":
        return ""

    body = event.content.get("body")
    if not isinstance(body, str):
        return ""
    return body


def to_meili_document(event: MatrixEvent) -> dict[str, Any]:
    """Map a Synapse event row into a stable Meilisearch document."""

    return {
        "id": event.event_id,
        "event_id": event.event_id,
        "room_id": event.room_id,
        "sender": event.sender,
        "origin_server_ts": event.origin_server_ts,
        "event_type": event.event_type,
        "stream_ordering": event.stream_ordering,
        "text": extract_searchable_text(event),
    }
