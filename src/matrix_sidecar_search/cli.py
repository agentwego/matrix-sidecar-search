import asyncio

import asyncpg
import typer
import uvicorn
from meilisearch_python_sdk import AsyncClient

from matrix_sidecar_search.async_adapters import MeiliDocumentWriter, SynapseEventReader
from matrix_sidecar_search.config import Settings
from matrix_sidecar_search.indexer import IndexerCursor
from matrix_sidecar_search.runner import run_index_once

app = typer.Typer(help="Matrix Sidecar Search service")


@app.command()
def api(host: str = "0.0.0.0", port: int = 8080) -> None:
    """Run the HTTP API."""

    uvicorn.run("matrix_sidecar_search.api:app", host=host, port=port)


async def _run_indexer_once(settings: Settings) -> None:
    connection = await asyncpg.connect(settings.database_dsn)
    client = AsyncClient(settings.meili_url, settings.meili_api_key)
    try:
        reader = SynapseEventReader(connection)
        writer = MeiliDocumentWriter(client.index(settings.index_uid))
        result = await run_index_once(
            reader,
            writer,
            cursor=IndexerCursor(settings.once_cursor),
            batch_size=settings.batch_size,
        )
        typer.echo(
            "indexer batch complete: "
            f"fetched={result.fetched} indexed={result.indexed} "
            f"cursor={result.cursor.last_stream_ordering}"
        )
    finally:
        await connection.close()
        await client.aclose()


@app.command()
def indexer(once: bool = False) -> None:
    """Run the indexer loop.

    The first deployable slice runs one bounded batch. A durable cursor store and
    continuous loop can be enabled after the in-cluster health path is verified.
    """

    settings = Settings()
    if not once:
        typer.echo("continuous loop is not enabled yet; running one safe batch")
    asyncio.run(_run_indexer_once(settings))


if __name__ == "__main__":
    app()
