from matrix_sidecar_search.meili import MatrixEvent, to_meili_document


def test_event_maps_to_stable_meili_document():
    event = MatrixEvent(
        stream_ordering=42,
        event_id="$event:example.org",
        room_id="!room:example.org",
        sender="@alice:example.org",
        origin_server_ts=1_700_000_000_000,
        event_type="m.room.message",
        content={"body": "你好，数据库", "msgtype": "m.text"},
    )

    doc = to_meili_document(event)

    assert doc["id"] == "$event:example.org"
    assert doc["room_id"] == "!room:example.org"
    assert doc["sender"] == "@alice:example.org"
    assert doc["text"] == "你好，数据库"
    assert doc["stream_ordering"] == 42


def test_non_text_event_has_empty_text():
    event = MatrixEvent(
        stream_ordering=43,
        event_id="$event2:example.org",
        room_id="!room:example.org",
        sender="@alice:example.org",
        origin_server_ts=1_700_000_000_001,
        event_type="m.room.member",
        content={"membership": "join"},
    )

    assert to_meili_document(event)["text"] == ""
