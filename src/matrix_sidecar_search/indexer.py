from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class IndexerCursor:
    last_stream_ordering: int = 0


def next_cursor(cursor: IndexerCursor, documents: Iterable[Mapping[str, Any]]) -> IndexerCursor:
    """Advance the cursor to the largest indexed stream ordering."""

    largest = cursor.last_stream_ordering
    for document in documents:
        stream_ordering = int(document.get("stream_ordering", largest))
        largest = max(largest, stream_ordering)
    return IndexerCursor(last_stream_ordering=largest)
