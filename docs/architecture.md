# Architecture

Matrix Sidecar Search is intentionally outside Synapse's write path.

```text
Synapse PostgreSQL ro pooler
        |
        v
matrix-search-indexer ---> Meilisearch
                                ^
                                |
client/search proxy ---> matrix-search-api ---> Synapse/PostgreSQL visibility checks
```

## Principles

1. Synapse remains the source of truth.
2. Meilisearch is only a recall engine.
3. The indexer uses the CNPG `ro` pooler by default.
4. The API denies by default if visibility cannot be proven.
5. Redactions must be removed from the index and filtered before display.
6. The service exposes index lag so eventual consistency is visible operationally.
