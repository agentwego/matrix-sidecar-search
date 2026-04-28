from matrix_sidecar_search.database import SynapseEventRow
from matrix_sidecar_search.indexer import IndexerCursor
from matrix_sidecar_search.runner import IndexerRunResult, run_index_once


class FakeSynapseReader:
    def __init__(self) -> None:
        self.seen_cursor = None
        self.seen_limit = None

    async def fetch_events_after(self, cursor: IndexerCursor, *, limit: int):
        self.seen_cursor = cursor
        self.seen_limit = limit
        return [
            SynapseEventRow(
                stream_ordering=7,
                event_id="$event:example.org",
                room_id="!room:example.org",
                sender="@alice:example.org",
                event_type="m.room.message",
                origin_server_ts=123,
                event_json={"content": {"body": "hello"}},
            )
        ]


class FakeMeiliWriter:
    def __init__(self) -> None:
        self.documents = None

    async def add_documents(self, documents):
        self.documents = list(documents)


async def test_run_index_once_reads_writes_and_advances_cursor() -> None:
    reader = FakeSynapseReader()
    writer = FakeMeiliWriter()

    result = await run_index_once(
        reader,
        writer,
        cursor=IndexerCursor(last_stream_ordering=3),
        batch_size=100,
    )

    assert reader.seen_cursor == IndexerCursor(last_stream_ordering=3)
    assert reader.seen_limit == 100
    assert writer.documents is not None
    assert writer.documents[0]["event_id"] == "$event:example.org"
    assert result == IndexerRunResult(fetched=1, indexed=1, cursor=IndexerCursor(7))
