from collections.abc import Iterable, Mapping
from typing import Any


def apply_redactions(
    documents: Iterable[Mapping[str, Any]], *, redacted_event_ids: set[str]
) -> list[dict[str, Any]]:
    """Remove redacted events from user-facing or index-bound documents."""

    return [
        dict(document)
        for document in documents
        if str(document.get("id")) not in redacted_event_ids
    ]
