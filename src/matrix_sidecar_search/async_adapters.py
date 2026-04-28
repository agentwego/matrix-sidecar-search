from __future__ import annotations

from typing import Any

from matrix_sidecar_search.database import build_events_query, row_from_record
from matrix_sidecar_search.indexer import IndexerCursor


class SynapseEventReader:
    def __init__(self, connection: Any) -> None:
        self.connection = connection

    async def fetch_events_after(self, cursor: IndexerCursor, *, limit: int) -> list:
        records = await self.connection.fetch(
            build_events_query(),
            cursor.last_stream_ordering,
            limit,
        )
        return [row_from_record(record) for record in records]


class MeiliDocumentWriter:
    def __init__(self, index: Any) -> None:
        self.index = index

    async def add_documents(self, documents: list[dict]) -> None:
        await self.index.add_documents(documents, primary_key="id")
