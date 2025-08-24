import typer
from rich.console import Console
from InquirerPy import inquirer
from typing import List
from pathlib import Path

from fastapi_cli.utils.config.config import load_config, Schema, save_config

app = typer.Typer()

console = Console()

@app.command()
def delete():
    config = load_config()

    schemas: List[str] = config.get_name_of_schemas()

    if len(schemas) == 0:
        console.print("[yellow]No schemas found in config or modules.[/]")
        typer.Exit(code=1)

    name_schema: str = inquirer.select(
        message="Choose the Schema :",
        choices=schemas,
        default=schemas[0],
    ).execute()

    delete = typer.confirm("Are you sure you want to delete it?", abort=True)

    if not delete:
        console.print("[red]command aborted ![/]")
        typer.Exit(code=1)

    schema: Schema =  config.get_schema(name_schema)
    path = Path(schema.path)
    
    if path.is_file():
        path.unlink(True)
    config.delete_schema(schema)
    save_config(config)
