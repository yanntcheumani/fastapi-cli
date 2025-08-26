import typer
from rich.console import Console

from fastapi_cli.command.modules import create


app = typer.Typer()
app.add_typer(create.app, short_help="Command to create Routers")

console = Console()

