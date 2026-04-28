from matrix_sidecar_search.async_adapters import MeiliDocumentWriter, SynapseEventReader
from matrix_sidecar_search.indexer import IndexerCursor


class FakeConnection:
    def __init__(self) -> None:
        self.query = None
        self.cursor_value = None
        self.limit = None

    async def fetch(self, query, cursor_value, limit):
        self.query = query
        self.cursor_value = cursor_value
        self.limit = limit
        return []


class FakeIndex:
    def __init__(self) -> None:
        self.documents = None
        self.primary_key = None

    async def add_documents(self, documents, primary_key="id"):
        self.documents = documents
        self.primary_key = primary_key


async def test_synapse_event_reader_uses_cursor_and_limit() -> None:
    connection = FakeConnection()
    reader = SynapseEventReader(connection)

    rows = await reader.fetch_events_after(IndexerCursor(11), limit=50)

    assert rows == []
    assert "stream_ordering > $1" in connection.query
    assert connection.cursor_value == 11
    assert connection.limit == 50


async def test_meili_document_writer_uses_stable_primary_key() -> None:
    index = FakeIndex()
    writer = MeiliDocumentWriter(index)

    await writer.add_documents([{"id": "$event"}])

    assert index.documents == [{"id": "$event"}]
    assert index.primary_key == "id"
