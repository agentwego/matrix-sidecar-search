from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from matrix_sidecar_search.indexer import IndexerCursor, documents_from_rows, next_cursor


class SynapseReader(Protocol):
    async def fetch_events_after(
        self,
        cursor: IndexerCursor,
        *,
        limit: int,
    ) -> list:
        """Fetch Synapse events after the provided cursor."""


class MeiliWriter(Protocol):
    async def add_documents(self, documents: list[dict]) -> None:
        """Add documents to the search index."""


@dataclass(frozen=True, slots=True)
class IndexerRunResult:
    fetched: int
    indexed: int
    cursor: IndexerCursor


async def run_index_once(
    reader: SynapseReader,
    writer: MeiliWriter,
    *,
    cursor: IndexerCursor,
    batch_size: int,
) -> IndexerRunResult:
    """Run one incremental indexing batch."""

    rows = await reader.fetch_events_after(cursor, limit=batch_size)
    documents = documents_from_rows(rows)
    if documents:
        await writer.add_documents(documents)
    return IndexerRunResult(
        fetched=len(rows),
        indexed=len(documents),
        cursor=next_cursor(cursor, documents),
    )
