from matrix_sidecar_search.search_pipeline import sanitize_results


def test_sanitize_results_filters_redacted_then_invisible_documents():
    documents = [
        {"id": "$visible", "text": "ok"},
        {"id": "$redacted", "text": "secret"},
        {"id": "$invisible", "text": "hidden"},
    ]

    result = sanitize_results(
        documents,
        redacted_event_ids={"$redacted"},
        visible_event_ids={"$visible"},
    )

    assert result == [{"id": "$visible", "text": "ok"}]
