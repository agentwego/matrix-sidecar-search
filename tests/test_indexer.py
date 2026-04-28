from matrix_sidecar_search.indexer import IndexerCursor, next_cursor


def test_next_cursor_advances_to_largest_stream_ordering():
    cursor = IndexerCursor(last_stream_ordering=10)
    documents = [
        {"id": "$a", "stream_ordering": 11},
        {"id": "$b", "stream_ordering": 15},
        {"id": "$c", "stream_ordering": 12},
    ]

    assert next_cursor(cursor, documents).last_stream_ordering == 15


def test_next_cursor_stays_put_when_batch_empty():
    cursor = IndexerCursor(last_stream_ordering=10)

    assert next_cursor(cursor, []).last_stream_ordering == 10
