from matrix_sidecar_search.database import SynapseEventRow, build_events_query
from matrix_sidecar_search.indexer import documents_from_rows


def test_build_events_query_reads_after_cursor_with_limit() -> None:
    query = build_events_query()

    assert "e.stream_ordering > $1" in query
    assert "limit $2" in query.lower()
    assert "event_json" in query
    assert "left join redactions" in query.lower()


def test_documents_from_rows_extracts_message_content() -> None:
    rows = [
        SynapseEventRow(
            stream_ordering=42,
            event_id="$event:example.org",
            room_id="!room:example.org",
            sender="@alice:example.org",
            event_type="m.room.message",
            origin_server_ts=1_700_000_000,
            event_json={
                "content": {
                    "body": "你好，Matrix 搜索",
                    "msgtype": "m.text",
                }
            },
            redacts=None,
        )
    ]

    docs = documents_from_rows(rows)

    assert docs == [
        {
            "id": "$event:example.org",
            "event_id": "$event:example.org",
            "room_id": "!room:example.org",
            "sender": "@alice:example.org",
            "type": "m.room.message",
            "origin_server_ts": 1_700_000_000,
            "stream_ordering": 42,
            "body": "你好，Matrix 搜索",
            "msgtype": "m.text",
        }
    ]


def test_documents_from_rows_skips_redacted_or_empty_events() -> None:
    rows = [
        SynapseEventRow(
            stream_ordering=1,
            event_id="$redacted:example.org",
            room_id="!room:example.org",
            sender="@alice:example.org",
            event_type="m.room.message",
            origin_server_ts=1,
            event_json={"content": {"body": "secret"}},
            redacts="$redacted:example.org",
        ),
        SynapseEventRow(
            stream_ordering=2,
            event_id="$empty:example.org",
            room_id="!room:example.org",
            sender="@alice:example.org",
            event_type="m.room.message",
            origin_server_ts=2,
            event_json={"content": {}},
            redacts=None,
        ),
    ]

    assert documents_from_rows(rows) == []
