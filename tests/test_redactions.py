from matrix_sidecar_search.redactions import apply_redactions


def test_apply_redactions_removes_redacted_events():
    documents = [
        {"id": "$visible", "text": "hello"},
        {"id": "$redacted", "text": "secret"},
    ]

    filtered = apply_redactions(documents, redacted_event_ids={"$redacted"})

    assert filtered == [{"id": "$visible", "text": "hello"}]


def test_apply_redactions_is_idempotent():
    documents = [{"id": "$visible", "text": "hello"}]

    assert apply_redactions(documents, redacted_event_ids=set()) == documents
