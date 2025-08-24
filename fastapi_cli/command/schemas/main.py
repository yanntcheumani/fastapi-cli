import typer
from rich.console import Console

from fastapi_cli.command.schemas import create, list, update, delete


app = typer.Typer()
app.add_typer(create.app, short_help="Command to create Schema")
app.add_typer(list.app, short_help="List all Schemas")
app.add_typer(update.app, short_help="Update Schema")
app.add_typer(delete.app, short_help="Delete Schema")

console = Console()

