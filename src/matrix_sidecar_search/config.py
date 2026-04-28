from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for Matrix Sidecar Search."""

    model_config = SettingsConfigDict(env_prefix="MATRIX_SEARCH_", env_file=".env", extra="ignore")

    database_dsn: str = Field(
        default="postgresql://matrix:matrix@app-db-ro.cnpg.svc.cluster.local:5432/synapse"
    )
    meili_url: str = "http://meilisearch.search.svc.cluster.local:7700"
    meili_api_key: str | None = None
    index_uid: str = "matrix_events"
    batch_size: int = 500
    allow_rw_database: bool = False

    @field_validator("database_dsn")
    @classmethod
    def database_dsn_must_be_read_only_by_default(cls, value: str, info):
        allow_rw = bool(info.data.get("allow_rw_database", False))
        if allow_rw:
            return value

        lowered = value.lower()
        read_only_markers = ("-ro", "_ro", "readonly", "read-only", "replica")
        if not any(marker in lowered for marker in read_only_markers):
            raise ValueError("database_dsn must point to a read-only replica/pooler by default")
        return value
