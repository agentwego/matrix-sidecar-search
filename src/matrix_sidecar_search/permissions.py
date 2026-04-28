from collections.abc import Iterable, Mapping
from typing import Any


def filter_visible_documents(
    documents: Iterable[Mapping[str, Any]], *, visible_event_ids: set[str]
) -> list[dict[str, Any]]:
    """Deny by default and keep only events proven visible by Synapse-derived checks."""

    return [
        dict(document) for document in documents if str(document.get("id")) in visible_event_ids
    ]
