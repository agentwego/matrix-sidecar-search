# Operations

## Deploy shape

- `matrix-search-indexer`: one replica, reads PostgreSQL `ro`, writes Meilisearch.
- `matrix-search-api`: one or more replicas, queries Meilisearch and validates results.

## Database routing

Use the CNPG read-only pooler for normal work. The write pooler is reserved for explicit diagnostics or strong-consistency probes.

## Rollback

Disable the API/proxy first, then stop the indexer. Synapse itself remains untouched.
