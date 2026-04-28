from collections.abc import Iterable, Mapping
from typing import Any

from matrix_sidecar_search.permissions import filter_visible_documents
from matrix_sidecar_search.redactions import apply_redactions


def sanitize_results(
    documents: Iterable[Mapping[str, Any]],
    *,
    redacted_event_ids: set[str],
    visible_event_ids: set[str],
) -> list[dict[str, Any]]:
    """Apply the mandatory safety filters before any result is returned."""

    unredacted = apply_redactions(documents, redacted_event_ids=redacted_event_ids)
    return filter_visible_documents(unredacted, visible_event_ids=visible_event_ids)
