from matrix_sidecar_search.permissions import filter_visible_documents


def test_filter_visible_documents_keeps_only_allowed_events():
    documents = [
        {"id": "$a", "room_id": "!room"},
        {"id": "$b", "room_id": "!room"},
    ]

    filtered = filter_visible_documents(documents, visible_event_ids={"$b"})

    assert filtered == [{"id": "$b", "room_id": "!room"}]


def test_filter_visible_documents_denies_by_default():
    documents = [{"id": "$a", "room_id": "!room"}]

    assert filter_visible_documents(documents, visible_event_ids=set()) == []
