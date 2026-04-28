import typer
import uvicorn

from matrix_sidecar_search.config import Settings

app = typer.Typer(help="Matrix Sidecar Search service")


@app.command()
def api(host: str = "0.0.0.0", port: int = 8080) -> None:
    """Run the HTTP API."""

    uvicorn.run("matrix_sidecar_search.api:app", host=host, port=port)


@app.command()
def indexer(once: bool = False) -> None:
    """Run the indexer loop. The first skeleton only validates configuration."""

    settings = Settings()
    typer.echo(
        "indexer configuration ok: "
        f"index={settings.index_uid} batch_size={settings.batch_size} once={once}"
    )


if __name__ == "__main__":
    app()
