# Matrix Sidecar Search

Matrix Sidecar Search is a sidecar search service for Matrix Synapse. It keeps Synapse as the source of truth, uses PostgreSQL read replicas for indexing and validation where possible, and uses Meilisearch as a Chinese-friendly recall layer.

## Goals

- Read Synapse data from the CNPG `ro` pooler by default.
- Index searchable event content into Meilisearch.
- Apply redaction handling before indexing and during repair.
- Validate visibility before returning results.
- Expose index lag and operational status.
- Keep the Synapse write path untouched.

## Components

```text
matrix-search-indexer
  Synapse PostgreSQL ro pooler -> Meilisearch

matrix-search-api
  Client/Bot/Search proxy -> Meilisearch -> Synapse permission validation
```

## Development

```bash
rtk run 'go-task install'
rtk run 'go-task test'
rtk run 'go-task lint'
```

## Runtime commands

```bash
matrix-sidecar-search indexer --once
matrix-sidecar-search api
```

## Safety model

Meilisearch is a recall layer only. It must not be exposed directly to end users. Every user-facing result must be filtered through Matrix visibility checks and redaction state before display.
