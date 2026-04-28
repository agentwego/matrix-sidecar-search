from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from matrix_sidecar_search.database import SynapseEventRow


@dataclass(frozen=True, slots=True)
class IndexerCursor:
    last_stream_ordering: int = 0


def document_from_row(row: SynapseEventRow) -> dict[str, Any] | None:
    """Convert a Synapse event row into a Meilisearch document."""

    if row.redacts:
        return None

    content = row.event_json.get("content", {})
    body = content.get("body")
    if not isinstance(body, str) or not body.strip():
        return None

    return {
        "id": row.event_id,
        "event_id": row.event_id,
        "room_id": row.room_id,
        "sender": row.sender,
        "type": row.event_type,
        "origin_server_ts": row.origin_server_ts,
        "stream_ordering": row.stream_ordering,
        "body": body,
        "msgtype": content.get("msgtype"),
    }


def documents_from_rows(rows: Iterable[SynapseEventRow]) -> list[dict[str, Any]]:
    """Convert Synapse rows into safe indexable documents."""

    documents: list[dict[str, Any]] = []
    for row in rows:
        document = document_from_row(row)
        if document is not None:
            documents.append(document)
    return documents


def next_cursor(cursor: IndexerCursor, documents: Iterable[Mapping[str, Any]]) -> IndexerCursor:
    """Advance the cursor to the largest indexed stream ordering."""

    largest = cursor.last_stream_ordering
    for document in documents:
        stream_ordering = int(document.get("stream_ordering", largest))
        largest = max(largest, stream_ordering)
    return IndexerCursor(last_stream_ordering=largest)
