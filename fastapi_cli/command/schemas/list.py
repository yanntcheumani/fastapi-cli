import typer
from rich.console import Console
from rich.table import Table

from fastapi_cli.utils.config.config import load_config, Schema
from typing import List

app = typer.Typer()
console = Console()

def _add_schema_in_table(schemas: List[Schema] | Schema, table: Table, source: str):
    if type(schemas) is Schema:
        name = schemas.name
        path = schemas.path
        table.add_row(source, name, str(path))
        return

    for schema in schemas:
        name = schema.name
        path = schema.path
        table.add_row(source, name, str(path))


@app.command()
def list():
    """
    Display all schemas from the global config and from each module.
    """
    config = load_config()

    table = Table(title="Schemas (config + modules)")
    table.add_column("Source", style="magenta")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Path", style="green")

    _add_schema_in_table(config.schemas, table, "Config")

    for mod in config.modules:
        for submodule in mod.submodules:
            _add_schema_in_table(submodule.schemas, table, f"Module: {mod.name}")

    if len(table.rows) == 0:
        console.print("[yellow]No schemas found in config or modules.[/]")
        raise typer.Exit(code=0)

    console.print(table)
