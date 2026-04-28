from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SynapseEventRow:
    stream_ordering: int
    event_id: str
    room_id: str
    sender: str
    event_type: str
    origin_server_ts: int
    event_json: dict[str, Any]
    redacts: str | None = None


def build_events_query() -> str:
    """Build the incremental read query for Synapse events.

    The query is intentionally read-only and cursor based so it can run against
    the CNPG read-only pooler. Redactions are joined in the same snapshot so the
    indexer can avoid publishing already-redacted events.
    """

    return """
        select
            e.stream_ordering,
            e.event_id,
            e.room_id,
            e.sender,
            e.type as event_type,
            e.origin_server_ts,
            ej.json as event_json,
            r.redacts
        from events e
        join event_json ej on ej.event_id = e.event_id
        left join redactions r on r.redacts = e.event_id
        where e.stream_ordering > $1
          and e.type = 'm.room.message'
        order by e.stream_ordering asc
        limit $2
    """


def row_from_record(record: Any) -> SynapseEventRow:
    """Convert an asyncpg Record or mapping-like row into a typed event row."""

    return SynapseEventRow(
        stream_ordering=int(record["stream_ordering"]),
        event_id=str(record["event_id"]),
        room_id=str(record["room_id"]),
        sender=str(record["sender"]),
        event_type=str(record["event_type"]),
        origin_server_ts=int(record["origin_server_ts"]),
        event_json=dict(record["event_json"]),
        redacts=record["redacts"],
    )
