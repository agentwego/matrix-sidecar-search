from matrix_sidecar_search.config import Settings


def test_settings_default_to_ro_pooler_style_dsn():
    settings = Settings(database_dsn="postgresql://matrix:secret@app-db-ro.cnpg.svc:5432/synapse")

    assert "-ro" in settings.database_dsn or "ro" in settings.database_dsn
    assert settings.batch_size == 500


def test_settings_reject_rw_dsn_by_default():
    try:
        Settings(database_dsn="postgresql://matrix:secret@app-db-rw.cnpg.svc:5432/synapse")
    except ValueError as exc:
        assert "read-only" in str(exc)
    else:
        raise AssertionError("rw DSN should be rejected unless explicitly allowed")
